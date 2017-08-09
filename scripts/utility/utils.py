# Copyright
# Author: zhujianwei@ict.ac.cn (Jianwei Zhu)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os, sys
import subprocess

# exception
if __name__ == '__main__':
    sys.exit('Please do not run me! Use xxx.py \n\n\tYours sincerely,\n\n\t %s' % sys.argv[0])

# print a command to stdout
def print_commands(cmds):
    print(' '.join(cmds))

# exculate a command and get output
def check_output(cmds):
    print(' '.join(cmds))
    return subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

# parse list file for some columns
def parse_listfile(listfile, col_list=None):
    lines = []
    try:
        with open(listfile, 'r') as fin:
            if col_list:
                for line in fin:
                    cols = line.split()
                    lines.append(tuple(cols[i-1] for i in col_list))
            else:
                for line in fin:
                    lines.append(tuple(line.split()))
    except Exception as e:
        print('ERROR: wrong list file "%s"\n      ' % listfile, e, file=sys.stderr)
    return lines

# parse sequence file
def parse_sequence_file(seqfile):
    # check file exists
    if not os.path.exists(seqfile):
        sys.exit('\n\n\n!!!ERROR: can not find sequence file: %s!!!\n\n\n' % seqfile)
    # get sequence fasta file target name
    seqname = seqfile.split('/')[-1]
    seqname = '.'.join(seqname.split('.')[:-1]) or seqname   
    # check sequence fsta format
    with open(seqfile, 'r') as fin:
        target_info = fin.readline().rstrip('\n')
        if target_info[0] != '>':
            sys.exit('!!!ERROR: wrong fasta file without label(>): %s!!!' % seqfile)
        sequence = ''.join([_.rstrip('\n') for _ in fin])
    return seqname, target_info, sequence

# check ouput directory
def check_outdir(outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)
