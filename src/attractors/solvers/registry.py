from collections.abc import Callable
from typing import ClassVar

from numba import njit  # type: ignore[import-untyped]

from attractors.type_defs import (
    SolverCallable,
)


class SolverRegistry:
    _solvers: ClassVar[dict[str, SolverCallable]] = {}

    @classmethod
    def register(cls, name: str) -> Callable[[SolverCallable], SolverCallable]:
        def decorator(f: SolverCallable) -> SolverCallable:
            if not isinstance(name, str):
                raise TypeError("Name must be string")
            if not callable(f):
                raise TypeError("Must register callable")
            if name in cls._solvers:
                msg = f"Solver {name} already registered"
                raise ValueError(msg)
            if not hasattr(f, "_numba_signature"):
                f = njit(f)
            cls._solvers[name] = f
            return f

        return decorator

    @classmethod
    def get(cls, name: str) -> SolverCallable:
        if name not in cls._solvers:
            msg = f"Solver {name} not found"
            raise KeyError(msg)
        return cls._solvers[name]

    @classmethod
    def list_solvers(cls) -> list[str]:
        return list(cls._solvers.keys())
