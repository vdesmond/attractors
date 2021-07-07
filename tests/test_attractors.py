import matplotlib.pyplot as plt

from attractors import __version__
from attractors.attractor import ATTRACTOR_PARAMS, Attractor


def test_version():
    assert __version__ == "1.1.0"


def test_des_methods():
    for des in Attractor.list_des():
        if des == "rk2":
            for rk2_method in ["heun", "imp_poly", "ralston"]:
                obj = Attractor("lorenz")
                func = getattr(obj, des)
                func(0, 10, 1000, rk2_method)
                assert len(obj) == 1000
        else:
            obj = Attractor("lorenz")
            func = getattr(obj, des)
            func(0, 10, 1000)
            assert len(obj) == 1000


def test_attractors():
    for attr in Attractor.list_attractors():
        obj = Attractor(attr)
        obj.rk4(0, 10, 1000)
        assert len(obj) == 1000


def test_attr_defaults():
    for attr in Attractor.list_attractors():
        attrparams = ATTRACTOR_PARAMS[attr]
        obj = Attractor(attr)
        obj.rk4(0, 10, 1000)
        assert obj.init_coord == attrparams["init_coord"]
        for i in range(len(attrparams["params"])):
            assert (
                getattr(obj, attrparams["params"][i]) == attrparams["default_params"][i]
            )


def test_fig_defaults_multipoint():
    for attr in Attractor.list_attractors():
        attrparams = ATTRACTOR_PARAMS[attr]
        obj = Attractor(attr)
        obj.rk4(0, 10, 1000)
        Attractor.set_animate_multipoint(obj)
        assert list(Attractor.ax.get_xlim()) == attrparams["xlim"]
        assert list(Attractor.ax.get_ylim()) == attrparams["ylim"]
        assert list(Attractor.ax.get_zlim()) == attrparams["zlim"]
        plt.close(Attractor.fig)


def test_fig_defaults_gradient():
    for attr in Attractor.list_attractors():
        attrparams = ATTRACTOR_PARAMS[attr]
        obj = Attractor(attr)
        obj.rk4(0, 10, 1000)
        Attractor.set_animate_gradient(obj)
        assert list(Attractor.ax.get_xlim()) == attrparams["xlim"]
        assert list(Attractor.ax.get_ylim()) == attrparams["ylim"]
        assert list(Attractor.ax.get_zlim()) == attrparams["zlim"]
        plt.close(Attractor.fig)
