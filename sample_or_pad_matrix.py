#! /usr/bin/env python
#
# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import numpy as np

def sample_or_pad_matrix(matrix, shape):
    # check data
    m, n = matrix.shape
    assert m == n and shape[0] == shape[1]
    # sample or pad matrix
    new_matrix = np.zeros(shape)
    if m <= shape[0]:
        new_matrix[:m, :n] = matrix
    else:
        nums = np.random.choice(m, shape[0], replace=False)
        nums.sort()
        new_matrix = matrix[np.ix_(nums, nums)] # equal to matrix[nums,:][:, nums]
    return new_matrix

def normalize_matrix(matrix):
    # matrix normalization [0, 1]
    matrix[matrix<0] = .0
    matrix *= 1.0/matrix.max()
    return matrix

def main(input_matrix, matrix_shape, output_matrix):
    print('Sampling or padding ccm to fixed size...')
    shape = tuple([int(i) for i in matrix_shape.split('x')])
    ccm_mat = np.loadtxt(input_matrix)
    print(ccm_mat.shape)
    #np.random.seed(123456)
    fix_mat = sample_or_pad_matrix(ccm_mat, shape)
    fix_mat = normalize_matrix(fix_mat)
    print(fix_mat.shape)
    np.savetxt(output_matrix, fix_mat)
    print('Sample or pad matrix done.')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit('Usage: %s <input_matrix> <matrix_shape(default: 256x256)> <output_matrix>' % sys.argv[0])
    #print(sys.argv[1:])
    input_matrix, matrix_shape, output_matrix = sys.argv[1:]

    # run hhpred
    main(input_matrix, matrix_shape, output_matrix)
