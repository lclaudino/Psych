#!/bin/bash

#$1 ALIAS TO THE DATA BEING IN USED FOR TRAINING
#$2 INPUT FILE WITH ONE ENTRY PER ROW
#$3 OUTPUT FOLDER
#$4 MALLET PATH
#$5 NUMBER OF TOPICS
#$6 NUMBER OF ITERATIONS
#$7 ALPHA

# Fixed LDA parameters
SEED=21911

# Create Mallet compatible input
$4/bin/mallet import-file \
--input $2 \
--output $3/$1.mallet.in \
--keep-sequence \
--token-regex '[\p{L}\p{P}]*\p{L}' \
--remove-stopwords  

# Generate LDA topic model
echo Creating LDA topics with Mallet
$4/bin/mallet train-topics \
   --input $3/$1.mallet.in \
   --random-seed $SEED \
   --num-topics $5 \
   --num-iterations $6 \
   --alpha $7 \
   --output-doc-topics $3/$1.lda-$5.docs \
   --output-model $3/$1.lda-$5.model \
   --output-topic-keys $3/$1.lda-$5.keys \
   --output-state $3/$1.lda-$5.state \
   --topic-word-weights-file $3/$1.lda-$5.words \
   --inferencer-filename $3/$1.lda-$5.inferencer \
