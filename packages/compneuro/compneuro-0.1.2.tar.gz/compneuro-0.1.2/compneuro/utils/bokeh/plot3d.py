"""Bokeh Custom 3D Plot

Bokeh supports wrapping external JS library for rendering complex data types.
In this case, we're using VisJs to plot 3d surface following the example
from https://github.com/bokeh/bokeh/tree/branch-2.4/examples/app/surface3d.

However, VisJs can support much more than just surface plots. See
https://visjs.github.io/vis-graph3d/docs/graph3d/index.html for more examples.
"""
import os
import typing as tp
import numpy as np
import bokeh as bk
import bokeh.models
import bokeh.util
import bokeh.util.compiler
from warnings import warn
from ... import errors as err
from .plot3d_options import Plot3DOptions

DIR_NAME = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(DIR_NAME, "plot3d.ts"), "r") as f:
    TS = f.read()


def plot_3d(
    X: np.ndarray,
    Y: np.ndarray,
    Z: np.ndarray,
    style: str = "surface",
    force_script_injection: bool = False,
    **options,
) -> "Plot3D":
    """Create 3D Plot in Bokeh

    All given X, Y, Z data are flattend in C-order (:py:func:`np.ravel`) after provided.
    You can choose the style of the plotting to change which type of the plots to use.

    Arguments:
        X: X data
        Y: Y data
        Z: Z data
        style: style of plot, available options are

            - bar: bar plot with color automatically set to reflect z value
            - bar-color: bar plot with color automatically set to reflect z value
            - bar-size: bar plot with bar-width automatically set to reflect z value
            - dot: scatter with color automatically set to reflect z value
            - dot-line: scatter with stem connecting to xy plane, color is set to reflect z value
            - dot-color: scatter with color automatically set to reflect z value
            - dot-size: scatter with size automatically set to reflect z value
            - line: 3d line plot
            - grid: 3d grid plot (mesh plot)
            - surface: 3d surface plot

        force_script_injection: force visjs javascript injection regardless whether
            existing javascript is found. This is useful for when rendering
            3D visualization into HTML for jupyter book as it will ensure that every
            embedded HTML document has visjs available.

    Keyword Arguments:
        **options: additional options for :code:`vis.Graph3d` module. The options
            are processed by :py:mod:`compneuro.utils.bokeh.plot3d_options.Plot3DOptions`
            and then used to configure the VisJs visaulization.

    Returns:
        A :py:mod:`Plot3D` instance if

    .. note::

        :code:`width,height` are options that are required by the Bokeh Layout
        module, which acts as the container for VisJs's Graph3D module which also
        specifies these dimensions. We set the same width and height value for both
        modules.

    .. note::

        By default, we're setting :code:`ctrlToZoom` option to `True`, which means
        that zooming is only possible by pressing the `Ctrl` key.

    Example:

        >>> x = np.arange(0, 300, 10 )
        >>> y = np.arange(0, 300, 10 )
        >>> xx, yy = np.meshgrid(x, y )
        >>> value = np.sin(xx / 50) * np.cos(yy / 50) * 50 + 50
        >>> mesh = plot_3d(X, Y, Z, width=600, height=600, style='surface')
        >>> show(mesh)
    """
    if not X.shape == Y.shape == Z.shape:
        raise err.CompNeuroPlotError("X,Y,Z must be arrays with equal shape")

    source = bk.models.ColumnDataSource(
        data=dict(x=X.ravel(), y=Y.ravel(), z=Z.ravel())
    )

    options.update({"style": style})
    dtypes = Plot3DOptions.dtypes()
    invalid_opts = [key for key in options if key not in dtypes]
    if len(invalid_opts) > 0:
        warn(f"Invalid options '{invalid_opts}' are ignored.", err.CompNeuroPlotWarning)
        for key in invalid_opts:
            options.pop(key)
    valid_opts = Plot3DOptions(**options)

    mesh = Plot3D(
        x="x",
        y="y",
        z="z",
        data_source=source,
        width=valid_opts.width,
        height=valid_opts.height,
        options=valid_opts.to_vis_dict(),
        force_script_injection=force_script_injection,
    )
    return mesh


class Plot3D(bk.models.LayoutDOM):
    """Create 3D Plot Using Bokeh

    Example:

        >>> x = np.arange(0, 300, 10 )
        >>> y = np.arange(0, 300, 10 )
        >>> xx, yy = np.meshgrid(x, y )
        >>> value = np.sin(xx / 50) * np.cos(yy / 50) * 50 + 50
        >>> source = ColumnDataSource(data=dict(x=xx, y=yy, z=value))
        >>> mesh = Plot3D(x="x", y="y", z="z", data_source=source, width=600, height=600 )
        >>> show(mesh)

    """

    # The special class attribute ``__implementation__`` should contain a string
    # of JavaScript code that implements the browser side of the extension model.
    __implementation__ = bk.util.compiler.TypeScript(TS)

    # Below are all the "properties" for this model. Bokeh properties are
    # class attributes that define the fields (and their types) that can be
    # communicated automatically between Python and the browser. Properties
    # also support type validation. More information about properties in
    # can be found here:
    #
    #    https://docs.bokeh.org/en/latest/docs/reference/core/properties.html#bokeh-core-properties

    # This is a Bokeh ColumnDataSource that can be updated in the Bokeh
    # server by Python code
    data_source = bk.core.properties.Instance(bk.models.ColumnDataSource)

    # The vis.js library that we are wrapping expects data for x, y, and z.
    # The data will actually be stored in the ColumnDataSource, but these
    # properties let us specify the *name* of the column that should be
    # used for each field.
    x = bk.core.properties.String
    y = bk.core.properties.String
    z = bk.core.properties.String

    # Any of the available vis.js options for Graph3d can be set by changing
    # the contents of this dictionary.
    options = bk.core.properties.Dict(
        bk.core.properties.String,
        bk.core.properties.Any,
        default=Plot3DOptions().to_vis_dict(),
    )

    force_script_injection = bk.core.properties.Bool

    def set(self, **options):
        """Set Attributes of the Mesh after instantiation

        Keyword Arguments:
            options: Options to be set for Graph3D instance
        """
        valid_opts = Plot3DOptions.validate(**options)
        if "width" in valid_opts:
            self.update(width=valid_opts["width"])
            valid_opts["width"] = f"{int(valid_opts['width'])}px"
        if "height" in valid_opts:
            self.update(height=valid_opts["height"])
            valid_opts["height"] = f"{int(valid_opts['height'])}px"
        self.update(options={**self.options, **valid_opts})
