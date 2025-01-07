import numpy as np
from numba import njit
from numpy.typing import NDArray

from attractors.type_defs import (
    ParamVector,
    SolverCallable,
    StateVector,
    SystemCallable,
)


@njit
def integrate_trajectory(
    system_func: SystemCallable,
    solver_step: SolverCallable,
    state: StateVector,
    params: ParamVector,
    steps: int,
    dt: float,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    trajectory = np.zeros((steps, len(state)), dtype=np.float64)
    current = state.copy()
    time = np.zeros(steps, dtype=np.float64)

    for i in range(steps):
        current = solver_step(system_func, current, params, dt)
        trajectory[i] = current
        time[i] = i * dt

    return trajectory, time
