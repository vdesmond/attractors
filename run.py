import matplotlib.pyplot as plt

from attractors import (
    SolverRegistry,
    StaticPlotter,
    SystemRegistry,
    Theme,
    ThemeManager,
    integrate_system,
)

theme = ThemeManager.get("aurora")
# or
# theme = Theme(
#     name="monochrome",
#     background="#FFFFFF",
#     colors=["#616161", "#7a7a7a", "#2e2e2e", "#1c1c1c"],
#     foreground="#000000",  # Black foreground for contrast with white background
# )

system = SystemRegistry.get("hadley")
solver = SolverRegistry.get("rk4")
steps = 1000000
dt = 0.001
trajectory, time = integrate_system(system, solver, steps, dt)


plotter = StaticPlotter(
    system,
    theme,
    fig_kwargs={"figsize": (10, 8)},
    line_kwargs={"linewidth": 0.5, "antialiased": True, "alpha": 0.7},
).plot(trajectory)

plt.show()
