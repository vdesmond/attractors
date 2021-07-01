#!/usr/bin/env python
# -*- coding: utf-8 -*-
from attractors.utils.des import DES

class Attractors(DES):
    def __init__(self, x, initial_coord, attractor, params):
        super(Attractors, self).__init__(initial_coord, attractor, params)

    def animate_gradient(self):
        