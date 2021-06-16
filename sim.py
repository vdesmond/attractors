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
fig.set_facecolor('#252a34') #! add bg argument
ax.set_facecolor('#252a34')

# * Lorenz
# initial_r_states = [[0.1,0.1,0.1], [0.15,0.1,0.1], [0.1,0.15,0.1], [0.1,0.1,0.15]]
# attractor_vects = [RK(r, 'lorenz', beta=8/3, sigma=5, rhoo=28) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK5(0, 50, 6000)

# ax.set_xlim((-20, 20))
# ax.set_ylim((-30, 30))
# ax.set_zlim((5, 45))

# * Rabinovich Fabrikant
# initial_r_states = [[-1, -1, 0.5]]
# attractor_vects = [RK(r, 'rabinovich_fabrikant', alpha=0.14, gamma=0.1) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK5(0, 350, 35000)

# ax.set_xlim((-5, 5))
# ax.set_ylim((-5, 5))
# ax.set_zlim((5, 45))

# initial_r_states = [[-1, 0, 0.5]]
# attractor_vects = [RK(r, 'rabinovich_fabrikant', alpha=1.1, gamma=0.87) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK5(0, 350, 35000)

# ax.set_xlim((-5, 5))
# ax.set_ylim((-5, 5))
# ax.set_zlim((5, 45))

# * Lotka Volterra
# initial_r_states = [[1.0, 1.0, 1.0]]
# attractor_vects = [RK(r, 'lotka_volterra', a=2.9851, b=3.0, c=2) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 300, 20000)

# ax.set_xlim((0.5, 1.5))
# ax.set_ylim((0.5, 1.5))
# ax.set_zlim((2, 10))

# * Rossler
# initial_r_states = [[0.1, 0, -0.1], [0.11, 0, -0.11]]
# attractor_vects = [RK(r, 'rossler', a=0.2, b=0.2, c=5.7) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 150, 18000)

# ax.set_xlim((-10, 10))
# ax.set_ylim((-10, 10))
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
# initial_r_states = [[0.1, 0.1, -0.1]]
# attractor_vects = [RK(r, 'rikitake', a=5, mu=2) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 100, 18000)

# ax.set_xlim((-5, 5))
# ax.set_ylim((-5, 5))
# ax.set_zlim((5, 45))

# * Nose Hoover
# initial_r_states = [[0.1, 0, -0.1], [0.2, 0.1, -0.2], [0.15, 0.05, -0.15]]
# attractor_vects = [RK(r, 'nose_hoover', a=1) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 100, 18000)

# ax.set_xlim((-5, 5))
# ax.set_ylim((-5, 5))
# ax.set_zlim((5, 45))

# * Duffing
# initial_r_states = [[0.1, 0, -0.1]]
# attractor_vects = [RK(r, 'duffing', alpha=0.5, beta=11) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 100, 18000)

# ax.set_xlim((-5, 5))
# ax.set_ylim((-5, 5))
# ax.set_zlim((5, 45))

# * Aizawa
# initial_r_states = [[0.1, 0, 0]]
# attractor_vects = [RK(r, 'aizawa', a=0.95, b=0.7, c=0.6, d=3.5, e=0.25,f=0.1) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 100, 18000)

# ax.set_xlim((-5, 5))
# ax.set_ylim((-5, 5))
# ax.set_zlim((0, 3))

# * Three Cell CNN
# initial_r_states = [[0.1, 0.1, 0.1]]
# attractor_vects = [RK(r, 'three_cell_cnn', p1=1.24, p2=1.1, r=4.4, s=3.21) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 100, 18000)

# ax.set_xlim((-5, 5))
# ax.set_ylim((-5, 5))
# ax.set_zlim((-2, 2))

# * Bouali Type I
# initial_r_states = [[0, -2, -0.25]]
# attractor_vects = [RK(r, 'bouali_type_1', k=0.02, mu=0.4, b=0.2, p=10, q=0.1, s=50) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 100, 5000)

# ax.set_xlim((-0.05, 0.05))
# ax.set_ylim((-5, 5))
# ax.set_zlim((-0.2, 0.2))

# * Bouali Type II
# initial_r_states = [[1, 1, 0]]
# attractor_vects = [RK(r, 'bouali_type_2', a=4, b= 1, c=1.4,s=2.8, alpha=1, beta=1) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 300, 20000)

# ax.set_xlim((-3, 22))
# ax.set_ylim((-3, 22))
# ax.set_zlim((-10, 10))

# initial_r_states = [[1, 1, 0]]
# attractor_vects = [RK(r, 'bouali_type_2', a=4, b= 1, c=1.5,s=1.0, alpha=0.3, beta=0.05) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 300, 20000)

# ax.set_xlim((-3, 22))
# ax.set_ylim((-3, 22))
# ax.set_zlim((-7, 7))

# * Bouali Type III
# initial_r_states = [[1, 1, 0]]
# attractor_vects = [RK(r, 'bouali_type_3', alpha=3, beta=2.2, gamma=1, mu=0.001) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 500, 10000)

# ax.set_xlim((-5, 1))
# ax.set_ylim((0, 3))
# ax.set_zlim((-0.5, 0.5))

# * Finance
# initial_r_states = [[0, -10, 0.1]]
# attractor_vects = [RK(r, 'finance', a=0.00001, b=0.1, c=1) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 300, 20000)

# ax.set_xlim((-2, 2))
# ax.set_ylim((-20, 0))
# ax.set_zlim((-1.5, 1.5))

# * Burke Shaw
# initial_r_states = [[1, 0, 0]]
# attractor_vects = [RK(r, 'burke_shaw', s=10, v=4.272) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 100, 20000)

# ax.set_xlim((-2, 2))
# ax.set_ylim((-2, 2))
# ax.set_zlim((-1.5, 1.5))

# * Ikeda
#! error
# initial_r_states = [[1, 1, 1]]
# attractor_vects = [RK(r, 'ikeda', a=1, b=0.9, c=0.4, d=6) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 1000, 200000)

# ax.set_xlim((-2, 2))
# ax.set_ylim((-5, 45))
# ax.set_zlim((-10, 5))

# * Moore Spiegel (t=26 -> stable)
# initial_r_states = [[0, 0.8, 0]]
# attractor_vects = [RK(r, 'moore_spiegel', t=20, r=100) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 100, 20000)

# ax.set_xlim((-10, 10))
# ax.set_ylim((-20, 20))
# ax.set_zlim((-200, 200))

# * Sakarya
# initial_r_states = [[1, -1, 1]]
# attractor_vects = [RK(r, 'sakarya', a=0.4, b=0.3) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 200, 20000)

# ax.set_xlim((-20, 15))
# ax.set_ylim((-10, 8))
# ax.set_zlim((-8, 10))

# * Dadras
# initial_r_states = [[5, 0, -4]]
# attractor_vects = [RK(r, 'dadras', a=3, b=2.7, c=1.7, d=2, h=9) for r in initial_r_states]
# for vect in attractor_vects:
#     vect.RK4(0, 200, 20000)

# ax.set_xlim((-20, 15))
# ax.set_ylim((-10, 8))
# ax.set_zlim((-8, 10))

# * Halvorsen
initial_r_states = [[-5, 0, 0]]
attractor_vects = [RK(r, 'halvorsen', a=1.89) for r in initial_r_states]
for vect in attractor_vects:
    vect.RK4(0, 200, 20000)

ax.set_xlim((-20, 15))
ax.set_ylim((-12, 8))
ax.set_zlim((-12, 8))

colors = plt.cm.hsv(np.linspace(0.1, 1, len(attractor_vects)))

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
    for line, pt, k in zip(lines, points, attractor_vects):
        if i>15000:
            line.set_data_3d(k.X[i-15000:i], k.Y[i-15000:i], k.Z[i-15000:i])
        else:
            line.set_data_3d(k.X[:i], k.Y[:i], k.Z[:i])
        pt.set_data_3d(k.X[i], k.Y[i], k.Z[i])
    ax.view_init(0.01 * i, 0.1 * i)
    fig.canvas.draw()
    return lines + points

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=18000//4, interval=5, blit=False)

# mywriter = animation.FFMpegWriter(bitrate=5000)
# anim.save('test2.mp4', writer='fclearfmpeg', fps=20, extra_args=['-vcodec', 'libx264'])

plt.show()