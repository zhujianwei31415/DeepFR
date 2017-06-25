#! /usr/bin/env python
#
# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import numpy as np


def main(raw_pdb_file, new_pdb_file):
    print('Reparing pdb %s ...' % raw_pdb_file)
    with open(new_pdb_file, 'w') as fout:
        with open(raw_pdb_file, 'r') as fin:
            for i in fin:
                if i[:4] != 'ATOM':
                    fout.write(i)
                    continue
                cols = list(i)
                if cols[21] == ' ':
                    cols[21] = 'A'
                fout.write(''.join(cols))

    
if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: %s <raw_pdb_file> <new_pdb_file>' % sys.argv[0])
    raw_pdb_file, new_pdb_file = sys.argv[1:]

    main(raw_pdb_file, new_pdb_file)
