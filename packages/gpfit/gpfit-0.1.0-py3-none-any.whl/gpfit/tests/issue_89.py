"""Tests issue #89 code"""
import numpy as np
from gpfit.fit import fit

# np.random.seed(314)
x = np.arange(-2, 2, 0.01)
a = -6*x + 6
b = 1/2*x
c = 1/5*x**5 + 1/2*x
y = np.max([a, b, c], axis=0)
K = 3
cstrt, rms = fit(x, y, K, "ISMA")
