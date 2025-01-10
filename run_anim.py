import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

from attractors import (
    SolverRegistry,
    SystemRegistry,
    ThemeManager,
    integrate_system,
)

# Setup
theme = ThemeManager.get("solarized_darcula")
system = SystemRegistry.get("langford")
solver = SolverRegistry.get("rk4")
steps = 100000
dt = 0.001

# Generate trajectory
trajectory, time = integrate_system(system, solver, steps, dt)

# Create figure
fig = plt.figure(figsize=(10, 8), facecolor=theme.background)
ax = fig.add_subplot(111, projection="3d")
ax.set_facecolor(theme.background)
ax.set_axis_off()

# Setup plot limits
ax.set_xlim(*system.plot_lims["xlim"])
ax.set_ylim(*system.plot_lims["ylim"])
ax.set_zlim(*system.plot_lims["zlim"])

# Setup segments
num_segments = 50
segment_length = len(trajectory) // num_segments
colors = theme.colormap(np.linspace(0, 1, num_segments))
lines = []

# Initialize empty lines
for i in range(num_segments):
    line = ax.plot([], [], [], "-", c=colors[i], linewidth=1, antialiased=True)[0]
    lines.append(line)


def init():
    for line in lines:
        line.set_data_3d([], [], [])
    return lines


speed = 20


def update(frame):
    # Calculate how many segments to show based on frame
    frame = frame * speed
    active_segments = min(frame // segment_length + 1, num_segments)

    for i in range(num_segments):
        if i < active_segments:
            start_idx = i * segment_length
            end_idx = min(start_idx + segment_length, frame + 1)
            line = lines[i]
            line.set_data_3d(
                trajectory[start_idx:end_idx, 0],
                trajectory[start_idx:end_idx, 1],
                trajectory[start_idx:end_idx, 2],
            )

    # Rotate view
    # ax.view_init(elev=30, azim=frame / 2)
    return lines


# Create animation
anim = animation.FuncAnimation(
    fig,
    update,
    init_func=init,
    frames=steps // speed,
    interval=1,
)

plt.show()
