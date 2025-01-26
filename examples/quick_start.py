import matplotlib.pyplot as plt

from attractors import SolverRegistry, StaticPlotter, SystemRegistry, ThemeManager, integrate_system

# Get system and solver from registry
system = SystemRegistry.get("rossler")  # Using default parameters
solver = SolverRegistry.get("rk4")  # 4th order Runge-Kutta

# Generate trajectory
trajectory, time = integrate_system(system, solver, steps=1000000, dt=0.001)

# Create visualization
theme = ThemeManager.random()
plotter = StaticPlotter(system, theme)
plotter.visualize(trajectory, line_kwargs={"linewidth": 1})
plt.savefig("output.png", dpi=600)
