# DeepFR
Improving Protein Fold Recognition by Extracting Fold-specific Features from Predicted Residue-residue Contacts

## Requirements
- caffe>=1.0
- numpy>=1.7.1
- scipy>=0.13.2
- biopython>=1.68
- matplotlib>=1.3.1
- scikit-learn>=0.18.1


## Installation
- Download the pretrained model, label_dict and pregenerated feature_dict from http://protein.ict.ac.cn/deepfr/evaluation_data/scripts/models/ and put it under ./models directory
- Install caffe from https://github.com/BVLC/caffe
- Install hhblits from https://github.com/soedinglab/hh-suite
- Install ccmpred from https://github.com/soedinglab/CCMpred
- Modify program path (hhblits, ccmpred, caffe) in ./scripts/localconfig.py

## Usage
- Run ```./scripts/Run_DeepFR.sh d1a3aa_ examples/d1a3aa_.fasta outdir```
- You can find the .rank file for each template in outdir.
```
Usage: ./scripts/Run_DeepFR.sh <target> <seqfile> <outdir>
```
