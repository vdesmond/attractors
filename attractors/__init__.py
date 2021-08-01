#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#  Copyright (c) 2021. Vignesh M
#  This file __init__.py, part of the attractors package is licensed under the MIT license.
#  See LICENSE.md in the project root for license information.
# ------------------------------------------------------------------------------

try:
    import importlib.metadata as metadata
except ImportError:
    import importlib_metadata as metadata

from .attractor import *

__version__ = metadata.version("attractors")
