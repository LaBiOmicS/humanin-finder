#!/bin/bash
# HumaninFinder Final Publication Analysis: Primate Evolution (61 Genomes)
set -e

GENOMES_DIR="study/primate_evolution/genomes"
PAPER_DIR="paper/primate_study"
PYTHON_BIN="/home/menegidio/.miniforge3/envs/humanin_env/bin/python"
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

echo "[*] Combining 61 primate genomes..."
COMBINED_FASTA="study/primate_evolution/all_primates_combined.fasta"
cat ${GENOMES_DIR}/*.fasta > ${COMBINED_FASTA}

echo "[*] Running Standard Analysis (Best Candidates Only)..."
${PYTHON_BIN} src/humaninfinder/cli.py predict \
    --input ${COMBINED_FASTA} \
    --output ${PAPER_DIR}/full_primate_study \
    --hmm --rescue --threshold 0.7

echo "[*] Running Complete Analysis (All Candidates)..."
${PYTHON_BIN} src/humaninfinder/cli.py predict \
    --input ${COMBINED_FASTA} \
    --output ${PAPER_DIR}/full_primate_study_all \
    --hmm --rescue --all-candidates

echo "[+] Analysis complete. Files generated in ${PAPER_DIR}/:"
ls -lh ${PAPER_DIR}/full_primate_study*
