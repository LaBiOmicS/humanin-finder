#!/bin/bash
# HumaninFinder Primate Evolution Case Study
# Replicates the analysis of 61 mitochondrial genomes

echo "Starting Primate Evolution Analysis..."
COMBINED_FASTA="all_primates.fasta"

# 1. Clean up and combine genomes
# Using a pattern that avoids including the output file if it were in the same dir, 
# and ensuring we are in the right directory context.
rm -f $COMBINED_FASTA
cat genomes/*.fasta > $COMBINED_FASTA

# 2. Run HumaninFinder
python ../../HumaninFinder --input $COMBINED_FASTA \
       --hmm --rescue --threshold 0.7 \
       --output results/primates_final_study_results

echo "Analysis finished. Results saved in study/primate_evolution/results/"
