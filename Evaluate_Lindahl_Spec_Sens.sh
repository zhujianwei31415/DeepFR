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

echo "$0 $1"

dir=`dirname $(readlink -f $0)`
L_DATA=$dir/list

echo "Label scores at three levels: "
$dir/label_pairwise_score.py $OUTPUT $L_DATA/lindahl_family $L_DATA/lindahl_superfamily $L_DATA/lindahl_fold
echo "Calculating Specificity and Sensitivity at three levels: "
$dir/evaluate_spec_sens_three_levels.py value-family value-superfamily value-fold  
