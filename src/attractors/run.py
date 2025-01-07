import matplotlib.pyplot as plt
import numpy as np

from attractors.solvers.core import integrate_trajectory
from attractors.solvers.registry import SolverRegistry
from attractors.systems.registry import SystemRegistry

# Setup
initial_state = np.array([0.1, 0.1, 0.1])
params = np.array([10.0, 28.0, 8 / 3])
system = SystemRegistry.get("lorenz")
solver = SolverRegistry.get("rk4")
steps = 10000
dt = 0.01


trajectory, time = integrate_trajectory(
    system, solver, initial_state, params, steps, dt
)

# Create 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")
ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2], lw=0.5)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Lorenz Attractor")

plt.show()
