#!/bin/bash

#$1 ALIAS TO THE DATA BEING INFERRED
#$2 INPUT FILE WITH ONE ENTRY PER ROW
#$3 OUTPUT FOLDER
#$4 MALLET PATH
#$5 MALLET INPUT FILE PRODUCED DURING TRAINING
#$6 INFERENCER FILE
#$7 BURN IN ITERATIONS
#$8 NUMBER OF ITERATIONS
#$9 ORIGINAL NUMBER OF TOPICS

SEED=21911

# Create Mallet compatible input using the input of the trained model as well (use-pipe)
$4/bin/mallet import-file \
--input $2 \
--output $3/$1.mallet.infer \
--keep-sequence \
--token-regex '[\p{L}\p{P}]*\p{L}' \
--use-pipe-from $5 \
--remove-stopwords  

# Compute topic posteriors for each document
echo Running inference
$4/bin/mallet infer-topics \
        --burn-in $7 \
        --inferencer $6 \
        --input $3/$1.mallet.infer \
        --num-iterations $8 \
        --output-doc-topics $3/lda-$9.$1.post \
        --random-seed $SEED


