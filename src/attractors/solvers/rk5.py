from attractors.solvers.registry import SolverRegistry
from attractors.type_defs import ParamVector, StateVector, SystemCallable


@SolverRegistry.register("rk5")
def rk5(
    system_func: SystemCallable, state: StateVector, params: ParamVector, dt: float
) -> StateVector:
    k1 = system_func(state, params)
    k2 = system_func(state + dt * k1 / 4, params)
    k3 = system_func(state + dt * (k1 + k2) / 8, params)
    k4 = system_func(state + dt * (k3 - k2 / 2 + k3), params)
    k5 = system_func(state + dt * (-3 * k1 / 16 + 9 * k4 / 16), params)
    k6 = system_func(
        state
        + dt * (-3 * k1 / 7 + 2 * k2 / 7 + 12 * k3 / 7 - 12 * k4 / 7 + 8 * k5 / 7),
        params,
    )
    return state + dt * (7 * k1 + 32 * k3 + 12 * k4 + 32 * k5 + 7 * k6) / 90
