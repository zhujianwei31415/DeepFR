# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# exception
import sys
if __name__ == '__main__':
    sys.exit('Please do not run me! Use xxx.py \n\n\tYours sincerely,\n\n\t %s' % sys.argv[0])

## HHblits configure
hhblits = '/home/zhujianwei/local/bin/hhblits'
hhblitsdb = '/home2/zhujianwei/databases/FALCON_databases/uniprot20.hhblitsdb/uniprot20'
HHBLITS_ITER = 5

## ccmpred configure
ccmpred = '/home/zhujianwei/local/bin/ccmpred'

# Maximum amount of cores to use per default
from multiprocessing import cpu_count
threads = cpu_count()

# caffe configure
caffe_root = '/home/zhujianwei/softwares/DeepLearning/caffe/'
