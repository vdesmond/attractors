from collections.abc import Callable
from typing import TypeAlias

import numpy as np
from numpy.typing import NDArray

StateVector: TypeAlias = NDArray[np.float64]
ParamVector: TypeAlias = NDArray[np.float64]
SystemCallable: TypeAlias = Callable[[StateVector, ParamVector], StateVector]
SolverCallable: TypeAlias = Callable[
    [SystemCallable, StateVector, ParamVector, float], StateVector
]
