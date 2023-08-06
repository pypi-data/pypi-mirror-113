import pytest
import numpy as np
from compneuro.memristors.soft_memristor import SoftMemristor
from compneuro.memristors.hard_memristor import HardMemristor
from compneuro.memristors.sodium_channel_memristor import SodiumChannelMemristor
from compneuro.memristors.potassium_channel_memristor import PotassiumChannelMemristor

from compneuro.utils.signal import generate_stimulus
from .test_compneuro import assert_snr
from .reference_memristor_implementations import smm, hmm, namm, kmm


@pytest.fixture
def inputs():
    dt = 1e-3
    t = np.arange(0.0, 0.1, dt)
    I_ext = generate_stimulus("step", dt, 0.1, (0.02, 0.1), 2.0)
    return dt, t, I_ext


def test_smm(inputs):
    dt, t, I_ext = inputs
    smm_ref_x = smm(t, I_ext)
    mem = SoftMemristor(num=1)
    res_euler = mem.solve(t, I_ext, solver="Euler", verbose=False)
    res_odeint = mem.solve(t, I_ext, solver="odeint", rtol=1e-10, verbose=False)
    res_rk45 = mem.solve(t, I_ext, solver="RK45", rtol=1e-10, verbose=False)

    assert_snr(smm_ref_x, res_euler["x"][0], threshold=6.0)
    assert_snr(res_euler["x"], res_odeint["x"], threshold=10.0)
    assert_snr(res_euler["x"], res_rk45["x"], threshold=10.0)


def test_hmm(inputs):
    dt, t, I_ext = inputs
    hmm_ref_x = hmm(t, I_ext)
    mem = HardMemristor(num=1)
    res_euler = mem.solve(t, I_ext, solver="Euler", verbose=False)
    res_odeint = mem.solve(t, I_ext, solver="odeint", rtol=1e-10, verbose=False)
    res_rk45 = mem.solve(t, I_ext, solver="RK45", rtol=1e-10, verbose=False)

    assert_snr(hmm_ref_x, res_euler["x"][0], threshold=6.0)
    assert_snr(res_euler["x"], res_odeint["x"], threshold=10.0)
    assert_snr(res_euler["x"], res_rk45["x"], threshold=10.0)


def test_namm(inputs):
    dt, t, I_ext = inputs
    namm_ref_M, namm_ref_H = namm(t, I_ext)
    mem = SodiumChannelMemristor(num=1)
    res_euler = mem.solve(t, I_ext, solver="Euler", verbose=False)
    res_odeint = mem.solve(t, I_ext, solver="odeint", rtol=1e-10, verbose=False)
    res_rk45 = mem.solve(t, I_ext, solver="RK45", rtol=1e-10, verbose=False)

    assert_snr(namm_ref_M, res_euler["M"][0], threshold=6.0)
    assert_snr(res_euler["M"], res_odeint["M"], threshold=10.0)
    assert_snr(res_euler["M"], res_rk45["M"], threshold=10.0)

    assert_snr(namm_ref_H, res_euler["H"][0], threshold=6.0)
    assert_snr(res_euler["H"], res_odeint["H"], threshold=10.0)
    assert_snr(res_euler["H"], res_rk45["H"], threshold=10.0)


def test_kmm(inputs):
    dt, t, I_ext = inputs
    kmm_ref_N = kmm(t, I_ext)
    mem = PotassiumChannelMemristor(num=1)
    res_euler = mem.solve(t, I_ext, solver="Euler", verbose=False)
    res_odeint = mem.solve(t, I_ext, solver="odeint", rtol=1e-10, verbose=False)
    res_rk45 = mem.solve(t, I_ext, solver="RK45", rtol=1e-10, verbose=False)

    assert_snr(kmm_ref_N, res_euler["N"][0], threshold=6.0)
    assert_snr(res_euler["N"], res_odeint["N"], threshold=10.0)
    assert_snr(res_euler["N"], res_rk45["N"], threshold=10.0)
