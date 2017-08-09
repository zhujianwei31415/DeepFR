#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

if len(sys.argv) != 3:
    sys.exit('Usage: %s <lindahl_scores> <pairs>' % sys.argv[0])

tmp_dict = {}
with open(sys.argv[1], 'r') as fin:
    for i in fin:
        cols = i.split()
        tmp_dict[(cols[0], cols[1])] = i.strip()

with open(sys.argv[2] , 'r') as fin:
    for i in fin:
        cols = i.split()
        print(tmp_dict[(cols[0], cols[1])])
