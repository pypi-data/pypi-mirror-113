# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2021
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


"""
Create a moving (left/right) MNIST dataset.
"""

# Imports
import os
import numpy as np
import torchvision
from torch.utils.data import Dataset


class MovingMNISTDataset(Dataset):
    """ Create moving (left/right) MNIST dataset.
    """
    def __init__(self, root, train=True, seq_size=10, shift=1,
                 binary=True, transform=None):
        """ Init class.

        Parameters
        ----------
        root: str
            root directory of dataset where data will be saved.
        train: bool, default True
            specifies training or test dataset.
        seq_len: int, default 10
            the temporal image sequence size.
        shift: int, default 1
            the shift in pixel applied in the left or right direction to
            generate the temporal sequence.
        binary: bool, default True
            binarize images.
        transform: callable, default None
            optional transform to be applied on a sample.
        """
        super(MovingMNISTDataset).__init__()
        self.root = root
        self.train = train
        self.seq_size = seq_size
        self.shift = shift
        self.binary = binary
        self.transform = transform
        self.data = torchvision.datasets.MNIST(
            root, train=train, download=True)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        # Get data
        image, label = self.data[idx]
        image = np.array(image).reshape(28, 28)

        # Binarize MNIST images
        if self.binary:
            tmp = np.random.rand(28, 28)
            image = tmp <= image
        image = image.astype(np.float32)

        # Randomly choose a direction and generate a sequence
        # of images that move in the chosen direction
        direction = np.random.choice(["left", "right"])
        image_list = []
        image_list.append(image.reshape(-1))
        for k in range(1, self.seq_size):
            if direction == "left":
                image = np.roll(image, -1, self.shift)
                image_list.append(image.reshape(-1))
            elif direction == "right":
                image = np.roll(image, 1, self.shift)
                image_list.append(image.reshape(-1))
        image_seq = np.array(image_list)
        label_seq = np.asarray([label] * len(image_seq))

        # Apply tranform
        if self.transform is not None:
            image_seq = self.transform(image_seq)

        return image_seq, label_seq
