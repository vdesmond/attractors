# Systems Guide

## Overview

Systems in the attractors package represent chaotic dynamical systems - mathematical models defined by differential equations that exhibit complex, unpredictable behavior despite being deterministic.

## Architecture

### System Structure

Each system in attractors is defined by:

1. **Differential Equations**: The mathematical model (ODEs) that govern the system's evolution
2. **Parameters**: System-specific constants that control behavior
3. **Initial Conditions**: Starting state of the system
4. **Dimension**: Spatial dimension (2D or 3D)

### The Registry Pattern

All systems are registered in the `SystemRegistry`, which provides:

- **Centralized lookup**: `SystemRegistry.get("lorenz")`
- **Discoverability**: `SystemRegistry.list_systems()`
- **Consistent interface**: All systems follow the same API

### System Definition Example

```python
from __future__ import annotations

import numpy as np
from numba import njit
from attractors.systems.registry import SystemRegistry

@njit
def equations(state: np.ndarray, _t: float, params: dict) -> np.ndarray:
    """Lorenz system equations."""
    x, y, z = state
    sigma = params["sigma"]
    rho = params["rho"]
    beta = params["beta"]

    dx_dt = sigma * (y - x)
    dy_dt = x * (rho - z) - y
    dz_dt = x * y - beta * z

    return np.array([dx_dt, dy_dt, dz_dt])

SystemRegistry.register(
    name="lorenz",
    equations=equations,
    default_params={"sigma": 10.0, "rho": 28.0, "beta": 8/3},
    default_initial_conditions=np.array([1.0, 1.0, 1.0]),
    dimension=3,
)
```

## Using Systems

### Basic Usage

```python
from attractors import SystemRegistry, SolverRegistry, integrate_system

# Get a system from the registry
system = SystemRegistry.get("lorenz")

# Inspect system properties
print(f"Dimension: {system.dimension}")
print(f"Parameters: {system.params}")
print(f"Initial conditions: {system.initial_conditions}")

# Integrate the system
solver = SolverRegistry.get("rk4")
trajectory, time = integrate_system(system, solver, steps=10000, dt=0.01)
```

### Customizing Parameters

```python
# Get system with custom parameters
system = SystemRegistry.get("lorenz", sigma=16.0, rho=45.92, beta=4.0)

# Or modify after creation
system = SystemRegistry.get("lorenz")
system.params["rho"] = 99.96
```

### Custom Initial Conditions

```python
import numpy as np

system = SystemRegistry.get("lorenz")
system.initial_conditions = np.array([10.0, 10.0, 10.0])
```

## Available Systems

The package includes 20+ strange attractors. List all available systems:

```python
from attractors import SystemRegistry

systems = SystemRegistry.list_systems()
print(systems)  # ['lorenz', 'rossler', 'thomas', ...]
```

### System Categories

**Classic Attractors**:
- `lorenz`: The iconic butterfly attractor
- `rossler`: Continuous-time chaotic system with one non-linearity
- `chen`: Lorenz-like system discovered in 1999

**Rare Gems**:
- `thomas`: Cyclically symmetric attractor
- `aizawa`: Seven-parameter system with rich dynamics
- `halvorsen`: Three-dimensional cyclically symmetric system

See the full list in the [API documentation](../api.md).

## Performance Considerations

### Numba JIT Compilation

All system equations are decorated with `@njit` (Numba's no-python JIT compiler):

- **First call**: Compilation overhead (~1 second)
- **Subsequent calls**: Native-speed execution (~100x faster than pure Python)

```python
# First integration: ~1 second (includes compilation)
trajectory1, _ = integrate_system(system, solver, steps=10000, dt=0.01)

# Second integration: ~0.01 seconds (compiled)
trajectory2, _ = integrate_system(system, solver, steps=10000, dt=0.01)
```

### Choosing Step Size (dt)

The integration step size affects:

- **Accuracy**: Smaller `dt` = more accurate
- **Performance**: Larger `dt` = faster
- **Stability**: Too large `dt` can cause divergence

**Guidelines**:
- Start with `dt=0.01` for most systems
- For stiff systems, use `dt=0.001`
- For long trajectories, use adaptive solvers like `rk45`

```python
# High accuracy (slow)
trajectory, _ = integrate_system(system, solver, steps=100000, dt=0.001)

# Balanced (recommended)
trajectory, _ = integrate_system(system, solver, steps=10000, dt=0.01)

# Fast preview (may be inaccurate)
trajectory, _ = integrate_system(system, solver, steps=1000, dt=0.1)
```

## Creating Custom Systems

See the [Contributing Guide](../../CONTRIBUTING.md#contributing-new-attractors) for detailed instructions on adding new attractors.

### Quick Template

```python
from __future__ import annotations

import numpy as np
from numba import njit
from attractors.systems.registry import SystemRegistry

@njit
def my_system_equations(state: np.ndarray, _t: float, params: dict) -> np.ndarray:
    x, y, z = state
    a = params["a"]

    dx_dt = # your equation
    dy_dt = # your equation
    dz_dt = # your equation

    return np.array([dx_dt, dy_dt, dz_dt])

SystemRegistry.register(
    name="my_system",
    equations=my_system_equations,
    default_params={"a": 1.0},
    default_initial_conditions=np.array([1.0, 1.0, 1.0]),
    dimension=3,
)
```

## Advanced Topics

### System Stability

Not all parameter combinations produce chaotic behavior. Some may:

- Converge to fixed points
- Diverge to infinity
- Exhibit periodic behavior

Always validate new parameter sets:

```python
trajectory, _ = integrate_system(system, solver, steps=10000, dt=0.01)

# Check for divergence
assert np.all(np.isfinite(trajectory)), "System diverged!"

# Check for boundedness
max_val = np.max(np.abs(trajectory))
assert max_val < 1e6, f"System unbounded: max value = {max_val}"
```

### Chaotic Behavior Verification

Verify sensitive dependence on initial conditions:

```python
import numpy as np

system1 = SystemRegistry.get("lorenz")
system2 = SystemRegistry.get("lorenz")

# Tiny perturbation
system2.initial_conditions = system1.initial_conditions + 1e-8

# Integrate both
traj1, _ = integrate_system(system1, solver, steps=5000, dt=0.01)
traj2, _ = integrate_system(system2, solver, steps=5000, dt=0.01)

# Calculate divergence
distance = np.linalg.norm(traj1 - traj2, axis=1)

# Should show exponential divergence initially
print(f"Final separation: {distance[-1]:.6f}")  # Should be >> 1e-8
```

## Troubleshooting

### Common Issues

**System diverges to infinity**:
- Reduce `dt`
- Check parameter values
- Verify initial conditions

**Results not reproducible**:
- Ensure same `dt` and `steps`
- Check NumPy/Numba versions
- Numerical errors accumulate over long integrations

**Compilation warnings**:
- Normal on first run (Numba JIT compilation)
- Ignored on subsequent runs

**Performance slower than expected**:
- First run includes compilation time
- Use `@njit(cache=True)` for persistent compilation (advanced)

## See Also

- [Solvers Guide](solvers.md) - Numerical integration methods
- [Visualization Guide](visualization.md) - Plotting trajectories
- [API Reference](../api.md) - Complete API documentation
