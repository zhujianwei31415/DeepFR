#!/usr/bin/env python3

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
        scores.append(i[2])
    return pairs, scores

def parse_pair(pairlist):
    return parse_listfile(pairlist, [1, 2])

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
    lindahl_names = list(set([i[0] for i in lindahl_pairs]))
    
    # calculte top1 top5
    top = [0, 0]
    for i in lindahl_names:
        tmp_scores = [s[1] for s in score_dict[i]]
        top_inds = np.argsort(tmp_scores)[::-1]
        if score_dict[i][top_inds[0]][0] in lindahl_pairs:
            top = [i + 1 for i in top]
        else:
            for k in top_inds[1:5]:
                if score_dict[i][k][0] in lindahl_pairs:
                    top[1] += 1
                    break
    print('Test_number:', len(lindahl_names))
    print('Top_number:', top)
    print('Sensitivity:', [i/len(lindahl_names) for i in top])

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: %s <lindahl_pairwise_score> <lindahl_data>' % sys.argv[0])
    lindahl_pairwise_score, lindahl_data = sys.argv[1:]
    main(lindahl_pairwise_score, lindahl_data)
