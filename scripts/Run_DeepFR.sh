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
deepfr=$dir/deepfr/
models=$dir/../models/

echo "Generating EC matrix..."
$deepfr/generate_EC_matrix.py -i $seqfile --outdir $outdir

echo "Converting coupling..."
ccmfile=$outdir/$target.ccm
imagelist=$outdir/$target.list
$deepfr/convert_coupling.py $ccmfile $outdir

echo "Running DeepFR..."
net=$models/deploy.prototxt
model=$models/caffe_deepfrnet.caffemodel
feat=$outdir/$target.feat
$deepfr/extract_feature.py -n $net -m $model -l $imagelist -o $feat

echo "Scoring ..."
namelabel=$models/scope95_2.06_label_dict.pkl
featlist=$models/scope95_2.06_feature_dict.pkl
score=$outdir/$target.score
$deepfr/score_query_template.py $namelabel $featlist $feat $score

echo "Ranking ..."
rank=$outdir/$target.rank
sort -nk2 -r $score > $rank
