#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import numpy as np

def parse_listfile(listfile, col_list=None):
    lines = []
    try:
        with open(listfile, 'r') as fin:
            if col_list:
                for line in fin:
                    cols = line.split()
                    lines.append(tuple(cols[i-1] for i in col_list))
            else:
                for line in fin:
                    lines.append(tuple(line.split()))
    except Exception as e:
        print('ERROR: wrong list file "%s"' % listfile, e, file=sys.stderr)
    return lines

def parse_pairwise_score(pairwise_score):
    lines = parse_listfile(pairwise_score, [1, 2, 3])
    pairs, scores = [], []
    for i in lines:
        pairs.append((i[0], i[1]))
        scores.append(float(i[2]))
    return pairs, scores

def parse_pair(pairlist):
    return parse_listfile(pairlist, [1, 2])

def get_top_indexs(scores):
    scores = np.array(scores)
    top_inds = np.argsort(scores)[::-1]
    # get top1
    top1 = list(top_inds[:1])
    for i in top_inds[1:]:
        if scores[i] == scores[top1[0]]:
            top1.append(i)
    # get top5
    top5 = list(top_inds[:5])
    for i in top_inds[5:]:
        if scores[i] == scores[top5[4]]:
            top5.append(i)
    assert len(top1) < 15 and len(top5) < 30
    return top1, top5

def main(lindahl_pairwise_score, lindahl_data):
    # score dict
    pairs, scores = parse_pairwise_score(lindahl_pairwise_score)
    score_dict = {}
    for i, p in enumerate(pairs):
        if p[0] not in score_dict:
            score_dict[p[0]] = []
        score_dict[p[0]].append((p, scores[i]))

    # lindahl data
    lindahl_pairs = parse_pair(lindahl_data)
    lindahl_names = []
    for i in lindahl_pairs:
        if i[0] not in lindahl_names:
            lindahl_names.append(i[0])
    #lindahl_names = list(set([i[0] for i in lindahl_pairs]))
    
    # calculte top1 top5
    top = [0, 0]
    for i in lindahl_names:
        tmp_scores = [s[1] for s in score_dict[i]]
        top1, top5 = get_top_indexs(tmp_scores)
        for k in top1:
            if score_dict[i][k][0] in lindahl_pairs:
                top[0] += 1
                break
        for k in top5:
            if score_dict[i][k][0] in lindahl_pairs:
                top[1] += 1
                break
    print('Test_number:', len(lindahl_names))
    print('Top_number:', top)
    print('Sensitivity:', '%4.1f %4.1f' % tuple([i/len(lindahl_names)*100 for i in top]))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: %s <lindahl_pairwise_score> <lindahl_data>' % sys.argv[0])
    lindahl_pairwise_score, lindahl_data = sys.argv[1:]
    main(lindahl_pairwise_score, lindahl_data)
