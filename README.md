# HumaninFinder v1.0.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Bioinformatics: Humanin](https://img.shields.io/badge/Bioinformatics-Humanin-brightgreen.svg)](https://github.com/LaBiOmicS/humanin-finder)
[![CI](https://github.com/LaBiOmicS/humanin-finder/actions/workflows/ci.yml/badge.svg)](https://github.com/LaBiOmicS/humanin-finder/actions/workflows/ci.yml)
[![JOSS](https://github.com/LaBiOmicS/humanin-finder/actions/workflows/paper.yml/badge.svg)](https://github.com/LaBiOmicS/humanin-finder/actions/workflows/paper.yml)
[![DOI](https://img.shields.io/badge/DOI-pending-lightgrey.svg)](#)

**HumaninFinder** is a professional bioinformatics tool for the discovery and classification of Humanin-like peptides (sORFs). It uses a Hybrid AI approach, combining deep learning (ESM-2) with biophysical properties to find peptides even in highly diverged or degenerated genomic regions.

---

## 🚀 Quick Start

### 1. Installation
The recommended way to install is using **Conda** or **Mamba**:

```bash
# Clone the repository
git clone https://github.com/LaBiOmicS/humanin-finder
cd humanin-finder

# Create and activate the environment
mamba env create -f environment.yml
mamba activate humanin_env
```

### 2. Basic Usage
To scan a mitochondrial genome and find the best Humanin candidate:

```bash
humanin-finder predict --input genome.fasta --output results --hmm --rescue
```

---

## 🌟 Key Features

- **Subcommand-based CLI:** Modular interface for prediction and future tools.
- **Intuitive Discovery:** Automatically localizes the 16S rRNA gene and scans for peptides.
- **Evolutionary Rescue:** Detects non-canonical starts and pseudogenic relics.
- **Smart Filtering:** Automatically removes redundant technical artifacts.

---

## 📖 Prediction Options

Use `humanin-finder predict --help` to see all options:

- `--input, -i`: Path to your FASTA file.
- `--output, -o`: Prefix for the output files.
- `--hmm`: (Recommended) Uses HMMER3 to improve localization accuracy.
- `--rescue`: (Recommended) Enables high-sensitivity scan for divergent peptides.
- `--all-candidates`: Generates a complete non-redundant list of all detected signals.
- `--table, -g`: NCBI Genetic Table (Default: 2 - Vertebrate Mitochondrial).

---

## 🛠 Troubleshooting: Prerequisites

If you choose to install via `pip`, you must have **HMMER3** installed on your system:
- **Ubuntu:** `sudo apt install hmmer`
- **MacOS:** `brew install hmmer`

---

## 📊 Output Files

1. `[output]_results.csv`: A professional table with coordinates, classifications, and confidence scores.
2. `[output]_results.fasta`: The identified peptide sequences for downstream analysis.

---
Developed by **LaBiOmicS, UMC, Brazil**.
