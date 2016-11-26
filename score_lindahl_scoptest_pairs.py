#! /usr/bin/env python
#
# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, sys
import time
import numpy as np
import scipy.spatial.distance as distance

from localconfig import caffe_root
sys.path.insert(0, caffe_root + 'python')
import caffe

from utils import parse_listfile
from extract_feature import *

def calculate_similarity(feature1, feature2):
    return 1 - distance.cosine(feature1, feature2)

def main(prototxt, caffemodel, list_names, input_dir, score_file):
    start = time.clock()
    # parse files
    names = [i[0] for i in parse_listfile(list_names, [1])]
    files = ['%s/%s.jpg' % (input_dir, i) for i in names]
    #for i, name in enumerate(names):
    #    print(name, files[i])
    # parse pairs
    pairs = [(i, j) for i in names for j in names if i != j]
    #for i in pairs:
    #    print(i)
    
    # check caffenet model
    net = generate_caffenet(prototxt, caffemodel)
    if not net:
        sys.exit('ERROR: cannot find CaffeNet model!')
    # create transformer
    transformer = create_transformer(net)
    features = extract_feature_list(net, transformer, files)
    #np.save('features', features)
    # test show
    #features = np.load('features.npy')
    np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
    print(features)
    print(features.shape, len(files))
    
    # generate features dictory
    featdict = {}
    for i, na in enumerate(names):
        featdict[na] = features[i]

    # calculate similarity for each pair
    with open(score_file, 'w') as fout:
        for i, p in enumerate(pairs):
            if not (i+1) % 100:
                print('.', end='', file=sys.stderr)
            if not (i+1) % 10000:
                print(i+1, file=sys.stderr)
            if p[0] not in names or p[1] not in names:
                print('\n\n\nERROR: pairs does not exist on file\n\n\n', file=sys.stderr)
                return
            sim = calculate_similarity(featdict[p[0]], featdict[p[1]])
            print(p[0], p[1], sim, file=fout)
        print(file=sys.stderr)
    
    stop = time.clock()
    print('Time Spent =', stop - start)
   
if __name__ == '__main__':
    if len(sys.argv) != 6:
        sys.exit('Usage: %s <prototxt> <caffemodel> <list_names> <input_dir> <score_file>' % sys.argv[0])
    print(sys.argv[1:])
    prototxt, caffemodel, list_names, input_dir, score_file = sys.argv[1:]

    main(prototxt, caffemodel, list_names, input_dir, score_file)
