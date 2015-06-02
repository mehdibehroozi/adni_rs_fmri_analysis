# -*- coding: utf-8 -*-
"""
Created on Thu May 28 10:52:46 2015

@author: mehdi.rahim@cea.fr
"""
import os, sys
import numpy as np
from fetch_data import fetch_adni_baseline_rs_fmri, fetch_adni_masks, \
                        fetch_adni_longitudinal_rs_fmri, set_cache_base_dir
from base_connectivity_classifier import ConnectivityClassifier

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 0)


CACHE_DIR = set_cache_base_dir()

#dataset = fetch_adni_baseline_rs_fmri()
dataset = fetch_adni_longitudinal_rs_fmri()
mask = fetch_adni_masks()['mask_petmr']


atlas_names = ['msdl', 'canica141', 'canica', 'mayo',
               'harvard_oxford', 'juelich', 'tvmsdl']
atlas_names = ['msdl']

for atlas_name in atlas_names:
    print atlas_name
    #conn_names = ['gl', 'lw', 'oas', 'scov']
    conn_names = ['lw']
    for conn_name in conn_names:
        all_groups = [['AD', 'MCI'], ['AD', 'Normal'], ['MCI', 'Normal']]
    for groups in all_groups:
        connclassif = ConnectivityClassifier(dataset.func, mask,
                                             atlas=atlas_name,
                                             dx_group=dataset.dx_group,
                                             n_jobs=-1)
        connclassif.compute_connectivity(conn_name)
        classifier_names = ['ridge', 'svc_l1', 'svc_l2',
                            'logreg_l1', 'logreg_l2']
        for classifier_name in classifier_names:
            connclassif.classify(dataset=dataset,
                                 groups=groups,
                                 classifier_name=classifier_name)
            output_folder = os.path.join(CACHE_DIR,
                                         '_'.join(['conn', atlas_name]))
            if not os.path.isdir(output_folder):
                os.mkdir(output_folder)
            output_file = os.path.join(output_folder,
                                       '_'.join([groups[0], groups[1],
                                                 atlas_name, conn_name,
                                                 classifier_name]))
            np.savez_compressed(output_file, data=connclassif.scores_)

