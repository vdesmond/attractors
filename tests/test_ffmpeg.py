import shlex
import subprocess

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import pytest

from attractors import __version__
from attractors.attractor import ATTRACTOR_PARAMS, Attractor

SIMTIME = 2
SIMPOINTS = 10


def check_err(videopath):
    cmd = shlex.split("ffmpeg -v error -i " + videopath + " -f null -")
    output = subprocess.run(cmd, capture_output=True)
    assert (
        output.stdout == b"" and output.stderr == b""
    ), f"Video possibly corrupted : {output.stderr}"


@pytest.fixture()
def attractor_obj_des(attr, des):
    func = getattr(Attractor(attr), des)
    return func(0, SIMTIME, SIMPOINTS)


@pytest.mark.parametrize("attr", Attractor.list_attractors()[0:2])
@pytest.mark.parametrize("plottype", ["multipoint", "gradient"])
def test_ffmpeg(attr, plottype):
    obj = Attractor(attr).rk4(0, SIMTIME, SIMPOINTS)
    animfunc = getattr(Attractor, f"set_animate_{plottype}")
    animfunc(obj).animate(outf=f"main_{attr}.mp4")
    check_err(f"main_{attr}.mp4")
    plt.close(Attractor.fig)
