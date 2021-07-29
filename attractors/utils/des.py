#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#  Copyright (c) 2021. Vignesh M
#  This file des.py, part of the attractors package is licensed under the MIT license.
#  See LICENSE.md in the project root for license information.
# ------------------------------------------------------------------------------
"""Module which contains iterative methods for solving Ordinary Differential Equations (ODE)"""

from __future__ import annotations

from typing import Iterator

import numpy as np

from attractors.utils.base import BaseAttractors


class DES(BaseAttractors):
    """Differential Equations Solver (DES) class contains iterative methods for solving Ordinary Differential
    Equations (ODE). Currently includes the following methods: Euler, RK2, RK3, RK4, RK5.
    For more info: see https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods

    Attributes:
        coord (np.ndarray): current coordinate of the attractor as (3,) ndarray
        X (float): current X coordinate of the attractor
        Y (float): current Y coordinate of the attractor
        Z (float): current Z coordinate of the attractor
        ts (int): current time step
        N (int): number of points set for simulating the attractor
    """

    def __init__(self, attractor: str, init_coord: np.ndarray, params: dict):
        """Constructor for DES class

        Args:
            attractor (str): attractor name
            init_coord (np.ndarray): initial coordinate array
            params (dict): dict of the attractor's parameters
        """
        super(DES, self).__init__(attractor, params)
        self.coord = init_coord
        self.X = 0
        self.Y = 0
        self.Z = 0
        self.ts = None
        self.N = None

    def __len__(self):
        return self.N

    def _unwrap(self, a: int, b: int, n: int):
        """Private method for getting the attractor function"""
        self.N = n
        h = (b - a) / n
        attractor_func = getattr(DES, self.attractor)
        return h, attractor_func

    def euler(self, a: int, b: int, n: int) -> Iterator[DES]:
        """First order Euler method

        Args:
            a (int): simulation initial time step
            b (int): simulation final time step
            n (int): simulation points

        Yields:
            object: instance of DES
        """
        h, afunc = self._unwrap(a, b, n)

        for ts in range(n):
            self.X = self.coord[0]
            self.Y = self.coord[1]
            self.Z = self.coord[2]

            k1 = h * afunc(self, self.coord)
            self.coord += k1
            self.ts = ts
            yield self

    def rk2(self, a: int, b: int, n: int, method: str) -> Iterator[DES]:
        """Second order Runge-Kutta method

        Euler's method is a simple one-step method used for solving ODEs. In Euler’s method, the slope is estimated
        in the most basic manner by using the first derivative.

        Args:
            a (int): simulation initial time step
            b (int): simulation final time step
            n (int): simulation points
            method (str): RK2 method to be used

        Yields:
            object: instance of DES
        """
        h, afunc = self._unwrap(a, b, n)

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

        for ts in range(n):
            self.X = self.coord[0]
            self.Y = self.coord[1]
            self.Z = self.coord[2]

            locals()[method]()

            self.ts = ts
            yield self

    def rk3(self, a: int, b: int, n: int) -> Iterator[DES]:
        """Third order Runge-Kutta method

        Args:
            a (int): simulation initial time step
            b (int): simulation final time step
            n (int): simulation points

        Yields:
            object: instance of DES
        """
        h, afunc = self._unwrap(a, b, n)

        for ts in range(n):
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

    def rk4(self, a: int, b: int, n: int) -> Iterator[DES]:
        """Fourth order Runge-Kutta method

        Args:
            a (int): simulation initial time step
            b (int): simulation final time step
            n (int): simulation points

        Yields:
            object: instance of DES
        """
        h, afunc = self._unwrap(a, b, n)

        for ts in range(n):
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

    def rk5(self, a: int, b: int, n: int) -> Iterator[DES]:
        """Fifth order Runge-Kutta method

        Args:
            a (int): simulation initial time step
            b (int): simulation final time step
            n (int): simulation points

        Yields:
            object: instance of DES
        """
        h, afunc = self._unwrap(a, b, n)

        for ts in range(n):
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
