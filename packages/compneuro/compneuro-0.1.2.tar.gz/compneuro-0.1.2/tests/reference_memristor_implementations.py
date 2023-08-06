import numpy as np


def smm(t, I_ext):
    # time-step:
    dt = t[1] - t[0]

    # Model parameters:
    beta = 1e-2
    r = 160

    # Internal state:
    x = 0.01 * np.ones(len(t))

    # Perform numerical integration of the ODEs:
    for i in range(1, len(t)):
        V = I_ext[i]
        M = x[i - 1] + (1 - x[i - 1]) * r
        I = V / M
        x[i] = x[i - 1] + dt * (I / beta)

    return x


def hmm(t, I_ext):
    # time-step:
    dt = t[1] - t[0]

    # Model parameters:
    beta = 1e-2
    r = 160

    # Internal state:
    x = 0.01 * np.ones(len(t))

    # Perform numerical integration of the ODEs:
    for i in range(1, len(t)):
        V = I_ext[i]
        M = x[i - 1] + (1 - x[i - 1]) * r
        I = V / M
        x[i] = x[i - 1] + dt * (I / beta) * x[i - 1] * (1 - x[i - 1])

    return x


def namm(t, I_ext):
    # time-step:
    dt = t[1] - t[0]

    # Model parameters:
    V_0 = 115
    G_0 = 120

    # Internal state:
    M = 1.0 * np.ones(len(t))
    H = 2.3e-4 * np.ones(len(t))

    # Perform numerical integration of the ODEs:
    for i in range(1, len(t)):
        G = G_0 * M[i - 1] ** 3 * H[i - 1]
        V = I_ext[i] / G + V_0

        am = 0.1 * (25 - V) / (np.exp(2.5 - 0.1 * V) - 1)
        bm = 4 * np.exp(-V / 18)
        ah = 0.07 * np.exp(-V / 20)
        bh = 1 / (np.exp(3 - 0.1 * V) + 1)

        d_M = am * (1 - M[i - 1]) - bm * M[i - 1]
        d_H = ah * (1 - H[i - 1]) - bh * H[i - 1]
        M[i] = M[i - 1] + dt * d_M
        H[i] = H[i - 1] + dt * d_H

    return M, H


def kmm(t, I_ext):
    # time-step:
    dt = t[1] - t[0]

    # Model parameters:
    V_0 = -12
    G_0 = 36

    # Internal state:
    N = 0.16 * np.ones(len(t))

    # Perform numerical integration of the ODEs:
    for i in range(1, len(t)):
        G = G_0 * N[i - 1] ** 4
        V = I_ext[i] / G + V_0

        an = 0.01 * (10 - V) / (np.exp(1 - 0.1 * V) - 1)
        bn = 0.125 * np.exp(-V / 80)

        d_N = an * (1 - N[i - 1]) - bn * N[i - 1]
        N[i] = N[i - 1] + dt * d_N

    return N
