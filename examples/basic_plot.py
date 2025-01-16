import matplotlib.pyplot as plt

from attractors import (
    SolverRegistry,
    StaticPlotter,
    SystemRegistry,
    ThemeManager,
    integrate_system,
)

# you cal also use custom themes, or get predefined themes from the ThemeManager
# theme = Theme(
#     name="monochrome",
#     background="#FFFFFF",
#     colors=["#616161", "#7a7a7a", "#2e2e2e", "#1c1c1c"],
#     foreground="#000000",  # Black foreground for contrast with white background
# )

# setup
theme = ThemeManager.random()
system = SystemRegistry.get("lorenz")
solver = SolverRegistry.get("rk4")
steps = 10000
dt = 0.001

# generate trajectory
trajectory, time = integrate_system(system, solver, steps, dt)

# use the StaticPlotter class to create an animation
plotter = StaticPlotter(
    system,
    theme,
    fig_kwargs={"figsize": (10, 8)},
).visualize(
    trajectory,
    line_kwargs={"linewidth": 1, "antialiased": True, "alpha": 0.7},
)

plt.show()
