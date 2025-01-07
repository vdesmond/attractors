from attractors.solvers.registry import SolverRegistry
from attractors.type_defs import ParamVector, StateVector, SystemCallable


@SolverRegistry.register("stormer_verlet")
def stormer_verlet(
    system_func: SystemCallable, state: StateVector, params: ParamVector, dt: float
) -> StateVector:
    k1 = system_func(state, params)
    half_state = state + 0.5 * dt * k1

    k2 = system_func(half_state, params)
    return state + dt * k2
