#!/bin/bash

if [ $# != 1 ]
then
  echo "Usage: $0 <db_fasta>"
  exit
fi

db_fasta=$1

mmseqs createdb $db_fasta DB

mkdir tmp

#mmseqs cluster DB clu tmp --min-seq-id 0.95
mmseqs cluster DB clu tmp --min-seq-id 0.40

mmseqs createseqfiledb DB clu clu_seq 

mmseqs result2flat DB DB clu_seq clu_seq.fasta

mmseqs createtsv DB DB clu clu.tsv

rm -rf tmp
