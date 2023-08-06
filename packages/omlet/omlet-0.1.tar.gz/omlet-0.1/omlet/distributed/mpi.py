import os
import sys
import subprocess

try:
    from mpi4py import MPI
except ImportError as e:
    print("please install mpi4py")
    raise e


def mpi_fork(n, sys_argv=()):
    """
    Fork the current script with workers

    Args:
        sys_argv: tuple of args to be appended to sys.argv

    Returns:
        -1 for parent process
        <rank> for child processes (between 0 and n-1)
    """
    assert n >= 1
    if os.getenv("IN_MPI") is None:
        env = os.environ.copy()
        env.update(MKL_NUM_THREADS="1", OMP_NUM_THREADS="1", IN_MPI="1")
        subprocess.check_call(
            ["mpirun", "-np", str(n), sys.executable]
            + sys.argv
            + list(map(str, sys_argv)),
            env=env,
        )
        return -1
    else:
        return MPI.COMM_WORLD.Get_rank()


def mpi_launch(n, sys_argv=(), parent_callback=None):
    """
    Run this as the **first line** in your main script.
    It will block the parent process and only proceed with the child processes.
    Has exactly the same effect as `mpiexec -n` on the command line

    Args:
        n: n children processes, excluding the parent
        parent_callback: calls before parent exists
    """
    rank = mpi_fork(n, sys_argv=sys_argv)
    if rank < 0:
        if parent_callback is not None:
            parent_callback()
        sys.exit(0)
