import pytest
import numpy as np
from compneuro.utils.bokeh import plot_3d
from compneuro.utils.bokeh.plot3d import Plot3D
from compneuro import errors as err


def test_plot_3d():
    x = np.arange(0, 300, 10)
    y = np.arange(0, 300, 10)
    xx, yy = np.meshgrid(x, y)
    value = np.sin(xx / 50) * np.cos(yy / 50) * 50 + 50
    mesh = plot_3d(
        xx,
        yy,
        value,
        xLabel="x",
        yLabel="y",
        zLabel="z",
        width=100,
        height=100,
        style="surface",
        showLegend=False,
    )
    assert isinstance(mesh, Plot3D)

    mesh.set(width=1000, height=500)
    assert mesh.width == 1000
    assert mesh.height == 500
    assert isinstance(mesh, Plot3D)

    with pytest.raises(
        err.CompNeuroPlotError, match=r".* must be arrays with equal shape.*"
    ):
        mesh = plot_3d(
            xx,
            yy,
            value[0],
            xLabel="x",
            yLabel="y",
            zLabel="z",
            width=100,
            height=100,
            style="surface",
            showLegend=False,
        )

    with pytest.raises(TypeError, match=r"Style .* not supported"):
        mesh = plot_3d(xx, yy, value, style="wrong")

    with pytest.warns(err.CompNeuroPlotWarning, match=r"Invalid options .* ignored"):
        mesh = plot_3d(xx, yy, value, wrong_attr="wrong_val")
