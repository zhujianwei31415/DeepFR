#!/usr/bin/env python

from __future__ import print_function

import random
import sys

if len(sys.argv) != 3:
    sys.exit('Usage: %s <fasta_file> <name_list>' % sys.argv[0])
fasta_file, name_list = sys.argv[1:]

with open(name_list, 'r') as fin:
    names_chosen = [_.strip() for _ in fin]
names_chosen = set(names_chosen)

def parse_scop_fasta(filename):
    names, sequences = [], []
    try:
        with open(filename, 'r') as fin:
            for line in fin:
                line = line.rstrip('\n')
                if line[0] == '>':
                    names.append(line)
                    sequences.append([])
                else:
                    sequences[-1].append(line)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
    # test show
    #for i, name in enumerate(names):
    #    print(name)
    #    for seq in sequences[i]:
    #        print(seq)
    return names, [''.join(seq).upper() for seq in sequences]

names, sequences = parse_scop_fasta(fasta_file)

include, exclude = [], []
for i, nam in enumerate(names):
    if nam[1:8] in names_chosen:
        include.append(i)
    else:
        exclude.append(i)
print(len(include), len(exclude))

#random.shuffle(include)
with open('include.fa', 'w') as fout:
    for i in include:
        print(names[i], file=fout)
        print(sequences[i], file=fout)

#random.shuffle(exclude)
with open('exclude.fa', 'w') as fout:
    for i in exclude:
        print(names[i], file=fout)
        print(sequences[i], file=fout)
