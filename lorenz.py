#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

class Lorenz(object):
    
    def __init__(self , sigma , beta , rho , initial_r):
        self.sigma = sigma
        self.beta = beta
        self.rho = rho
        self.r = initial_r
        self.X = []
        self.Y = []
        self.Z = []

    def lorenz_func(self):
        x =self.r[0]
        y = self.r[1]
        z = self.r[2]
        x_prime = self.sigma * ( y - x )
        y_prime = x * ( self.rho - z ) - z
        z_prime = x * y - ( self.beta * z )
        return np.array([x_prime , y_prime , z_prime ],float)

    def RK2(self, a, b, N, method='heun'):
        h = (b-a)/N
        time_scale = np.arange(a,b,h)
    
        for _ in time_scale:
            self.X.append(self.r[0])
            self.Y.append(self.r[1])
            self.Z.append(self.r[2])
            
            rt = self.r
            k1 = h*self.lorenz_func()

            if method == 'heun':
                self.r = self.r+ k1
                k2 = h*self.lorenz_func()
                self.r = rt

                self.r += (k1+k2)/2
            
            elif method == 'heun':
                self.r = self.r+ k1
                k2 = h*self.lorenz_func()
                self.r = rt

                self.r += (k1+k2)/2

    def RK3(self, a, b, N):
        h = (b-a)/N
        time_scale = np.arange(a,b,h)
    
        for _ in time_scale:
            self.X.append(self.r[0])
            self.Y.append(self.r[1])
            self.Z.append(self.r[2])
            
            rt = self.r
            k1 = h*self.lorenz_func()

            self.r = self.r+ k1
            k2 = h*self.lorenz_func()
            self.r = rt

            self.r += (k1+k2)/2
    
    def RK4(self, a, b, N):
        h = (b-a)/N
        time_scale = np.arange(a,b,h)

        for _ in time_scale:
            self.X.append(self.r[0])
            self.Y.append(self.r[1])
            self.Z.append(self.r[2])
            
            rt = self.r
            k1 = h*self.lorenz_func()
            
            self.r = self.r+ 0.5*k1
            k2 = h*self.lorenz_func()
            self.r = rt

            self.r = self.r + 0.5*k2
            k3 = h*self.lorenz_func()
            self.r = rt

            self.r = self.r+k3
            k4=h*self.lorenz_func()
            self.r = rt

            self.r += (k1+2*k2+2*k3+k4)/6
