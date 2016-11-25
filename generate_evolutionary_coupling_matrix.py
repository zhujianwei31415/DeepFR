#!/usr/bin/env python3

import os, sys
import argparse
import subprocess

from localconfig import *
from utils import *

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate evolutionary coupling matrix for protein fold recognition.", usage='%(prog)s <-i input_fasta_file> [options]' , add_help=False)
    
    input_args = parser.add_argument_group('Input arguments')
    input_args.add_argument('-i', '--input', metavar='<input_fasta_file>', type=open, help='input sequence fasta file')

    output_args = parser.add_argument_group('Output arguments')
    output_args.add_argument('--outdir', metavar='<output_dir>', help='output all results to directory')

    other_args = parser.add_argument_group('Other arguments')
    other_args.add_argument('-c', '--cpu', metavar='<number_of_cpus>', type=int, help='number of cpus, [default=%d]' % threads)
    other_args.add_argument('-h', '--help', action='help', help='show this help message and exit')
    other_args.add_argument('--version', action='version', version='%(prog)s 1.0')
    
    return parser.parse_args()

def check_dependencies():
    try:
        with open(os.devnull, 'w') as fout:
            subprocess.call([hhblits, '-h'], stderr=fout, stdout=fout)
            subprocess.call([ccmpred, '-h'], stderr=fout, stdout=fout)
    except:
        sys.exit('''
*****************
    ERROR!
*****************
%s -h
%s -h
Chosen binaries does not seem to work!
''' % (hhblits, ccmpred))

def check_hhblitsdb():
    if hhblitsdb.endswith('_a3m_db'):
        sys.exit('hhblitsdb can not end with _a3m_db, please delete the suffix')
    if not os.path.exists(hhblitsdb + '_a3m_db'):
        sys.exit('\n%s_a3m_db does not exist\n' % hhblitsdb)

def convert_a3m_to_aln(a3m_file, aln_file):
    lines = []
    with open(a3m_file, 'r') as fin:
        for line in fin:
            if line[0] == '>':
                continue
            lines.append(''.join([_ for _ in line if not _.islower()]))
    with open(aln_file, 'w') as fout:
        fout.writelines(lines)

def main(seqfile, threads=1, output_dir='./'):
    print('Generating evolutionary coupling matrix for %s ...' % seqfile)
    print('Testing Dependencies...')
    check_dependencies()
    print('Dependencies OK.')
    
    print('Checking databases...')
    check_hhblitsdb()
    print('Databases OK.')
    
    print('Checking output directory...')
    check_outdir(output_dir)
    
    print('Parsing sequence file...')
    seqname, target_info, sequence = parse_sequence_file(seqfile)
    prefix = output_dir + '/' + seqname
    seqfile = prefix + '.fasta'
    with open(seqfile, 'w') as fout:
        fout.write('%s\n%s\n' % (target_info, sequence))

    print('Generating a3m file by hhblits...')
    hhr_file = prefix + '.hhr'
    a3m_file = prefix + '.a3m'
    cmds = [hhblits, '-i', seqfile, '-d', hhblitsdb, '-n', str(HHBLITS_ITER), '-cpu', str(threads), '-oa3m', a3m_file, '-o', hhr_file]
    print_commands(cmds)
    subprocess.call(cmds)

    print('Converting a3m file to aln file...')
    aln_file = prefix + '.aln'
    convert_a3m_to_aln(a3m_file, aln_file)

    print('CCMpred from aln file...')
    ccm_file = prefix + '.ccm'
    cmds = [ccmpred, '-t', str(threads), aln_file, ccm_file]
    print_commands(cmds)
    subprocess.call(cmds)
    
    print('Generating evolutionary coupling matrix done.')

if __name__ == '__main__':
    args = parse_arguments()
    print('Parsing Parameters...')
    threads = args.cpu or threads
    output_dir = args.outdir or 'test'
    # check input file
    not args.input and not os.system(sys.argv[0] + ' -h') and sys.exit('\n\n\n!!!ERROR: Usage: %s -i <input_fasta_file>!!!\n\n\n' % sys.argv[0])
    seqfile = args.input.name
    print('Parameters OK.')
    
    # run hhpred
    main(seqfile, threads, output_dir);
