import numpy as np
from numba import njit

from attractors.solvers.registry import Solver
from attractors.systems.registry import System
from attractors.type_defs import (
    SolverCallable,
    SystemCallable,
    Vector,
)
from attractors.utils.logger import setup_logger

logger = setup_logger(name=__name__)


# non-jitted
def _integrate_trajectory_impl(
    system_func: SystemCallable,
    solver_step: SolverCallable,
    init_coord: Vector,
    params: Vector,
    steps: int,
    dt: float,
) -> tuple[Vector, Vector]:
    trajectory = np.empty((steps, len(init_coord)), dtype=np.float64)
    time = np.empty(steps, dtype=np.float64)
    current = init_coord.copy()

    for i in range(steps):
        current = solver_step(system_func, current, params, dt)
        trajectory[i] = current
        time[i] = i * dt

    return trajectory, time


# jitted
_integrate_trajectory_jitted = njit(_integrate_trajectory_impl)


def integrate_system(
    system: System, solver: Solver, steps: int, dt: float, use_jit: bool | None = None
) -> tuple[Vector, Vector]:
    """Integrates a dynamical system using the specified numerical solver.

    Args:
        system (System): System to integrate
        solver (Solver): Numerical solver to use for integration
        steps (int): Number of integration steps
        dt (float): Time step size
        use_jit (bool | None): Whether to use Numba JIT compilation. Defaults to True.

    Raises:
        ValueError: If steps <= 0 or dt <= 0

    Returns:
        tuple[Vector, Vector]: A tuple containing:
            - Vector: System state trajectory at each time step
            - Vector: Time points corresponding to trajectory

    """
    if steps <= 0:
        raise ValueError("Number of steps must be positive")
    if dt <= 0:
        raise ValueError("Time step must be positive")

    jit_enabled = True if use_jit is None else use_jit
    logger.debug("JIT enabled: %s", jit_enabled)
    logger.info("Integrating system: %s with solver: %s", system, solver)
    logger.info("Steps: %d, dt: %.6g", steps, dt)

    if jit_enabled is True:
        integrate_func = _integrate_trajectory_jitted
    else:
        integrate_func = _integrate_trajectory_impl

    system_func = system.get_func(jit_enabled)
    solver_func = solver.get_func(jit_enabled)

    return integrate_func(  # type: ignore[no-any-return]
        system_func, solver_func, system.init_coord, system.params, steps, dt
    )
