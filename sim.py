#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
import matplotlib.pyplot as plt
import matplotlib as mpl
from runge_kutta import RK

mpl.use("Qt5Cairo")
plt.style.use('dark_background')
fig = plt.figure(figsize=(16, 9), dpi=120)
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('off')

# * Lorenz
# initial_r_states = [[0.1,0.1,0.1], [0.15,0.1,0.1], [0.1,0.15,0.1], [0.1,0.1,0.15]]
# attractor_vects = [RK(r, 'lorenz', sigma=5, beta=8/3, rho=28) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK5(0, 50, 6000)

# ax.set_xlim((-20, 20))
# ax.set_ylim((-30, 30))
# ax.set_zlim((5, 45))

# * Rabinovich Fabrikant
# initial_r_states = [[-1, -0, 0.5], [-0.5, -0.03, 0.45]]
# attractor_vects = [RK(r, 'rabinovich_fabrikant', alpha=0.14, gamma=0.1) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK5(0, 70, 6000)

# ax.set_xlim((-5, 5))
# ax.set_ylim((-5, 5))
# ax.set_zlim((5, 45))

# * Lotka Volterra
# initial_r_states = [[0.1, -0.1, -0.1]]
# attractor_vects = [RK(r, 'lotka_volterra') for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 50, 6000)

# ax.set_xlim((-20, 20))
# ax.set_ylim((-30, 30))
# ax.set_zlim((5, 45))

# * Rossler
# initial_r_states = [[0.1, 0, -0.1], [0.11, 0, -0.11]]
# attractor_vects = [RK(r, 'rossler', a=0.2, b=0.2, c=5.7) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 150, 18000)

# ax.set_xlim((-2, 2))
# ax.set_ylim((-2, 2))
# ax.set_zlim((5, 30))

# * Wang Sun
# initial_r_states = [[0.5, 0.1, 0.1]]
# attractor_vects = [RK(r, 'wang_sun', a=0.2, b=-0.01, c=1,d=-0.4, e=-1.0,f=-1) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 350, 18000)

# ax.set_xlim((-5, 5))
# ax.set_ylim((-5, 5))
# ax.set_zlim((5, 45))

# * Rikitake
initial_r_states = [[0.1, 0.1, -0.1]]
attractor_vects = [RK(r, 'rikitake', a=5, mu=2) for r in initial_r_states]
for vect in attractor_vects:
    vect.RK4(0, 100, 18000)

ax.set_xlim((-5, 5))
ax.set_ylim((-5, 5))
ax.set_zlim((5, 45))

#! 0
colors = plt.cm.hsv(np.linspace(0.5, 0.5, len(attractor_vects)))

lines = sum([ax.plot([], [], [], '-', c=c, linewidth=1, antialiased=True)
             for c in colors], [])
points = sum([ax.plot([], [], [], 'o', c=c)
           for c in colors], [])                   

def init():
    for line, pt in zip(lines, points):
        line.set_data_3d([], [], [])

        pt.set_data_3d([], [], [])
    return lines + points

def animate(i):
    steps = 4
    i = (steps * i) % len(attractor_vects[0].X)
    # print(i)
    for line, pt, k in zip(lines, points, attractor_vects):
        if i>10000:
            line.set_data_3d(k.X[i-10000:i], k.Y[i-10000:i], k.Z[i-10000:i])
        else:
            line.set_data_3d(k.X[:i], k.Y[:i], k.Z[:i])
        pt.set_data_3d(k.X[i], k.Y[i], k.Z[i])
    ax.view_init(0.005 * i, 0.05 * i)
    fig.canvas.draw()
    return lines + points

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=18000//4, interval=5, blit=False)

# mywriter = animation.FFMpegWriter(bitrate=5000)
# anim.save('test2.mp4', writer='fclearfmpeg', fps=20, extra_args=['-vcodec', 'libx264'])

plt.show()