# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2021
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Module provinding the Brain Tumor Segmentation (BraTS) challenge dataset
(http://braintumorsegmentation.org).
"""

# Imports
import os
import numpy as np
import pandas as pd
import nibabel as nib
from torch.utils.data import Dataset


class BraTSDataset(Dataset):
    """ Create the Brats dataset.
    """
    modalities = ("t1", "t1ce", "t2", "flair")

    def __init__(self, root, train=True, transform=None):
        """ Init class.

        Parameters
        ----------
        root: str
            root directory of dataset where the data will be saved.
        train: bool, default True
            specifies training or test dataset.
        transform: callable, default None
            optional transform to be applied on a sample.
        """
        super(BraTSDataset).__init__()
        self.root = root
        self.train = train
        if not self.train:
            raise NotImplementedError("Test dataset not implemented yet.")
        self.transform = transform
        self.traindir = os.path.join(
            datasetdir, "MICCAI_BraTS_2019_Data_Training")
        self.data_file = os.path.join(root, "brats.npy")
        self.download()
        self.data = np.load(self.data_file, mmap_mode="r")

    def download(self):
        """ Download data.
        """
        if not os.path.isfile(self.data_file):

            # Check data has been downloaded
            mapping_path = os.path.join(self.traindir, "name_mapping.csv")
            if not os.path.isfile(mapping_path):
                raise ValueError(
                    "You must first download the Brats data in the '{0}' "
                    "folder following the 'https://www.med.upenn.edu/sbia/"
                    "brats2018/registration.html' instructions.".format(
                        self.root))

            # Parse data
            df = pd.read_csv(mapping_path, sep=",")
            arr = df[["BraTS_2019_subject_ID", "Grade"]].values
            dataset = []
            dataset = []
            nb_subjects = len(arr)
            for cnt, (sid, grade) in enumerate(arr):
                datadir = os.path.join(traindir, grade, sid)
                data = []
                for mod in self.modalities:
                    path = os.path.join(datadir, "{0}_{1}.nii.gz".format(
                        sid, mod))
                    data.append(_norm(_crop(nib.load(path).get_data())))
                data = np.asarray(data)
                input_dataset.append(data)
                path = os.path.join(datadir, "{0}_seg.nii.gz".format(sid))
                _arr = nib.load(path).get_data()
                data = []
                for value in (0, 1, 2, 4):
                    data.append(_crop(_arr == value))
                data = np.asarray(data)
                output_dataset.append(data)
            dataset["image"] = np.asarray(input_dataset)
            dataset["segmentation"] = np.asarray(output_dataset)
            dataset["participant_id"] = arr[:, 0]
            dataset["grade"] = arr[:, 1]

            # Save dataset
            np.savez(self.data_file, **dataset)

    def _crop(arr):
        return arr[45: 195, 30: 220, 10: 145]

    def _norm(arr):
        logical_mask = (arr != 0)
        mean = arr[logical_mask].mean()
        std = arr[logical_mask].std()
        return ((arr - mean) / std).astype("float32")

    def __len__(self):
        return len(self.data["image"])

    def __getitem__(self, idx):
        image = self.data["image"][idx]
        segmentation = self.data["segmentation"][idx]
        grade = self.data["grade"][idx]
        if self.transform is not None:
            image = self.transform(image)
            segmentation = self.transform(segmentation)
        return image, segmentation, grade
