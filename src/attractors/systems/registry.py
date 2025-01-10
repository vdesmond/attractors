from collections.abc import Callable
from dataclasses import dataclass
from typing import ClassVar, TypeVar

from numba import njit  # type: ignore[import-untyped]

from attractors.type_defs import PlotLimits, SystemCallable, Vector


@dataclass
class System:
    func: SystemCallable
    name: str
    params: Vector
    param_names: list[str]
    reference: str
    init_coord: Vector
    plot_lims: PlotLimits | None = None

    def set_params(self, params: Vector) -> None:
        if len(params) != len(self.param_names):
            msg = f"Expected {len(self.param_names)} parameters"
            raise ValueError(msg)
        self.params = params

    def set_init_coord(self, coord: Vector) -> None:
        if len(coord) != 3:
            raise ValueError("State vector must have length 3")
        self.init_coord = coord


F = TypeVar("F", bound=SystemCallable)


class SystemRegistry:
    _systems: ClassVar[dict[str, System]] = {}

    @classmethod
    def register(
        cls,
        name: str,
        *,
        default_params: Vector,
        param_names: list[str],
        reference: str = "",
        init_coord: Vector,
        plot_lims: PlotLimits | None = None,
    ) -> Callable[[F], F]:
        def decorator(f: F) -> F:
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
                name=name,
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
