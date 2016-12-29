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

from utils import parse_listfile

def calculate_similarity(feature1, feature2):
    return 1 - distance.cosine(feature1, feature2)

def main(namelabellist, featurelist, feature_file, output_score):
    print('Starting and timing...')
    start = time.clock()

    print('Parsing names and labels...')
    names, labels = [], []
    for n, l in parse_listfile(namelabellist):
        names.append(n)
        labels.append(l)
    #for i, n in enumerate(names):
    #    print(n, labels[i])

    print('Loading template features...')
    features = np.load(featurelist)
    assert features.shape == (len(names), 1024)
    np.set_printoptions(precision=3, suppress=True)
    print(features)
    print(features.shape, len(names), len(labels))
    
    print('Reading target feature...')
    feature = np.loadtxt(feature_file)
    print(feature.shape, feature)
    
    print("Running fold recognition...")
    scores = []
    for feat in features:
        scores.append(calculate_similarity(feature, feat))
    # write to file
    with open(output_score, 'w') as fout:
        for i, f in enumerate(names):
            print('%7s %10.8f %s' % (f, scores[i], labels[i]), file=fout)

    stop = time.clock()
    print('Time Spent =', stop - start)
   
if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.exit('Usage: %s <namelabellist> <featurelist> <feature_file> <output_score>' % sys.argv[0])
    print(sys.argv[1:])
    namelabellist, featurelist, feature_file, output_score = sys.argv[1:]

    main(namelabellist, featurelist, feature_file, output_score)
