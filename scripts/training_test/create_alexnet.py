#! /usr/bin/env python
#
# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)
import sys

from localconfig import caffe_root
sys.path.insert(0, caffe_root + 'python')
import caffe
from caffe import layers as L, params as P


def alexnet(train_data_source, test_data_source, train_batch_size=128, test_batch_size=50):
    n = caffe.NetSpec()

    n.data, n.label = L.ImageData(
            include=dict(phase=caffe.TRAIN),
            transform_param=dict(mirror=False, crop_size=227, scale=1./255),
            batch_size=train_batch_size,
            source=train_data_source,
            new_height=256,
            new_width=256,
            is_color=False,
            ntop=2)

    n.test_data, n.test_label = L.ImageData(
            include=dict(phase=caffe.TEST),
            transform_param=dict(mirror=False, crop_size=227, scale=1./255),
            batch_size=test_batch_size,
            source=test_data_source,
            new_height=256,
            new_width=256,
            is_color=False,
            name='data',
            top=['data', 'label'],
            in_place=True,
            ntop=2)

    n.conv1 = L.Convolution(n.data, name='conv1', num_output=96, kernel_size=7, stride=2, group=1,
                            weight_filler=dict(type='gaussian', std=0.01),
                            bias_filler=dict(type='constant', value=0),
                            param=[dict(lr_mult=1, decay_mult=1), dict(lr_mult=2, decay_mult=0)])
    n.conv1_bn = L.BatchNorm(n.conv1, eps=0)
    n.relu1 = L.ReLU(n.conv1_bn, in_place=True)
    n.pool1 = L.Pooling(n.relu1, kernel_size=3, stride=2, pool=P.Pooling.MAX)

    n.conv2 = L.Convolution(n.pool1, name='conv2', num_output=192, pad=1, kernel_size=5, stride=2, group=1,
                            weight_filler=dict(type='gaussian', std=0.01),
                            bias_filler=dict(type='constant', value=0),
                            param=[dict(lr_mult=1, decay_mult=1), dict(lr_mult=2, decay_mult=0)])
    n.conv2_bn = L.BatchNorm(n.conv2, eps=0)
    n.relu2 = L.ReLU(n.conv2_bn, in_place=True)
    n.pool2 = L.Pooling(n.relu2, kernel_size=3, stride=2, pool=P.Pooling.MAX)

    n.conv3 = L.Convolution(n.pool2, name='conv3', num_output=384, pad=1, kernel_size=3, stride=1, group=1,
                            weight_filler=dict(type='gaussian', std=0.01),
                            bias_filler=dict(type='constant', value=0),
                            param=[dict(lr_mult=1, decay_mult=1), dict(lr_mult=2, decay_mult=0)])
    n.conv3_bn = L.BatchNorm(n.conv3, eps=0)
    n.relu3 = L.ReLU(n.conv3_bn, in_place=True)

    n.conv4 = L.Convolution(n.relu3, name='conv4', num_output=384, pad=1, kernel_size=3, stride=1, group=1,
                            weight_filler=dict(type='gaussian', std=0.01),
                            bias_filler=dict(type='constant', value=0),
                            param=[dict(lr_mult=1, decay_mult=1), dict(lr_mult=2, decay_mult=0)])
    n.conv4_bn = L.BatchNorm(n.conv4, eps=0)
    n.relu4 = L.ReLU(n.conv4_bn, in_place=True)

    n.conv5 = L.Convolution(n.relu4, name='conv5', num_output=192, pad=1, kernel_size=3, stride=1, group=1,
                            weight_filler=dict(type='gaussian', std=0.01),
                            bias_filler=dict(type='constant', value=0),
                            param=[dict(lr_mult=1, decay_mult=1), dict(lr_mult=2, decay_mult=0)])
    n.conv5_bn = L.BatchNorm(n.conv5, eps=0)
    n.relu5 = L.ReLU(n.conv5_bn, in_place=True)
    n.pool5 = L.Pooling(n.relu5, kernel_size=3, stride=2, pool=P.Pooling.MAX)

    n.fc6 = L.InnerProduct(n.pool5, name='fc6', num_output=2048,
                           weight_filler=dict(type='gaussian', std=0.01),
                           bias_filler=dict(type='constant', value=0),
                           param=[dict(lr_mult=1, decay_mult=1), dict(lr_mult=2, decay_mult=0)])
    n.fc6_bn = L.BatchNorm(n.fc6, eps=0)
    n.relu6 = L.ReLU(n.fc6_bn, in_place=True)
    n.drop6 = L.Dropout(n.relu6, in_place=True)

    n.fc7 = L.InnerProduct(n.drop6, name='fc7', num_output=1024,
                           weight_filler=dict(type='gaussian', std=0.01),
                           bias_filler=dict(type='constant', value=0),
                           param=[dict(lr_mult=1, decay_mult=1), dict(lr_mult=2, decay_mult=0)])
    n.fc7_bn = L.BatchNorm(n.fc7, eps=0)
    n.relu7 = L.ReLU(n.fc7_bn, in_place=True)
    n.drop7 = L.Dropout(n.relu7, in_place=True)

    n.fc8 = L.InnerProduct(n.drop7, name='fc8', num_output=1221)

    n.accuracy = L.Accuracy(n.fc8, n.label, include=dict(phase=caffe.TEST))
    n.loss = L.SoftmaxWithLoss(n.fc8, n.label)

    return 'name: "AlexNet"\n' + str(n.to_proto())

def convert_to_deploy(prototxt):
    deploy_str = []
    tmp_str = []
    with open(prototxt, 'r') as fin:
        for i in fin:
            tmp_str.append(i)
            if i[0] == '}':
                for s in tmp_str:
                    if s[0] == ' ' and s[1] == ' ' and s[2] == 't' and s[3] == 'y':
                        tag = s.split('"')[1]
                if tag in ['Data', 'ImageData']:
                    for s in tmp_str:
                        if len(s) > 10 and s[:9] == '    phase' and s.split()[-1] == 'TEST':
                            tmp_str = []
                            break
                        if len(s) > 10 and s[:8] == '    crop':
                            length = s.split()[1]
                            tmp_str = [tmp_str[0], 'layer {\n', '  name: "data"\n', '  type: "Input"\n', '  top: "data"\n',
                                       '  input_param { shape: { dim: 1 dim: 1 dim: %s dim: %s } }\n' % (length, length), '}\n']
                elif tag == 'Accuracy':
                    tmp_str = []
                elif tag in ['SoftmaxWithLoss']:
                    tmp_str = ['layer {\n', '  name: "prob"\n', '  type: "Softmax"\n', '  bottom: "fc8"\n', '  top: "prob"\n', '}\n']
                else:
                    ss = []
                    start = False
                    for s in tmp_str:
                        if start:
                            if s[:5] == '    }':
                                start = False
                            else:
                                continue
                        elif len(s) > 10 and (s[:8] == '    weig' or s[:8] == '    bias'):
                            start = True
                        else:
                            ss.append(s)
                    tmp_str = ss
                deploy_str += tmp_str
                tmp_str = []
    return ''.join(deploy_str)

if __name__ == '__main__':
    train_test = 'train_test.prototxt'
    deploy = 'deploy.prototxt'
    
    net_spec_str = alexnet('train.txt', 'test.txt', train_batch_size=32, test_batch_size=16)
    with open(train_test, 'w') as f:
        f.write(net_spec_str)
        print(f.name)

    deploy_str = convert_to_deploy(train_test)
    with open(deploy, 'w') as f:
        f.write(deploy_str)
        print(f.name)
