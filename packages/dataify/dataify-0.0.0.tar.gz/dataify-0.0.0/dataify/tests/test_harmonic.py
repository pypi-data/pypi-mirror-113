# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2021
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# Imports
import os
import sys
import logging
import unittest
import numpy as np
from dataify import SinOscillatorDataset
from torch.utils.data import DataLoader


class TestSinOscillatorDataset(unittest.TestCase):
    """ Test Sin Oscillator Dataset.
    """
    def setUp(self):
        """ Setup test.
        """
        logging.basicConfig(stream=sys.stderr)
        self.logger = logging.getLogger("unittest")
        self.logger.setLevel(logging.DEBUG)

    def tearDown(self):
        """ Run after each test.
        """
        pass

    def test_dataset_creation(self):
        """ Test dataset creation.
        """
        dataset = SinOscillatorDataset()
        dataloader = DataLoader(dataset, batch_size=64, shuffle=True)
        batch_data = next(iter(dataloader))
        self.logger.debug(batch_data.shape)


if __name__ == "__main__":

    unittest.main()
