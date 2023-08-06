# pylint:disable=C0103

from collections import OrderedDict
import numpy as np
from ..base_model import BaseModel


class SoftMemristor(BaseModel):
    """Soft Switching Memristor Model"""

    Time_Scale = 1.0
    """Soft Switching Operates on Second Scale"""
    Default_States = OrderedDict(x=0.01)
    """Default State Variables of the Soft Switching Memristor Model"""
    Default_Params = OrderedDict(beta=1e-2, r=160)
    """Default Parameters of the Soft Switching Memristor Model"""

    def ode(self, t, states, I_ext):
        """Memristor gradient function"""
        V = I_ext
        x = states
        M = x + (1 - x) * self.params["r"]
        I = V / M
        d_x = I / self.params["beta"]
        return d_x
