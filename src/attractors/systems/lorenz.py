import numpy as np

from attractors.systems.registry import SystemRegistry
from attractors.type_defs import ParamVector, StateVector


@SystemRegistry.register("lorenz")
def lorenz(state: StateVector, params: ParamVector) -> StateVector:
    if len(state) != 3 or len(params) != 3:
        msg = f"Expected 3 components, got {len(state)}/{len(params)}"
        raise ValueError(msg)
    x, y, z = state
    sigma, rho, beta = params
    return np.array(
        [sigma * (y - x), x * (rho - z) - y, x * y - beta * z], dtype=np.float64
    )
