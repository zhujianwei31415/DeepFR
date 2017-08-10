#! /usr/bin/env python
#
# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import time

import numpy as np
import scipy.spatial.distance as distance

try:
    import cPickle as pickle
except:
    import pickle

from utils import parse_listfile




def calculate_similarity(feature1, feature2):
    return 1 - distance.cosine(feature1, feature2)


def read_single_feature(query_feature):
    features = []
    with open(query_feature, 'r') as fin:
        for i in fin:
            if i[0] == '>': continue
            features.append([float(_) for _ in i.split()])
    features = np.array(features)

    return np.mean(features, axis = 0)


def main(label_dict, feature_dict, query_feature, output_score):
    print('Starting and timing...')
    start = time.clock()

    print('Parsing names and labels...')
    with open(label_dict, 'r') as fin:
        labeldict = pickle.load(fin)
    print(len(labeldict))

    print('Loading template features...')
    with open(feature_dict, 'r') as fin:
        featdict = pickle.load(fin)
    print(len(featdict))
    
    print('Reading target feature...')
    feature = read_single_feature(query_feature)
    print(feature.shape, feature)

    print("Running fold recognition...")
    with open(output_score, 'w') as fout:
        for na, feat in featdict.items():
            score = calculate_similarity(feature, feat)
            print('%7s %10.8f %s' % (na, score, labeldict[na]), file=fout)

    stop = time.clock()
    print('Time Spent =', stop - start)
   
if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.exit('Usage: %s <label_dict> <feature_dict> <query_feature> <output_score>' % sys.argv[0])
    print(sys.argv[1:])
    label_dict, feature_dict, query_feature, output_score = sys.argv[1:]

    main(label_dict, feature_dict, query_feature, output_score)
