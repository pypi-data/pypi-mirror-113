"""
Easily configure pl.Trainer with Hydra
"""
import os
import sys
import time
from typing import Optional, Union, Dict, Any, List, Callable

import pytorch_lightning as pl
from pytorch_lightning.callbacks import Callback

from .loggers import *
from omegaconf import DictConfig, OmegaConf
import omlet.utils as U
import omlet.distributed as dist
from . import omlet_logger as _omlet_log
from .checkpoint import ExtendedCheckpoint


DEFAULT_OS_ENVS = {
    # https://discuss.pytorch.org/t/issue-with-multiprocessing-semaphore-tracking/22943/4
    "PYTHONWARNINGS": "ignore:semaphore_tracker:UserWarning",
    "OMP_NUM_THREADS": 1,
}


def _omlet_trainer_schema(cfg: DictConfig = None):
    schema = dict(
        root_dir="???",
        run_name="???",
        epochs="???",
        gpus="???",
        fp16=False,
        resume=False,  # Union[str, int, bool]
        monitor_metric="???",
        monitor_metric_mode="auto",
        save_top_k=3,
        save_epoch_interval=5,
        always_save_last=True,
        best_filename_template=None,
        eval=False,
        # ===== ExtendedModule specific fields
        batch_size=None,  # per GPU
        global_batch_size=None,  # will be used if batch_size is not specified
        eval_batch_size=None,  # per GPU
        global_eval_batch_size=None,  # will be used if eval_batch_size is not specified
        num_workers=4,  # per GPU
        global_num_workers=None,  # will be used if num_workers is not specified
        train_metrics=[],  # e.g. [loss, acc1, acc5]
        val_metrics=[],
        best_metrics={},  # e.g. {'train/loss': 'max', 'val/loss': min}
        # ===== distributed environment variables
        master_addr="localhost",
        master_port="auto",
        node_rank=0,
        distributed_backend="ddp",  # the only thing we support now
        # ===== reproducibility
        seed=None,  # use system time
        deterministic=False,  # cuDNN deterministic mode
        # ===== callbacks
        wandb={"enable": False},
        callbacks={},  # callbacks to be instantiated
        trainer={},  # extra trainer args
        # ===== added by omlet_trainer(), user should not add directly:
        exp_dir=None,  # "{root_dir}/{run_name}"
        ckpt_dir=None,  # "{root_dir}/{run_name}/ckpt"
        omlet={},  # to be filled by initialize_omlet_config() function
    )
    schema = OmegaConf.create(schema)
    if cfg is None:
        return schema
    else:
        return OmegaConf.merge(schema, cfg)


class OmletTrainer:
    def __init__(
        self,
        pl_module_cls,
        cfg: DictConfig,
        extra_callbacks: List[Callback] = [],
        run_name_generator: Optional[Callable[[DictConfig], str]] = None,
    ):
        self._pl_module_cls = pl_module_cls
        self._run_name_generator = run_name_generator
        self.cfg = _omlet_trainer_schema(cfg)
        # init_logging=False because we need to manipulate log fpath to be relative to exp_dir
        U.initialize_omlet_config(self.cfg, init_logging=False, set_os_envs=True)
        U.set_os_envs(DEFAULT_OS_ENVS)
        self._exp_dir_exists = False
        self._extra_callbacks = extra_callbacks
        self.trainer = None
        self.model = None

    @property
    def C(self):
        return self.cfg

    def configure(self):
        """
        Configures pl.Trainer
        """
        if self.model is not None or self.trainer is not None:
            return
        self._configure_run_name()
        self._configure_exp_dir()
        self._configure_logging()
        self._configure_random()
        self._configure_distributed()
        checkpoint_callback = self._configure_checkpoint()
        logger_callbacks = self._configure_logger_callbacks()
        callbacks = self._configure_generic_callbacks()
        callbacks.extend(self._extra_callbacks)
        resume_path = self._configure_resume()
        self._dump_config_yaml()

        C = self.C
        self.model = self._pl_module_cls(C)
        self.trainer = pl.Trainer(
            gpus=C.gpus,
            max_epochs=C.epochs,
            distributed_backend=C.distributed_backend,
            precision=16 if C.fp16 else 32,
            checkpoint_callback=checkpoint_callback,
            callbacks=callbacks,
            logger=logger_callbacks,
            resume_from_checkpoint=resume_path,
            **C.trainer,
        )

    def fit(self):
        try:
            self.configure()
            return self.trainer.fit(self.model)
        except KeyboardInterrupt:
            _omlet_log.critical("KeyboardInterrupt: stop training")
            sys.exit(0)

    def test(self):
        try:
            self.configure()
            return self.trainer.test(self.model)
        except KeyboardInterrupt:
            _omlet_log.critical("KeyboardInterrupt: stop testing")
            sys.exit(0)

    def run(self):
        if self.C.eval:
            return self.test()
        else:
            return self.fit()

    def _configure_run_name(self):
        C = self.cfg
        if self._run_name_generator is not None:
            C.run_name = self._run_name_generator(C)
        # strip away trailing item_sep, such as "," or "_"
        C.run_name = C.run_name.strip(" _" + C.omlet.override_name.item_sep)
        # check run_name sanity
        for special_char in "\\/$#&|\"'~!^*:<>":
            assert (
                special_char not in C.run_name
            ), f'Run name "{C.run_name}" cannot have special character {special_char}'

    def _configure_exp_dir(self):
        """
        Sets up file structure
        """
        C = self.cfg
        # set up experiment dir file structure
        C.root_dir = os.path.expanduser(C.root_dir)
        assert os.path.isdir(C.root_dir), f"root dir {C.root_dir} is not a folder."
        C.exp_dir = U.f_join(C.root_dir, C.run_name)
        self._exp_dir_exists = os.path.exists(C.exp_dir)
        if not self._exp_dir_exists:
            U.f_mkdir(C.exp_dir)
        C.ckpt_dir = U.f_join(C.exp_dir, "ckpt")
        U.f_mkdir(C.ckpt_dir)

    def _configure_logging(self):
        C = self.cfg
        if U.is_relative_path(C.omlet.logging.file_path):
            C.omlet.logging.file_path = U.f_join(C.exp_dir, C.omlet.logging.file_path)
        U.initialize_omlet_logging(**C.omlet.logging)
        _omlet_log.info(f"Full config:\n{C.pretty(resolve=True)}")
        _omlet_log.info(f"Run name: {C.run_name}")

    def _configure_random(self):
        # if seed is None, will return the actual seed based on system time
        seed = U.set_seed_everywhere(self.C.seed, deterministic=self.C.deterministic)
        self.C.seed = seed
        if seed >= 0:
            _omlet_log.info(f"Random seed: {seed}")
        if self.C.deterministic:
            _omlet_log.warn(
                "You have set cudnn to deterministic mode, will impact performance!"
            )

    def _configure_distributed(self):
        C = self.C
        if C.distributed_backend == "ddp":
            # update env variables for distributed use case
            if C.master_port == "auto":
                C.master_port = dist.random_free_tcp_port()
                _omlet_log.info(
                    f"MASTER_PORT env not specified. Randomly picks a free port: {C.master_port}"
                )
            else:
                C.master_port = int(C.master_port)
            C.node_rank = int(C.node_rank)
            _envs = {
                "MASTER_ADDR": C.master_addr,
                "NODE_RANK": C.node_rank,
                "MASTER_PORT": C.master_port,
            }
            U.set_os_envs(_envs)
        else:
            raise NotImplementedError(
                "distributed_backend=ddp is the only mode supported for now"
            )

    def _configure_checkpoint(self):
        C = self.C
        assert "/" in C.monitor_metric
        if not C.monitor_metric_mode:
            C.monitor_metric_mode = "auto"
        assert C.monitor_metric_mode in ["min", "max", "auto"]

        if not C.best_filename_template:
            C.best_filename_template = "best/{epoch}-{" + C.monitor_metric + ":.2f}"

        _omlet_log.info(f"checkpoint dir: {C.ckpt_dir}")
        return ExtendedCheckpoint(
            C.ckpt_dir,
            filename_template="{epoch}",
            best_filename_template=C.best_filename_template,
            monitor_metric=C.monitor_metric,
            monitor_metric_mode=C.monitor_metric_mode,
            save_top_k=C.save_top_k,
            save_epoch_interval=C.save_epoch_interval,
            always_save_last=C.always_save_last,
        )

    def _configure_logger_callbacks(self):
        """
        Currently supported:
            - Tensorboard
            - Wandb
        """
        C = self.C
        loggers = []
        tb_logger = ExtendedTensorBoardLogger(
            U.f_join(C.exp_dir, "tb"), name="", version=""
        )
        loggers.append(tb_logger)

        if C.wandb.pop("enable"):
            _kwargs = {
                "save_dir": C.exp_dir,
                "name": C.run_name,
                "log_model": True,
                "project": os.path.basename(os.path.normpath(C.root_dir)),
            }
            _kwargs.update(C.wandb)
            wandb_logger = ExtendedWandbLogger(**_kwargs)
            loggers.append(wandb_logger)

        return loggers

    def _configure_generic_callbacks(self):
        callbacks = []
        C = self.C
        for callback_cfg in C.get("callbacks", {}).values():
            cb = U.instantiate(callback_cfg)
            # hack link reference to config
            cb.cfg = C
            cb.run_name = C.run_name
            cb.exp_dir = C.exp_dir
            callbacks.append(cb)
        return callbacks

    def _configure_resume(self) -> str:
        C = self.C
        resume = C.resume
        if resume:
            assert isinstance(resume, (int, str, bool))
            if resume is True:
                resume = U.f_join(C.ckpt_dir, "last.ckpt")
            elif isinstance(resume, int):
                resume = U.f_join(C.ckpt_dir, f"epoch={resume}.ckpt")
            elif os.path.isabs(resume):
                resume = os.path.expanduser(resume)
                if self._exp_dir_exists:
                    _omlet_log.warn(
                        f"The destination experiment dir already exists: {C.exp_dir}, make sure you do not unintentionally overwrite old checkpoints and logs"
                    )
                    # give the user a bit time to terminate
                    time.sleep(2)
            else:
                resume = U.f_join(C.ckpt_dir, resume)
            if not resume.endswith(".ckpt"):
                resume += ".ckpt"
            # check resume ckpt path must exist
            if not os.path.exists(resume):
                raise FileNotFoundError(f"Resume file {resume} does not exist")
            _omlet_log.info(f"Resuming run from checkpoint: {resume}")
        else:
            if self._exp_dir_exists:
                _omlet_log.warn(
                    f"The destination experiment dir already exists: {C.exp_dir}, but `resume` option is not set. Make sure you do not unintentionally overwrite old checkpoints and logs"
                )
                # give the user a bit time to terminate
                time.sleep(2)
            _omlet_log.info(f"Starting a new run from scratch: {C.run_name}")
            resume = None
        return resume

    def _dump_config_yaml(self):
        orig_fpath = U.f_join(self.C.exp_dir, "config.yaml")
        fpath = U.next_available_file_name(orig_fpath, suffix_template="_v{i+1}")
        U.yaml_dump(U.to_dict(self.C), fpath)
        if fpath == orig_fpath:
            _omlet_log.info(f"config saved to {fpath}")
        else:
            _omlet_log.warning(
                f"config.yaml already exists in the experiment folder, saving to another version {fpath}"
            )
