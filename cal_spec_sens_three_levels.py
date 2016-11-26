#! /usr/bin/env python
#
# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import sys
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import average_precision_score

# read in score function
def read_score(score_file):
    labels, values = [], []
    with open(score_file, 'r') as fin:
        for line in fin:
            cols = line.split()
            labels.append(0 if cols[0] == '-1' else 1)
            values.append(float(cols[1]))
    return np.array(labels), np.array(values)

# calculate specificity and sensitivity
def cal_spec_sens(y_test, y_score):
    spec, sens, _ = precision_recall_curve(y_test, y_score)
    return spec, sens

# write specificity and sensitivity
def write_spect_sens(spec, sens, outfile):
    with open(outfile, 'w') as fout:
        for j, _ in enumerate(spec):
            print('%10.8f  %10.8f' % (spec[j], sens[j]), file=fout)

def main(family_score, superfamily_score, fold_score):
    # calculate family level
    y_test, y_score = read_score(family_score)
    spec, sens = cal_spec_sens(y_test, y_score)
    write_spect_sens(spec, sens, 'fam.txt')
    # calculate superfamily level
    y_test, y_score = read_score(superfamily_score)
    spec, sens = cal_spec_sens(y_test, y_score)
    write_spect_sens(spec, sens, 'super.txt')
    # calculate fold level
    y_test, y_score = read_score(fold_score)
    spec, sens = cal_spec_sens(y_test, y_score)
    write_spect_sens(spec, sens, 'fold.txt')

if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit('Usage: %s <family_score> <superfamily_score> <fold_score>' % sys.argv[0])
    family_score, superfamily_score, fold_score = sys.argv[1:]
    
    main(family_score, superfamily_score, fold_score)
