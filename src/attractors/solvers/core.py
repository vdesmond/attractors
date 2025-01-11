import numpy as np
from numba import njit  # type: ignore[import-untyped]

from attractors.systems.registry import System
from attractors.type_defs import (
    SolverCallable,
    SystemCallable,
    Vector,
)


@njit  # type: ignore[misc]
def _integrate_trajectory(
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


def integrate_system(
    system: System,
    solver_step: SolverCallable,
    steps: int,
    dt: float,
) -> tuple[Vector, Vector]:
    return _integrate_trajectory(  # type: ignore[no-any-return]
        system.func, solver_step, system.init_coord, system.params, steps, dt
    )
