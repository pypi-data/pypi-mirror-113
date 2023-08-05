# -*- coding: utf-8 -*-
########################################################################
# NSAp - Copyright (C) CEA, 2021
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
########################################################################

"""
Create the anatomical HCP (http://www.humanconnectomeproject.org) dataset
composed of T1w images and associated brain mask.
"""

# Imports
import os
import boto3
from botocore.exceptions import NoCredentialsError
import nibabel as nib
import numpy as np
import pandas as pd
from scipy import ndimage
from torch.utils.data import Dataset


class HCPAnatDataset(Dataset):
    """ Create the HCP T1/brain mask dataset.

    Go to 'https://db.humanconnectome.org' and get an account and log in.
    Then, click on the Amazon S3 button that should give you a key pair.
    Then use 'aws configure' to add this to our machine.
    AWS Access Key ID: ****************
    AWS Secret Access Key: ****************
    Default region name: eu-west-3
    Default output format: json
    """
    def __init__(self, root, train=True, space="mni", lowres=False,
                 n_subjects=None, transform=None, seed=None):
        """ Init class.

        Parameters
        ----------
        root: str
            root directory of dataset where the data will be saved.
        train: bool, default True
            specifies training or test dataset.
        space: str, default
            the data space: "native", "mni"
        lowres: bool, default False
            build a low resolution dataset.
        n_subjects: int, default None
            the number of subjects to be that will be fetched.
        transform: callable, default None
            optional transform to be applied on a sample.
        seed: int, default None
            controls the shuffling applied to the data before applying the
            split.
        """
        super(HCPAnatDataset, self).__init__()
        self.root = root
        self.train = train
        self.space = space
        self.lowres = lowres
        self.n_subjects = n_subjects
        self.tranform = transform
        self.seed = seed
        self.data_file = os.path.join(root, "hcp_anat.npz")
        self.download()
        self.data = np.load(self.data_file, mmap_mode="r")
        splitdata = train_test_split(
            self.data["image"], self.data["mask"], test_size=0.25,
            shuffle=True, random_state=seed)
        if self.train:
            self.X = splitdata[::2]
        else:
            self.X = splitdata[1::2]

    def download(self):
        """ Download data.
        """
        if not os.path.isfile(self.data_file):

            # Get subjects
            client = boto3.client("s3")
            paginator = client.get_paginator("list_objects")
            prefix = "HCP_1200/"
            result = paginator.paginate(
                Bucket="hcp-openaccess", Delimiter="/", Prefix=prefix)
            try:
                subjects_prefix = list(result.search("CommonPrefixes"))
            except NoCredentialsError:
                msg = """
                Go to 'https://db.humanconnectome.org' and get an account and
                log in.
                Then, click on the Amazon S3 button that should give you a key
                pair.
                Then use 'aws configure' to add this to our machine.
                AWS Access Key ID: ****************
                AWS Secret Access Key: ****************
                Default region name: eu-west-3
                Default output format: json
                """
                raise ValueError(msg)
            if self.n_subjects is not None:
                subjects_prefix = subjects_prefix[:self.n_subjects]

            # Fetch data
            images = []
            masks = []
            subjects = []
            for subject in subjects_prefix:
                subject_prefix = subject["Prefix"]
                data = get_hcp_data(self.root, subject_prefix,
                                    self.space + "_t1w", self.lowres)
                subjects.append(subject_prefix[11: -1])
                images.append(data["image"])
                masks.append(data["mask"].astype(int))
            dataset = {
                "image": np.expand_dims(np.asarray(images), axis=1),
                "mask": np.expand_dims(np.asarray(masks), axis=1),
                "subjects": np.asarray(subjects)}

            # Save dataset
            np.savez(self.data_file, **dataset)

    def __len__(self):
        return len(self.X[0])

    def __getitem__(self, idx):
        image = self.X[0][idx]
        mask = self.X[1][idx]
        if self.transform is not None:
            image = self.transform(image)
            mask = self.transform(mask)
        return image, mask


def get_hcp_data(datasetdir, subject_prefix, modality, low):
    """ Get the requested data.

    Parameters
    ----------
    datasetdir: str
        the dataset destination folder.
    subject_prefix: str
        subject path.
    modality: str
        type of image to be extracted ('T1w' or 'MNINonLinear').
    low: bool
        set image in low resolution.

    Returns
    -------
    data: dict
        the loaded data.
    """
    s3 = boto3.resource("s3")
    bucket = s3.Bucket("hcp-openaccess")
    mapping = {
        "native_t1w": {
            "image": "T1w_acpc_dc_restore.nii.gz",
            "mask": "brainmask_fs.nii.gz"},
        "mni_t1w": {
            "image": "T1w_restore.nii.gz",
            "mask": "brainmask_fs.nii.gz"}
    }
    if modality not in mapping:
        raise ValueError("Unexpected modality '{0}'. Valid modalities "
                         "are: {1}".format(modality, mapping.keys()))
    data = {}
    for key, basename in mapping[modality].items():
        url = subject_prefix + "/".join([modality, basename])
        pattern = url.split("/")
        destfile = os.path.join(datasetdir, *pattern)
        if not os.path.isfile(destfile):
            logger.info("  url: {0}".format(url))
            logger.info("  dest: {0}".format(destfile))
            dirname = os.path.dirname(destfile)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            obj = s3.Object(bucket, url)
            bucket.download_file(obj.key, destfile)
        data[key] = load_image(destfile, low)
    return data


def load_image(filename, low=False):
    """ Load an MRI image.

    High resolution images are resampled to (256, 312, 256) and low resolution
    images are resampled to (32, 40, 32) which can be divided by 8.

    Parameters
    ----------
    filename: str
        file to be loaded.
    low: bool, default False
        set image in low resolution.

    Returns
    -------
    img_data: np.array
        loaded image.
    """
    img = nib.load(filename)
    img_data = img.get_data()
    img_data = np.append(
        img_data[2:-2, :, 2:-2], np.zeros((256, 1, 256)), axis=1)
    if low:
        img_data = ndimage.zoom(img_data, 1. / 8., order=0)
        img_data = np.append(img_data, np.zeros((32, 1, 32)), axis=1)
    return img_data
