# DeepFR
The source code for DeepFR.

## requirements
- mmseqs
https://github.com/soedinglab/mmseqs2
- cd-hit
https://github.com/weizhongli/cdhit
- blastp
https://blast.ncbi.nlm.nih.gov/Blast.cgi?PROGRAM=blastp&PAGE_TYPE=BlastSearch&LINK_LOC=blasthome
- caffe
https://github.com/BVLC/caffe
- numpy>=1.7.1
- scipy>=0.13.2
- matplotlib>=1.3.1
- scikit-learn>=0.18.1

## prepare data
- choose_sequences_by_name_list.py
- convert_ccmpred_to_image.py
- convert_pdb_to_image.py
- generate_EC_matrix.py
- repair_pdb_chain.py
- sample_pad_ccmpred_to_image.py

## score for query
- create_alexnet.py
- create_solver.py
- extract_feature.py
- add_EC_feature.py
- score_deepfr.py
- score_lindahl_scoptest_pairs.py
- test_random_forest.py
- train_test_random_forest.py

## evaluation
- calculate_top1_top5.py
- choose_scores_by_pairs.py
- choose_subfeature_from_list.py
- evaluate_spec_sens_three_levels.py
- label_pairwise_score.py
- parse_Top1_Top5.py
- plot_dendroheatmap.py
- plot_specificity_sensitivity.py

## utility
- pydendroheatmap.py
- localconfig.py
- utils.py
