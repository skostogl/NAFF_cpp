import numpy as np
import random
import itertools
from numpy.fft import rfft, irfft
import matplotlib.pyplot as plt

def ms(x):
    return (np.abs(x)**2.0).mean()

def normalize(y, x=None):
    if x is not None:
        x = ms(x)
    else:
        x = 1.0
    return y * np.sqrt( x / ms(y) )


def pink(N, data, state=None):
    state = np.random.RandomState() if state is None else state
    uneven = N%2
    X = state.randn(N//2+1+uneven) + 1j * state.randn(N//2+1+uneven)
    S = np.sqrt(np.arange(len(X))+1.) # +1 to avoid divide by zero
    y = (irfft(X/S)).real
    if uneven:
        y = y[:-1]
    return normalize(y, data)

