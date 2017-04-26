#! /usr/bin/env python
#
# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

if len(sys.argv) == 2:
    fin = open(sys.argv[1], 'r')
else:
    fin = sys.stdin

names = []
results = []
sens = []
for line in fin:
    if line[:3] == '../':
        names.append(line.split()[1])
        results.append(sens)
        sens = []
    elif line[:4] == 'Sens':
        cols = line.split()[1:3]
        sens += [float(i) for i in cols]
    else:
        pass
results.append(sens)
del results[0]
if len(sys.argv) == 2:
    fin.close()

# show results
for i, res in enumerate(results):
    print(names[i], end='\t')
    for j in res:
        print('%4.1f' % j, end=' ')
    print()
