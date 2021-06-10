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
        pass
    
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
        dz = -2*z + ( self.alpha + x*z )
        #! log
        print([dx , dy , dz])
        return np.array([dx , dy , dz], dtype='double')

    def lotka_volterra(self, r):
        x, y, z = r
        dx = x * (1 - x - 9*y)
        dy = -y * (1 - 6*x - y + 9*z)
        dz = z * ( 1 - 3*x - z )
        #! log
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