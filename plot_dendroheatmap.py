#!/usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Matthew Antalek Jr
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')


import numpy as np
import pydendroheatmap as pdh
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance as ssd

from utils import parse_listfile

def main(name_label_list, feature_file, image_name):
    print('Ploting dendroheatmap...')

    # read in names and labels
    names = [i[0] for i in parse_listfile(name_label_list, [1, 2])]
    labels = [i[1] for i in parse_listfile(name_label_list, [1, 2])]

    # read in features
    data = np.load(feature_file)

    # cluster the rows
    row_dist = ssd.squareform(ssd.pdist(data, 'cosine'))
    row_Z = sch.linkage(row_dist)
    row_idxing = sch.leaves_list(row_Z)
    row_labels = ['%s.%s' % (labels[i], names[i]) for i in row_idxing]

    # cluster the columns
    col_dist = ssd.squareform(ssd.pdist(data.T, 'cosine'))
    col_Z = sch.linkage(col_dist)
    col_idxing = sch.leaves_list(col_Z)

    # make the dendrogram
    data = data[:, col_idxing][row_idxing, :]
    #heatmap = pdh.DendroHeatMap(heat_map_data=data, left_dendrogram=row_Z, top_dendrogram=col_Z)
    heatmap = pdh.DendroHeatMap(heat_map_data=data, left_dendrogram=row_Z)
    heatmap.row_labels = row_labels
    heatmap.title = 'Feature dendroheatmap'
    heatmap.export(image_name)


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 4:
        sys.exit('Usage: %s <name_label_list> <feature_file(.npy)> <image_name(.eps)>' % sys.argv[0])
    name_label_list, feature_file, image_name = sys.argv[1:]
    main(name_label_list, feature_file, image_name)
