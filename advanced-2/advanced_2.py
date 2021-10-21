#Assignment advanced-2 for cmepda - by Antoine Venturini and Marco Riggirello.

"""The VoltageData class manipulates time and voltage data."""

import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline as IUS

class VoltageData:
    #pylint: disable=invalid-name
    """
    The VoltageData class manipulates two sets of data: time and voltage.

    Arguments
    ---------
    voltage : (N,) array of floats
        Voltage measurements.
    time : (N,) array of floats
        Time measurements.

    Note
    ----
    voltage and time must have the same shape.

    Methods
    -------
    load_data(cls, fname)
        This classmethod permits to initialize a VoltageData instance loading
        the data from a file.

    __len__(self)
        The length of a VoltageData instance is the length of the data samples.

    __getitem__(self, indexx)
        Permits to access the voltage or time data through [].

        Parameter
        ---------

        indexx : (2,) tuple of int

        Return
        ------
        tension[index2] if index1 = 0
        time[index2] if index1 = 1
    __call__(self, time_0)
        Transform a class instance in a function if a float
        is passed as argument.

        Parameter
        ---------
        time_0 : float
            Instant in which evauate the voltage.

        Return
        ------
        voltage_0 : float
            Voltage value at time_0 extrapolated with a spline interpolation.
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

        return iter(self._data)


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
        'line number \t tension entry \t time entry'
        """

        s = ''
        for i, data in enumerate(self):
            s += f'{i} \t {data[0]} \t {data[1]}\n'
        return s

    def __str__(self):

        """
        Prints class instances.

        The data are printed with this organization:
        'tension entry \t time entry'
        """

        s = ''
        for data in self:
            s += f'{data[0]} \t {data[1]}\n'
        return s

    def __call__(self, time_0):

        """
        The function permits to evaluate the voltage at the istant time_0.
        The value is derived through interpolation of the data with a spline.

        Parameter
        ---------
        time_0 : float
            Instant in which evauate the voltage.

        Return
        ------
        voltage_0 : float
            Voltage value at time_0 extrapolated with a spline interpolation.
        """

        #Interpolation esteem fails out self.time bonds.
        if self.time[0]<= time_0 <= self.time[-1]:
            spline = IUS(self.time, self.voltage, ext='zeros')
            return spline(time_0)
        else:
            raise ValueError('Input data out of time measurements limits.')
