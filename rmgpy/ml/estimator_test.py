#!/usr/bin/env python3

###############################################################################
#                                                                             #
# RMG - Reaction Mechanism Generator                                          #
#                                                                             #
# Copyright (c) 2002-2020 Prof. William H. Green (whgreen@mit.edu),           #
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

import unittest

from rmgpy.ml.estimator import MLEstimator


class TestMLEstimator(unittest.TestCase):
    """
    Contains unit tests for rmgpy.ml.estimator
    """

    def setUp(self):
        """
        Set up the MLEstimator class. This method is run once before all
        other unit tests.
        """
        self.ml_estimator = MLEstimator("attn_mpn")

    def test_get_thermo_data_from_smiles(self):
        """
        Test that we can make a prediction using MLEstimator using gnns_thermo.
        """
        smi = "C1C2C1C2"
        thermo = self.ml_estimator.get_thermo_data(smi, mode="from_smiles")
        self.assertTrue(thermo.comment.startswith("ML Estimation using from_smiles"))
        self.assertAlmostEqual(thermo.Cp0.value_si, 33.15302276611328, 1)
        self.assertAlmostEqual(thermo.CpInf.value_si, 232.1982879638672, 1)
        self.assertEqual(len(thermo.Cpdata.value_si), 9)

    def test_get_thermo_data_from_rdkit_mol(self):
        """
        Test that we can make a prediction using MLEstimator using gnns_thermo.
        """
        smi = "C1C2C1C2"
        thermo = self.ml_estimator.get_thermo_data(smi, mode="from_rdkit_mol")
        self.assertTrue(thermo.comment.startswith("ML Estimation using from_rdkit"))
        self.assertAlmostEqual(thermo.Cp0.value_si, 33.15302276611328, 1)
        self.assertAlmostEqual(thermo.CpInf.value_si, 232.1982879638672, 1)
        self.assertEqual(len(thermo.Cpdata.value_si), 9)

    def test_convert_thermo_data(self):
        """
        Test that we can make a prediction using gnns_thermo and convert to wilholt.
        """
        smi = "C1C2C1C2"
        thermo = self.ml_estimator.get_thermo_data(smi)
        thermo.to_wilhoit(B=1000.0)
