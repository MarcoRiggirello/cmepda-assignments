#Assignment basic 3 for cmepda - by Antoine Venturini

"""La classe LabData gestisce un file di dati tensioni-tempo"""

import numpy as np

class VoltageData:
    #pylint: disable=invalid-name
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
        self._data = np.array([tension, time], dtype=float).transpose()

    @classmethod
    def load_data(cls, fname):

        """The data initializing the class can be loaded from a file."""

        tension, time = np.loadtxt(fname, unpack=True)
        return cls(tension, time)

    @property
    def voltage(self):

        """Allows to read the private variable self._v."""

        return self._data[:,0]

    @property
    def time(self):

        """Allows to read the private variable self._t."""

        return self._data[:,1]

    def __iter__(self):

        """La classe è iterabile e restituisce la coppia (v[i], t[i])."""

        return iter(list(zip(self._v, self._t)))


    def __getitem__(self, indexx):

        """
        Return
        ------
        tension[index2] if index1 = 0
        time[index2] if index1 = 1
        """

        return self._data[indexx[0], indexx[1]]

    def __len__(self):

        """Returns the length of the data samples."""

        return len(self._data)

    def __repr__(self):

        """
        Prints class instances in a pretty way.

        The data are printed with this organization:
        line number - tension entry    time entry
        """

        s = ''
        for i, data in enumerate(self):
            s += f'{i} \t {data[0]} \t {data[1]}\n'
        return s

#Spunto per gli unittest
tempo = np.array([0., 1., 2., 3., 4., 6.])
tensione = np.array([1., 2., 5., 2., 1., 2.])

lab_session = VoltageData(tensione, tempo)
print(lab_session[0, 3])
print(len(lab_session))
print(lab_session)
