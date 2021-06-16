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
            self.r = self.params["rr"]
            self.s = self.params["s"]

        except:
            raise ValueError("Parameter Argument error")

    def _bouali_type_1_params(self):
        try:
            self.k = self.params["k"]
            self.mu = self.params["mu"]
            self.b = self.params["b"]
            self.p = self.params["p"]
            self.q = self.params["q"]
            self.s = self.params["s"]

        except:
            raise ValueError("Parameter Argument error")
    
    def _bouali_type_2_params(self):
        try:
            self.a = self.params["a"]
            self.b = self.params["b"]
            self.c = self.params["c"]
            self.s = self.params["s"]
            self.alpha = self.params["alpha"]
            self.beta = self.params["beta"]

        except:
            raise ValueError("Parameter Argument error")

    def _bouali_type_3_params(self):
        try:
            self.alpha = self.params["alpha"]
            self.beta = self.params["beta"]
            self.gamma = self.params["gamma"]
            self.mu = self.params["mu"]

        except:
            raise ValueError("Parameter Argument error")

    def _finance_params(self):
        try:
            self.a = self.params["a"]
            self.b = self.params["b"]
            self.c = self.params["c"]

        except:
            raise ValueError("Parameter Argument error")
            
    def _burke_shaw_params(self):
        try:
            self.s = self.params["s"]
            self.v = self.params["v"]

        except:
            raise ValueError("Parameter Argument error")

    def _ikeda_params(self):
        try:
            self.a = self.params["a"]
            self.b = self.params["b"]
            self.c = self.params["c"]
            self.d = self.params["d"]
        except:
            raise ValueError("Parameter Argument error")

    def _moore_spiegel_params(self):
        try:
            self.t = self.params["t"]
            self.r = self.params["r"]
        except:
            raise ValueError("Parameter Argument error")

    def _sakarya_params(self):
        try:
            self.a = self.params["a"]
            self.b = self.params["b"]
        except:
            raise ValueError("Parameter Argument error")

    def _dadras_params(self):
        try:
            self.a = self.params["a"]
            self.b = self.params["b"]
            self.c = self.params["c"]
            self.d = self.params["d"]
            self.h = self.params["h"]
        except:
            raise ValueError("Parameter Argument error")

    def lorenz(self, coord):
        x, y, z = coord
        dx = self.sigma * ( y - x )
        dy = x * ( self.rho - z ) - z
        dz = x * y - ( self.beta * z )
        return np.array([dx , dy , dz], dtype='double')

    def rabinovich_fabrikant(self, coord):
        x, y, z = coord
        dx = y * ( z - 1 + (x * x)) + (self.gamma * x)
        dy = x * (3*z + 1 - (x * x)) + (self.gamma * y)
        dz = -2*z*( self.alpha + x*y)
        return np.array([dx , dy , dz], dtype='double')

    def lotka_volterra(self, coord):
        x, y, z = coord
        dx = x - x*y + self.c*x*x - self.a*z*x*x
        dy = -y + x*y
        dz = -self.b*z + self.a*z*x*x
        return np.array([dx , dy , dz], dtype='double')

    def rossler(self, coord):
        x, y, z = coord
        dx = - (y + z)
        dy = x + (self.a*y)
        dz = self.b + z * (x-self.c)
        return np.array([dx , dy , dz], dtype='double')

    def wang_sun(self, coord):
        x, y, z = coord
        dx = self.a*x + self.c*y*z
        dy = self.b*x + self.d*y - x*z
        dz = self.e*z + self.f*x*y
        return np.array([dx , dy , dz], dtype='double')

    def rikitake(self, coord):
        x, y, z = coord
        dx = - self.mu*x + z*y
        dy = - self.mu*y + x*(z-self.a)
        dz = 1 - x*y
        return np.array([dx , dy , dz], dtype='double')

    def nose_hoover(self, coord):
        x, y, z = coord
        dx = self.a*y
        dy = - x + y*z
        dz = 1 - y*y
        return np.array([dx , dy , dz], dtype='double')

    def duffing(self, coord):
        x, y, z = coord
        dx = y
        dy = x - (self.alpha * y) - (x ** 3) + self.beta*np.cos(z)
        dz = 0.5
        return np.array([dx , dy , dz], dtype='double')

    def aizawa(self, coord):
        x, y, z = coord
        dx = (z - self.b)*x - self.d*y
        dy = self.d*x + (z-self.b)*y
        dz = self.c + self.a*z - (z**3/3) - (x**2 + y**2)*(1+self.e*z) + self.f*z* x**3
        return np.array([dx , dy , dz], dtype='double')

    def three_cell_cnn(self, coord):
        x, y, z = coord
        fx = 0.5 * (np.abs(x+1) - np.abs(x-1))
        fy = 0.5 * (np.abs(y+1) - np.abs(y-1))
        fz = 0.5 * (np.abs(z+1) - np.abs(z-1))
        dx = -x + self.p1*fx - self.s*fy - self.s*fz
        dy = -y - self.s*fx + self.p2*fy - self.r*fz
        dz = -z - self.s*fx + self.r*fy + fz
        return np.array([dx , dy , dz], dtype='double')

    def bouali_type_1(self, coord):
        x, y, z = coord
        dx = self.k*y + self.mu*x*(self.b - y*y)
        dy = -x + self.s*z
        dz = self.p*x - self.q*y
        return np.array([dx , dy , dz], dtype='double')
    
    def bouali_type_2(self, coord):
        x, y, z = coord
        dx = x*(self.a-y)+self.alpha*z
        dy = -y*(self.b-x*x)
        dz = -x*(self.c-self.s*z) - self.beta*z
        return np.array([dx , dy , dz], dtype='double')

    def bouali_type_3(self, coord):
        x, y, z = coord
        dx = self.alpha*x*(1-y) - self.beta*z
        dy = -self.gamma*y*(1-x*x)
        dz = self.mu*x
        return np.array([dx , dy , dz], dtype='double')

    def finance(self, coord):
        x, y, z = coord
        dx = (1/self.b - self.a)*x + x*y + z
        dy = -self.b*y - x*x
        dz = -x - self.c*z
        return np.array([dx , dy , dz], dtype='double')

    def burke_shaw(self, coord):
        x, y, z = coord
        dx = -self.s * (x+y)
        dy = -y - self.s*x*z
        dz = self.s*x*y + self.v
        return np.array([dx , dy , dz], dtype='double')

    def ikeda(self, coord):
        x, y, z = coord
        dx = self.a + self.b*(x*np.cos(z) - y*np.sin(z))
        dy = self.b*(x*np.sin(z) + y*np.cos(z))
        dz = self.c - (self.d / (1+ x*x + y*y))
        return np.array([dx , dy , dz], dtype='double')

    def moore_spiegel(self, coord):
        x, y, z = coord
        dx = y
        dy = z
        dz = - z - (self.t - self.r*(1 - x*x))*y - self.t*x
        return np.array([dx , dy , dz], dtype='double')

    def sakarya(self, coord):
        x, y, z = coord
        dx = -x + y + y*z
        dy = - x- y+ self.a*x*z
        dz = z - self.b*x*y
        return np.array([dx , dy , dz], dtype='double')

    def dadras(self, coord):
        x, y, z = coord
        dx = y - self.a*x + self.b*y*z 
        dy = self.c*y - x*z + z
        dz = self.d*x*y - self.h*z
        return np.array([dx , dy , dz], dtype='double')

