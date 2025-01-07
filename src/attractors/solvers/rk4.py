from attractors.solvers.registry import SolverRegistry
from attractors.type_defs import ParamVector, StateVector, SystemCallable


@SolverRegistry.register("rk4")
def rk4(
    system_func: SystemCallable, state: StateVector, params: ParamVector, dt: float
) -> StateVector:
    k1 = system_func(state, params)
    k2 = system_func(state + dt * k1 / 2, params)
    k3 = system_func(state + dt * k2 / 2, params)
    k4 = system_func(state + dt * k3, params)
    return state + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
