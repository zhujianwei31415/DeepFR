#! /usr/bin/env python
#
# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) != 3:
    sys.exit('Usage: %s <coupling> <image_name>' % sys.argv[0])
print(sys.argv[1:])
coupling, image_name = sys.argv[1:]

matrix = np.loadtxt(coupling)
plt.imsave(image_name, matrix, cmap=plt.cm.gray_r)
