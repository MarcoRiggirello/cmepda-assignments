""" pseudo-random number generator """

import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline as IUS

class ProbabilityDensityFunction(IUS):
    def __init__(self, x, y):
        if np.any(y<0):
            raise ValueError("Sampled pdf values must not be less than zero.")
        not_normalized_pdf = IUS(x, y, ext="zeros")
        norm_coeff = not_normalized_pdf.integral(-np.inf,np.inf)
        IUS.__init__(self, x, y/norm_coeff, ext="zeros")
        self.cdf = self.antiderivative()
        ppf_mask = np.concatenate(([True], np.diff(self.cdf(x))>0.0))
        self.ppf = IUS(self.cdf(x[ppf_mask]), x[ppf_mask], ext="zeros")

    def probability(self, a, b):
        """Tells the probability to find a value between a and b.
        """
        return self.integral(a,b)

    def random(self, **kwargs):
        """ Same as numpy.Generator.random() but random numbers
        are distributed according to ProbabilityDensityFunction.
        """
        rng = np.random.default_rng()
        return self.ppf(rng.random(**kwargs))
