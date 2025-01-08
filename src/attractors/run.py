import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from attractors.solvers.core import integrate_trajectory
from attractors.solvers.registry import SolverRegistry
from attractors.systems.registry import SystemRegistry
from attractors.themes.manager import ThemeManager

theme = ThemeManager.get("ayu")
initial_state = np.array([0.1, 0.1, 0.1])
params = np.array([10.0, 28.0, 8 / 3])
system = SystemRegistry.get("lorenz")
solver = SolverRegistry.get("rk4")
steps = 10000
dt = 0.01

mpl.rcParams["path.simplify"] = True
mpl.rcParams["agg.path.chunksize"] = 10000
mpl.rcParams["path.simplify_threshold"] = 1.0

trajectory, time = integrate_trajectory(
    system, solver, initial_state, params, steps, dt
)

fig = plt.figure(figsize=(10, 8), facecolor=theme.background)
ax = fig.add_subplot(111, projection="3d")
ax.set_facecolor(theme.background)

# Create segments and colors
segments = np.stack([trajectory[:-1], trajectory[1:]], axis=1)
z_avg = (trajectory[:-1, 2] + trajectory[1:, 2]) / 2
norm = plt.Normalize(trajectory[:, 2].min(), trajectory[:, 2].max())
colors = theme.colormap(norm(z_avg))

lc = Line3DCollection(segments, colors=colors, linewidth=1)
ax.add_collection3d(lc)

ax.set_xlim(trajectory[:, 0].min(), trajectory[:, 0].max())
ax.set_ylim(trajectory[:, 1].min(), trajectory[:, 1].max())
ax.set_zlim(trajectory[:, 2].min(), trajectory[:, 2].max())

for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
    axis.label.set_color(theme.foreground)
    axis.set_tick_params(colors=theme.foreground)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Lorenz Attractor", color=theme.foreground)

plt.show()
