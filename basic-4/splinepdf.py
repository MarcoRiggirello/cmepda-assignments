# Copyright (C) 2021 Marco Riggirello & Antoine Venturini
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>

"""
In this module a ProbabilityDensityFunction class is defined.

It permits the user to create a pdf from the sampling of any given function f.

The ProbabilityDensityFunction class allows the following operations:

- It can calculate the probability P(a <= x < b) according to the pdf.

- It can throw a random float according to that pdf.

Many other methods are inherited from the
scipy.interpolate.InterpolatedUnivariateSpline class.
"""

import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline as IUS

class ProbabilityDensityFunction(IUS):

    """
    A probability density function (pdf) class. It uses
    scipy.interpolate.InterpolatedUnivariateSpline class
    to build a continuous function starting from two user defined arrays
    sampling a pdf.

    Attributes
    ----------
    cdf : Cumulative density function of the pdf.
    ppf : Percentile point function of the pdf.

    Methods
    -------
    probability : returns the probability for a value to be find in the
        interval [a, b).
    random : returns a float number distributed according to the pdf.

    Note on the interpolation method to build a pdf:
    ------
    The spline built from x and y arrays has k-1 continuous derivatives, which
    may lead to a pdf with values < 0. This in turn gives rise to a non
    monotonic cdf, hence not invertible. In this case a RuntimeError is issued,
    which can
    be fixed by the user in two ways:
        a) Use a denser sampling to initialize the pdf;
        b) Try lowering the order of the interpolating spline (k=3 for
        default).
           In any case, setting k = 1 (interpolation with a straight line
           between the points) will certainly result in a pdf >= 0.
    """

    def __init__(self, x, y, k=3):

        """
        Parameters
        ----------
        x : (N,) array-like
            Input data-points. Must be streactly increasing.
        y : (N,) array-like
            Input values of the pdf evalueted over x data. Must be greater
            than zero.
        k : int, optional
            Order of the spline that interpolates between x and y. 1 <= k <= 5
            and k < N.
        """

        #Check if y-array has the correct values for a pdf sample.
        if np.any(y<0):
            raise ValueError("Sampled pdf values must not be less than zero.")
        # Check if the cubic spline interpolation produces a pdf with any
        # values lower than 0.
        # Returns a RuntimeError if so, since the cdf is not invertible.
        try:
            raw_spl_int = IUS(x, y, k=k, ext="zeros").antiderivative()
            #Calculate che normalization coefficient
            norm_coeff = raw_spl_int(x[-1])
            #Initialize the pdf as a spline
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

        """
        Returns the probability to find a value between a and b.

        Parameters
        ----------
        a : float
            Lower limit of the interval.
        b : float
            Upper limit of the interval.

        Returns
        -------
        Probability : float
            The probability to find a value between a and b, calculated from
            the integral of the pdf.
        """
        return self.integral(a,b)

    def random(self, **kwargs):

        """
        Returns a random number distributed according to
        ProbabilityDensityFunction.

        The random number is calculated evaluating
        the ppf of the pdf over a uniformly distributed random number obtained
        with the method numpy.random.default_rng().

        Returns
        -------
        random number : float
            A random float distributed according to the pdf.

        For more informations see the API documentation at this link:
        https://numpy.org/doc/stable/reference/random/generator.html
        """

        rng = np.random.default_rng()
        return self.ppf(rng.random(**kwargs))

print(ProbabilityDensityFunction.__doc__)

if __name__ == "__main__":
    print("This is a module.")
