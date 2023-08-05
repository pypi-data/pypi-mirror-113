# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2021
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Create the Sinus or Harmonic Oscillator dataset.
"""

# Imports
import numbers
import numpy as np
from scipy import integrate
from sklearn.preprocessing import StandardScaler
from torch.utils.data import Dataset


class SinOscillatorDataset(Dataset):
    """ Create a sinus or harmonic oscillator dataset.
    """
    def __init__(self, n_samples=100, duration=60, fs=10, freq=(0.1, 0.5),
                 amp=2, phase=np.pi, target_snr=20, seed=None):
        """ Init class.

        Parameters
        ----------
        n_samples: int
            the number of generated samples
        duration: float
            duration in seconds.
        fs: int
            sampling rate in Hz.
        freq: float
            sine frequency in Hz.
        amp: float
            sine amplitude.
        phase: float
            sine phase in radians.
        target_snr: int
            the signal SNR in db.
        seed: int, default None
            seed to control random number generator.
        """
        super(SinOscillatorDataset).__init__()
        self.freq = interval(freq)
        self.freq_vals = pick_random(n_samples, self.freq, seed)
        self.amp = interval(amp)
        self.amp_vals = pick_random(n_samples, self.amp, seed)
        self.phase = interval(phase)
        self.phase_vals = pick_random(n_samples, self.phase, seed)
        self.time = np.arange(fs * duration) / fs
        self.target_snr = target_snr
        self.data = []
        for freq, amp, phase in zip(self.freq_vals, self.amp_vals,
                                    self.phase_vals):
            self.data.append(self.get_sin_oscillator(freq, amp, phase))
        self.data = np.asarray(self.data).astype(np.float32)
        scaler = StandardScaler()
        self.data = scaler.fit_transform(self.data)
        self.data.shape += (1, )

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    def get_sin_oscillator(self, freq, amp, phase, target_snr_db=20):
        # Compute signal
        sig = amp * np.sin(2 * np.pi * freq * self.time + phase)

        # Noise up the original signal
        noise = self.generate_noise(sig)
        sig += noise

        return sig

    def generate_noise(self, sig):
        # Calculate signal power and convert to dB
        sig_watts = sig ** 2
        sig_avg_watts = np.mean(sig_watts)
        sig_avg_db = 10 * np.log10(sig_avg_watts)

        # Calculate noise then convert to watts
        noise_avg_db = sig_avg_db - self.target_snr
        noise_avg_watts = 10 ** (noise_avg_db / 10)

        # Generate an sample of white noise
        mean_noise = 0
        noise_volts = np.random.normal(mean_noise, np.sqrt(noise_avg_watts),
                                       len(sig))

        return noise_volts

    def ode(self, X, t, zeta, omega0):
        """ Free Harmonic Oscillator ODE.
        """
        x, dotx = X
        ddotx = -2 * zeta * omega0 * dotx - omega0**2 * x
        return [dotx, ddotx]

    def get_harmonic_oscillator(self, zeta=0.05, omega0=(2. * np.pi)):
        """ Damping harmonic oscillator.
        https://scientific-python.readthedocs.io/en/latest/notebooks_rst/
        3_Ordinary_Differential_Equations/02_Examples/Harmonic_Oscillator.html
        """
        X0 = [1., 0.]
        sol = integrate.odeint(self.ode, X0, self.time, args=(zeta, omega0))
        return sol[:, 0]

    def ode_driven(self, X, t, zeta, omega0, omegad_omega0, f_m=1.):
        """ Driven Harmonic Oscillator ODE.
        """
        x, dotx = X
        omegad = omegad_omega0 * omega0
        ddotx = (-2 * zeta * omega0 * dotx - omega0**2 * x +
                 f_m * np.sin(omegad * t))
        return [dotx, ddotx]

    def get_driven_harmonic_oscillator(self, zeta=0.05, omega0=(2. * np.pi),
                                       omegad_omega0=1.):
        """ Damping harmonic oscillator.
        https://scientific-python.readthedocs.io/en/latest/notebooks_rst/
        3_Ordinary_Differential_Equations/02_Examples/Harmonic_Oscillator.html
        """
        X0 = np.zeros(2)
        sol = integrate.odeint(self.ode_driven, X0, self.time,
                               args=(zeta, omega0, omegad_omega0))
        return sol[:, 0]


def interval(obj, lower=None):
    """ Listify an object.

    Parameters
    ----------
    obj: 2-uplet or number
        the object used to build the interval.
    lower: number, default None
        the lower bound of the interval. If not specified, a symetric
        interval is generated.

    Returns
    -------
    interval: 2-uplet
        an interval.
    """
    if isinstance(obj, numbers.Number):
        if obj < 0:
            raise ValueError("Specified interval value must be positive.")
        if lower is None:
            lower = -obj
        return (lower, obj)
    if len(obj) != 2:
        raise ValueError("Interval must be specified with 2 values.")
    min_val, max_val = obj
    if min_val > max_val:
        raise ValueError("Wrong interval boudaries.")
    return tuple(obj)


def pick_random(n_samples, interval, seed=None):
    """ Pick random values in input interval.

    Parameters
    ----------
    n_samples: int
        the number of samples
    interval: 2-uplet
        an interval.
    seed: int, default None
        seed to control random number generator.

    Returns
    -------
    random_values: array
        uniformly sampled random values.
    """
    np.random.seed(seed)
    return np.random.uniform(low=interval[0], high=interval[1], size=n_samples)
