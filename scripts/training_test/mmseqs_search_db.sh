#!/bin/bash

if [ $# != 2 ]
then
  echo "Usage: $0 <query_fasta> <target_fasta>"
  exit
fi

query_fasta=$1
target_fasta=$2

rm -r tmp queryDB* targetDB* resultDB*

mmseqs createdb $query_fasta queryDB

mmseqs createdb $target_fasta targetDB

mmseqs createindex targetDB

mkdir tmp

mmseqs search queryDB targetDB resultDB tmp --min-seq-id 0.25 -e 0.0001

mmseqs convertalis queryDB targetDB resultDB resultDB.m8

rm -r tmp
