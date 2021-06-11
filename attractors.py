#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

class Attractors(object):
    
    def __init__(self, attractor, **kwargs):
        self.attractor = attractor
        self.params = kwargs

        getattr(Attractors, "_"+ self.attractor + "_params")(self)

    def _lorenz_params(self):
        try:
            self.sigma = self.params["sigma"]
            self.beta = self.params["beta"]
            self.rho = self.params["rho"]
        except:
            raise ValueError("Parameter Argument error")

    def _rabinovich_fabrikant_params(self):
        try:
            self.alpha = self.params["alpha"]
            self.gamma = self.params["gamma"]
        except:
            raise ValueError("Parameter Argument error")

    def _lotka_volterra_params(self):
        try:
            self.a = self.params["a"]
            self.b = self.params["b"]
            self.c = self.params["c"]
        except:
            raise ValueError("Parameter Argument error")
    
    def _rossler_params(self):
        try:
            self.a = self.params["a"]
            self.b = self.params["b"]
            self.c = self.params["c"]

        except:
            raise ValueError("Parameter Argument error")

    def _wang_sun_params(self):
        try:
            self.a = self.params["a"]
            self.b = self.params["b"]
            self.c = self.params["c"]
            self.d = self.params["d"]
            self.e = self.params["e"]
            self.f = self.params["f"]

        except:
            raise ValueError("Parameter Argument error")

    def _rikitake_params(self):
        try:
            self.a = self.params["a"]
            self.mu = self.params["mu"]

        except:
            raise ValueError("Parameter Argument error")
    
    def _nose_hoover_params(self):
        try:
            self.a = self.params["a"]

        except:
            raise ValueError("Parameter Argument error")
    
    def _duffing_params(self):
        try:
            self.alpha = self.params["alpha"]
            self.beta = self.params["beta"]

        except:
            raise ValueError("Parameter Argument error")

    def _aizawa_params(self):
        try:
            self.a = self.params["a"]
            self.b = self.params["b"]
            self.c = self.params["c"]
            self.d = self.params["d"]
            self.e = self.params["e"]
            self.f = self.params["f"]

        except:
            raise ValueError("Parameter Argument error")

    def _three_cell_cnn_params(self):
        try:
            self.p1 = self.params["p1"]
            self.p2 = self.params["p2"]
            self.rr = self.params["rr"]
            self.s = self.params["s"]

        except:
            raise ValueError("Parameter Argument error")

    def lorenz(self, r):
        x, y, z = r
        dx = self.sigma * ( y - x )
        dy = x * ( self.rho - z ) - z
        dz = x * y - ( self.beta * z )
        return np.array([dx , dy , dz], dtype='double')

    def rabinovich_fabrikant(self, r):
        x, y, z = r
        dx = y * ( z - 1 + (x * x)) + (self.gamma * x)
        dy = x * (3*z + 1 - (x * x)) + (self.gamma * y)
        dz = -2*z*( self.alpha + x*y)
        return np.array([dx , dy , dz], dtype='double')

    def lotka_volterra(self, r):
        x, y, z = r
        dx = x - x*y + self.c*x*x - self.a*z*x*x
        dy = -y + x*y
        dz = -self.b*z + self.a*z*x*x
        print([dx , dy , dz])
        return np.array([dx , dy , dz], dtype='double')

    def rossler(self, r):
        x, y, z = r
        dx = - (y + z)
        dy = x + (self.a*y)
        dz = self.b + z * (x-self.c)
        return np.array([dx , dy , dz], dtype='double')

    def wang_sun(self, r):
        x, y, z = r
        dx = self.a*x + self.c*y*z
        dy = self.b*x + self.d*y - x*z
        dz = self.e*z + self.f*x*y
        return np.array([dx , dy , dz], dtype='double')

    def rikitake(self, r):
        x, y, z = r
        dx = - self.mu*x + z*y
        dy = - self.mu*y + x*(z-self.a)
        dz = 1 - x*y
        return np.array([dx , dy , dz], dtype='double')

    def nose_hoover(self, r):
        x, y, z = r
        dx = self.a*y
        dy = - x + y*z
        dz = 1 - y*y
        return np.array([dx , dy , dz], dtype='double')

    def duffing(self, r):
        x, y, z = r
        dx = y
        dy = x - (self.alpha * y) - (x ** 3) + self.beta*np.cos(z)
        dz = 0.5
        return np.array([dx , dy , dz], dtype='double')

    def aizawa(self, r):
        x, y, z = r
        dx = (z - self.b)*x - self.d*y
        dy = self.d*x + (z-self.b)*y
        dz = self.c + self.a*z - (z**3/3) - (x**2 + y**2)*(1+self.e*z) + self.f*z* x**3
        return np.array([dx , dy , dz], dtype='double')

    def three_cell_cnn(self, r):
        x, y, z = r
        fx = 0.5 * (np.abs(x+1) - np.abs(x-1))
        fy = 0.5 * (np.abs(y+1) - np.abs(y-1))
        fz = 0.5 * (np.abs(z+1) - np.abs(z-1))
        dx = -x + self.p1*fx - self.s*fy - self.s*fz
        dy = -y - self.s*fx + self.p2*fy - self.rr*fz
        dz = -z - self.s*fx + self.rr*fy + fz
        return np.array([dx , dy , dz], dtype='double')