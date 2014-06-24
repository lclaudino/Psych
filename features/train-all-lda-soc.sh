#!/bin/bash

LOCAL=/Users/claudino/git/Psych/features/
FEAT_FOLDER=/Users/claudino/Desktop/collaborations/with-CLIP/2014/summer/psych/data/output/SOC/feat-files/
LDA_MODEL_FOLDER=/Users/claudino/Desktop/collaborations/with-CLIP/2014/summer/psych/data/output/SOC/lda-mallet/
MALLET_FOLDER=/Users/claudino/Desktop/collaborations/with-CLIP/2013/mallet-2.0.7/
NUM_TOPICS=20
NUM_ITERATIONS=1000

for YEAR in {1997..2008}; do	
	$LOCAL/train-lda.sh \
	soc-$YEAR \
	$FEAT_FOLDER/soc-$YEAR.mallet \
	$LDA_MODEL_FOLDER \
	$MALLET_FOLDER \
	$NUM_TOPICS \
	$NUM_ITERATIONS \
	$ALPHA
done