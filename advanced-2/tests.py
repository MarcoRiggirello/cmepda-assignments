"""Module for Unit Tests to test the VoltageData class."""

import unittest

import numpy as np

from advanced_2 import VoltageData

class TestVoltageData(unittest.TestCase):
    #pylint: disable = invalid-name
    """
    A class for Unit Tests to check the behaviour of VoltageData class.
    """

    def test_init(self):

        """
        Test of the correct initialization of a class instance.
        Checking for the correct assignment of attributes and private
        variables.
        """

        #Local variables for tests
        v = np.array([0., 5.])
        t = np.array([0., 1.])
        v_load, t_load = np.loadtxt('test_data.TXT', unpack = True)
        lab_session = VoltageData(v, t)
        lab_load = VoltageData.load_data('test_data.TXT')
        #Tests on initialization and attributes
        self.assertEqual(lab_session._data.all(), np.array([v, t]).all())
        self.assertEqual(lab_session.voltage.all(), v.all())
        self.assertEqual(lab_session.time.all(), t.all())
        #Tests on initialization with classmethod load_data
        self.assertEqual(lab_load._data.all(), np.array([v_load, t_load]).all())
        self.assertEqual(lab_load.voltage.all(), v_load.all())
        self.assertEqual(lab_load.time.all(), t_load.all())

    def test_error(self):

        """
        Test of the correct management of errors.
        Checking that the class isn't initialized with incorrect data sets.
        """

        #Tests on incorrect array tipe
        v_nofloat = np.array([0., 5., 's'])
        t_nofloat = np.array([0., 1., 't'])
        with self.assertRaises(ValueError):
            lab_session = VoltageData(v_nofloat, t_nofloat)
        #Tests on incorrect shape
        v_wronglen = np.array([0., 1.])
        t_wronglen = np.array([0.])
        with self.assertRaises(ValueError):
            lab_session = VoltageData(v_wronglen, t_wronglen)

    def test_getitem(self):

        """Unit test for __getitem__ method."""

        v = np.array([0., 5.])
        t = np.array([0., 1.])
        lab_session = VoltageData(v, t)
        self.assertAlmostEqual(lab_session[0, 0], 0.)
        self.assertAlmostEqual(lab_session[1, 0], 5.)
        self.assertAlmostEqual(lab_session[0, 1], 0.)
        self.assertAlmostEqual(lab_session[1, 1], 1.)

    def test_len(self):

        """Unit test for __len__ method."""

        v = np.array([0., 5.])
        t = np.array([0., 1.])
        lab_session = VoltageData(v, t)
        self.assertEqual(len(lab_session), 2)

    def test_call(self):

        """Unit test for the call method based on interpolation of the data."""

        #The data in the file obey the relation V(t) = 5 * t.
        lab_session = VoltageData.load_data('test_data.TXT')
        self.assertAlmostEqual(lab_session(1.5), 7.5)
        #Function should return ValueError if param out of bonds for t array. 
        with self.assertRaises(ValueError):
            lab_session(-1.)



if __name__ == '__main__':
    unittest.main()
