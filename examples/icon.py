import matplotlib.pyplot as plt
import numpy as np

from attractors import (
    SolverRegistry,
    SystemRegistry,
    ThemeManager,
    integrate_system,
)


def generate_icon(include_text=True, output_filename=None):
    # Setup
    theme = ThemeManager.get("vdesmond_horizon")
    print(theme.name)
    system = SystemRegistry.get("rucklidge")
    solver = SolverRegistry.get("rk4")

    # Generate trajectory
    steps = 500000
    dt = 0.001
    trajectory, _ = integrate_system(system, solver, steps, dt)

    # Create figure
    fig = plt.figure(figsize=(9, 8), facecolor=theme.background)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor(theme.background)
    ax.set_axis_off()

    # Plot attractor
    colors = theme.colormap(np.linspace(0, 0.9, 50))
    segment_size = len(trajectory) // 50

    for i, color in enumerate(colors):
        start_idx = i * segment_size
        end_idx = start_idx + segment_size
        segment = trajectory[start_idx:end_idx]
        ax.plot(segment[:, 0], segment[:, 1], segment[:, 2], c=color, linewidth=1, alpha=0.7)

    # Set view and limits
    ax.view_init(elev=152.90, azim=40.754)
    ax.set_xlim(-15.64, 5.98)
    ax.set_ylim(-9.86, 12.06)
    ax.set_zlim(-2.69, 19.08)

    if include_text:
        ax.text2D(
            0.7,
            0.5,
            "ttractors",
            fontsize=60,
            ha="center",
            va="center",
            transform=fig.transFigure,
            color=theme.foreground,
            alpha=1,
            weight="light",
            fontname="Sora",
            rasterized=False,
        )

    # Save
    if output_filename:
        plt.savefig(output_filename, dpi=1200, bbox_inches="tight", pad_inches=0.1)
        plt.close()
    else:
        plt.show()


# Generate both versions
# generate_icon(include_text=True, output_filename="attractor_with_text.png")
generate_icon(include_text=False, output_filename="attractor_icon.png")
