import os, sys
import subprocess

def check_output(cmds):
    print(' '.join(cmds))
    return subprocess.Popen(cmds, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

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

def check_outdir(outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)

def print_commands(cmds):
    print(' '.join(cmds))
