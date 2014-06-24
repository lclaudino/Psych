#!/bin/bash

LOCAL=/Users/claudino/git/Psych/features/
FEAT_FOLDER=/Users/claudino/Desktop/collaborations/with-CLIP/2014/summer/casl/data/output/tweets/feat-files/
LDA_MODEL_FOLDER=/Users/claudino/Desktop/collaborations/with-CLIP/2014/summer/casl/data/output/tweets/lda-mallet/
MALLET_FOLDER=/Users/claudino/Desktop/collaborations/with-CLIP/2013/mallet-2.0.7/
NUM_TOPICS=5
NUM_ITERATIONS=1000
ALPHA=50

$LOCAL/train-lda.sh "casl-tweets" \
$FEAT_FOLDER/casl-wmdtweets_2014-06-09.tsv.filt.mallet \
$LDA_MODEL_FOLDER \
$MALLET_FOLDER \
$NUM_TOPICS \
$NUM_ITERATIONS \
$ALPHA