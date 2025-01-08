import numpy as np

from attractors.systems.registry import SystemRegistry
from attractors.type_defs import ParamVector, StateVector


@SystemRegistry.register(
    name="rucklidge",
    default_params=np.array([2.0, 6.7]),  # k, alpha
    param_names=["k", "alpha"],
    init_coord=np.array([1.0, 0.0, 4.5]),
    reference="Rucklidge, A. Chaos in models of double convection. J. Fluid Mech. 1992, 237, 209–229.",
    plot_lims={"xlim": (-10.0, 10.0), "ylim": (-10.0, 10.0), "zlim": (-10.0, 10.0)},
)
def rucklidge(state: StateVector, params: ParamVector) -> StateVector:
    """Rucklidge attractor system."""
    x, y, z = state
    k, alpha = params
    dx = -k * x + alpha * y - y * z
    dy = x
    dz = -z + y * y
    return np.array([dx, dy, dz], dtype=np.float64)
