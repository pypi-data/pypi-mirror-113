# pylint:disable=C0103

from collections import OrderedDict
import numpy as np
from tqdm.auto import tqdm  # pylint:disable=F0002
from .. import errors as err
from .. import types as tpe
from ..base_model import BaseModel


class LeakyIntegrateFire(BaseModel):
    """Leaky Integrate and Fire (LIF) Neuron Model"""

    Time_Scale = 1  # s to ms
    """LIF Operates on Second Scale"""
    Default_States = OrderedDict(V=0.0)
    """Default State Variables of the LIF Model"""
    Default_Params = OrderedDict(C=1.0, R=1.0, V_0=0.0, V_T=1.0)
    """Default Parameters of the LIF Model"""

    @staticmethod
    def disabledmethod():
        raise Exception("Function Disabled")

    def ode(self, t: float, states: np.ndarray, I_ext: float = None) -> np.ndarray:
        """Definition of Differential Equation

        .. warning::
            This function is disabled because the LIF neuron model has non-differentiable dynamics at the firing threshold, so we cannot use an ODE solver.
        """
        LeakyIntegrateFire.disabledmethod()

    def _ode_update(self, t: float, y: np.ndarray, *args, **kwargs) -> np.ndarray:
        """The actual update function that is passed to ode solvers

        .. warning::
            This function is disabled because the LIF neuron model has non-differentiable dynamics at the firing threshold, so we cannot use an ODE solver.
        """
        LeakyIntegrateFire.disabledmethod()

    def solve(
        self,
        t: np.ndarray,
        I_ext: np.ndarray = None,
        reset_initial_state: bool = True,
        verbose: bool = True,
    ) -> np.ndarray:
        """Solve model equation for entire input

        .. warning::
            The argument list for this method is a subset of the argument list for the same method defined for the base neuron model.
            This is because the LIF neuron model has non-differentiable dynamics at the firing threshold, so we cannot use an ODE solver,
            and thus the corresponding scipy arguments are absent.

        Arguments:
            t: 1d numpy array of time vector of the simulation
            I_ext: 1d/2d numpy array of external input stimulus of shape

                - 1D: :code:`(len(t),)`, where the same input is shared for all model instances.
                - 2D: :code:`(len(t), num)` where :code:`num` is the number of components to simulate. The value `num` must be equal to the `self.num` value.
            reset_initial_state: whether to reset the initial state value of the
                model to the values in :code:`Default_State`. Default to True.
            verbose: whether to show progress
                    ode solvers.

        Returns:
            A dictionary of simulation results keyed by state variables and each entry is of shape :code:`(num, len(t))`
        """
        if reset_initial_state:
            self.reset()

        t_long = t * self.Time_Scale
        d_t = t_long[1] - t_long[0]

        if verbose:
            pbar = tqdm(total=len(t_long))

        if I_ext is not None:
            if I_ext.ndim == 1:
                I_ext = np.repeat(I_ext[:, None], self.num, axis=-1)
            elif I_ext.ndim != 2:
                raise err.CompNeuroModelError("I_ext must be 1D or 2D")
            if len(I_ext) != len(t):
                raise err.CompNeuroModelError(
                    "I_ext's first dimesion must be the same length as t"
                )
            if I_ext.shape[1] > 1:
                if I_ext.shape != (len(t_long), self.num):
                    raise err.CompNeuroModelError(
                        f"I_ext expecting shape ({len(t_long)},{self.num}), "
                        f"got {I_ext.shape}"
                    )

        res = np.zeros((len(t_long), self.num))
        res[0] = self.states["V"]
        if I_ext is not None:
            for tt, (_I, _t) in enumerate(zip(I_ext[:-1], t_long[:-1])):
                d_V = (_I - self.states["V"] / self.params["R"]) / self.params["C"]
                self.states["V"] += d_t * d_V
                res[tt + 1] = np.clip(self.states["V"], -np.inf, self.params["V_T"])
                self.states["V"][
                    (self.states["V"] >= self.params["V_T"])
                ] = self.params["V_0"]
                if verbose:
                    pbar.update()
        else:
            for tt, _t in enumerate(t_long[:-1]):
                d_V = -self.states["V"] / (self.params["R"] * self.params["C"])
                self.states["V"] += d_t * d_V
                res[tt + 1] = np.clip(self.states["V"], -np.inf, self.params["V_T"])
                self.states["V"][(self.states["V"] > self.params["V_T"])] = self.params[
                    "V_0"
                ]
                if verbose:
                    pbar.update()
        res = res[:, np.newaxis, :]
        res = np.moveaxis(res, 0, 2)

        if verbose:
            pbar.close()

        res = OrderedDict({key: res[n] for n, key in enumerate(self.states.keys())})
        return res
