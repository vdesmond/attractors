#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from attractors.utils.attr import Attractors


class RK(Attractors):
    def __init__(self, initial_coord, attractor, params):
        super(RK, self).__init__(attractor, params)
        self.coord = initial_coord
        self.X = []
        self.Y = []
        self.Z = []

    def _unwrap(self, a, b, N):
        h = (b - a) / N
        timescale = np.arange(a, b, h)
        attractor_func = getattr(RK, self.attractor)
        return h, timescale, attractor_func

    def euler(self, a, b, N):
        h ,ts, afunc = self._unwrap(a, b, N)

        
        for _ in ts:
            self.X.append(self.coord[0])
            self.Y.append(self.coord[1])
            self.Z.append(self.coord[2])

            k1 = h * afunc(self, self.coord)
            self.coord += k1

    def rk2(self, a, b, N, method):
        h ,ts, afunc = self._unwrap(a, b, N)


        def heun():
            rt = self.coord
            k1 = h * afunc(self, self.coord)

            self.coord = self.coord + k1
            k2 = h * afunc(self, self.coord)
            self.coord = rt

            self.coord += (k1 + k2) / 2

        def imp_poly():
            rt = self.coord
            k1 = h * afunc(self, self.coord)

            self.coord = self.coord + k1 / 2
            k2 = h * afunc(self, self.coord)
            self.coord = rt

            self.coord += k2

        def ralston():
            rt = self.coord
            k1 = h * afunc(self, self.coord)

            self.coord = self.coord + 3 * k1 / 4
            k2 = h * afunc(self, self.coord)
            self.coord = rt

            self.coord += (k1 + 2 * k2) / 3

        for _ in ts:
            self.X.append(self.coord[0])
            self.Y.append(self.coord[1])
            self.Z.append(self.coord[2])
            eval(method)()

    def rk3(self, a, b, N):
        h ,ts, afunc = self._unwrap(a, b, N)


        for _ in ts:
            self.X.append(self.coord[0])
            self.Y.append(self.coord[1])
            self.Z.append(self.coord[2])

            rt = self.coord
            k1 = h * afunc(self, self.coord)

            self.coord = self.coord + k1 / 2
            k2 = h * afunc(self, self.coord)
            self.coord = rt

            self.coord = self.coord - k1 + 2 * k2
            k3 = h * afunc(self, self.coord)
            self.coord = rt

            self.coord += (k1 + 4 * k2 + k3) / 6

    def rk4(self, a, b, N):
        h ,ts, afunc = self._unwrap(a, b, N)

        for _ in ts:
            self.X.append(self.coord[0])
            self.Y.append(self.coord[1])
            self.Z.append(self.coord[2])

            rt = self.coord
            k1 = h * afunc(self, self.coord)

            self.coord = self.coord + k1 / 2
            k2 = h * afunc(self, self.coord)
            self.coord = rt

            self.coord = self.coord + k2 / 2
            k3 = h * afunc(self, self.coord)
            self.coord = rt

            self.coord = self.coord + k3
            k4 = h * afunc(self, self.coord)
            self.coord = rt

            self.coord += (k1 + 2 * k2 + 2 * k3 + k4) / 6

    def rk5(self, a, b, N):
        h ,ts, afunc = self._unwrap(a, b, N)

        for _ in ts:
            self.X.append(self.coord[0])
            self.Y.append(self.coord[1])
            self.Z.append(self.coord[2])

            rt = self.coord
            k1 = h * afunc(self, self.coord)

            self.coord = self.coord + k1 / 4
            k2 = h * afunc(self, self.coord)
            self.coord = rt

            self.coord = self.coord + k2 / 8 + k1 / 8
            k3 = h * afunc(self, self.coord)
            self.coord = rt

            self.coord = self.coord + k3 - k2 / 2 + k3
            k4 = h * afunc(self, self.coord)
            self.coord = rt

            self.coord = self.coord - 3 * k1 / 16 + 9 * k4 / 16
            k5 = h * afunc(self, self.coord)
            self.coord = rt

            self.coord = (
                self.coord
                - 3 * k1 / 7
                + 2 * k2 / 7
                + 12 * k3 / 7
                - 12 * k4 / 7
                + 8 * k5 / 7
            )
            k6 = h * afunc(self, self.coord)
            self.coord = rt

            self.coord += (7 * k1 + 32 * k3 + 12 * k4 + 32 * k5 + 7 * k6) / 90
