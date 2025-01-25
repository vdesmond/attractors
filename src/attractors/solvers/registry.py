from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, ClassVar, TypeVar

from numba import njit
from numba.core.dispatcher import Dispatcher

from attractors.type_defs import (
    SolverCallable,
)
from attractors.utils.logger import setup_logger

logger = setup_logger(name=__name__)


@dataclass
class Solver:
    """
    Data class representing a numerical ODE solver with JIT compilation support.

    Attributes:
        func (SolverCallable): Original solver function
        jitted_func (SolverCallable): JIT-compiled solver function
        name (str): Solver identifier
    """

    func: SolverCallable
    jitted_func: SolverCallable
    name: str

    def get_func(self, jitted: bool = True) -> SolverCallable:
        """
        Get solver function.

        Args:
            jitted (bool, optional): Whether to return JIT-compiled version. Defaults to True.

        Returns:
            SolverCallable: Solver function (JIT-compiled or original)
        """
        return self.jitted_func if jitted else self.func

    def __repr__(self) -> str:
        return f"Solver(name={self.name})"


F = TypeVar("F", bound=SolverCallable)


class SolverRegistry:
    """
    Registry for numerical ODE solvers with JIT compilation support.

    Each solver must be registered with a unique name and follow the interface:
        - Input: (system_func, state, params, dt)
        - Output: next state vector

    Solvers are automatically JIT-compiled during registration.

    Attributes:
        _solvers: Internal dict mapping solver names to Solver instances

    Examples:
        >>> @SolverRegistry.register("rk4")
        >>> def rk4(system_func, state, params, dt):
        ...     # RK4 implementation
        ...     return next_state

        >>> solver = SolverRegistry.get("rk4")
    """

    _solvers: ClassVar[dict[str, Solver]] = {}

    @classmethod
    def register(cls, name: str) -> Callable[[F], F]:
        """Register a solver function in the SolverRegistry.

        Decorator that registers a solver function and creates a JIT-compiled version.
        The registered solver must take (system_func, state, params, dt) arguments and
        return the next state vector.

        Args:
            name (str): Unique identifier for the solver

        Returns:
            Callable[[F], F]: Decorator function that registers and JIT-compiles the solver

        Raises:
            TypeError: If name is not a string or decorated object is not callable
            ValueError: If solver name is already registered

        Examples:
            >>> @SolverRegistry.register("solver_name")
            >>> def custom_solver(system_func, state, params, dt):
            ...     # Solver implementation
            ...     return next_state
        """

        def decorator(f: F) -> F:
            if not isinstance(name, str):
                raise TypeError("Name must be string")
            if not callable(f):
                raise TypeError("Must register callable")
            if name in cls._solvers:
                msg = f"Solver {name} already registered"
                raise ValueError(msg)

            jitted_f = njit(f)
            cls._solvers[name] = Solver(f, jitted_f, name)
            return f

        logger.debug("Registered solver: %s", name)
        return decorator

    @classmethod
    def get(cls, name: str) -> Solver:
        """
        Retrieve a registered solver by name

        Args:
            name (str): Name of solver to retrieve

        Raises:
            KeyError: If solver name not found

        Returns:
            Solver: Registered Solver instance
        """
        if name not in cls._solvers:
            msg = f"Solver {name} not found"
            raise KeyError(msg)
        logger.debug("Getting solver: %s", name)
        return cls._solvers[name]

    @classmethod
    def list_solvers(cls) -> list[str]:
        """
        Get list of all registered solver names.

        Returns:
            list[str]: List of solver names
        """
        return list(cls._solvers.keys())

    @staticmethod
    def is_jitted(func: Callable[..., Any]) -> bool:
        """
        Check if a function is JIT-compiled.

        Args:
            func (Callable[..., Any]): Function to check

        Returns:
            bool: True if function is JIT-compiled
        """
        return isinstance(func, Dispatcher)
