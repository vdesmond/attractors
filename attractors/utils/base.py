#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#  Copyright (c) 2021. Vignesh M
#  This file base.py, part of the attractors package is licensed under the MIT license.
#  See LICENSE.md in the project root for license information.
# ------------------------------------------------------------------------------

"""Base module which contains the BaseAttractors class.

Attributes:
    ATTRACTOR_PARAMS (dict): Contains attributes of all attractors. Loaded from data/params.json file.
"""

import importlib.resources as pkg_resources
import json

import numpy as np

from attractors import data

ATTRACTOR_PARAMS = json.load(pkg_resources.open_text(data, "params.json"))


class BaseAttractors(object):
    """Base class where all the attractors are defined with their respective ODE equations.

    Note:
        The attributes for this class which involve the Attractor Parameters are dynamically generated during runtime.

    Attributes:
        attractor (str): attractor name
    """

    def __init__(self, attractor: str, params: dict):
        """Constructor for BaseAttractors class

        Args:
            attractor (str): attractor name
            params (dict): dict of the attractor's parameters
        """

        self.attractor = attractor
        self._func_params(params)

    def _func_params(self, params: dict):
        """
        Dynamic object attribute generator for attractor

        Args:
            params (dict): dict of the attractor's parameters

        Raises:
            Exception: if invalid parameters are provided
        """
        try:
            for prm in ATTRACTOR_PARAMS[self.attractor]["params"]:
                exec("self.{} = {}".format(prm, params[prm]))
        except KeyError as e:
            raise Exception(
                "Parameter argument error. Invalid parameter"
                f" for {self.attractor} attractor."
            ) from e

    def lorenz(self, coord: np.ndarray) -> np.ndarray:
        """
        Lorenz, E. N. (1963). "Deterministic Nonperiodic Flow", Journal of Atmospheric Sciences, 20(2), 130-141.

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            sigma, beta, gamma

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = self.sigma * (y - x)
        dy = x * (self.rho - z) - z
        dz = x * y - (self.beta * z)
        return np.array([dx, dy, dz], dtype="double")

    def rabinovich_fabrikant(self, coord: np.ndarray) -> np.ndarray:
        """
        Rabinovich, M. I. and Fabrikant, A. L., “Stochastic self-modulation of waves in nonequilibrium media”,
        Soviet Journal of Experimental and Theoretical Physics, vol. 50, p. 311, 1979.

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            alpha, gamma

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = y * (z - 1 + (x * x)) + (self.gamma * x)
        dy = x * (3 * z + 1 - (x * x)) + (self.gamma * y)
        dz = -2 * z * (self.alpha + x * y)
        return np.array([dx, dy, dz], dtype="double")

    def lotka_volterra(self, coord: np.ndarray) -> np.ndarray:
        """
        J. S. Costello, “Synchronization of chaos in a generalized Lotka–Volterra attractor,” The Nonlinear Journal,
        vol. 1, pp. 11–17, 1999.

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a, b, c

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = x - x * y + self.c * x * x - self.a * z * x * x
        dy = -y + x * y
        dz = -self.b * z + self.a * z * x * x
        return np.array([dx, dy, dz], dtype="double")

    def rossler(self, coord: np.ndarray) -> np.ndarray:
        """
        O. E. Rossler, “An Equation for Continuous Chaos,” Physics Letters A, Vol. 57, No. 5, 1976, pp. 397-398.

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a, b, c

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = -(y + z)
        dy = x + (self.a * y)
        dz = self.b + z * (x - self.c)
        return np.array([dx, dy, dz], dtype="double")

    def wang_sun(self, coord: np.ndarray) -> np.ndarray:
        """
        Wang, Z., Sun, Y., van Wyk, B. J., Qi, G. & van Wyk, M. A. “A 3-D four-wing attractor and its analysis,
        ” Brazilian J. Phys. 39, (2009) 547–553.

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a, b, c, d, e, f

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = self.a * x + self.c * y * z
        dy = self.b * x + self.d * y - x * z
        dz = self.e * z + self.f * x * y
        return np.array([dx, dy, dz], dtype="double")

    def rikitake(self, coord: np.ndarray) -> np.ndarray:
        """
        Rikitake, Tsuneji. “Oscillations of a System of Disk Dynamos.” Mathematical Proceedings of the Cambridge
        Philosophical Society, vol. 54, no. 1, 1958, pp. 89–105.,

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a, mu

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = -self.mu * x + z * y
        dy = -self.mu * y + x * (z - self.a)
        dz = 1 - x * y
        return np.array([dx, dy, dz], dtype="double")

    def nose_hoover(self, coord: np.ndarray) -> np.ndarray:
        """
        Posch et al. “Canonical dynamics of the Nosé oscillator: Stability, order, and chaos.” Physical review. A,
        General physics 33 6 (1986): 4253-4265.

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = self.a * y
        dy = -x + y * z
        dz = 1 - y * y
        return np.array([dx, dy, dz], dtype="double")

    def langford(self, coord: np.ndarray) -> np.ndarray:
        """
        W. F. Langford, Numerical studies of torus bifurcations, Numerical methods for bifurcation problems (
        Dortmund, 1983), Internat. Schriftenreihe Numer. Math., vol. 70, Birkhäuser, Basel, 1984, pp. 285–295. MR821035

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            alpha, beta, lmbda. omega, rho, epsilon

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = (z - self.beta) * x - self.omega * y
        dy = self.omega * x + (z - self.beta) * y
        dz = (
            self.lmbda
            + self.alpha * z
            - (z ** 3 / 3)
            - (x ** 2 + y ** 2) * (1 + self.rho * z)
            + self.epsilon * z * x ** 3
        )
        return np.array([dx, dy, dz], dtype="double")

    def three_cell_cnn(self, coord: np.ndarray) -> np.ndarray:
        """
        Arena, P., Caponetto, R., Fortuna, L., and Porto, D., “Bifurcation and Chaos in Noninteger Order Cellular
        Neural Networks”, International Journal of Bifurcation and Chaos, vol. 8, no. 7, pp. 1527–1539, 1998

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            p1, p2, r, s

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        fx = 0.5 * (np.abs(x + 1) - np.abs(x - 1))
        fy = 0.5 * (np.abs(y + 1) - np.abs(y - 1))
        fz = 0.5 * (np.abs(z + 1) - np.abs(z - 1))
        dx = -x + self.p1 * fx - self.s * fy - self.s * fz
        dy = -y - self.s * fx + self.p2 * fy - self.r * fz
        dz = -z - self.s * fx + self.r * fy + fz
        return np.array([dx, dy, dz], dtype="double")

    def bouali_type_1(self, coord: np.ndarray) -> np.ndarray:
        """
        S. Bouali, A. Buscarino, L. Fortuna, M. Frasca, and L.V. Gambuzza, "Emulating complex business cycles by
        using an electronic analogue", Nonlinear Analysis: Real World Applications, 13 (2012), pp. 2459–2465.

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            k, b, mu, p, q, s

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = self.k * y + self.mu * x * (self.b - y * y)
        dy = -x + self.s * z
        dz = self.p * x - self.q * y
        return np.array([dx, dy, dz], dtype="double")

    def bouali_type_2(self, coord: np.ndarray) -> np.ndarray:
        """
        Bouali, S. "A novel strange attractor with a stretched loop". Nonlinear Dyn 70, 2375–2381 (2012).

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a, b, c, s, alpha, beta

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = x * (self.a - y) + self.alpha * z
        dy = -y * (self.b - x * x)
        dz = -x * (self.c - self.s * z) - self.beta * z
        return np.array([dx, dy, dz], dtype="double")

    def bouali_type_3(self, coord: np.ndarray) -> np.ndarray:
        """
        Bouali, S. "A 3D Strange Attractor with a Distinctive Silhouette. The Butterfly Effect Revisited". arXiV, (2013).

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            gamma, mu, alpha, beta

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = self.alpha * x * (1 - y) - self.beta * z
        dy = -self.gamma * y * (1 - x * x)
        dz = self.mu * x
        return np.array([dx, dy, dz], dtype="double")

    def finance(self, coord: np.ndarray) -> np.ndarray:
        """
        Cai, Guoliang & Huang, Juanjuan. (2007). A new finance chaotic attractor. International Journal of Nonlinear
        Science. vol 3. pp. 1479-3889.

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a, b, c

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = (1 / self.b - self.a) * x + x * y + z
        dy = -self.b * y - x * x
        dz = -x - self.c * z
        return np.array([dx, dy, dz], dtype="double")

    def burke_shaw(self, coord: np.ndarray) -> np.ndarray:
        """
        Shaw, Robert. "Strange Attractors, Chaotic Behavior, and Information Flow" Zeitschrift für Naturforschung A,
        vol. 36, no. 1, 1981, pp. 80-112.

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            s, v

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = -self.s * (x + y)
        dy = -y - self.s * x * z
        dz = self.s * x * y + self.v
        return np.array([dx, dy, dz], dtype="double")

    def moore_spiegel(self, coord: np.ndarray) -> np.ndarray:
        """
        Moore, D. W. and Spiegel, E. A., “A Thermally Excited Non-Linear Oscillator”, The Astrophysical Journal,
        vol. 143, p. 871, 1966.


        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            t, r

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = y
        dy = z
        dz = -z - (self.t - self.r * (1 - x * x)) * y - self.t * x
        return np.array([dx, dy, dz], dtype="double")

    def sakarya(self, coord: np.ndarray) -> np.ndarray:
        """
        NA

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a, b

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = -x + y + y * z
        dy = -x - y + self.a * x * z
        dz = z - self.b * x * y
        return np.array([dx, dy, dz], dtype="double")

    def dadras(self, coord: np.ndarray) -> np.ndarray:
        """
        Dadras, Sara & Momeni, Hamid. (2009). A novel three-dimensional autonomous chaotic system generating two,
        three and four-scroll attractors. Physics Letters A. 373. 3637-3642.

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a, b, c, d, h

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = y - self.a * x + self.b * y * z
        dy = self.c * y - x * z + z
        dz = self.d * x * y - self.h * z
        return np.array([dx, dy, dz], dtype="double")

    def halvorsen(self, coord: np.ndarray) -> np.ndarray:
        """
        J. C. Sprott and J. C. Sprott, Chaos and time-series analysis, Vol. 69 (Citeseer, 2003)

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = -self.a * x - 4 * y - 4 * z - y * y
        dy = -self.a * y - 4 * z - 4 * x - z * z
        dz = -self.a * z - 4 * x - 4 * y - x * x
        return np.array([dx, dy, dz], dtype="double")

    def hadley(self, coord: np.ndarray) -> np.ndarray:
        """
        J. C. Sprott and J. C. Sprott, Chaos and time-series analysis, Vol. 69 (Citeseer, 2003)

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a, b, f, g

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = -y * y - z * z - self.a * (x - self.f)
        dy = x * y - self.b * x * z - y + self.g
        dz = self.b * x * y + z * (x - 1)
        return np.array([dx, dy, dz], dtype="double")

    def chen(self, coord: np.ndarray) -> np.ndarray:
        """
        Chen, G. & Ueta, T. “Yet another chaotic attractor,” International Journal of Bifurcation and Chaos 9,
        1465–1466. [1999]

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a, b, c

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = self.a * (y - x)
        dy = (self.c - self.a) * x - (x * z) + self.c * y
        dz = x * y - self.b * z
        return np.array([dx, dy, dz], dtype="double")

    def chen_lee(self, coord: np.ndarray) -> np.ndarray:
        """
        Chen HK, Lee CI. "Anti-control of chaos in rigid body motion.", Chaos, Solitons & Fractals (2004), vol. 21,
        pp. 957–65

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a, b, c

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = self.a * x - y * z
        dy = self.b * y + x * z
        dz = self.c * z + x * y / 3
        return np.array([dx, dy, dz], dtype="double")

    def chen_lu(self, coord: np.ndarray) -> np.ndarray:
        """
        Lu, Jinhu & Chen, Guanrong. (2002). "A New Chaotic Attractor Coined.". International Journal of Bifurcation
        and Chaos. vol. 12. pp-659-661.

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a, b, c

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = self.a * (y - x)
        dy = -(x * z) + self.c * y
        dz = x * y - self.b * z
        return np.array([dx, dy, dz], dtype="double")

    def thomas(self, coord: np.ndarray) -> np.ndarray:
        """
        Thomas, René. “DETERMINISTIC CHAOS SEEN IN TERMS OF FEEDBACK CIRCUITS: ANALYSIS, SYNTHESIS, "LABYRINTH
        CHAOS".” International Journal of Bifurcation and Chaos 9 (1999): 1889-1905.

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            b

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = np.sin(y) - self.b * x
        dy = np.sin(z) - self.b * y
        dz = np.sin(x) - self.b * z
        return np.array([dx, dy, dz], dtype="double")

    def dequan_li(self, coord: np.ndarray) -> np.ndarray:
        """
        Li, Dequan., "A three-scroll chaotic attractor." Physics Letters A. 372. 387-393. (2008).

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a, c, d, e, k, f

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = self.a * (y - x) + self.d * x * z
        dy = self.k * x + self.f * y - x * z
        dz = self.c * z + x * y - self.e * x * x
        return np.array([dx, dy, dz], dtype="double")

    def yu_wang(self, coord: np.ndarray) -> np.ndarray:
        """
        F. Yu, C. H. Wang, and J. W. Yin, “A 4-D chaos with fully qualified four-wing type,” Acta Physica Sinica,
        vol. 61, (2012).

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            a, b, c, d

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = self.a * (y - x)
        dy = self.b * x - self.c * x * z
        dz = np.exp(x * y) - self.d * z
        return np.array([dx, dy, dz], dtype="double")

    def newton_leipnik(self, coord: np.ndarray) -> np.ndarray:
        """
        Leipnik, R. B. & Newton, T. A. “Double strange attractors in rigid body motion with linear feedback control,
        ” Phys. Lett. A86, 63–67. (1981)

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor Parameters:
            alpha, beta

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = -self.alpha * x + y + 10 * y * z
        dy = -x - 0.4 * y + 5 * x * z
        dz = self.beta * z - 5 * x * y
        return np.array([dx, dy, dz], dtype="double")

    def rucklidge(self, coord: np.ndarray) -> np.ndarray:
        """Rucklidge, A. Chaos in models of double convection. J. Fluid Mech. 1992, 237, 209–229.

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor parameters:
            k,alpha

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = -self.k * x + (self.alpha * y) - (y * z)
        dy = x
        dz = -z + (y * y)
        return np.array([dx, dy, dz], dtype="double")

    def shimizu_morioka(self, coord: np.ndarray) -> np.ndarray:
        """Shimizu, T.; Morioka, N. On the bifurcation of a symmetric limit cycle to an asymmetric one in a simple model. Phys. Lett. A 1980, 76, 201–204.

        Args:
            coord (np.ndarray): Initial coordinate array [x, y, z]

        Attractor parameters:
            a,B

        Returns:
            np.ndarray: ODE for single step [dx, dy, dz]
        """
        x, y, z = coord
        dx = y
        dy = x - (self.B * y) - (x * z)
        dz = -self.a * z + (x * x)
        return np.array([dx, dy, dz], dtype="double")
