#! /usr/bin/env python
#
# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import sys
import time
import numpy as np

from utils import parse_listfile, parse_protein_id
from localconfig import caffe_root
sys.path.insert(0, caffe_root + 'python')
import caffe

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate evolutionary coupling matrix for protein fold recognition.", add_help=False)
    
    input_args = parser.add_argument_group('Input arguments')
    input_args.add_argument('-n', '--network', help='convolutional neural network', required=True)
    input_args.add_argument('-m', '--model', help='caffemodel', required=True)
    file_args = input_args.add_mutually_exclusive_group(required=True)
    file_args.add_argument('-i', '--input', metavar='<input_filename>', help='input a single file')
    file_args.add_argument('-l', '--list', metavar='<input_listfile>', help='input a list of files')

    output_args = parser.add_argument_group('Output arguments')
    output_args.add_argument('-o', '--output', metavar='<output_file>', help='output all features to a file [default=stdout]')

    other_args = parser.add_argument_group('Other arguments')
    other_args.add_argument('-h', '--help', action='help', help='show this help message and exit')
    other_args.add_argument('--version', action='version', version='%(prog)s 1.0')
    
    return parser.parse_args()

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
   
def extract_feature_list(net, transformer, filelist):
    features = []
    for i, v in enumerate(filelist):
        print('.', end='', file=sys.stderr)
        if not (i+1) % 100:
            print(i+1, file=sys.stderr)
        feature = extract_feature(net, transformer, v)
        features.append(feature)
    print(file=sys.stderr)
    return np.array(features)

if __name__ == '__main__':
    args = parse_arguments()
    print('Parsing Parameters...')
    prototxt = args.network
    caffemodel = args.model
    filename = args.input if args.input else args.list
    print(prototxt, caffemodel, filename)
    print('Parameters OK.')

    # check file
    if not os.path.exists(filename):
        sys.exit('ERROR: %s does not exist' % filename)

    # get filelist
    if args.input:
        filelist = [filename]
    else:
        filelist = [i[0] for i in parse_listfile(filename)]
    print(len(filelist))
    
    # check caffenet model
    net = generate_caffenet(prototxt, caffemodel)
    if not net:
        sys.exit('ERROR: cannot find CaffeNet model!')
    # create transformer
    transformer = create_transformer(net)
    
    # extract features
    features = extract_feature_list(net, transformer, filelist)

    # output features
    fout = open(args.output, 'w') if args.output else sys.stdout
    for f, feat in zip(filelist, features):
        print('>%s' % parse_protein_id(f), file=fout)
        for i in feat:
            print('%.8f' % i, end=' ', file=fout)
        print(file=fout)
    if args.output:
        fout.close()
