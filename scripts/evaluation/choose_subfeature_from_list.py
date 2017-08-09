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

from utils import parse_listfile

def parse_namelabellist(namelabellist):
    names, labels = [], []
    for n, l in parse_listfile(namelabellist, [1, 2]):
        names.append(n)
        labels.append(l)
    return names, labels

def main(namelabellist, featurelist, sublist):
    print('Starting and timing...')
    start = time.clock()
    
    print('Parsing namelabellist...')
    names, labels = parse_namelabellist(namelabellist)
    #for i, f in enumerate(names):
    #    print(f, labels[i])
    
    print('Loading template features...')
    features = np.load(featurelist)
    assert features.shape == (len(names), 1024)
    np.set_printoptions(precision=3, suppress=True)
    print(features)
    print(features.shape)

    print('Parsing sublist...')
    subnames, sublabels = parse_namelabellist(sublist)
    #for i, f in enumerate(subnames):
    #    print(f, sublabels[i])

    print('Extracing subfeatures for sublist...')
    subfeatures = []
    for i, f in enumerate(subnames):
        subfeatures.append(features[names.index(f)])
    subfeatures = np.array(subfeatures)
    print(subfeatures)
    print(subfeatures.shape)
    np.save('subfeatures', subfeatures)
    np.savetxt('subfeatures', subfeatures)

    stop = time.clock()
    print('Time Spent =', stop - start)
   
if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit('Usage: %s <namelabellist> <featurelist> <sublist>' % sys.argv[0])
    print(sys.argv[1:])
    namelabellist, featurelist, sublist = sys.argv[1:]

    main(namelabellist, featurelist, sublist)
