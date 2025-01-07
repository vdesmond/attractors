from attractors.solvers.registry import SolverRegistry
from attractors.type_defs import ParamVector, StateVector, SystemCallable


@SolverRegistry.register("rk2")
def rk2(
    system_func: SystemCallable, state: StateVector, params: ParamVector, dt: float
) -> StateVector:
    k1 = system_func(state, params)
    k2 = system_func(state + dt * k1, params)
    return state + dt * (k1 + k2) / 2
