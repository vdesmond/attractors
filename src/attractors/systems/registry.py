from collections.abc import Callable
from dataclasses import dataclass
from typing import ClassVar

from numba import njit

from attractors.type_defs import ParamVector, PlotLimits, StateVector


@dataclass
class System:
    func: Callable
    params: ParamVector
    param_names: list[str]
    reference: str
    init_coord: StateVector
    plot_lims: PlotLimits | None = None

    def set_params(self, params: ParamVector) -> None:
        if len(params) != len(self.param_names):
            msg = f"Expected {len(self.param_names)} parameters"
            raise ValueError(msg)
        self.params = params

    def set_init_coord(self, coord: StateVector) -> None:
        if len(coord) != 3:
            raise ValueError("State vector must have length 3")
        self.init_coord = coord


class SystemRegistry:
    _systems: ClassVar[dict[str, System]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        *,
        default_params: ParamVector,
        param_names: list[str],
        reference: str = "",
        init_coord: StateVector,
        plot_lims: dict[str, tuple[float, float]] | None = None,
    ) -> Callable:
        def decorator(f: Callable[[StateVector, ParamVector], StateVector]) -> Callable:
            if not isinstance(name, str):
                raise TypeError("Name must be string")
            if not callable(f):
                raise TypeError("Must register callable")
            if name in cls._systems:
                msg = f"System {name} already registered"
                raise ValueError(msg)

            if not hasattr(f, "_numba_signature"):
                f = njit(f)

            cls._systems[name] = System(
                func=f,
                params=default_params,
                param_names=param_names,
                reference=reference,
                init_coord=init_coord,
                plot_lims=plot_lims,
            )
            return f

        return decorator

    @classmethod
    def get(cls, name: str) -> System:
        if name not in cls._systems:
            msg = f"System {name} not found"
            raise KeyError(msg)
        return cls._systems[name]

    @classmethod
    def list_systems(cls) -> list[str]:
        return list(cls._systems.keys())
