#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys

# check biopython module
try:
    from Bio.PDB import PDBParser
    from Bio.PDB.DSSP import DSSP
    from Bio import SeqIO
except ImportError:
    raise SystemExit('Install biopython module if you want to use this script.')


def calculate_distance(chain):
    dist = []
    for res1 in chain:
        c1 = res1['CB'] if 'CB' in res1 else res1['CA']
        tmp_dist = []
        for res2 in chain:
            c2 = res2['CB'] if 'CB' in res2 else res2['CA']
            tmp_dist.append(c1 - c2)
        dist.append(tmp_dist)
    return np.matrix(dist)


def distance_to_contact(dist):
    contact = np.matrix(np.zeros(dist.shape)) 
    contact[dist>8.0] = 0
    contact[dist<=8.0] = 1
    contact -= np.matrix(np.eye(dist.shape[0]))
    return contact


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('Usage: %s <pdbfile> <image_name>' % sys.argv[0])
    print(sys.argv[1:])
    pdb, image_name = sys.argv[1:]

    print('Loading pdb file %s ...' % pdb)
    p = PDBParser(PERMISSIVE=1)
    structure = p.get_structure('', pdb)
    model = structure[0]
    assert len(model) == 1
    chain = model.get_list()[0]

    print('Calculating distance ...')
    dist = calculate_distance(chain) 
    print(dist)

    contacts = distance_to_contact(dist)
    #np.savetxt('tmp.con', contacts, fmt='%1d')

    plt.imsave(image_name, contacts, cmap=plt.cm.gray_r)
