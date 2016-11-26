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
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib

def generate_X_y(pairs_file):
    X, y, pairs = [], [], []
    with open(pairs_file, 'r') as fin:
        i = 0
        while True:
            if not (i+1) % 100:
                print('.', end='', file=sys.stderr)
            if not (i+1) % 10000:
                print(i+1, file=sys.stderr)
            i += 1
            line = fin.readline()
            if not line:
                break
            if line[0] != '#':
                sys.exit('ERROR: wrong line!!!')
            pairs.append(line[1:-1])
            cols = fin.readline().split()
            X.append([float(_.split(':')[-1]) for _ in cols[1:]])
            y.append(1 if cols[0] == '+1' else 0)
        print(file=sys.stderr)
    return np.array(X), np.array(y), pairs

def main(train_pairs, test_pairs, model, output):
    start = time.clock()

    # generate features labels
    train_X, train_y, train_pairs = generate_X_y(train_pairs)
    print(train_X, file=sys.stderr)
    print(train_y, file=sys.stderr)
    print(train_X.shape, train_y.shape, file=sys.stderr)
    test_X, test_y, test_pairs = generate_X_y(test_pairs)
    print(test_X, file=sys.stderr)
    print(test_y, file=sys.stderr)
    print(test_X.shape, test_y.shape, file=sys.stderr)
    
    # random forest training
    rfc = RandomForestClassifier(n_estimators=307, n_jobs=-1)
    rfc.fit(train_X, train_y)
    
    # save and load back the pickled model
    joblib.dump(rfc, model)
    rfc = joblib.load(model) 

    # random forest test
    test_p = rfc.predict_proba(test_X)
    
    # output score
    with open(output, 'w') as fout:
        for i, p in enumerate(test_pairs):
            print(p, test_p[i, 1], file=fout)

    stop = time.clock()
    print('Time Spent =', stop - start)
   
if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.exit('Usage: %s <train_pairs> <test_pairs> <model> <output>' % sys.argv[0])
    print(sys.argv[1:])
    train_pairs, test_pairs, model, output = sys.argv[1:]

    main(train_pairs, test_pairs, model, output)
