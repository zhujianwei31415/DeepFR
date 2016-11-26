#!/bin/bash

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <Output with label:./results/output_with_label>"
  exit
fi

OUTPUT=$1

if [ ! -f $OUTPUT ]
then
  echo "$OUTPUT does not exist."
  exit
fi

L_DATA=./list

mkdir -p ./tmp

echo "Calculating correctly predicted template at family level(Top1, Top5): "
./calculate_top1_top5.py $OUTPUT $L_DATA/lindahl_family

echo "Calculating correctly predicted template at superfamily level(Top1, Top5): "
grep -F -v -f  $L_DATA/lindahl_family $OUTPUT > ./tmp/deleted-family
./calculate_top1_top5.py ./tmp/deleted-family $L_DATA/lindahl_superfamily

echo "Calculating correctly predicted template at fold level(Top1, Top5): "
grep -F -v -f $L_DATA/lindahl_superfamily ./tmp/deleted-family > ./tmp/deleted-family-super
./calculate_top1_top5.py ./tmp/deleted-family-super $L_DATA/lindahl_fold

rm -r ./tmp
