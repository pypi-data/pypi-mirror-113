"""Animate Plotly Figure

Defines helper function that animates plotly scatter plot figures (including
line plots) where a dot will move along the trajectory following time.
"""
from warnings import warn
import numpy as np
import typing as tp
import plotly
import plotly.graph_objects as go
from ... import errors as err

TRACE_TYPE = tp.Union[str, int, go.Scatter3d, go.Scatter]
TRACES_TYPE = tp.Iterable[tp.Union[TRACE_TYPE, tp.Tuple[TRACE_TYPE, int, int]]]


def _find_traces(
    fig: tp.Union[plotly.graph_objects.FigureWidget, plotly.graph_objects.Figure],
    traces: TRACES_TYPE,
    t: np.ndarray = None,
) -> tp.Tuple[
    tp.Union[plotly.graph_objects.Scatter, plotly.graph_objects.Scatter3d], tp.Tuple
]:
    """Find traces in figure

    This function looks for traces that in a given figure and supports a
    variety of ways of specifying traces.

    Arguments:
        fig: plotly Figure instance where the traces should be found
        traces: An iterable of traces to be found in :code:`fig`. Each
            entry of the iterable can either be a single element of the
            type below, or a length-3 iterable of :code:`(element, row, col)`,
            where :code:`row`, :code:`col` correspond to the row and column
            index of the subplot which contains the trace. The element can
            be one of following types:

            - :code:`str`: name of the trace, used to match to `plotly.graph_objects.Scatter3d.name`
              or `plotly.graph_objects.Scatter.name`
            - :code:`int`: index of the trace in `plotly.graph_objects.Figure.data` tuple
            - :py:mod:`plotly.graph_objects.Scatter3d`/:py:mod:`plotly.graph_objects.Scatter`:
              used to match exactly to `plotly.graph_objects.Figure.data`

        t: time vector. If specified, we filter the traces found in figure by so that
            at least one of the array dimension matches the length of time vector `t`.

    Raises:
        compneuro.errors.CompNeuroPlotError: rasied if

            1) the entry in the traces is iterable but not length 3;
            2) the entry in the traces indicates :code:`(row, col)` that is not
              a valid subplot index in the figure;
            3) the trace specified is not of a type that is understood.

    Returns:
        A 2-tuple of format :code:`(trace, (row, col))`
    """
    valid_traces = []
    valid_trace_coords = []
    traces = np.atleast_1d(traces)
    for _tr in traces:
        if isinstance(_tr, (tuple, list, np.ndarray)):
            if not len(_tr) == 3:
                raise err.CompNeuroPlotError(
                    f"Each iterable trace must be length 3, got {len(_tr)}"
                )
            tr, row, col = _tr
            row = int(row)
            col = int(col)
            # TODO: Ideally, the subplot index should be identifiable given
            # the trace and the figure instance. Can't seem to find how to
            # do this though.
        else:
            tr = _tr
            row, col = None, None
        if isinstance(tr, str):
            tr = [d for d in fig.data if hasattr(d, "name") and d.name == tr]
        elif isinstance(tr, int):
            try:
                tr = [fig.data[tr]]
            except:
                tr = []
        elif isinstance(tr, (go.Scatter3d, go.Scatter)):
            if tr in fig.data:
                tr = [tr]
            else:
                tr = []
        else:
            raise err.CompNeuroPlotError(
                f"Trace '{tr}' is not understood. Skipped.",
            )

        if fig._has_subplots() and row is not None and col is not None:
            try:
                fig.get_subplot(row, col)
            except Exception as e:
                raise err.CompNeuroPlotError(
                    f"Subplot at Coordinate (Row, Col) = ({row}, {col}) cannot "
                    "be found in figure"
                ) from e

        valid_traces += list(tr)
        valid_trace_coords.append((row, col))

    # filter by attribute 'x'
    def filter_func(tr):
        if not hasattr(tr, "x"):
            return False

        if t is not None:
            # check to see if at least one of the data
            # fields have some length as t if specified
            Nt = len(t)
            for attr in ["x", "y", "z"]:
                if hasattr(tr, attr):
                    if Nt == len(getattr(tr, attr)):
                        break
            else:
                return False
            return True
        return True

    filtered_traces = list(filter(filter_func, valid_traces))
    return (
        filtered_traces,
        [c for tr, c in zip(valid_traces, valid_trace_coords) if tr in filtered_traces],
    )


def animate_traces(
    fig: "plotly.graph_objects.Figure",
    traces: TRACES_TYPE = None,
    t: np.ndarray = None,
    t_fmt: str = "t={t_:.1f}",
    sample_rate: int = 1,
    max_steps: int = 1000,
    frame_delay: int = 100,
    marker_options: dict = None,
    slider_options: dict = None,
    button_options: dict = None,
) -> "plotly.graph_objects.Figure":
    """Animate traces in a Plotly Figure

    Supports animating lines, scatter and 3d lines and scatter plots. It will
    add animated frames to the current figure where each frame shows moving dots
    following tracjectories of all traces.

    .. warning::

        The animation `appends` frames and slider onto the current
        figure incase existing frames and slider already exist, but adding
        animation to a figure that already has frames is not tested and may
        lead to unintended behaviors. A :py:mod:`compneuro.errors.CompNeuroPlotWarning`
        is fired if existing frames are found.

    Arguments:
        fig: :py:mod:`go.Figure` instance to animate
        traces: traces to animate, see also :py:func:`find_traces`
        t: time vector to animate, see also :py:func:`find_traces`
        t_fmt: formatting time display for the slider bar. the fomatting follows
            :py:func:`str.format` syntax and uses :code:`t_` to indicate the
            current time value. For example :code:`Time={t_:.1f}` will format
            the time value into `Time=0.0`.
        sample_rate: the rate at which the values are being animated. Both time
            vector and the data for each trace will be animated every `sample_rate`
            indices
        max_steps: Maximum number of steps to animate, default to 1000.
        frame_delay: Delay between each animation frame in milisecond, default
            to 100.

            .. note:: The actual frame-rate is data-dependent and may vary from
                this value.

        marker_options: A map for Marker_ options for the scatter dot indicate time.
        slider_options: A map for Slider_ options.
        button_options: A map for play/pause Button_ options.


    Returns:
        The same figure instance in the argument. If a :py:mod:`go.FigureWidget`
        instance is provided as input, it is cast to :py:mod:`go.Figure` instance
        because an error when specifying frames for :py:mod:`go.FigureWidget`.


    Examples:

        Minimal example, will animate all valid traces in a given figure.

        >>> import numpy as np
        >>> from compneuro.utils.plotly import plot_3d, animate_trraces
        >>> X, Y, Z = np.random.rand(3, 100)
        >>> fig = plot_3d(X, Y, Z, style='line')
        >>> fig = animate_traces(fig)

        Animate trace matching name in a given figure.

        >>> import numpy as np
        >>> from compneuro.utils.plotly import plot_3d, animate_trraces
        >>> X, Y, Z = np.random.rand(3, 100)
        >>> fig = plot_3d(X, Y, Z, style='line', name='Animate')
        >>> X2, Y2, Z2 = np.random.rand(3, 100)
        >>> _ = plot_3d(X2, Y2, Z2, fig=fig, style='line', name='Dont Animate')
        >>> fig = animate_traces(fig, ['Animate'])

        Animate a specific trace in subplot.

        >>> import numpy as np
        >>> from compneuro.utils.plotly import plot_3d, animate_trraces
        >>> fig = go.Figure().set_subplots(1,2)
        >>> X, Y, Z = np.random.rand(3, 100)
        >>> _ = plot_3d(X, Y, Z, style='line', name='Dont Animate', fig=fig, row=1, col=1)
        >>> X2, Y2, Z2 = np.random.rand(3, 100)
        >>> _ = plot_3d(X2, Y2, Z2, tyle='line', name='Animate', fig=fig, row=1, col=2)
        >>> fig = animate_traces(fig, ['Animate', 1, 2])
        >>> # This will likely not work, you should always specify (row,col) in subplots
            # fig = animate_traces(fig, ['Animate'])


    .. _Marker: https://plotly.com/python/marker-style/
    .. _Slider: https://plotly.com/python/sliders/
    .. _Button: https://plotly.com/python/custom-buttons/
    """
    # convert FigureWidget to Figure since FigureWidget does not
    # accept frames
    if isinstance(fig, go.FigureWidget):
        fig = go.Figure(fig)
    if traces is None:
        traces = fig.data

    # 1. filter traces to retain only valid ones
    valid_traces, valid_traces_coords = _find_traces(fig, traces, t=t)

    if len(valid_traces) == 0:
        raise err.CompNeuroPlotError("No valid trace has been found to be plotted.")

    # 2. get data
    Xs = [tr.x for tr in valid_traces]
    Ys = [tr.y for tr in valid_traces]
    Zs = [tr.z if hasattr(tr, "z") else None for tr in valid_traces]
    is_3d = [True if hasattr(tr, "z") else False for tr in valid_traces]

    # 3. create initial data points for animation
    animated_trace_indices = []
    N_existing_traces = len(fig.data)
    for tr_idx, (x, y, z, (row, col), _3d) in enumerate(
        zip(Xs, Ys, Zs, valid_traces_coords, is_3d)
    ):
        # add first frame
        if _3d:
            fig.add_scatter3d(
                x=np.atleast_1d(x[0]),
                y=np.atleast_1d(y[0]),
                z=np.atleast_1d(z[0]),
                mode="markers",
                name=f"Time Point - {tr_idx}",
                marker=marker_options,
                row=row,
                col=col,
            )
        else:
            fig.add_scatter(
                x=np.atleast_1d(x[0]),
                y=np.atleast_1d(y[0]),
                mode="markers",
                name=f"Time Point - {tr_idx}",
                marker=marker_options,
                row=row,
                col=col,
            )
        animated_trace_indices.append(N_existing_traces + tr_idx)

    # 4. create frames
    max_length = max([len(x) for x in Xs])
    if t is None:
        t = np.arange(max_length)
    else:
        max_length = min([max_length, len(t)])
        t = t[:max_length]
    plot_idx = np.arange(max_length)[::sample_rate][:max_steps]
    frames = []
    for fr_idx, t_idx in enumerate(plot_idx):
        _data = []
        for tr_idx, (x, y, z, _3d) in enumerate(zip(Xs, Ys, Zs, is_3d)):
            Constructor = go.Scatter3d if _3d else go.Scatter
            if len(x) <= t_idx:
                _data.append(Constructor(visible=True))
                continue

            if _3d:
                _data.append(
                    go.Scatter3d(
                        x=np.atleast_1d(x[t_idx]),
                        y=np.atleast_1d(y[t_idx]),
                        z=np.atleast_1d(z[t_idx]),
                        mode="markers",
                        name=f"Time Point - {tr_idx}",
                        marker=marker_options,
                    )
                )
            else:
                _data.append(
                    go.Scatter(
                        x=np.atleast_1d(x[t_idx]),
                        y=np.atleast_1d(y[t_idx]),
                        mode="markers",
                        name=f"Time Point - {tr_idx}",
                        marker=marker_options,
                    )
                )
        frames.append(
            go.Frame(
                data=_data,
                traces=animated_trace_indices,
                name=f"Animated-frame-{fr_idx}",
            )
        )

    if len(fig.frames) > 0:
        warn(
            (
                "Figure already contains frames, appending new animation frames "
                "may result in unintended animation behaviors."
            ),
            err.CompNeuroPlotWarning,
        )
    fig.update(frames=tuple(list(fig.frames) + frames))

    # 5. set options
    marker_options = marker_options or {}
    button_options = button_options or {}
    button_options = {
        **{
            "direction": "left",
            "pad": {"r": 10, "t": 70},
            "type": "buttons",
            "x": 0.1,
            "y": 0,
        },
        **button_options,
    }
    slider_options = slider_options or {}
    slider_options = {
        **{
            "pad": {"b": 10, "t": 60},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
        },
        **slider_options,
    }

    # 6. Create Controls
    def frame_args(duration):
        return {
            "frame": {"duration": duration, "redraw": any(is_3d)},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration},
        }

    slider = {
        **slider_options,
        "steps": [
            {
                "args": [[f.name], frame_args(0)],
                "label": t_fmt.format(t_=t[plot_idx[k]]),
                "method": "animate",
            }
            for k, f in enumerate(frames)
        ],
    }
    buttons = [
        {
            "args": [None, frame_args(frame_delay)],
            "label": "&#9654;",  # play symbol
            "method": "animate",
        },
        {
            "args": [[None], frame_args(0)],
            "label": "&#9724;",  # pause symbol
            "method": "animate",
        },
    ]
    # 7. Update Figaure with Controls
    fig.update_layout(
        updatemenus=[{"buttons": buttons, **button_options}],
        sliders=list(fig.layout.sliders) + [slider],
    )
    return fig
