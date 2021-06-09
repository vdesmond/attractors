#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation
import matplotlib.pyplot as plt


class Lorenz(object):
    def __init__(self , sigma , beta , rho , Initial_r ):
        self.Sigma = sigma
        self.Beta = beta
        self.Rho = rho
        self.r = Initial_r
        self.X = []
        self.Y = []
        self.Z = []
        
#Vector valued derivative function that updates the position of the particle describing its
#Dynamics using the Lorenz DEs
    def f(self):
        x =self.r[0]
        y = self.r[1]
        z = self.r[2]
        x_prime = self.Sigma * ( y - x )
        y_prime = x * ( self.Rho - z ) - z
        z_prime = x * y - ( self.Beta * z )
        return np.array([x_prime , y_prime , z_prime ],float)

#RK4 integration function with N as time step
    def RK4(self, a, b, N):
        h = (b-a)/N
        time_scale = np.arange(a,b,h)

        for _ in time_scale:
            self.X.append(self.r[0])
            self.Y.append(self.r[1])
            self.Z.append(self.r[2])
            rTemp = self.r
            k1 = h*self.f()
            self.r = self.r+ 0.5*k1
            k2 = h*self.f()
            self.r = rTemp
            self.r = self.r + 0.5*k2
            k3 = h*self.f()
            self.r = rTemp
            self.r = self.r+k3
            k4=h*self.f()
            self.r = rTemp
            self.r += (k1+2*k2+2*k3+k4)/6

#plot statements     


x = Lorenz(5, 8/3, 28, [0.1,0.1,0.1])
y = Lorenz(5, 8/3, 28, [0.11,0.1,0.1])
x.RK4(0, 100, 15000)
y.RK4(0, 100, 15000)


fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1], projection='3d')
ax.axis('off')

ax.set_xlim((-20, 20))
ax.set_ylim((-30, 30))
ax.set_zlim((5, 45))
# ax.plot(x.X,x.Y,x.Z)
# ax.plot(y.X,y.Y,y.Z)

lines = sum([ax.plot([], [], [], '-', c=c)
             for c in ("r", "g")], [])
pts = sum([ax.plot([], [], [], 'o', c=c)
           for c in ("r", "g")], [])                   
def init():
    for line, pt in zip(lines, pts):
        line.set_data_3d([], [], [])

        pt.set_data_3d([], [], [])
    return lines + pts

def animate(i):
    # we'll step two time-steps per frame.  This leads to nice results.
    steps = 4
    i = (steps * i) % len(x.X)
    print(i)
    for line, pt, k in zip(lines, pts, (x,y)):
        if i>5000:
            line.set_data_3d(k.X[i-5000:i], k.Y[i-5000:i], k.Z[i-5000:i])
        else:
            line.set_data_3d(k.X[:i], k.Y[:i], k.Z[:i])
        pt.set_data_3d(k.X[i], k.Y[i], k.Z[i])
    ax.view_init(0.01 * i, 0.05 * i)
    fig.canvas.draw()
    return lines + pts

anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=6000, interval=30, blit=True)

plt.show()