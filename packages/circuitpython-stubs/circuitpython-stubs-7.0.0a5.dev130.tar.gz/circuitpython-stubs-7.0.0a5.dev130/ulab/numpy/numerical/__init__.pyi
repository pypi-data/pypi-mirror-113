"""Numerical and Statistical functions

Most of these functions take an "axis" argument, which indicates whether to
operate over the flattened array (None), or a particular axis (integer)."""

from __future__ import annotations

from typing import Optional, Union

import ulab
from ulab import _ArrayLike

def argmax(array: _ArrayLike, *, axis: Optional[int] = None) -> int:
    """Return the index of the maximum element of the 1D array"""
    ...

def argmin(array: _ArrayLike, *, axis: Optional[int] = None) -> int:
    """Return the index of the minimum element of the 1D array"""
    ...

def argsort(array: ulab.ndarray, *, axis: int = -1) -> ulab.ndarray:
    """Returns an array which gives indices into the input array from least to greatest."""
    ...

def cross(a: ulab.ndarray, b: ulab.ndarray) -> ulab.ndarray:
    """Return the cross product of two vectors of length 3"""
    ...

def diff(array: ulab.ndarray, *, n: int = 1, axis: int = -1) -> ulab.ndarray:
    """Return the numerical derivative of successive elements of the array, as
    an array.  axis=None is not supported."""
    ...

def flip(array: ulab.ndarray, *, axis: Optional[int] = None) -> ulab.ndarray:
    """Returns a new array that reverses the order of the elements along the
    given axis, or along all axes if axis is None."""
    ...

def max(array: _ArrayLike, *, axis: Optional[int] = None) -> float:
    """Return the maximum element of the 1D array"""
    ...

def mean(array: _ArrayLike, *, axis: Optional[int] = None) -> float:
    """Return the mean element of the 1D array, as a number if axis is None, otherwise as an array."""
    ...

def median(array: ulab.ndarray, *, axis: int = -1) -> ulab.ndarray:
    """Find the median value in an array along the given axis, or along all axes if axis is None."""
    ...

def min(array: _ArrayLike, *, axis: Optional[int] = None) -> float:
    """Return the minimum element of the 1D array"""
    ...

def roll(array: ulab.ndarray, distance: int, *, axis: Optional[int] = None) -> None:
    """Shift the content of a vector by the positions given as the second
    argument. If the ``axis`` keyword is supplied, the shift is applied to
    the given axis.  The array is modified in place."""
    ...

def sort(array: ulab.ndarray, *, axis: int = -1) -> ulab.ndarray:
    """Sort the array along the given axis, or along all axes if axis is None.
    The array is modified in place."""
    ...

def std(array: _ArrayLike, *, axis: Optional[int] = None, ddof: int = 0) -> float:
    """Return the standard deviation of the array, as a number if axis is None, otherwise as an array."""
    ...

def sum(
    array: _ArrayLike, *, axis: Optional[int] = None
) -> Union[float, int, ulab.ndarray]:
    """Return the sum of the array, as a number if axis is None, otherwise as an array."""
    ...
