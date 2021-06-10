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

    def lorenz(self, r):
        x = r[0]
        y = r[1]
        z = r[2]
        dx = self.sigma * ( y - x )
        dy = x * ( self.rho - z ) - z
        dz = x * y - ( self.beta * z )
        return np.array([dx , dy , dz], dtype='double')

    def rabinovich_fabrikant(self, r):
        x = r[0]
        y = r[1]
        z = r[2]
        dx = y * ( z - 1 + (x * x)) + (self.gamma * x)
        print(dx)
        dy = x * (3*z + 1 - (x * x)) + (self.gamma * y)
        dz = -2*z + ( self.alpha + x*z )
        return np.array([dx , dy , dz], dtype='double')