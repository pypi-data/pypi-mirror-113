from __future__ import annotations

import ulab

def spectrogram(r: ulab.ndarray) -> ulab.ndarray:
    """
    :param ulab.ndarray r: A 1-dimension array of values whose size is a power of 2

    Computes the spectrum of the input signal.  This is the absolute value of the (complex-valued) fft of the signal.
    This function is similar to scipy's ``scipy.signal.spectrogram``."""
    ...
