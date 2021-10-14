""" pseudo-random number generator """

import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline as IUS

class ProbabilityDensityFunction(IUS):
    """ Spline-based pdf class.
    """
    def __init__(self, x, y, k=3):
        if np.any(y<0):
            raise ValueError("Sampled pdf values must not be less than zero.")
        # Due to the fact that splines of order k have smoothness C^(k-1)
        # some very sharp distribution may not be well described by a
        # cubic spline. This means that the pdf may have values < 0,
        # hence the cdf is not monotone, hence not invertible.
        try:
            raw_spl_int = IUS(x, y, k=k, ext="zeros").antiderivative()
            norm_coeff = raw_spl_int(x[-1])
            IUS.__init__(self, x, y/norm_coeff, k=k, ext="zeros")
            self.cdf = self.antiderivative()
            ppf_mask = np.concatenate(([True], np.diff(self.cdf(x))>0.0))
            self.ppf = IUS(self.cdf(x[ppf_mask]), x[ppf_mask], ext="zeros")
        except ValueError:
            raise RuntimeError(("Spline interpolation returned non-monotone "
                "cumulative density function. Try to lower the spline order or "
                "to increase the number of sampled point to avoid this problem."
                " See the documentation for more details.")) from ValueError

    def probability(self, a, b): # pylint: disable=invalid-name
        """Tells the probability to find a value between a and b.
        """
        return self.integral(a,b)

    def random(self, **kwargs):
        """ Same as numpy.Generator.random() but random numbers
        are distributed according to ProbabilityDensityFunction.
        """
        rng = np.random.default_rng()
        return self.ppf(rng.random(**kwargs))

if __name__ == "__main__":
    print("This is a module.")
