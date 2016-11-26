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

def generate_caffenet(prototxt, caffemodel):
    if not os.path.isfile(caffemodel) or not os.path.isfile(prototxt):
        print('cannot find caffemodel', file=sys.stderr)
        return None
    try:
        # set caffe mode
        caffe.set_mode_cpu()
        #caffe.set_mode_gpu()
        # load weights
        net = caffe.Net(prototxt, caffemodel, caffe.TEST)
    except:
        print('load caffenet failed', file=sys.stderr)
        return None
    return net

def create_transformer(net):
    # create transformer for the input called 'data'
    net.blobs['data'].reshape(1, 1, 227, 227)
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2,0,1))     # move image channels to outermost dimension
    transformer.set_raw_scale('data', 1)           # rescale from [0, 1] to [0, 255]
    #transformer.set_channel_swap('data', (2,1,0)) # swap channels from RGB to BGR
    return transformer

def extract_feature(net, transformer, image_path):
    image = caffe.io.load_image(image_path, color=False)
    image = caffe.io.resize_image(image, (256, 256))
    image = caffe.io.oversample([image], (227, 227))
    transformed_image = transformer.preprocess('data', image[0])
    net.blobs['data'].data[...] = transformed_image
    output = net.forward()        
    feature = net.blobs['fc7_bn'].data[0].copy()
    return feature

def extract_feature_list(net, transformer, file_list):
    features = []
    for i, v in enumerate(file_list):
        print('.', end='', file=sys.stderr)
        if not (i+1) % 100:
            print(i+1, file=sys.stderr)
        feature = extract_feature(net, transformer, v)
        features.append(feature)
    print(file=sys.stderr)
    return features

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
