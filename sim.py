#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

#Implement a Lorentz_Attractor class with 3 system paramaters and a state vector 
class Lorenz_Attractor(object):
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
    def RK4(self):
        a = 0
        b = 100
        N = 15000
        h = (b-a)/N
        time_scale = np.arange(a,b,h)

        for t in time_scale:
            self.X.append(self.r[0])
            self.Y.append(self.r[1])
            self.Z.append(self.r[2])
            rTemp = self.r
 #Work around for OOP , this is done by creating a dummy variable rTemp that we can change throught RK4
#to reflect changes to r that are used to evaluate the K weights without actually changing the Field r until the very end
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


x = Lorenz_Attractor(5, 8/3, 28, [0.1,0.1,0.1])
y = Lorenz_Attractor(5, 8/3, 28, [0.11,0.1,0.1])
x.RK4()
y.RK4()

fig = plt.figure()
fig.add_subplot(111, projection='3d')   # Don't forget to add a 3d axes!
plt.plot(x.X,x.Y,x.Z, 'r')
plt.plot(y.X,y.Y,y.Z, 'g')
plt.tight_layout()
plt.show()