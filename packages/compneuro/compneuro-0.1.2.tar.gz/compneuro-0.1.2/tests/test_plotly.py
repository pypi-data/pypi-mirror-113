import pytest
import numpy as np
import plotly.graph_objects as go
from compneuro.utils.plotly import plot_3d, animate_traces
from compneuro import errors as err


def test_plot_3d():
    # Generated 3D line plot from data without specifying figure.
    X, Y, Z = np.random.rand(3, 30, 20)
    fig = plot_3d(
        X,
        Y,
        Z,
        xlabel="V [mV]",
        ylabel="n",
        zlabel="h",
        color=X,
        style="line",
        linewidth=4,
        name="My 3D Plot",
        scenes_options=dict(
            xaxis_range=[-80, 50],
            yaxis_range=[0.4, 0.85],
            zaxis_range=[0, 0.4],
        ),
    )

    assert len(fig.data) == 1
    assert fig.data[0].name == "My 3D Plot"

    # Generated 3D surface plot from data with given figure.
    X, Y, Z = np.random.rand(3, 30, 20)
    fig = go.Figure()
    fig = plot_3d(
        X,
        Y,
        Z,
        fig=fig,
        xlabel="V [mV]",
        ylabel="n",
        zlabel="h",
        color=X,
        style="line",
        linewidth=4,
        name="My 3D Plot",
        scenes_options=dict(
            xaxis_range=[-80, 50],
            yaxis_range=[0.4, 0.85],
            zaxis_range=[0, 0.4],
        ),
    )

    # Generated 3D scatter plot from data with given figure and in a subplot.
    X, Y, Z = np.random.rand(3, 30, 20)
    fig = go.Figure().set_subplots(1, 2, specs=[[{"type": "scene"}, {"type": "scene"}]])
    fig = plot_3d(
        X,
        Y,
        Z,
        fig=fig,
        row=1,
        col=2,
        xlabel="V [mV]",
        ylabel="n",
        zlabel="h",
        color=X,
        style="line",
        linewidth=4,
        name="My 3D Plot",
        scenes_options=dict(
            xaxis_range=[-80, 50],
            yaxis_range=[0.4, 0.85],
            zaxis_range=[0, 0.4],
        ),
    )


def test_animate():
    X, Y, Z = np.random.rand(3, 100)
    X2, Y2, Z2 = np.random.rand(3, 100)
    fig = plot_3d(X, Y, Z, style="line")
    _ = plot_3d(X2, Y2, Z2, fig=fig, style="scatter")
    fig = animate_traces(fig)
    assert len(fig.frames) == len(X)
    assert len(fig.frames[0].data) == 2

    # Animate trace matching name in a given figure.
    X, Y, Z = np.random.rand(3, 100)
    fig = plot_3d(X, Y, Z, style="line", name="Animate")
    X2, Y2, Z2 = np.random.rand(3, 100)
    _ = plot_3d(X2, Y2, Z2, fig=fig, style="line", name="Dont Animate")
    fig = animate_traces(fig, ["Animate"])

    # Animate a specific trace in subplot.

    fig = go.Figure().set_subplots(1, 2, specs=[[{"type": "scene"}, {"type": "scene"}]])
    X, Y, Z = np.random.rand(3, 100)
    _ = plot_3d(X, Y, Z, style="line", name="Dont Animate", fig=fig, row=1, col=1)
    X2, Y2, Z2 = np.random.rand(3, 100)
    _ = plot_3d(X2, Y2, Z2, style="line", name="Animate", fig=fig, row=1, col=2)
    fig = animate_traces(fig, [("Animate", 1, 2)])
