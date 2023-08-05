# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2021
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
Create the Single-Cell RNA-Sequencing dataset derived from H. M. Kang, et al.,
Multiplexed droplet single-cell rna-sequencing using natural genetic
variation, Nature biotechnology, 2018.
"""

# Imports
import os
import subprocess
import requests
import numpy as np
import pandas as pd
import anndata
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset


class SingleCellRNASeqDataset(Dataset):
    """ Create the Single-Cell RNA-Sequencing dataset.
    """
    url_data = ("https://docs.google.com/uc?export=download&id=1-N7wPpYUf_"
                "QcG5566WVZlaxVC90M7NNE")
    url_gt = ("https://public.bmi.inf.ethz.ch/projects/2020/pmvae/"
              "kang_recons.h5ad")
    url_gmt = ("https://raw.githubusercontent.com/ratschlab/pmvae/main/data/"
               "c2.cp.reactome.v4.0.symbols.gmt")

    def __init__(self, root, train=True, transform=None, seed=None):
        """ Init class.

        Parameters
        ----------
        root: str
            root directory of dataset where the data will be saved.
        train: bool, default True
            specifies training or test dataset.
        transform: callable, default None
            optional transform to be applied on a sample.
        seed: int, default None
            controls the shuffling applied to the data before applying the
            split.
        """
        super(SingleCellRNASeqDataset).__init__()
        self.root = root
        self.train = train
        self.transform = transform
        self.seed = seed
        self.data_file = os.path.join(root, "single_cell_rna_sequencing.npz")
        self.download()
        self.data = np.load(self.data_file, mmap_mode="r")
        trainset, testset = train_test_split(
            self.data["X"], test_size=0.25, shuffle=True, random_state=seed)
        if self.train:
            self.X = trainset
        else:
            self.X = testset

    def download(self):
        """ Download data.
        """
        if not os.path.isfile(self.data_file):

            # Download data
            origdatapath = os.path.join(self.root, "orig_kang_count.h5ad")
            datapath = os.path.join(self.root, "kang_count.h5ad")
            gtpath = os.path.join(self.root, "kang_recons.h5ad")
            gmtpath = os.path.join(
                self.root, "c2.cp.reactome.v4.0.symbols.gmt")
            if not os.path.isfile(origdatapath):
                cmd = ["wget", "--no-check-certificate", self.url_data, "-O",
                       origdatapath]
                subprocess.check_call(cmd)
            if not os.path.isfile(datapath):
                data = anndata.read(origdatapath)
                data.obs = data.obs[["condition", "cell_type"]]
                data.uns = dict()
                data.obsm = None
                data.varm = None
                data.write(datapath)
            if not os.path.isfile(gtpath):
                cmd = ["wget", self.url_gt, "-O", gtpath]
                subprocess.check_call(cmd)
            if not os.path.isfile(gmtpath):
                response = requests.get(self.url_gmt)
                with open(gmtpath, "wt") as open_file:
                    open_file.write(response.text)

            # Build dataset
            data = anndata.read(datapath)
            data.varm["annotations"] = load_annotations(
                gmtpath, data.var_names, min_genes=13)
            membership_mask = data.varm["annotations"].astype(bool).T
            dataset = {
                "X": data.X,
                "membership_mask": membership_mask.to_numpy(),
                "obs_names": data.obs_names.to_numpy(),
                "var_names": data.var_names.to_numpy(),
                "obs": data.obs.to_numpy(),
                "annotations": data.varm["annotations"].to_numpy()}

            # Save dataset
            np.savez(self.data_file, **dataset)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        data = self.X[idx]
        if self.transform is not None:
            data = self.transform(data)
        return data


def load_annotations(gmt, genes, min_genes=10):
    genesets = parse_gmt(gmt, genes, min_genes)
    annotations = pd.DataFrame(False, index=genes, columns=genesets.keys())
    for key, genes in genesets.items():
        annotations.loc[genes, key] = True
    return annotations


def parse_gmt(path, symbols=None, min_genes=10):
    lut = dict()
    with open(path, "r") as of:
        for line in of.readlines():
            key, _, *genes = line.strip().split()
            if symbols is not None:
                genes = symbols.intersection(genes).tolist()
            if len(genes) < min_genes:
                continue
            lut[key] = genes
    return lut
