# Quickstart Guide

This guide walks you through setting up and running **HumaninFinder** on your mitochondrial genome sequences.

---

## 💻 System Prerequisites

- **Operating System:** Linux or macOS (x86_64 / arm64)
- **Python:** 3.10, 3.11, or 3.12
- **External Binaries:** [HMMER3](http://hmmer.org/) (`nhmmer` and `hmmsearch`) must be accessible in your `$PATH`.

---

## 📦 Installation

Choose the installation method that fits your workflow:

### Option A: via `pip` (Standard / Fastest)

```bash
# Install package with optional Ollama AI agent support
pip install "humaninfinder[agent]"

# Verify environment and external binaries
humanin-finder setup
```

> **Note:** Ensure HMMER3 is installed on your operating system (e.g., `sudo apt install hmmer` on Ubuntu/Debian or `brew install hmmer` on macOS).

---

### Option B: via `Conda` / `Mamba` (Isolated Bioinformatics Environment)

Conda/Mamba automatically installs both Python and external system binaries like `hmmer`:

```bash
# Clone the repository
git clone https://github.com/LaBiOmicS/humanin-finder.git
cd humanin-finder

# Create environment from provided configuration
mamba env create -f environment.yml
mamba activate humanin_env

# Install package in editable mode
pip install -e .

# Run environment verification
humanin-finder setup
```

---

### Option C: via `Pixi` (Modern Reproducible Packaging)

```bash
# Clone the repository
git clone https://github.com/LaBiOmicS/humanin-finder.git
cd humanin-finder

# Install dependencies and setup
pixi run setup

# Run test suite
pixi run test
```

---

## 🔍 Basic Discovery Walkthrough

### 1. Single Genome or Sample FASTA

Run the predictor on a mitochondrial FASTA file with Profile HMM locus targeting (`--hmm`) and 3-frame evolutionary rescue (`--rescue`):

```bash
humanin-finder predict \
  -i examples/test_sample.fasta \
  -o results/sample_run \
  --hmm \
  --rescue
```

### 2. High-Throughput Cohort Processing

To analyze multiple genomes in parallel across multiple CPU cores:

```bash
humanin-finder predict \
  -i cohorts/mammals_collection.fasta \
  -o results/mammals_study \
  --hmm \
  --rescue \
  --cpus 8
```

### 3. Exhaustive Sorfome Exploration (`--all-candidates`)

By default, HumaninFinder applies adaptive selection to output the top confident candidate per genome. To output all non-redundant candidates:

```bash
humanin-finder predict \
  -i examples/test_sample.fasta \
  -o results/sample_all \
  --hmm \
  --rescue \
  --all-candidates
```

---

## 📊 Understanding Pipeline Outputs

The pipeline produces two output files based on your `-o/--output` prefix:

1. **Structured Predictions Table (`<output>_results.csv`)**:
   - `Genome_ID`: Identifier from the FASTA header.
   - `Start` / `End`: Genomic nucleotide coordinates of the detected locus.
   - `Strand`: Positive (`+1`) or reverse complement (`-1`).
   - `Frame`: Reading frame offset ($0, 1, 2$).
   - `Status`: `Canonical` (standard Met initiation), `Non-canonical` (alternative initiation codon), or `Pseudogenic` (nonsense stop codon relic).
   - `Peptide_Seq`: Translated amino acid sequence.
   - `AI_Score`: Posterior probability from the ESM-2 + biophysical classifier.
   - `HMM_Score` & `HMM_Evalue`: Orthogonal validation metrics from `hmmsearch`.
   - `Final_Score`: Calibrated score combining AI probability, HMM bonus, and biological status penalties.

2. **Peptide Sequences (`<output>_results.fasta`)**:
   FASTA-formatted peptides with rich metadata headers, directly usable for multiple sequence alignment (MAFFT, MUSCLE) or phylogenetic tree reconstruction.

---

## 🤖 Consulting the Local AI Research Agent

HumaninFinder includes an integrated domain-expert research agent that interprets discovery results in the context of mitochondrial biology, BAX/IGFBP-3 signaling, and aging.

### 1. Start Ollama
Ensure [Ollama](https://ollama.com) is installed and serving:

```bash
ollama serve &
ollama pull llama3
```

### 2. Run Biological Interpretation
```bash
# General summary of findings
humanin-finder agent --results results/sample_run_results.csv

# Query specific biological hypotheses
humanin-finder agent \
  --results results/sample_run_results.csv \
  --query "Analyze the evolutionary stability of the central hydrophobic core and potential cytoprotective activity."
```

---

## 📚 Next Steps

- 🧬 Read the **[Architecture & Technical Design](architecture.md)** for deep dives into ESM-2 embeddings, biophysical features, and algorithms.
- 📋 Check the **[CLI Reference](cli_reference.md)** for complete documentation of all command-line arguments.
