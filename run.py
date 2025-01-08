import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection

from attractors import (
    SolverRegistry,
    SystemRegistry,
    ThemeManager,
    integrate_system,
)

theme = ThemeManager.get("ayu")

mpl.rcParams["path.simplify"] = True
mpl.rcParams["agg.path.chunksize"] = 10000
mpl.rcParams["path.simplify_threshold"] = 1.0

lorenz_system = SystemRegistry.get("lorenz")

solver = SolverRegistry.get("rk4")
steps = 10000
dt = 0.01


trajectory, time = integrate_system(lorenz_system, solver, steps, dt)

fig = plt.figure(figsize=(10, 8), facecolor=theme.background)
ax = fig.add_subplot(111, projection="3d")
ax.set_facecolor(theme.background)

segments = np.stack([trajectory[:-1], trajectory[1:]], axis=1)
z_avg = (trajectory[:-1, 2] + trajectory[1:, 2]) / 2
norm = plt.Normalize(trajectory[:, 2].min(), trajectory[:, 2].max())
colors = theme.colormap(norm(z_avg))

lc = Line3DCollection(segments, colors=colors, linewidth=1)
ax.add_collection3d(lc)

ax.set_xlim(*lorenz_system.plot_lims["xlim"])
ax.set_ylim(*lorenz_system.plot_lims["ylim"])
ax.set_zlim(*lorenz_system.plot_lims["zlim"])

for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
    axis.label.set_color(theme.foreground)
    axis.set_tick_params(colors=theme.foreground)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Lorenz Attractor", color=theme.foreground)

plt.show()
