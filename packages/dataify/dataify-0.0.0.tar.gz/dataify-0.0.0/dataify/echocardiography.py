# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2019
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Create the echocardiography dataset.
"""

# Imports
import os
import glob
import urllib
import tarfile
import numpy as np
import skimage.io as skio
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset


class EchocardiographyDataset(Dataset):
    """ Create the echocardiography dataset.
    """
    url = ("https://deepimaging2019.sciencesconf.org/data/pages/"
           "ge_insa_lyon_datasets_camus_dataset_2.tar")
    label_map = {"ES": 0, "ED": 1}

    def __init__(self, root, train=True, transform=None, seed=None):
        """ Init class.

        Parameters
        ----------
        root: str
            root directory of dataset where the data will be saved.
        train: str, default True
            specifies training or test dataset.
        transform: callable, default None
            optional transform to be applied on a sample.
        """
        super(EchocardiographyDataset).__init__()
        self.root = root
        self.train = train
        self.transform = transform
        self.height, self.width = (256, 256)
        self.data_file = os.path.join(root, "echocardiography.npz")
        self.download()
        self.data = np.load(self.data_file, mmap_mode="r")
        splitdata = train_test_split(
            self.data["image"], self.data["segmentation"], self.data["name"],
            self.data["label"], test_size=0.25, shuffle=True,
            random_state=seed)
        if train:
            self.X = splitdata[::2]
        else:
            self.X = splitdata[1::2]

    def download(self):
        """ Download data.
        """
        if not os.path.isfile(self.data_file):

            # Download & extract data
            print("Downloading {0}.".format(self.url))
            tarball = os.path.join(self.root, "echocardiography.tar")
            urllib.request.urlretrieve(self.url, tarball)
            downloaddir = tarball.replace(".tar", "")
            tar = tarfile.open(tarball)
            tar.extractall(path=downloaddir)
            tar.close()

            # Parse data
            files = glob.glob(os.path.join(downloaddir, "images", "*.png"))
            nb_files = len(files)
            data = []
            masks = []
            metadata = dict((key, []) for key in ("name", "label"))
            for path in files:
                basename = os.path.basename(path)
                im = skio.imread(path)
                im = im / np.max(im)
                mask_path = os.path.join(downloaddir, "masks", basename)
                mask = skio.imread(mask_path)
                mask = mask.astype(np.single)
                mask = (mask / 255. * 3.).astype(int)
                mask = self.to_categorical(y=mask, num_classes=4)
                data.append(im)
                masks.append(mask)
                basename = basename.replace(".png", "")
                metadata["name"].append(basename)
                metadata["label"].append(basename[-2:])
            data = np.expand_dims(data, axis=1)
            dataset = {
                "image": np.asarray(data).astype("float32"),
                "segmentation": np.asarray(masks).astype("float32"),
                "name": np.array(metadata["name"]),
                "label": np.array(metadata["label"])}

            # Save dataset
            np.savez(self.data_file, **dataset)

    def to_categorical(self, y, num_classes):
        """ 1-hot encodes a tensor.
        """
        return np.eye(num_classes, dtype="uint8")[y].transpose(2, 0, 1)

    def __len__(self):
        return len(self.X[0])

    def __getitem__(self, idx):
        image = self.X[0][idx]
        segmentation = self.X[1][idx]
        label = self.label_map[self.X[3][idx]]
        if self.transform is not None:
            image = self.transform(image)
            segmentation = self.transform(segmentation)
        return image, segmentation, label
