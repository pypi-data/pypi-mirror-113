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
import tempfile
import numpy as np
from dataify import EchocardiographyDataset
from torch.utils.data import DataLoader


class TestEchocardiographyDataset(unittest.TestCase):
    """ Test Echocardiography Dataset.
    """
    root = None

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
        if self.root is None:
            with tempfile.TemporaryDirectory() as root:
                dataset = EchocardiographyDataset(root, train=True)
        else:
            dataset = EchocardiographyDataset(self.root, train=True)
        dataloader = DataLoader(dataset, batch_size=64, shuffle=True)
        batch_data = next(iter(dataloader))
        self.logger.debug([item.shape for item in batch_data])


if __name__ == "__main__":

    root = "/tmp/dataify/echocardiography"
    if not os.path.isdir(root):
        os.makedirs(root)
    TestEchocardiographyDataset.root = root
    unittest.main()
