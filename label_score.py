#! /usr/bin/env python
#
# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import numpy as np

from utils import parse_listfile

def parse_pairwise_score(pairwise_score):
    lines = parse_listfile(pairwise_score, [1, 2, 3])
    pairs, scores = [], []
    for i in lines:
        pairs.append((i[0], i[1]))
        scores.append(i[2])
    return pairs, scores

def parse_pair(pairlist):
    return parse_listfile(pairlist, [1, 2])

def main(lindahl_pairwise_score, lindahl_family, lindahl_superfamily, lindahl_fold):
    # score dict
    pairs, scores = parse_pairwise_score(lindahl_pairwise_score)

    # lindahl data
    lindahl_family = parse_pair(lindahl_family)
    lindahl_superfamily = parse_pair(lindahl_superfamily)
    lindahl_fold = parse_pair(lindahl_fold)
    assert len(lindahl_family) == 1646 and len(lindahl_superfamily) == 2130 and len(lindahl_fold) == 3662

    # label +1 or -1 for scores
    fout_family = open('family.txt', 'w')
    fout_superfamily = open('superfamily.txt', 'w')
    fout_fold = open('fold.txt', 'w')
    for i, p in enumerate(pairs):
        if not (i+1) % 100:
            print('.', end='', file=sys.stderr)
        if not (i+1) % 10000:
            print(i+1, file=sys.stderr)
        if p in lindahl_family:
            print('+1', scores[i], file=fout_family)
        elif p in lindahl_superfamily:
            print('+1', scores[i], file=fout_superfamily)
        elif p in lindahl_fold:
            print('+1', scores[i], file=fout_fold)
        else:
            print('-1', scores[i], file=fout_family)
            print('-1', scores[i], file=fout_superfamily)
            print('-1', scores[i], file=fout_fold)
    fout_family.close()
    fout_superfamily.close()
    fout_fold.close()
    
if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.exit('Usage: %s <lindahl_pairwise_score> <lindahl_family> <lindahl_superfamily> <lindahl_fold>' % sys.argv[0])
    lindahl_pairwise_score, lindahl_family, lindahl_superfamily, lindahl_fold = sys.argv[1:]
    main(lindahl_pairwise_score, lindahl_family, lindahl_superfamily, lindahl_fold)
