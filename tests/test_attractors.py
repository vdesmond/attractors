import matplotlib
import matplotlib.pyplot as plt
import pytest

from attractors import __version__
from attractors.attractor import ATTRACTOR_PARAMS, Attractor

SIMTIME = 10
SIMPOINTS = 1000


@pytest.fixture()
def attractor_obj_des(attr, des):
    func = getattr(Attractor(attr), des)
    obj = func(0, SIMTIME, SIMPOINTS)
    return obj


@pytest.fixture
def attractor_obj_des_rk2(attr, rk2_method):
    func = getattr(Attractor(attr), "rk2")
    obj = func(0, SIMTIME, SIMPOINTS, rk2_method)
    return obj


des_list = Attractor.list_des()
des_list.remove("rk2")


@pytest.mark.parametrize("attr", Attractor.list_attractors())
@pytest.mark.parametrize("des", des_list)
def test_attractors_des(attr, attractor_obj_des):
    attrparams = ATTRACTOR_PARAMS[attr]
    for aod in attractor_obj_des:   
        assert aod.init_coord == attrparams["init_coord"]
        for i in range(len(attrparams["params"])):
            assert (
                getattr(aod, attrparams["params"][i])
                == attrparams["default_params"][i]
            )


@pytest.mark.parametrize("attr", Attractor.list_attractors())
@pytest.mark.parametrize("rk2_method", ["heun", "imp_poly", "ralston"])
def test_attractors_des_rk2(attr, attractor_obj_des_rk2):
    attrparams = ATTRACTOR_PARAMS[attr]
    for aod in attractor_obj_des_rk2:
        assert aod.init_coord == attrparams["init_coord"]
        for i in range(len(attrparams["params"])):
            assert (
                getattr(aod, attrparams["params"][i])
                == attrparams["default_params"][i]
            )


@pytest.mark.parametrize("attr", Attractor.list_attractors())
@pytest.mark.parametrize("plottype", ["multipoint", "gradient"])
def test_fig_defaults(attr, plottype):
    attrparams = ATTRACTOR_PARAMS[attr]
    obj = Attractor(attr).rk4(0, SIMTIME, SIMPOINTS)
    animfunc = getattr(Attractor, f"set_animate_{plottype}")
    animfunc(obj)
    assert list(Attractor.ax.get_xlim()) == attrparams["xlim"]
    assert list(Attractor.ax.get_ylim()) == attrparams["ylim"]
    assert list(Attractor.ax.get_zlim()) == attrparams["zlim"]
    plt.close(Attractor.fig)


@pytest.mark.parametrize("attr", Attractor.list_attractors())
@pytest.mark.parametrize("plottype", ["multipoint", "gradient"])
def test_live_fig(attr, plottype):
    obj = Attractor(attr).rk4(0, SIMTIME, SIMPOINTS)
    animfunc = getattr(Attractor, f"set_animate_{plottype}")
    anim = animfunc(obj).animate(live=True, show=False)
    assert type(anim) == matplotlib.animation.FuncAnimation
    plt.draw()
    plt.close(Attractor.fig)
