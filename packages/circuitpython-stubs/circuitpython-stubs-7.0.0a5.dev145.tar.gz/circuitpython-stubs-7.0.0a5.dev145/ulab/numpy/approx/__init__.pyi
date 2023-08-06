"""Numerical approximation methods"""

from __future__ import annotations

from typing import Optional

import ulab

def interp(
    x: ulab.ndarray,
    xp: ulab.ndarray,
    fp: ulab.ndarray,
    *,
    left: Optional[float] = None,
    right: Optional[float] = None
) -> ulab.ndarray:
    """
    :param ulab.ndarray x: The x-coordinates at which to evaluate the interpolated values.
    :param ulab.ndarray xp: The x-coordinates of the data points, must be increasing
    :param ulab.ndarray fp: The y-coordinates of the data points, same length as xp
    :param left: Value to return for ``x < xp[0]``, default is ``fp[0]``.
    :param right: Value to return for ``x > xp[-1]``, default is ``fp[-1]``.

    Returns the one-dimensional piecewise linear interpolant to a function with given discrete data points (xp, fp), evaluated at x."""
    ...

def trapz(y: ulab.ndarray, x: Optional[ulab.ndarray] = None, dx: float = 1.0) -> float:
    """
    :param 1D ulab.ndarray y: the values of the dependent variable
    :param 1D ulab.ndarray x: optional, the coordinates of the independent variable. Defaults to uniformly spaced values.
    :param float dx: the spacing between sample points, if x=None

    Returns the integral of y(x) using the trapezoidal rule.
    """
    ...
