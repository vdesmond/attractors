#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#  Copyright (c) 2021. Vignesh M
#  This file des.py, part of the attractors package is licensed under the MIT license.
#  See LICENSE.md in the project root for license information.
# ------------------------------------------------------------------------------

import numpy as np

from attractors.utils.base import BaseAttractors


class DES(BaseAttractors):
    def __init__(self, attractor, init_coord, params):
        super(DES, self).__init__(attractor, params)
        self.coord = init_coord
        self.X = 0
        self.Y = 0
        self.Z = 0
        self.ts = None
        self.N = None

    def __len__(self):
        return self.N

    def _unwrap(self, a, b, N):
        self.N = N
        h = (b - a) / N
        attractor_func = getattr(DES, self.attractor)
        return h, attractor_func

    def euler(self, a, b, N):
        h, afunc = self._unwrap(a, b, N)

        for ts in range(N):

            self.X = self.coord[0]
            self.Y = self.coord[1]
            self.Z = self.coord[2]

            k1 = h * afunc(self, self.coord)
            self.coord += k1
            self.ts = ts
            yield self

    def rk2(self, a, b, N, method):
        h, afunc = self._unwrap(a, b, N)

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

        for ts in range(N):

            self.X = self.coord[0]
            self.Y = self.coord[1]
            self.Z = self.coord[2]

            eval(method)()

            self.ts = ts
            yield self

    def rk3(self, a, b, N):
        h, afunc = self._unwrap(a, b, N)

        for ts in range(N):

            self.X = self.coord[0]
            self.Y = self.coord[1]
            self.Z = self.coord[2]

            rt = self.coord
            k1 = h * afunc(self, self.coord)

            self.coord = self.coord + k1 / 2
            k2 = h * afunc(self, self.coord)
            self.coord = rt

            self.coord = self.coord - k1 + 2 * k2
            k3 = h * afunc(self, self.coord)
            self.coord = rt

            self.coord += (k1 + 4 * k2 + k3) / 6

            self.ts = ts
            yield self

    def rk4(self, a, b, N):
        h, afunc = self._unwrap(a, b, N)

        for ts in range(N):

            self.X = self.coord[0]
            self.Y = self.coord[1]
            self.Z = self.coord[2]

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

            self.ts = ts
            yield self

    def rk5(self, a, b, N):
        h, afunc = self._unwrap(a, b, N)

        for ts in range(N):
            self.X = self.coord[0]
            self.Y = self.coord[1]
            self.Z = self.coord[2]

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

            self.ts = ts
            yield self
