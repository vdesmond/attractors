from collections.abc import Callable
from typing import ClassVar

from numba import njit

from attractors.type_defs import ParamVector, StateVector


class SystemRegistry:
    _system: ClassVar[dict[str, Callable]] = {}

    @classmethod
    def register(cls, name: str) -> Callable:
        def decorator(f: Callable[[StateVector, ParamVector], StateVector]) -> Callable:
            if not isinstance(name, str):
                raise TypeError("Name must be string")
            if not callable(f):
                raise TypeError("Must register callable")
            if name in cls._system:
                msg = f"System {name} already registered"
                raise ValueError(msg)
            if not hasattr(f, "_numba_signature"):
                f = njit(f)
            cls._system[name] = f
            return f

        return decorator

    @classmethod
    def get(cls, name: str) -> Callable:
        if name not in cls._system:
            msg = f"System {name} not found"
            raise KeyError(msg)
        return cls._system[name]

    @classmethod
    def list_system(cls) -> list[str]:
        return list(cls._system.keys())
