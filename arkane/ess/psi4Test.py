#!/usr/bin/env python3

###############################################################################
#                                                                             #
# RMG - Reaction Mechanism Generator                                          #
#                                                                             #
# Copyright (c) 2002-2022 Prof. William H. Green (whgreen@mit.edu),           #
# Prof. Richard H. West (r.west@neu.edu) and the RMG Team (rmg_dev@mit.edu)   #
#                                                                             #
# Permission is hereby granted, free of charge, to any person obtaining a     #
# copy of this software and associated documentation files (the 'Software'),  #
# to deal in the Software without restriction, including without limitation   #
# the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
# and/or sell copies of the Software, and to permit persons to whom the       #
# Software is furnished to do so, subject to the following conditions:        #
#                                                                             #
# The above copyright notice and this permission notice shall be included in  #
# all copies or substantial portions of the Software.                         #
#                                                                             #
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER      #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
# DEALINGS IN THE SOFTWARE.                                                   #
#                                                                             #
###############################################################################

"""
This module contains unit tests of the :mod:`arkane.ess.psi4` module.
"""

import os
import unittest

import numpy as np

from rmgpy.statmech import IdealGasTranslation, NonlinearRotor, HarmonicOscillator, HinderedRotor

from arkane.exceptions import LogError
from arkane.ess.psi4 import Psi4Log

################################################################################


class Psi4LogTest(unittest.TestCase):
    """
    Contains unit tests for the Psi4Log module, used for parsing Psi4 log files.
    """
    @classmethod
    def setUpClass(cls):
        """
        A method that is run before all unit tests in this class.
        """
        cls.data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'psi4')

    def test_check_for_errors(self):
        """
        Uses Psi4 log files that had various errors to test if errors are properly parsed.
        """
        with self.assertRaises(LogError):
            Psi4Log(os.path.join(self.data_path, 'IO_error.out'))

    def test_number_of_atoms_from_psi4_log(self):
        """
        Uses a Psi4 log files to test that
        number of atoms can be properly read.
        """
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq.out'))
        self.assertEqual(log.get_number_of_atoms(), 3)
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq_ts.out'))
        self.assertEqual(log.get_number_of_atoms(), 4)
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq_dft.out'))
        self.assertEqual(log.get_number_of_atoms(), 3)
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq_dft_ts.out'))
        self.assertEqual(log.get_number_of_atoms(), 4)

    def test_energy_from_psi4_log(self):
        """
        Uses a Psi4 log files to test that
        molecular energies can be properly read.
        """
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq.out'))
        self.assertAlmostEqual(log.load_energy(), -199599899.9822719, delta=1e-2)
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq_ts.out'))
        self.assertAlmostEqual(log.load_energy(), -395828407.5987777, delta=1e-2)
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq_dft.out'))
        self.assertAlmostEqual(log.load_energy(), -200640009.37231186, delta=1e-2)
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq_dft_ts.out'))
        self.assertAlmostEqual(log.load_energy(), -397841662.56434655, delta=1e-2)

    def test_zero_point_energy_from_psi4_log(self):
        """
        Uses Psi4 log files to test that zero-point energies can be properly read.
        """
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq.out'))
        self.assertAlmostEqual(log.load_zero_point_energy(), 60868.832, delta=1e-3)
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq_dft.out'))
        self.assertAlmostEqual(log.load_zero_point_energy(), 56107.44, delta=1e-3)
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq_dft_ts.out'))
        self.assertAlmostEqual(log.load_zero_point_energy(), 67328.928, delta=1e-3)
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq_ts.out'))
        self.assertAlmostEqual(log.load_zero_point_energy(), 75136.272, delta=1e-3)

    def test_load_force_constant_matrix_from_psi4_log(self):
        """
        Uses Psi4 log files to test that force constant matrices can be properly read.
        """
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq.out'))
        expected_mat_1 = np.array([[79.60709821, 0., 0., -158.56969492, 0., -119.50250089, -158.56969492, 0., 119.50250089],
                                   [0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   [0., 0., 51.88196366, -92.52464457, 0., -103.3438893, 92.52464457, 0., -103.3438893],
                                   [-158.56969492, 0., -92.52464457, 682.40616438, 0., 422.33771249, -50.69495535, 0., -53.73729893],
                                   [0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   [-119.50250089, 0., -103.3438893, 422.33771249, 0., 385.24274073, 53.73729893, 0., 26.45946547],
                                   [-158.56969492, 0., 92.52464457, -50.69495535, 0., 53.73729893, 682.40616438, 0., -422.33771249],
                                   [0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   [119.50250089, 0., -103.3438893, -53.73729893, 0., 26.45946547, -422.33771249, 0., 385.24274073]],
                                  np.float64)
        self.assertTrue(np.allclose(log.load_force_constant_matrix(), expected_mat_1))

        log = Psi4Log(os.path.join(self.data_path, 'opt_freq_dft.out'))
        expected_mat_2 = np.array([[65.29227021, 0., 0., -130.05593215, 0., -102.09767406, -130.05593215, 0., 102.09767406],
                                   [0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   [0., 0., 44.51008758, -77.12673693, 0., -88.65982001, 77.12673693, 0., -88.65982001],
                                   [-130.05593215, 0., -77.12673693, 567.48290169, 0., 356.99781537, -49.36504715, 0., -49.73970876],
                                   [0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   [-102.09767406, 0., -88.65982001, 356.99781537, 0., 336.25221646, 49.73970876, 0., 16.95147799],
                                   [-130.05593215, 0., 77.12673693, -49.36504715, 0., 49.73970876, 567.48290169, 0., -356.99781537],
                                   [0., 0., 0., 0., 0., 0., 0., 0., 0.],
                                   [102.09767406, 0., -88.65982001, -49.73970876, 0., 16.95147799, -356.99781537, 0., 336.25221646]],
                                  np.float64)
        self.assertTrue(np.allclose(log.load_force_constant_matrix(), expected_mat_2))

        log = Psi4Log(os.path.join(self.data_path, 'opt_freq_dft_ts.out'))
        expected_mat_3 = np.array([[-1.13580195, 0., 0., 3.38451439, 0., 0., 1.13580195, 0., 0., -3.38451439, 0., 0.],
                                   [0., 32.96704817, -7.81315371, 0., -24.52602914, 47.62525747, 0., -23.84113467, -5.93732553, 0., -11.82985738, 7.15401071],
                                   [0., -7.81315371, 54.99575056, 0., 23.33047286, -191.28989554, 0., 5.93732553, -7.5316094, 0., -15.85753341, 2.20187269],
                                   [3.38451439, 0.,  0., -10.08532992, 0., 0., -3.38451439, 0., 0., 10.08532992, 0., 0.],
                                   [0., -24.52602914, 23.33047286, 0., 143.78387645, -158.67358218, 0., -11.82985738, 15.85753341, 0., 1.05099332, 2.55609183],
                                   [0., 47.62525747, -191.28989554, 0., -158.67358218, 742.27868659, 0., -7.15401071, 2.20187269, 0., -2.55609183, 11.01167933],
                                   [1.13580195, 0., 0., -3.38451439, 0., 0., -1.13580195, 0., 0., 3.38451439, 0., 0.],
                                   [0., -23.84113467, 5.93732553, 0., -11.82985738, -7.15401071, 0., 32.96704817, 7.81315371, 0., -24.52602914, -47.62525747],
                                   [0., -5.93732553, -7.5316094, 0., 15.85753341, 2.20187269, 0., 7.81315371, 54.99575056, 0., -23.33047286, -191.28989554],
                                   [-3.38451439, 0., 0., 10.08532992, 0., 0., 3.38451439, 0., 0., -10.08532992, 0., 0.],
                                   [0., -11.82985738, -15.85753341, 0., 1.05099332, -2.55609183, 0., -24.52602914, -23.33047286, 0., 143.78387645, 158.67358218],
                                   [0., 7.15401071, 2.20187269, 0., 2.55609183, 11.01167933, 0., -47.62525747, -191.28989554, 0., 158.67358218, 742.27868659]],
                                  np.float64)
        self.assertTrue(np.allclose(log.load_force_constant_matrix(), expected_mat_3))

        log = Psi4Log(os.path.join(self.data_path, 'opt_freq_ts.out'))
        expected_mat_4 = np.array([[-1.36856086, 0., 0., 3.91653225, 0., 0., 1.36856086, 0., 0., -3.91653225, 0., 0.],
                                   [0., 47.82294224, -11.20296807, 0., -35.81980174, 65.25989773, 0., -35.42652343, -7.19264812, 0., -13.56514966, 8.02470416],
                                   [0., -11.20296807, 66.4797624, 0., 35.78782098, -229.4811002, 0., 7.19264812, -9.74548387, 0., -19.81147687, 3.46263087],
                                   [3.91653225, 0., 0., -11.2082886, 0., 0., -3.91653225, 0., 0., 11.2082886, 0., 0.],
                                   [0., -35.81980174, 35.78782098, 0., 194.95334567, -224.75547126, 0., -13.56514966, 19.81147687, 0., 1.78681563, 3.25854712],
                                   [0., 65.25989773, -229.4811002, 0., -224.75547126, 889.16020169, 0., -8.02470416, 3.46263087, 0., -3.25854712, 11.25397079],
                                   [1.36856086, 0., 0., -3.91653225, 0., 0., -1.36856086, 0., 0., 3.91653225, 0., 0.],
                                   [0., -35.42652343, 7.19264812, 0., -13.56514966, -8.02470416, 0., 47.82294224, 11.20296807, 0., -35.81980174, -65.25989773],
                                   [0., -7.19264812, -9.74548387, 0., 19.81147687, 3.46263087, 0., 11.20296807, 66.4797624, 0., -35.78782098, -229.4811002],
                                   [-3.91653225, 0., 0., 11.2082886, 0., 0., 3.91653225, 0., 0., -11.2082886, 0., 0.],
                                   [0., -13.56514966, -19.81147687, 0., 1.78681563, -3.25854712, 0., -35.81980174, -35.78782098, 0., 194.95334567, 224.75547126],
                                   [0., 8.02470416, 3.46263087, 0., 3.25854712, 11.25397079, 0., -65.25989773, -229.4811002, 0., 224.75547126, 889.16020169]],
                                  np.float64)
        self.assertTrue(np.allclose(log.load_force_constant_matrix(), expected_mat_4))

    def test_load_vibrations_from_psi4_log(self):
        """
        Uses a Psi4 log files to test that
        molecular energies can be properly read.
        """
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq.out'))
        conformer, unscaled_frequencies = log.load_conformer()
        self.assertEqual(len(conformer.modes[2]._frequencies.value), 3)
        self.assertEqual(conformer.modes[2]._frequencies.value[2], 4261.7445)
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq_dft_ts.out'))
        conformer, unscaled_frequencies = log.load_conformer()
        self.assertEqual(len(conformer.modes[2]._frequencies.value), 5)
        self.assertEqual(conformer.modes[2]._frequencies.value[2], 1456.2449)

    def test_load_modes_from_psi4_log(self):
        """
        Uses a Psi4 log file for opt_freq.out to test that its
        molecular modes can be properly read.
        """
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq.out'))
        conformer, unscaled_frequencies = log.load_conformer()
        self.assertTrue(len([mode for mode in conformer.modes if isinstance(mode, IdealGasTranslation)]) == 1)
        self.assertTrue(len([mode for mode in conformer.modes if isinstance(mode, NonlinearRotor)]) == 1)
        self.assertTrue(len([mode for mode in conformer.modes if isinstance(mode, HarmonicOscillator)]) == 1)
        self.assertEqual(len(unscaled_frequencies), 3)

    def test_load_negative_frequency(self):
        """
        Test properly loading negative frequencies.
        """
        log_1 = Psi4Log(os.path.join(self.data_path, 'opt_freq_dft_ts.out'))
        neg_freq_1 = log_1.load_negative_frequency()
        self.assertEqual(neg_freq_1, -617.1749)
        log_2 = Psi4Log(os.path.join(self.data_path, 'opt_freq_ts.out'))
        neg_freq_2 = log_2.load_negative_frequency()
        self.assertEqual(neg_freq_2, -653.3950)

    def test_spin_multiplicity_from_psi4_log(self):
        """
        Uses a Psi4 log file for opt_freq_dft_ts.out to test that its
        molecular degrees of freedom can be properly read.
        """
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq.out'))
        conformer, unscaled_frequencies = log.load_conformer()
        self.assertEqual(conformer.spin_multiplicity, 1)
        log = Psi4Log(os.path.join(self.data_path, 'opt_freq_dft_ts.out'))
        conformer, unscaled_frequencies = log.load_conformer()
        self.assertEqual(conformer.spin_multiplicity, 1)


################################################################################


if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=2))
