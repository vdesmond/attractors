from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, ClassVar, TypeVar

from numba import njit
from numba.core.dispatcher import Dispatcher

from attractors.type_defs import PlotLimits, SystemCallable, Vector
from attractors.utils.logger import setup_logger

logger = setup_logger(name=__name__)


@dataclass
class System:
    """
    Data class representing a dynamical system with JIT compilation support.

    Attributes:
        func (SystemCallable): Original system function
        jitted_func (SystemCallable): JIT-compiled system function
        name (str): System identifier
        params (Vector): System parameters vector
        param_names (list[str]): List of parameter names
        reference (str): Academic reference
        init_coord (Vector): Initial state vector
        plot_lims (PlotLimits | None): Optional plotting limits
    """

    func: SystemCallable
    jitted_func: SystemCallable
    name: str
    params: Vector
    param_names: list[str]
    reference: str
    init_coord: Vector
    plot_lims: PlotLimits | None = None

    def set_params(self, params: Vector) -> None:
        """
        Set system parameters.

        Args:
            params (Vector): New parameter vector

        Raises:
            ValueError: If parameter count doesn't match expected number of parameters
        """
        if len(params) != len(self.param_names):
            msg = f"Expected {len(self.param_names)} parameters"
            raise ValueError(msg)
        logger.debug("Setting parameters: %s for system: %s", params, self.name)
        self.params = params

    def set_init_coord(self, coord: Vector) -> None:
        """
        Set initial state coordinates.

        Args:
            coord (Vector): Initial state vector (must have length 3)

        Raises:
            ValueError: If coordinate vector length is not 3
        """
        if len(coord) != 3:
            raise ValueError("State vector must have length 3")
        logger.debug("Setting initial coord: %s for system: %s", coord, self.name)
        self.init_coord = coord

    def get_func(self, jitted: bool = True) -> SystemCallable:
        """
        Get system function.

        Args:
            jitted (bool, optional): Whether to return JIT-compiled version. Defaults to True.

        Returns:
            SystemCallable: System function (JIT-compiled or original)
        """
        return self.jitted_func if jitted else self.func


F = TypeVar("F", bound=SystemCallable)


class SystemRegistry:
    """
    Registry for dynamical systems with JIT compilation support.

    Each system must be registered with:
        - Unique name
        - Default parameters and their names
        - Initial coordinates
        - Optional plotting limits and academic reference

    Systems are automatically JIT-compiled during registration.

    Attributes:
        _systems: Internal dict mapping system names to System instances

    Examples:
        >>> @SystemRegistry.register(
        ...     "lorenz",
        ...     default_params=np.array([10.0, 28.0, 8 / 3]),
        ...     param_names=["sigma", "rho", "beta"],
        ...     init_coord=np.array([0.0, 1.0, 0.0]),
        ... )
        ... def lorenz(state: Vector, params: Vector) -> Vector:
        ...     x, y, z = state
        ...     sigma, rho, beta = params
        ...     return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])
    """

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
        """
        Register a system function in the SystemRegistry.

        Decorator that registers a system function and creates a JIT-compiled version.
        The registered system must take (state, params) Vector type arguments and
        return the next state vector.

        Args:
            name (str): Unique identifier for the system
            default_params (Vector): Default parameter values
            param_names (list[str]): Names of parameters
            reference (str, optional): Academic reference. Defaults to "".
            init_coord (Vector): Initial state vector
            plot_lims (PlotLimits | None, optional): Plotting limits. Defaults to None.

        Returns:
            Callable[[F], F]: Decorator function that registers and JIT-compiles the system

        Raises:
            TypeError: If name is not a string or decorated object is not callable
            ValueError: If system name is already registered

        Examples:
            >>> @SystemRegistry.register("lorenz")
            ... def lorenz(state: Vector, params: Vector) -> Vector:
            ...     x, y, z = state
            ...     sigma, rho, beta = params
            ...     return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])
        """

        def decorator(f: F) -> F:
            if not isinstance(name, str):
                raise TypeError("Name must be string")
            if not callable(f):
                raise TypeError("Must register callable")
            if name in cls._systems:
                msg = f"System {name} already registered"
                raise ValueError(msg)

            jitted_f = f if cls.is_jitted(f) else njit(f)
            cls._systems[name] = System(
                func=f,
                jitted_func=jitted_f,
                name=name,
                params=default_params,
                param_names=param_names,
                reference=reference,
                init_coord=init_coord,
                plot_lims=plot_lims,
            )
            return f

        logger.debug("Registered system: %s", name)
        return decorator

    @classmethod
    def get(cls, name: str) -> System:
        """
        Get registered system by name.

        Args:
            name (str): Name of system to retrieve

        Returns:
            System: Registered System instance

        Raises:
            KeyError: If system name is not found
        """
        if name not in cls._systems:
            msg = f"System {name} not found"
            raise KeyError(msg)
        logger.debug("Getting system: %s", name)
        return cls._systems[name]

    @classmethod
    def list_systems(cls) -> list[str]:
        """
        Get list of all registered system names.

        Returns:
            list[str]: List of registered system names
        """
        return list(cls._systems.keys())

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
