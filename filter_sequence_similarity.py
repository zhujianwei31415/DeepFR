#! /usr/bin/env python
#
# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os
import subprocess
import sys

from localconfig import *
from utils import *

def parse_arguments():
    parser = argparse.ArgumentParser(description="Filter sequence from databases.", usage='%(prog)s <-i input_fasta_file> [options]' , add_help=False)
    
    input_args = parser.add_argument_group('Input arguments')
    file_args = input_args.add_mutually_exclusive_group(required=True)
    file_args.add_argument('-i', '--input', metavar='<input_filename>', help='input a single file')
    file_args.add_argument('-l', '--list', metavar='<input_listfile>', help='input a list of files')

    output_args = parser.add_argument_group('Output arguments')
    output_args.add_argument('-o', '--output', metavar='<output_file>', help='output all features to a file [default=stdout]')

    other_args = parser.add_argument_group('Other arguments')
    other_args.add_argument('-h', '--help', action='help', help='show this help message and exit')
    other_args.add_argument('--version', action='version', version='%(prog)s 1.0')
    
    return parser.parse_args()

def check_dependencies():
    try:
        with open(os.devnull, 'w') as fout:
            subprocess.call([fasta, '-h'], stderr=fout, stdout=fout)
    except:
        sys.exit('''
*****************
    ERROR!
*****************
%s -h
Chosen binaries does not seem to work!
''' % (fasta))

def check_fastadb():
    if not os.path.exists(fastadb):
        sys.exit('\n%s_a3m_db does not exist\n' % fastadb)

def filter_sequence_signle(filename, threshold=40.0):
    # filter using fasta
    cmds = [fasta, filename, fastadb]
    out = check_output(cmds)
    sims = []
    for l in out.split('\n'):
        if l[:2] == '>>':
            name = l.split()[0][2:]
        elif l[:5] == 'Smith':
            sim = float(l.split()[3][:-1])
            if sim > threshold:
                sims.append((name, sim))
    return sims

def filter_sequence_list(filelist, threshold=40.0):
    sims = []
    for f in filelist:
        sims.append(filter_sequence_signle(f, threshold))
    return sims

def main(filename, single=True, fout=sys.stdout):
    print('Filtering sequence similarity ...')
    print('Testing Dependencies...')
    check_dependencies()
    print('Dependencies OK.')
    
    print('Checking databases...')
    check_fastadb()
    print('Databases OK.')

    # check input file and get filelist
    if single:
        filelist = [filename]
    else:
        filelist = [i[0] for i in parse_listfile(filename)]

    sims = filter_sequence_list(filelist)

    for i, f in enumerate(filelist):
        for p in sims[i]:
            print(f, p[0], p[1])
        
    print('Filter done.')

if __name__ == '__main__':
    args = parse_arguments()
    print('Parsing Parameters...')
    filename = args.input if args.input else args.list
    print('Parameters OK.')
    
    if args.output:
        with open(args.output, 'w') as fout:
            main(filename, args.input, fout)
    else:
        main(filename, args.input)
