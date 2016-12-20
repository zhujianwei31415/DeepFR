#!/bin/bash

if [ $# != 2 ]
then
  echo "Usage: $0 <query_fasta> <target_fasta>"
  exit
fi

query_fasta=$1
target_fasta=$2

mmseqs createdb $query_fasta queryDB

mmseqs createdb $target_fasta targetDB

mmseqs createindex targetDB

rm -rf resultDB*

mkdir tmp

mmseqs search queryDB targetDB resultDB tmp --max-seq-id 1.0 --min-seq-id 0.95

mmseqs convertalis queryDB targetDB resultDB resultDB.m8

rm -rf tmp
