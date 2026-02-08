# Contributing to Attractors

Thank you for your interest in contributing to attractors! This guide will help you understand the project architecture and how to contribute new attractors, solvers, themes, or improvements.

## Table of Contents

- [Getting Started](#getting-started)
- [Architecture Overview](#architecture-overview)
- [Contributing New Attractors](#contributing-new-attractors)
- [Contributing New Solvers](#contributing-new-solvers)
- [Contributing Themes](#contributing-themes)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)

## Getting Started

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/attractors.git
   cd attractors
   ```

2. **Install [uv](https://docs.astral.sh/uv/)** (recommended)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies**
   ```bash
   uv sync --all-groups
   ```

4. **Run tests to verify setup**
   ```bash
   uv run pytest
   ```

### Development Tools

- **Format code**: `uv run ruff format`
- **Lint code**: `uv run ruff check --fix .`
- **Type check**: `uv run mypy src/`
- **Run tests**: `uv run pytest`
- **Run tests with coverage**: `uv run pytest --cov`

## Architecture Overview

The attractors package is built around a modular, registry-based architecture with four core components:

### 1. **Systems** (`src/attractors/systems/`)

Define the differential equations that govern chaotic systems. Each attractor is a system with:
- **Equations**: The mathematical model (ODEs)
- **Parameters**: System-specific constants (e.g., σ, ρ, β for Lorenz)
- **Metadata**: Name, description, dimensions, default initial conditions

**Registry Pattern**: All systems are registered in `SystemRegistry` for easy lookup and instantiation.

### 2. **Solvers** (`src/attractors/solvers/`)

Numerical integration methods that evolve systems over time:
- **Runge-Kutta methods**: RK4, RK45 (adaptive), Dormand-Prince
- **Numba-accelerated**: High-performance JIT compilation
- **Modular interface**: Easy to add new integration schemes

**Registry Pattern**: Solvers are registered in `SolverRegistry`.

### 3. **Themes** (`src/attractors/themes/`)

Visual styling for plots:
- **Color schemes**: Background, foreground, accent colors
- **Typography**: Font configurations
- **Presets**: Nord, Monokai, Solarized, etc.

**Registry Pattern**: Themes loaded from JSON via `ThemeManager`.

### 4. **Visualizers** (`src/attractors/visualizers/`)

Rendering engines for static and animated plots:
- **StaticPlotter**: Single-frame visualizations
- **AnimatedPlotter**: Time-evolving animations
- **Color mappers**: Velocity, distance, time-based coloring
- **Downsampling**: Compression for large trajectories

### Data Flow

```
System → Solver → Trajectory → Visualizer → Plot
   ↓        ↓                      ↓
Registry Registry              ThemeManager
```

## Contributing New Attractors

### Step-by-Step Guide

#### 1. Choose a System

Research and select a chaotic attractor. Good sources:
- Academic papers
- [Chaos Book](https://chaosbook.org/)
- [Wikipedia's list of chaotic maps](https://en.wikipedia.org/wiki/List_of_chaotic_maps)

Ensure the system:
- Exhibits chaotic behavior
- Has known stable parameters
- Is visually interesting

#### 2. Create System File

Create a new file in `src/attractors/systems/` named `<attractor_name>.py`:

```python
"""Short description of the attractor.

Historical context, discovered by whom, when, significance, etc.
Include references if applicable.
"""

from __future__ import annotations

import numpy as np
from numba import njit

from attractors.systems.registry import SystemRegistry

# Define system parameters (with sensible defaults)
DEFAULT_PARAM_A = 10.0
DEFAULT_PARAM_B = 28.0
# ... more parameters


@njit
def equations(state: np.ndarray, _t: float, params: dict) -> np.ndarray:
    """Compute derivatives for the <AttractorName> system.

    Args:
        state: Current state [x, y, z, ...]
        _t: Current time (unused for autonomous systems)
        params: System parameters

    Returns:
        Derivatives [dx/dt, dy/dt, dz/dt, ...]
    """
    # Unpack state
    x, y, z = state  # Adjust dimensions as needed

    # Unpack parameters
    a = params["a"]
    b = params["b"]
    # ... more params

    # Define equations
    dx_dt = # ... your equation
    dy_dt = # ... your equation
    dz_dt = # ... your equation

    return np.array([dx_dt, dy_dt, dz_dt])


# Register the system
SystemRegistry.register(
    name="attractor_name",  # lowercase, snake_case
    equations=equations,
    default_params={
        "a": DEFAULT_PARAM_A,
        "b": DEFAULT_PARAM_B,
        # ... all parameters
    },
    default_initial_conditions=np.array([1.0, 1.0, 1.0]),  # Stable starting point
    dimension=3,  # 2D or 3D
)
```

#### 3. Parameter Guidelines

**Choosing Default Parameters:**
- Use values from literature when available
- Ensure parameters produce stable, chaotic behavior
- Avoid parameters that cause overflow, underflow, or convergence to fixed points
- Test with different integration step sizes (`dt`)

**Initial Conditions:**
- Should lead to attractor (not escape to infinity)
- Non-zero for most systems
- Test sensitivity: slightly different ICs should still show chaotic behavior

**Validation Checklist:**
- [ ] System exhibits sensitive dependence on initial conditions
- [ ] Trajectory is bounded (doesn't explode to infinity)
- [ ] Visually distinct and interesting structure
- [ ] Stable across dt values (0.001 - 0.1)

#### 4. Add Tests

Create/update `tests/systems/test_<attractor_name>.py`:

```python
import numpy as np
import pytest

from attractors import SystemRegistry


def test_attractor_name_registered():
    """Test that the attractor is registered."""
    system = SystemRegistry.get("attractor_name")
    assert system is not None


def test_attractor_name_integration():
    """Test that integration produces bounded results."""
    from attractors import SolverRegistry, integrate_system

    system = SystemRegistry.get("attractor_name")
    solver = SolverRegistry.get("rk4")

    trajectory, time = integrate_system(system, solver, steps=1000, dt=0.01)

    # Check trajectory is bounded
    assert np.all(np.isfinite(trajectory))
    assert np.max(np.abs(trajectory)) < 1e6  # Adjust bound as needed

    # Check shape
    assert trajectory.shape == (1000, 3)  # Adjust dimension


def test_attractor_name_chaotic():
    """Test sensitive dependence on initial conditions."""
    from attractors import SolverRegistry, integrate_system

    system1 = SystemRegistry.get("attractor_name")
    system2 = SystemRegistry.get("attractor_name")

    # Slightly perturb initial conditions
    system2.initial_conditions = system1.initial_conditions + 1e-8

    solver = SolverRegistry.get("rk4")

    traj1, _ = integrate_system(system1, solver, steps=5000, dt=0.01)
    traj2, _ = integrate_system(system2, solver, steps=5000, dt=0.01)

    # Trajectories should diverge
    distance = np.linalg.norm(traj1[-1] - traj2[-1])
    assert distance > 0.1  # Adjust threshold based on system
```

#### 5. Update Documentation

Add your system to the appropriate section in `docs/` (TBD - will be clarified in future).

#### 6. Create Example Visualization

Add an example in `examples/` demonstrating your attractor:

```python
"""Example visualization of <AttractorName> attractor."""

import matplotlib.pyplot as plt

from attractors import (
    SolverRegistry,
    StaticPlotter,
    SystemRegistry,
    ThemeManager,
    integrate_system,
)

# Get system and solver
system = SystemRegistry.get("attractor_name")
solver = SolverRegistry.get("rk4")

# Generate trajectory
trajectory, time = integrate_system(system, solver, steps=10000, dt=0.01)

# Visualize
theme = ThemeManager.get("nord")
plotter = StaticPlotter(system, theme)
plotter.visualize(trajectory)
plt.show()
```

## Contributing New Solvers

New numerical integration methods are welcome! Follow the existing solver pattern:

1. Create solver in `src/attractors/solvers/methods/`
2. Decorate with `@njit` for performance
3. Implement solver interface (see existing solvers)
4. Register in `SolverRegistry`
5. Add tests comparing against known solutions

## Contributing Themes

To add new color themes:

1. Edit `src/attractors/themes/viz_themes.json`
2. Follow the existing schema:
   ```json
   {
     "theme_name": {
       "background": "#HEX",
       "foreground": "#HEX",
       "accent": "#HEX",
       "font": "Font Name"
     }
   }
   ```
3. Ensure sufficient contrast between background and foreground

## Code Standards

### Style

- **Format**: Ruff (automatic formatting)
- **Linting**: Ruff (enforced in CI)
- **Type hints**: Required for all public APIs
- **Docstrings**: Google style for all public functions/classes

### Conventions

- **Naming**:
  - Systems: lowercase, snake_case (e.g., `lorenz`, `rossler`)
  - Solvers: lowercase abbreviations (e.g., `rk4`, `rk45`)
  - Classes: PascalCase
  - Functions/variables: snake_case

- **Imports**: Use `from __future__ import annotations` at the top

- **Type Checking**: Code must pass `mypy src/`

### Performance

- Use `@njit` from Numba for numerical code
- Avoid Python loops in hot paths
- Prefer NumPy vectorization

## Testing

### Test Requirements

All contributions must include tests:

- **Systems**: Integration tests, chaos validation
- **Solvers**: Accuracy tests against known solutions
- **Visualizers**: Output validation (not visual inspection)

### Running Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov --cov-report=term

# Specific test file
uv run pytest tests/systems/test_lorenz.py

# Verbose output
uv run pytest -v
```

### Coverage

Maintain >90% code coverage. Check coverage report after adding code.

## Submitting Changes

### Pull Request Process

1. **Create a branch**
   ```bash
   git checkout -b feature/new-attractor-name
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

3. **Verify quality**
   ```bash
   uv run ruff format
   uv run ruff check --fix .
   uv run mypy src/
   uv run pytest
   ```

4. **Commit with clear messages**
   ```bash
   git commit -m "Add <AttractorName> system

   - Implement equations with default parameters
   - Add integration and chaos tests
   - Include example visualization
   "
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/new-attractor-name
   ```
   Then open a PR on GitHub.

### PR Checklist

Use this checklist in your PR description:

- [ ] Code follows style guidelines (ruff format, ruff check)
- [ ] Type hints pass mypy validation
- [ ] All tests pass locally
- [ ] New tests added for new functionality
- [ ] Documentation updated (if applicable)
- [ ] Example code provided (for new systems)
- [ ] Parameters validated (for new systems)
- [ ] Chaos behavior verified (for new systems)

### Review Process

- Maintainers will review your PR
- CI must pass (lint, type check, tests on multiple platforms)
- Address feedback in new commits
- Once approved, maintainers will merge

## Questions?

- **Bugs/Issues**: [GitHub Issues](https://github.com/vdesmond/attractors/issues)
- **Discussions**: [GitHub Discussions](https://github.com/vdesmond/attractors/discussions)
- **Documentation**: [attractors.vdesmond.com](https://attractors.vdesmond.com/)

## Code of Conduct

Be respectful, constructive, and collaborative. We're all here to create beautiful chaos together!

---

**Thank you for contributing to attractors!** 🦋
