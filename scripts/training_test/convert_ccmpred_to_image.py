#! /usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

import sys

if len(sys.argv) != 3:
    sys.exit('Usage: %s <coupling> <image_name>' % sys.argv[0])
print(sys.argv[1:])
coupling, image_name = sys.argv[1:]

matrix = np.loadtxt(coupling)
plt.imsave(image_name, matrix, cmap=plt.cm.gray_r)
