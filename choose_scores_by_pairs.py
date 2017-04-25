#!/usr/bin/env python3
# coding: utf-8

import sys

if len(sys.argv) != 3:
    sys.exit('Usage: %s <lindahl_scores> <pairs>' % sys.argv[0])

tmp_dict = {}
with open(sys.argv[1], 'r') as fin:
    for i in fin:
        cols = i.split()
        tmp_dict[(cols[0], cols[1])] = cols[2]

with open(sys.argv[2] , 'r') as fin:
    for i in fin:
        cols = i.split()
        #print(cols[0], cols[1], tmp_dict[(cols[0], cols[1])])
        print(tmp_dict[(cols[0], cols[1])])
