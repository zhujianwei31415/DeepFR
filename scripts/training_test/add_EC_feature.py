#! /usr/bin/env python
#
# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import time
import numpy as np

from utils import *

def main(lindahl_scores, pairwise_feature, output_feature):
    print('Time Start ...')
    start = time.clock()

    # parse names
    scores = parse_listfile(lindahl_scores, [1, 2, 3])
    
    # generate scores dictory
    scoredict = {}
    for i, s in enumerate(scores):
        scoredict[(s[0], s[1])] = s[2]
    
    # add scores to the feature file
    lines = []
    with open(pairwise_feature, 'r') as fin:
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
            lines.append(line)
            p = tuple(line[1:-1].split())
            line = fin.readline().strip()
            lines.append('%s 85:%s\n' % (line, scoredict[p]))
        print(file=sys.stderr)

    # output new pairwise feature
    with open(output_feature, 'w') as fout:
        fout.writelines(lines)
    
    stop = time.clock()
    print('Time Spent =', stop - start)
   
if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit('Usage: %s <lindahl_scores> <pairwise_feature> <output_feature>' % sys.argv[0])
    print(sys.argv[1:])
    lindahl_scores, pairwise_feature, output_feature = sys.argv[1:]

    main(lindahl_scores, pairwise_feature, output_feature)
