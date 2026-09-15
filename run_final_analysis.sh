#!/bin/bash
# HumaninFinder Final Publication Analysis: Primate Evolution (61 Genomes)
set -e

PAPER_DIR="paper/primate_study"
PYTHON_BIN="${PYTHON_BIN:-python3}"
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

mkdir -p "${PAPER_DIR}"

COMBINED_FASTA="examples/full_primates_collection.fasta"
if [ ! -f "${COMBINED_FASTA}" ]; then
    COMBINED_FASTA="full_primates_collection.fasta"
fi
if [ ! -f "${COMBINED_FASTA}" ]; then
    GENOMES_DIR="study/primate_evolution/genomes"
    if [ -d "${GENOMES_DIR}" ]; then
        echo "[*] Combining primate genomes..."
        cat ${GENOMES_DIR}/*.fasta > ${COMBINED_FASTA}
    else
        echo "[-] Error: ${COMBINED_FASTA} or ${GENOMES_DIR} not found."
        exit 1
    fi
fi

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
