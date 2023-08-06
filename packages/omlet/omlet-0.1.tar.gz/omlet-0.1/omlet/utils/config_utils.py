import os
import random
import re
import hydra
import pkg_resources
import sys
from omegaconf import OmegaConf, DictConfig
from omegaconf.errors import OmegaConfBaseException
from typing import Optional, List, Union
import omlet.utils as U


_CLASS_REGISTRY = {}  # for instantiation


def _register_omlet_resolvers():
    def _random_int(spec):
        if '-' in spec:
            start, end = spec.split('-')
            start, end = int(start), int(end)
        else:
            start, end = 0, int(spec)
        return random.randint(start, end)
    OmegaConf.register_resolver('randint', _random_int)


_register_omlet_resolvers()


def _omlet_internal_config_schema(cfg: DictConfig = None):
    schema = OmegaConf.create(
        {
            "shorthand": {},
            "override_name": {
                "kv_sep": "=",
                "item_sep": ",",
                "use_shorthand": False,  # use shorthand names for override
                "include_keys": None,
                "exclude_keys": [],
            },
            "os_envs": {},
            "job": {"override_name": None, "launch_dir": None},
            "logging": {  # omlet.utils.logging_utils
                "enable": True,
                "file_path": None,
                "level": None,
                "replace_all_stream_handlers": True,
            },
            "_internal": {"is_initialized": False},
        }
    )
    if cfg is None:
        return schema
    else:
        return OmegaConf.merge(schema, cfg)


def initialize_omlet_config(
    cfg: DictConfig, init_logging: bool = True, set_os_envs: bool = True
):
    """
    See _omlet_config_schema()
    """
    assert isinstance(cfg, DictConfig)
    OmegaConf.set_struct(cfg, False)
    om = _omlet_internal_config_schema()
    for k in cfg.get("omlet", {}):
        if k not in om:
            raise KeyError(f"Unrecognized omlet config key: {k}")
    om.update(cfg.get("omlet", {}))
    cfg.omlet = om  # this is a copy operation
    om = cfg.omlet

    om._internal.is_initialized = True
    assert is_omlet_initialized(cfg), "INTERNAL"

    # process shorthands
    shortset = set()
    for original, short in om.shorthand.items():
        if short in shortset:
            raise KeyError(f"Shorthand {short} is duplicated")
        if short in cfg:
            # user has already passed the short value
            cfg[original] = cfg[short]  # create a redirection to short name
            del cfg[short]
        shortset.add(short)

    # set os environment variables
    if set_os_envs:
        U.set_os_envs(om.os_envs)

    # set override_name
    om.job.override_name = omlet_override_name(cfg)
    om.job.launch_dir = hydra_original_dir()
    # override Hydra's chdir, switch batch to launch dir
    os.chdir(om.job.launch_dir)

    if init_logging:
        U.initialize_omlet_logging(**cfg.omlet.logging)
    return cfg


def print_config(cfg: DictConfig):
    print(cfg.pretty(resolve=True))


def is_hydra_initialized():
    return hydra.utils.HydraConfig.initialized()


def is_omlet_initialized(cfg):
    try:
        return bool(cfg.omlet._internal.is_initialized)
    except OmegaConfBaseException:
        return False


def hydra_config():
    # https://github.com/facebookresearch/hydra/issues/377
    # HydraConfig() is a singleton
    if is_hydra_initialized():
        return hydra.utils.HydraConfig().cfg.hydra
    else:
        return None


def hydra_override_arg_list() -> List[str]:
    """
    Returns:
        list ["lr=0.2", "batch=64", ...]
    """
    if is_hydra_initialized():
        return hydra_config().overrides.task
    else:
        return []


def hydra_override_name():
    if is_hydra_initialized():
        return hydra_config().job.override_dirname
    else:
        return ""


def omlet_override_name(cfg: Optional[DictConfig]) -> str:
    """
    Command line overrides, e.g. "gpus=4,arch=resnet18"

    If your cfg provides a top-level dict:

    omlet:
        override_name:
            kv_sep: =
            item_sep: ,
            include_keys: ['lr', 'momentum', 'model.*']  # supports patterns
            exclude_keys: ['lr', 'momentum', 'model.*']  # supports patterns

    `include_keys` takes precedence over `exclude_keys`
    """
    assert is_hydra_initialized() and is_omlet_initialized(cfg)

    override_cfg = cfg.omlet.override_name
    # cfg.omlet.shorthand maps original -> short
    # build a reverse lookup for short -> original
    longhand = {short: original for original, short in cfg.omlet.shorthand.items()}
    args = []
    for arg in hydra_override_arg_list():
        assert "=" in arg, f'INTERNAL ERROR: arg should contain "=": {arg}'
        key, value = arg.split("=", 1)
        if key in longhand:  # key is a shorthand
            key = longhand[key]
        append = U.match_patterns(
            key,
            include=override_cfg.include_keys,
            exclude=override_cfg.exclude_keys,
            precedence="exclude",
        )
        if append:
            # key is always a longhand by now
            if override_cfg.use_shorthand and key in cfg.omlet.shorthand:
                key = cfg.omlet.shorthand[key]
            args.append((key, value))
    args.sort()
    item_sep = override_cfg.item_sep
    kv_sep = override_cfg.kv_sep
    return item_sep.join(f"{key}{kv_sep}{value}" for key, value in args)


def hydra_original_dir(*subpaths):
    return os.path.join(hydra.utils.get_original_cwd(), *subpaths)


def resource_file(*subpaths):
    # return os.path.join(kitten.__path__[0], 'resources', *subpaths)
    return pkg_resources.resource_filename(
        "kitten", os.path.join("resources", *subpaths)
    )


def disable_unknown_key_check(cfg):
    OmegaConf.set_struct(cfg, False)


# ==================== Instantiation tools ====================
def register_class(name, class_type):
    assert callable(class_type)
    _CLASS_REGISTRY[name] = class_type


def get_class(path):
    """
    First try to find the class in the registry,
    if it doesn't exist, use importlib to locate it
    """
    if path in _CLASS_REGISTRY:
        return _CLASS_REGISTRY[path]
    try:
        from importlib import import_module

        module_path, _, class_name = path.rpartition(".")
        mod = import_module(module_path)
        try:
            class_type = getattr(mod, class_name)
        except AttributeError:
            raise ImportError(
                "Class {} is not in module {}".format(class_name, module_path)
            )
        return class_type
    except ValueError as e:
        print("Error initializing class " + path, file=sys.stderr)
        raise e


def _is_instantiable(cfg: DictConfig):
    return isinstance(cfg, DictConfig) and ("cls" in cfg or "class" in cfg)


def _get_params(cfg, kwargs={}):
    if "params" in cfg:
        params = cfg["params"]
    else:
        params = cfg
    for k in params:
        if OmegaConf.is_missing(params, k) and k not in kwargs:
            raise ValueError(f'Missing required keyword arg "{k}"')
    return {k: v for k, v in params.items() if k not in ["cls", "class"]}


def instantiate(cfg: DictConfig, recursive=False, *args, **kwargs):
    """
    If 'class' key exists but not 'params' key, rest of the keys will be treated as params
    """
    assert bool("cls" in cfg) != bool(
        "class" in cfg
    ), 'to instantiate from config, one and only one of "cls" or "class" key should be provided'
    assert _is_instantiable(cfg)
    if "class" in cfg:
        cls = cfg["class"]
    else:
        cls = cfg["cls"]
    params = _get_params(cfg)
    params.update(kwargs)
    if recursive:
        for key, value in params.items():
            if _is_instantiable(value):
                # args and kwargs are only for top-level
                value = instantiate(value, recursive=True)
            params[key] = value
    try:
        class_type = get_class(cls)
        return class_type(*args, **params)
    except Exception as e:
        raise RuntimeError(f"Error instantiating {cls}: {e}")


def to_dict(conf):
    if OmegaConf.is_config(conf):
        return OmegaConf.to_container(conf, resolve=True)
    elif isinstance(conf, dict):
        return conf
    else:
        raise NotImplementedError(f"Unknown dict type: {type(conf)}")
