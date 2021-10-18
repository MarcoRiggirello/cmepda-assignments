#Assignment basic 3 for cmepda - by Antoine Venturini 

"""La classe LabData gestisce un file di dati tensioni-tempo"""

import unittest as utest

import numpy as np
import matplotlib.pyplot as plt

class VoltageData:

    """
    The VoltageData class manipulates two sets of data: time and voltage.
    """

    def __init__(self, tension, time):

        """
        Parameters
        ----------
        tension : (N,) iterable item containing floats
            Tension measurements.
        time : (N,) iterable item containing floats
            Time mesurements.
        
        Notes
        -----
        tension and time must be of the same size.
        """

        if len(tension)=len(time):
            try:
                self._v = np.array(tension, dtype=float)
                self._t = np.array(time, dtype=float)            
            except ValueError as e:
                print(e)
        else:
            raise ValueError("incorrect shape: data must have the same length")

    @classmethod
    def load_data(cls, fname):

        """The data initializing the class can be loaded from a file."""

        tension, time = np.loadtxt(fname, unpack=True)
        return cls(tension, time)

    def __getitem__(self, index1, index2):

        """
        Return
        ------
        tension[index2] if index1 = 0
        time[index2] if index1 = 1
        """

        self._measure = np.array([self._v, self._t])
        return self._measure[index1, index2]

