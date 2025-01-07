from attractors.solvers.registry import SolverRegistry
from attractors.type_defs import ParamVector, StateVector, SystemCallable


@SolverRegistry.register("euler")
def euler(
    system_func: SystemCallable, state: StateVector, params: ParamVector, dt: float
) -> StateVector:
    return state + dt * system_func(state, params)
