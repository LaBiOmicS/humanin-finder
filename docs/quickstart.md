# Quickstart Guide

## Installation

### With Pixi (Recommended for modern environments)
```bash
pixi run test
```

### With Conda / Mamba
```bash
mamba env create -f environment.yml
mamba activate humanin_env
pip install -e .
```

### With Pip
```bash
pip install "humaninfinder[agent]"
humanin-finder setup
```

## Basic Usage

### 1. Predict Humanin Peptides from FASTA
```bash
humanin-finder predict -i examples/test_sample.fasta -o results/propithecus --hmm --rescue
```

### 2. Predict with All Candidates
```bash
humanin-finder predict -i examples/full_primates_collection.fasta -o results/all_candidates --hmm --rescue --all-candidates
```

### 3. Consult the Local AI Agent (Requires Ollama)
```bash
ollama serve &
ollama pull llama3
humanin-finder agent --results results/propithecus_results.csv
```
