# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2021
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Create the DSprites dataset (https://github.com/deepmind/dsprites-dataset).
"""

# Imports
import os
import subprocess
import numpy as np
from torch.utils.data import Dataset


class DSpritesDataset(Dataset):
    """ Disentanglement test Sprites dataset.

    Procedurally generated 2D shapes, from 6 disentangled latent factors.
    This dataset uses 6 latents, controlling the color, shape, scale,
    rotation and position of a sprite.
    All possible variations of the latents are present. Ordering along
    dimension 1 is fixed and can be mapped back to the exact latent values
    that generated that image. Pixel outputs are different. No noise added.
    """
    url = ("https://github.com/deepmind/dsprites-dataset/blob/master/"
           "dsprites_ndarray_co1sh3sc6or40x32y32_64x64.npz?raw=true")
    lat_names = ("color", "shape", "scale", "orientation", "posX", "posY")
    img_size = (64, 64)

    def __init__(self, root, size=None, transform=None):
        """ Init class.

        Parameters
        ----------
        root: string
            the dataset destination folder.
        size: int, default None
            the size of the dataset, default use all images available.
        transform: callable, default None
            optional transform to be applied on a sample.

        Returns
        -------
        item: namedtuple
            a named tuple containing 'input_path', and 'metadata_path'.
        """
        super(DSpritesDataset, self).__init__()
        self.root = root
        self.transform = transform
        self.data_file = os.path.join(self.root, "dsprites.npz")
        self.download()
        self.data = np.load(self.data_file, mmap_mode="r")
        self.X = self.data["imgs"]
        self.lfactors = self.data["latents_values"]
        self.size = size or len(self.X)
        self.size = min(self.size, len(self.X))

    def download(self):
        """ Download the dataset.
        """
        if not os.path.isfile(self.data_file):

            # Fetch data
            print("Downloading {0}.".format(self.url))
            subprocess.check_call(["curl", "-L", self.url,
                                   "--output", self.data_file])

    def __len__(self):
        return self.size

    def __getitem__(self, idx):
        image = np.expand_dims(self.X[idx], axis=0)
        latent_vals = self.lfactors[idx]
        if self.transform is not None:
            image = self.transform(image)
        return image, latent_vals
