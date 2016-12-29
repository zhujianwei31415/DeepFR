#!/bin/bash

if [ $# != 3 ]
then
  echo "Usage: $0 <target> <seqfile> <outdir>"
  exit
fi

target=$1
seqfile=$2
outdir=$3/$target
echo $target $seqfile $outdir

if [ ! -f $seqfile ]
then
  echo "ERROR: $seqfile does not exist"
  exit
fi

if [ ! -d $outdir ]
then
  mkdir -p $outdir
fi

dir=`dirname $(readlink -f $0)`
server=$dir/../deepfr_model/server

echo "Generating EC matrix..."
$dir/generate_EC_matrix.py -i $seqfile --outdir $outdir

echo "Converting coupling..."
ccmfile=$outdir/$target.ccm
image=$outdir/$target.jpg
$dir/convert_coupling.py $ccmfile $image

echo "Running DeepFR..."
net=$server/deploy.prototxt
model=$server/caffe_deepfrnet.caffemodel
feat=$outdir/$target.feat
$dir/extract_feature.py -n $net -m $model -i $image -o $feat

echo "Scoring and Ranking..."
namelabel=$server/scope95_2.06_name_label_list
featlist=$server/scope95_2.06_features.npy
score=$outdir/$target.score
rank=$outdir/$target.rank
$dir/score_deepfr.py $namelabel $featlist $feat $score
sort -nk2 -r $score > $rank
