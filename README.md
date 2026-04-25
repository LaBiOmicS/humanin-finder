# HumaninFinder v1.0.0

<!-- Institutional Badges -->
[![University: UMC](https://img.shields.io/badge/University-UMC-0D47A1.svg)](https://www.umc.br/)
[![Laboratory: LaBiOmicS](https://img.shields.io/badge/Laboratory-LaBiOmicS-7B1FA2.svg)](https://github.com/LaBiOmicS)
[![Bioinformatics: Humanin](https://img.shields.io/badge/Bioinformatics-Humanin-brightgreen.svg)](https://github.com/LaBiOmicS/humanin-finder)


<!-- Open Science Badges -->
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI Version](https://img.shields.io/pypi/v/metalncrna.svg)](https://pypi.org/project/humanin-finder/)
[![Open Source](https://img.shields.io/badge/Open-Source-brightgreen.svg)](https://github.com/LaBiOmicS/humanin-finder)
[![Open Science](https://img.shields.io/badge/Open-Science-blue.svg)](https://github.com/LaBiOmicS/humanin-finder)
[![Open Data](https://img.shields.io/badge/Open-Data-brightgreen.svg)](https://github.com/LaBiOmicS/humanin-finder)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![JOSS Status](https://img.shields.io/badge/JOSS-Pre--submission-brightgreen.svg)](https://joss.theoj.org/)
[![CI Status][(https://github.com/LaBiOmicS/humanin-finder/actions/workflows/ci.yml/badge.svg)](https://github.com/LaBiOmicS/humanin-finder/actions/workflows/ci.yml)](https://github.com/LaBiOmicS/humanin-finder/actions/workflows/ci.yml/badge.svg)](https://github.com/LaBiOmicS/humanin-finder/actions/workflows/ci.yml))


**HumaninFinder** is an easy-to-use bioinformatics tool for the discovery and classification of Humanin-like peptides (sORFs). It uses a Hybrid AI approach, combining deep learning (ESM-2) with biophysical properties to find peptides even in highly diverged or degenerated genomic regions.

---

## 🚀 Quick Start

### 1. Installation
The easiest way to install is using **Conda** or **Mamba**, which handles all dependencies for you:

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
humanin-finder --input genome.fasta --output results --hmm --rescue
```

---

## 🌟 Key Features

- **Intuitive Discovery:** Automatically localizes the 16S rRNA gene and scans for peptides.
- **Evolutionary Rescue:** Detects non-canonical starts and pseudogenic relics.
- **Smart Filtering:** Automatically removes redundant technical artifacts.
- **Organism Agnostic:** Works with any species and all NCBI genetic codes.

---

## 📖 Main Options

- `--input`: Path to your FASTA file.
- `--output`: Prefix for the output files.
- `--hmm`: (Recommended) Uses HMMER3 to improve localization accuracy.
- `--rescue`: (Recommended) Enables high-sensitivity scan for divergent peptides.
- `--all-candidates`: Generates a complete non-redundant list of all detected signals.
- `--table`: NCBI Genetic Table (Default: 2 - Vertebrate Mitochondrial).

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
