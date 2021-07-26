import random
from collections import Counter

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import pytest

from attractors import __version__
from attractors.attractor import THEMES, Attractor

SIMTIME = 2
SIMPOINTS = 10


def compare(s, t):
    assert Counter(s) == Counter(t)


def random_color():
    return "#" + "%06x" % random.randint(0, 0xFFFFFF)


def random_palette(palette_length):
    palette = [random_color() for _ in range(palette_length)]
    return palette


# Randomly test 20 themes (cant test more due to memory limits)
d = Attractor.list_themes()
keys = random.sample(d.keys(), 20)
sample_d = {k: d[k] for k in keys}


@pytest.mark.parametrize("plottype", ["multipoint", "gradient"])
@pytest.mark.parametrize("theme", sample_d)
def test_themes(plottype, theme):
    obj = Attractor("lorenz").rk4(0, SIMTIME, SIMPOINTS)
    animfunc = getattr(Attractor, f"plot_{plottype}")
    animfunc(SIMPOINTS - 1, obj, theme=theme)
    assert Attractor.bgcolor == THEMES[theme]["background"]
    tmp = list(THEMES[theme].values())
    tmp.remove(THEMES[theme]["background"])
    compare(Attractor.palette, tmp)
    plt.close(Attractor.fig)


@pytest.mark.parametrize("plottype", ["multipoint", "gradient"])
def test_palettes(plottype):
    obj = Attractor("lorenz").rk4(0, SIMTIME, SIMPOINTS)
    animfunc = getattr(Attractor, f"plot_{plottype}")
    bg = random_color()
    palette = random_palette(random.randint(5, 8))
    animfunc(SIMPOINTS - 1, obj, bgcolor=bg, palette=palette)
    assert Attractor.bgcolor == bg
    assert Attractor.palette == palette
    plt.close(Attractor.fig)
