# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2021
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Create the IMaging-PsychiAtry Challenge (IMPAC) dataset to predict autism
which is a data challenge on Autism Spectrum Disorder detection
(https://paris-saclay-cds.github.io/autism_challenge).
"""

# Imports
import os
import requests
import zipfile
import hashlib
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from nilearn.connectome import ConnectivityMeasure
from torch.utils.data import Dataset


class IMPACDataset(Dataset):
    """ Create the IMPAC dataset.

    To compute the functional connectivity using the rfMRI data, we use the
    BASC atlas with 122 ROIs.
    """
    atlas = ("basc064", "basc122", "basc197", "craddock_scorr_mean",
             "harvard_oxford_cort_prob_2mm", "msdl", "power_2011")
    archive = "https://zenodo.org/record/3625740/files/{0}.zip"
    checksum = {
        "basc064":
        "75eb5ee72344d11f056551310a470d00227fac3e87b7205196f77042fcd434d0",
        "basc122":
        "2d0d2c2338f9114877a0a1eb695e73f04fc664065d1fb75cff8d59f6516b0ec7",
        "basc197":
        "68135bb8e89b5b3653e843745d8e5d0e92876a5536654eaeb9729c9a52ab00e9",
        "craddock_scorr_mean":
        "634e0bb07beaae033a0f1615aa885ba4cb67788d4a6e472fd432a1226e01b49b",
        "harvard_oxford_cort_prob_2mm":
        "638559dc4c7de25575edc02e58404c3f2600556239888cbd2e5887316def0e74",
        "msdl":
        "fd241bd66183d5fc7bdf9a115d7aeb9a5fecff5801cd15a4e5aed72612916a97",
        "power_2011":
        "d1e3cd8eaa867079fe6b24dfaee08bd3b2d9e0ebbd806a2a982db5407328990a"}
    urls = [
        "https://raw.githubusercontent.com/ramp-kits/autism/master/data/" +
        name for name in ["anatomy.csv", "anatomy_qc.csv", "fmri_filename.csv",
                          "fmri_qc.csv", "fmri_repetition_time.csv",
                          "participants.csv", "test.csv", "train.csv"]]

    def __init__(self, root, train=True, ftype="all", transform=None):
        """ Init class.

        Parameters
        ----------
        root: str
            root directory of dataset where data will be saved.
        train: bool, default True
            specifies training or test dataset.
        ftype: str, default 'all'
            the features type: 'anatomy', 'fmri', or 'all'.
        transform: callable, default None
            optional transform to be applied on a sample.
        """
        super(IMPACDataset).__init__()
        self.root = root
        self.train = train
        self.ftype = ftype
        self.transform = transform
        self.data_file = os.path.join(root, "impac.npz")
        self.download()
        self.data = np.load(self.data_file, mmap_mode="r")

    def download(self):
        """ Download data.
        """
        if not os.path.isfile(self.data_file):

            # Fetch data
            self.fetch_fmri_time_series(self.root, atlas="basc122")
            data = []
            sets = {}
            for url in self.urls:
                basename = url.split("/")[-1]
                name = basename.split(".")[0]
                local_file = os.path.join(self.root, basename)
                if not os.path.isfile(local_file):
                    response = requests.get(url, stream=True)
                    with open(local_file, "wt") as out_file:
                        out_file.write(response.text)
                    del response
                if name not in ("train", "test"):
                    prefix = name.split("_")[0]
                    df = pd.read_csv(local_file, index_col=0)
                    df.columns = [
                        "{0}_{1}".format(prefix, col) for col in df.columns]
                    data.append(df)
                else:
                    df = pd.read_csv(local_file, header=None)
                    sets[name] = df[0].values.tolist()
            data = pd.concat(data, axis=1)

            # Filter data
            data = data[data["anatomy_select"].isin((1, 2))]
            data = data[data["fmri_select"].isin((1, 2))]

            # Extract features
            data_train = data[data.index.isin(sets["train"])]
            data_test = data[data.index.isin(sets["test"])]
            y_train = data_train["participants_asd"]
            y_test = data_test["participants_asd"]
            features = FeatureExtractor()
            features.fit(data_train, y_train, self.root)
            features_train = features.transform(data_train, self.root)
            features.fit(data_test, y_test, self.root)
            features_test = features.transform(data_test, self.root)
            dataset = {
                "data_train": features_train,
                "label_train": y_train,
                "data_test": features_test,
                "label_test": y_test}

            # Save dataset
            np.savez(self.data_file, **dataset)

    def fetch_fmri_time_series(self, outdir, atlas="all"):
        """ Fetch the time-series extracted from the fMRI data using a specific
        atlas.

        Parameters
        ----------
        outdir: str
            the detination folder.
        atlas: string, default='all'
            the name of the atlas used during the extraction. The possibilities
            are:
            * `'basc064`, `'basc122'`, `'basc197'`: BASC parcellations with 64,
            122, and 197 regions [1]_;
            * `'craddock_scorr_mean'`: Ncuts parcellations [2]_;
            * `'harvard_oxford_cort_prob_2mm'`: Harvard-Oxford anatomical
            parcellations;
            * `'msdl'`: MSDL functional atlas [3]_;
            * `'power_2011'`: Power atlas [4]_.

        References
        ----------
        .. [1] Bellec, Pierre, et al. "Multi-level bootstrap analysis of stable
           clusters in resting-state fMRI." Neuroimage 51.3 (2010): 1126-1139.
        .. [2] Craddock, R. Cameron, et al. "A whole brain fMRI atlas generated
           via spatially constrained spectral clustering." Human brain mapping
           33.8 (2012): 1914-1928.
        .. [3] Varoquaux, Gaël, et al. "Multi-subject dictionary learning to
           segment an atlas of brain spontaneous activity." Biennial
           International Conference on Information Processing in Medical
           Imaging. Springer, Berlin, Heidelberg, 2011.
        .. [4] Power, Jonathan D., et al. "Functional network organization of
           the human brain." Neuron 72.4 (2011): 665-678.
        """
        if atlas == "all":
            for single_atlas in self.atlas:
                self._download_fmri_data(single_atlas, outdir)
        elif atlas in self.atlas:
            self._download_fmri_data(atlas, outdir)
        else:
            raise ValueError(
                "'atlas' should be one of {0}. Got {1} instead.".format(
                    self.atlas, atlas))

    def _download_fmri_data(self, atlas, outdir):
        zip_file = os.path.join(outdir, atlas + ".zip")
        if not os.path.isfile(zip_file):
            response = requests.get(self.archive.format(atlas))
            with open(zip_file, "wb") as of:
                of.write(response.content)
        atlas_directory = os.path.join(outdir, "data", "fmri")
        if not os.path.isdir(atlas_directory):
            self._check_and_unzip(zip_file, atlas, atlas_directory)

    def _check_and_unzip(self, zip_file, atlas, atlas_directory):
        checksum_download = self._sha256(zip_file)
        if checksum_download != self.checksum[atlas]:
            os.remove(zip_file)
            raise IOError("The file downloaded was corrupted. Try again "
                          "to execute this fetcher.")
        zip_ref = zipfile.ZipFile(zip_file, "r")
        zip_ref.extractall(atlas_directory)
        zip_ref.close()

    def _sha256(self, path):
        """ Calculate the sha256 hash of the file at path.
        """
        sha256hash = hashlib.sha256()
        chunk_size = 8192
        with open(path, "rb") as f:
            while True:
                buffer = f.read(chunk_size)
                if not buffer:
                    break
                sha256hash.update(buffer)
        return sha256hash.hexdigest()

    def __len__(self):
        dtype = ("train" if self.train else "test")
        return len(self.data["data_{0}".format(dtype)])

    def __getitem__(self, idx):
        dtype = ("train" if self.train else "test")
        features = self.data["data_{0}".format(dtype)][idx]
        if dtype == "anatomy":
            features = features[:, 7503:]
        elif dtype == "fmri":
            features = features[:, :7503]
        label = self.data["label_{0}".format(dtype)][idx]
        if self.transform is not None:
            features = self.transform(features)
        return features, label


class FeatureExtractor(BaseEstimator, TransformerMixin):
    """ Make a transformer which will load the time series and compute the
    connectome matrix.
    """
    def __init__(self):
        self.transformer_fmri = make_pipeline(
            FunctionTransformer(func=_load_fmri, validate=False),
            ConnectivityMeasure(kind="tangent", vectorize=True))

    def fit(self, X_df, y, datadir):
        fmri_filenames = [path.replace(".", datadir, 1)
                          for path in X_df["fmri_basc122"]]
        self.transformer_fmri.fit(fmri_filenames, y)
        return self

    def transform(self, X_df, datadir):
        fmri_filenames = [path.replace(".", datadir, 1)
                          for path in X_df["fmri_basc122"]]
        X_connectome = self.transformer_fmri.transform(fmri_filenames)
        X_connectome = pd.DataFrame(X_connectome, index=X_df.index)
        X_connectome.columns = ["connectome_{0}".format(i)
                                for i in range(X_connectome.columns.size)]
        X_anatomy = X_df[[col for col in X_df.columns
                          if col.startswith("anatomy")]]
        X_anatomy = X_anatomy.drop(columns="anatomy_select")
        return pd.concat([X_connectome, X_anatomy], axis=1)


def _load_fmri(fmri_filenames):
    """ Load time-series extracted from the fMRI using a specific atlas.
    """
    return np.array([pd.read_csv(subject_filename,
                                 header=None).values
                     for subject_filename in fmri_filenames])
