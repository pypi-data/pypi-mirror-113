# pylint:disable=unsubscriptable-object
# pylint:disable=invalid-name
"""
This class contains all possible options for Plot3D.
It will check if the types are correct, if required if the option is one
of the allowed values.
"""
import sys
import typing as tp
from dataclasses import dataclass, field, asdict, fields
from warnings import warn
from pylatexenc.latex2text import LatexNodes2Text
from ... import errors as err

PY39 = sys.version_info.major == 3 and sys.version_info.minor >= 9

Dict = dict if PY39 else tp.Dict

SUPPORTED_STYLES = [
    "bar",
    "bar-color",
    "bar-size",
    "dot",
    "dot-line",
    "dot-color",
    "dot-size",
    "line",
    "grid",
    "surface",
]


@dataclass
class Plot3DOptions:
    """All supported options to VisJs Graph3D

    This class is not meanted to be used by user. It is a helper class that
    process the configuration setting of. :py:func:`compneuro.utils.bokeh.plot3d.plot_3d`

    For more details on the list of supported settings, see VisJs Graph3d_.

    .. note::

        Some default settings here are different from the ones in Graph3d_.

    .. _`Graph3d`: https://visjs.github.io/vis-graph3d/docs/graph3d/index.html

    """

    width: int = 600
    height: int = 600
    filterLabel: str = "time"
    legendLabel: str = "z-value"
    xLabel: str = "x"
    yLabel: str = "y"
    zLabel: str = "z"
    showXAxis: bool = True
    showYAxis: bool = True
    showZAxis: bool = True
    showGrayBottom: bool = False
    showGrid: bool = True
    showPerspective: bool = True
    showShadow: bool = False
    showSurfaceGrid: bool = True
    keepAspectRatio: bool = False
    rotateAxisLabels: bool = True
    verticalRatio: float = 1.0
    """0.1 to 1.0, where 1.0 results in a 'cube'"""
    dotSizeRatio: float = 0.02
    """size of the dots as a fraction of the graph width"""
    dotSizeMinFraction: float = 0.5
    """size of min-value dot as a fraction of dotSizeRatio"""
    dotSizeMaxFraction: float = 2.5
    """size of max-value dot as a fraction of dotSizeRatio"""
    showAnimationControls: bool = None
    animationInterval: int = 1000
    """Interval in milliseconds"""
    animationPreload: bool = False
    animationAutoStart: bool = None
    axisFontSize: int = 14
    axisFontType: str = "arial"
    axisColor: str = "#4D4D4D"
    gridColor: str = "#D3D3D3"
    xCenter: str = "55%"
    yCenter: str = "50%"
    style: str = "surface"
    tooltip: bool = True
    tooltipDelay: int = 300
    tooltipStyle: Dict[str, Dict[str, str]] = field(
        default_factory=lambda: {
            "content": {
                "padding": "10px",
                "border": "1px solid #4d4d4d",
                "color": "#1a1a1a",
                "background": "rgba(255,255,255,0.7)",
                "borderRadius": "2px",
                "boxShadow": "5px 5px 10px rgba(128,128,128,0.5)",
            },
            "line": {
                "height": "40px",
                "width": "0",
                "borderLeft": "1px solid #4d4d4d",
                "pointerEvents": "none",
            },
            "dot": {
                "height": "0",
                "width": "0",
                "border": "5px solid #4d4d4d",
                "borderRadius": "5px",
                "pointerEvents": "none",
            },
        }
    )
    dataColor: Dict[str, tp.Union[str, float]] = field(
        default_factory=lambda: {
            "fill": "#7DC1FF",
            "stroke": "#3267D2",
            "strokeWidth": 1,
        }
    )
    surfaceColors: str = None
    colormap: tp.Any = None
    cameraPosition: Dict[str, float] = field(
        default_factory=lambda: {"horizontal": 1.0, "vertical": 0.5, "distance": 1.7}
    )
    zoomable: bool = True
    ctrlToZoom: bool = True
    showLegend: bool = False
    backgroundColor: str = None
    xBarWidth: float = None
    yBarWidth: float = None
    valueMin: float = None
    valueMax: float = None
    xMin: float = None
    xMax: float = None
    xStep: float = None
    yMin: float = None
    yMax: float = None
    yStep: float = None
    zMin: float = None
    zMax: float = None
    zStep: float = None

    def __post_init__(self):
        if self.style not in SUPPORTED_STYLES:
            raise TypeError(
                f"Style '{self.style}' not supported, must be one of {SUPPORTED_STYLES}"
            )

    def to_vis_dict(self) -> dict:
        """Convert Plot3D option instance to VisJs compatible dict"""
        cfg = asdict(self)
        keys = list(cfg.keys())
        for k in keys:
            if cfg[k] is None:
                cfg.pop(k)
        cfg = self.validate(**cfg)
        width = cfg["width"]
        height = cfg["height"]
        cfg["width"] = f"{int(width)}px"
        cfg["height"] = f"{int(height)}px"
        return cfg

    @classmethod
    def dtypes(cls) -> dict:
        """Return a dictionary that indicates the dtype for each field"""
        return {
            f.name: f.type.__origin__ if hasattr(f.type, "__origin__") else f.type
            for f in fields(Plot3DOptions)
        }

    @classmethod
    def validate(cls, **kwargs) -> dict:
        """Validate a dictionary of options and return the cleaned up version"""
        all_fields = {
            f.name: f.type.__origin__ if hasattr(f.type, "__origin__") else f.type
            for f in fields(Plot3DOptions)
        }
        valid_dict = {}
        not_found_fields = []
        not_castable_fields = []
        for key, val in kwargs.items():

            # find field
            if key not in all_fields:
                not_found_fields.append(key)
                continue

            # style is special
            if key == "style":
                if val not in SUPPORTED_STYLES:
                    not_castable_fields.append(key)
                else:
                    valid_dict[key] = val
                continue

            # convert textual label to unicode
            if key in ["xLabel", "yLabel", "zLabel", "legendLabel"]:
                try:
                    valid_dict[key] = LatexNodes2Text().latex_to_text(val)
                except:
                    valid_dict[key] = val
                continue

            # cast by dtype
            dtype = all_fields[key]
            try:
                if dtype == tp.Any:
                    valid_dict[key] = val
                else:
                    valid_dict[key] = dtype(val)
            except TypeError:
                not_castable_fields.append(key)
            except Exception as e:
                raise err.CompNeuroPlotError(
                    f"Unknown error occured when validating variable '{key}' of value {val}"
                ) from e

        msg = ""
        if len(not_found_fields) > 0:
            msg += f"fields '{not_found_fields}' are not valid options. "
        if len(not_castable_fields) > 0:
            msg += (
                f"fields '{not_castable_fields}' are not castable "
                "to the corresponding types"
            )
        if msg:
            warn(msg, err.CompNeuroPlotWarning)
        return valid_dict
