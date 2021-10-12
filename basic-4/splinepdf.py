""" pseudo-random number generator """

import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline

class ProbabilityDensityFunction(InterpolatedUnivariateSpline):
    def __init__(self, x, y):
        if np.any(y<0):
            raise ValueError("Sampled pdf values must not be less than zero.")
        _not_normalized_pdf = InterpolatedUnivariateSpline(x, y, ext="zeros")
        _norm_coeff = _not_normalized_pdf.integral(-np.inf,np.inf)
        InterpolatedUnivariateSpline.__init__(self, x, y/_norm_coeff, ext="zeros")
        self.cdf = self.antiderivative()

    def probability(self, a, b):
        """Tells the probability to find a value between a and b.
        """
        return self.integral(a,b)


