#! /usr/bin/env python
#
# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
import os
import sys

SHAPE = (256, 256)
CUTOFF = 10


def parse_protein_id(filename):
    #filename = "/tmp/d1a3aa_"
    #filename = "/tmp/d1a3aa_.fasta"
    name = filename.split('/')[-1]
    protein_id = '.'.join(name.split('.')[:-1]) or name
    return protein_id


def sample_matrix(matrix):
    new_matrix = np.zeros(SHAPE)
    nums = np.random.choice(matrix.shape[0], SHAPE[0], replace=False)
    nums.sort()

    return matrix[np.ix_(nums, nums)] # equal to matrix[nums,:][:, nums]


def pad_matrix(matrix):
    new_matrix = np.zeros(SHAPE)
    start = np.random.randint(0, SHAPE[0] - matrix.shape[0])
    end = start + matrix.shape[0]
    new_matrix[start:end, start:end] = matrix
    
    return new_matrix


def sample_or_pad_matrix(matrix):
    # check data
    assert matrix.shape[0] == matrix.shape[1]

    # calculate random choose times
    num = abs(SHAPE[0] - matrix.shape[0])
    times = int(num // CUTOFF) + 1 # add pseudo-count 1

    # sample or pad matrix
    if matrix.shape[0] < SHAPE[0]:
        return [pad_matrix(matrix) for _ in range(times)]
    else:
        return [sample_matrix(matrix) for _ in range(times)]


def main(ccmpred_output, outdir):
    # parse name
    name = parse_protein_id(ccmpred_output)

    # load ccmpred outfile
    ccm_mat = np.loadtxt(ccmpred_output)

    # for debug
    #np.random.seed(31415)

    # sample or pad matrix
    fix_mat = sample_or_pad_matrix(ccm_mat)
    assert isinstance(fix_mat, list)

    # check output directory
    outdir = os.path.abspath(outdir)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # save file
    list_file = '%s/%s.list' % (outdir, name)
    print('>%s' % name, ccm_mat.shape, SHAPE, len(fix_mat))
    with open(list_file, 'w') as fout:
        for i, mat in enumerate(fix_mat):
            image_name = '%s/%s.%02d.jpg' % (outdir, name, i)
            print(image_name, file=fout)
            plt.imsave(image_name, mat, cmap=plt.cm.gray_r)




if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: %s <ccmpred_output> <outdir>' % sys.argv[0])
    ccmpred_output, outdir = sys.argv[1:]

    main(ccmpred_output, outdir)
