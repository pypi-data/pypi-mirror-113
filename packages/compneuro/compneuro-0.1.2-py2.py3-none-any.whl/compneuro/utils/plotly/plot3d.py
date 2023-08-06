"""Plotly 3D plotting helper function

Defines a :py:func:`plot_3d` function that can be used to visualized 3D
data in a more unified API.
"""
import typing as tp
import plotly
import numpy as np
import plotly.graph_objects as go
from pylatexenc.latex2text import LatexNodes2Text
from ... import errors as err


def _parse_latex(*list_of_strings) -> tp.Iterable[str]:
    parsed_strings = []
    for l in list_of_strings:
        try:
            l = LatexNodes2Text().latex_to_text(l)
        except:
            pass
        parsed_strings.append(l)
    return parsed_strings


def plot_3d(
    X: np.ndarray,
    Y: np.ndarray,
    Z: np.ndarray,
    style: str = "surface",
    name: str = "3D Plot",
    colorbar_title: str = "",
    xlabel: str = "X",
    ylabel: str = "y",
    zlabel: str = "z",
    markersize: float = 4.0,
    linewidth: float = 1.0,
    color: "any" = None,
    cmap: "any" = "Viridis",
    fig: "plotly.graph_objs.Figure" = None,
    row: int = None,
    col: int = None,
    traces_options: dict = None,
    scenes_options: dict = None,
    layout_options: dict = None,
) -> "plotly.graph_objs.Figure":
    """Plot 3D with Plotly API

    Arguments:
        X: X data, 1D or 2D numpy array
        Y: Y data, 1D or 2D numpy array
        Z: Z data, 1D or 2D numpy array
        style: style of figure to be plotted

            - surface: 3D surface plot that ravels the input data
            - scatter: 3D scatter plot which ravels the input data
            - line: 3D line plot which ravels the input data

        name: Name of the trace
        colorbar_title: title of colorbar, only applicable for `surface` style
        xlabel: xaxis label
        ylabel: yaxis label
        zlabel: zaxis label
        markersize: markersize of the scatter plot
        linewidth: linewidth of the line plot
        color: color value for the plot, see Plotly's Color_ options for details.
        cmap: color map, see Plotly's ColorScale_ doc.
        fig: Figure_ instance to add data into. If not provided, a new
            Figure_ instance will be created.
        row: row index of the subplot in `fig` to be added into
        col: col index of the subplot in `fig` to be added into
        traces_options: A map of options for Plotly's `update_traces`_ API call
        scenes_options: A map of options for Plotly's `update_scenes`_ API call
        layout_options: A map of options for Plotly's `update_layout`_ API call

    Returns:
        A Figure_ instance that contains the 3D plot. If :code:`(row, col)` is
        specified, it is added into that subplot.

    Examples:

        Generated 3D line plot from data without specifying figure.

        >>> from compneuro.utils.plotly import plot_3d
        >>> X, Y, Z = np.random.rand(3, 30, 20)
        >>> fig = plot_3d(
                X, Y, Z,
                xlabel='V [mV]', ylabel='n', zlabel='h',
                color=X, style='line', linewidth=4,
                name='My 3D Plot',
                scenes_options=dict(
                    xaxis_range=[-80, 50],
                    yaxis_range=[.4, .85],
                    zaxis_range=[0, .4],
                )
            )

        Generated 3D surface plot from data with given figure.

        >>> import plotly.graph_objects as go
        >>> from compneuro.utils.plotly import plot_3d
        >>> X, Y, Z = np.random.rand(3, 30, 20)
        >>> fig = go.Figure()
        >>> fig = plot_3d(
                X, Y, Z,
                fig=fig,
                xlabel='V [mV]', ylabel='n', zlabel='h',
                color=X, style='line', linewidth=4,
                name='My 3D Plot',
                scenes_options=dict(
                    xaxis_range=[-80, 50],
                    yaxis_range=[.4, .85],
                    zaxis_range=[0, .4],
                )
            )

        Generated 3D scatter plot from data with given figure and in a subplot.

        >>> import plotly.graph_objects as go
        >>> from compneuro.utils.plotly import plot_3d
        >>> X, Y, Z = np.random.rand(3, 30, 20)
        >>> fig = go.Figure().set_subplots(1,2)
        >>> fig = plot_3d(
                X, Y, Z,
                fig=fig, row=1, col=2,
                xlabel='V [mV]', ylabel='n', zlabel='h',
                color=X, style='line', linewidth=4,
                name='My 3D Plot',
                scenes_options=dict(
                    xaxis_range=[-80, 50],
                    yaxis_range=[.4, .85],
                    zaxis_range=[0, .4],
                )
            )

    .. _Figure: https://plotly.com/python/figure-structure/
    .. _ColorScale: https://plotly.com/python/builtin-colorscales/
    .. _Color: https://plotly.com/python/discrete-color/
    .. _`update_traces`: https://plotly.com/python/creating-and-updating-figures/
    .. _`update_layout`: https://plotly.com/python/creating-and-updating-figures/
    .. _`update_scenes`: https://plotly.com/python/reference/layout/scene/

    """
    if fig is None:
        fig = go.Figure()
    layout_options = layout_options or {}
    traces_options = traces_options or {}
    scenes_options = scenes_options or {}

    # We first parse the text to unicode in case LateX syntax is used because
    # MathJax is not supported in 3D plots.
    xlabel, ylabel, zlabel, colorbar_title = _parse_latex(
        xlabel, ylabel, zlabel, colorbar_title
    )

    if style == "surface":
        fig.add_surface(x=X, y=Y, z=Z, row=row, col=col)
        fig.update_traces(
            colorbar=dict(title=colorbar_title),
            contours_z=dict(
                show=True, usecolormap=True, highlightcolor="limegreen", project_z=True
            ),
            name=name,
            row=row,
            col=col,
        )
    elif style == "scatter":
        fig.add_scatter3d(
            x=X.ravel(),
            y=Y.ravel(),
            z=Z.ravel(),
            mode="markers",
            name=name,
            marker=dict(
                size=markersize,
                color=color if color is not None else Z.ravel(),
                colorscale=cmap,
            ),
            row=row,
            col=col,
        )
    elif style == "line":
        fig.add_scatter3d(
            x=X.ravel(),
            y=Y.ravel(),
            z=Z.ravel(),
            mode="lines",
            name=name,
            line=dict(
                color=color if color is not None else Z.ravel(),
                colorscale=cmap,
                width=linewidth,
            ),
            row=row,
            col=col,
        )
    else:
        raise err.CompNeuroPlotError(f"Style '{style}' not understood.")

    # set 3d axes labels
    fig.update_scenes(
        {
            **dict(
                xaxis_title=xlabel,
                yaxis_title=ylabel,
                zaxis_title=zlabel,
            ),
            **scenes_options,
        },
        row=row,
        col=col,
    )
    fig.update_traces(**traces_options, row=row, col=col)
    fig.update_layout(**layout_options)
    return fig
