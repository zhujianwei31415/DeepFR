#!/usr/bin/env python

import sys

if len(sys.argv) != 3:
    sys.exit('%s <results_dir> <level(family, superfamily, fold)>' % sys.argv[0])
results_dir = sys.argv[1]
level = sys.argv[2]

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

# read in score function
def read_spec_sens(score_file):
    spec, sens = [], []
    with open(score_file, 'r') as fin:
        for line in fin:
            cols = line.split()
            spec.append(float(cols[0]))
            sens.append(float(cols[1]))
    return np.array(spec), np.array(sens)

# read in score
# setup colors
colors = ['red', 'blue', 'green', 'gold', 'maroon', 'purple', 'black', 'c', 'm']
names = ['DeepFRpro', 'DeepFR', 'RFDN-Fold', 'DN-Fold', 'DN-FoldS', 'RF-Fold', 'FOLDpro', 'HMMER', 'THREADER']
files = ['%s/%s/spec-sens-%s' % (results_dir, i, level) for i in names]

# Binarize the output
n_classes = len(files)

# Compute Precision-Recall and plot curve
precision = dict()
recall = dict()
for i in range(n_classes):
    precision[i], recall[i] = read_spec_sens(files[i])

## filter by threshold
#threshold=0.01
#for i in range(n_classes):
#    precision[i][recall[i]<threshold] = 1
#    recall[i][recall[i]<threshold] = 0

# Turn interactive plotting off
plt.ioff()

# set figure
plt.figure(figsize=(16, 16), dpi=100)

# Plot Precision-Recall curve for each class
for i, color in zip(range(n_classes), colors):
    if i < 2:
        plt.plot(precision[i], recall[i], color=color, lw=3, label='{0}'.format(names[i]))
    else:
        plt.plot(precision[i], recall[i], color=color, lw=2, label='{0}'.format(names[i]))

plt.xticks(fontsize=24)
plt.yticks(fontsize=24)
plt.xlim([0, 1.05])
plt.ylim([-0.05, 1])
plt.xlabel('Specificity', fontsize=24)
plt.ylabel('Sensitivity', fontsize=24)
#plt.title('Specificity-Sensitivity curve to multi-class')
plt.legend(loc="upper right", fontsize=16)
plt.grid()
#plt.show()
plt.savefig('%s.eps' % level, format='eps', bbox_inches='tight')
