# HumaninFinder v1.0.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Bioinformatics: Humanin](https://img.shields.io/badge/Bioinformatics-Humanin-brightgreen.svg)](https://github.com/LaBiOmicS/humanin-finder)
[![CI](https://github.com/LaBiOmicS/humanin-finder/actions/workflows/ci.yml/badge.svg)](https://github.com/LaBiOmicS/humanin-finder/actions/workflows/ci.yml)
[![JOSS](https://github.com/LaBiOmicS/humanin-finder/actions/workflows/paper.yml/badge.svg)](https://github.com/LaBiOmicS/humanin-finder/actions/workflows/paper.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1220989570.svg)](https://doi.org/10.5281/zenodo.1220989570)

**HumaninFinder** is a professional bioinformatics tool for the discovery and classification of Humanin-like peptides (sORFs). It uses a Hybrid AI approach, combining deep learning (ESM-2) with biophysical properties and a specialized **AI Research Agent**.

---

## 🚀 Installation

### Option 1: Fast Install (Recommended)
Install the latest stable version directly from PyPI:
```bash
pip install humaninfinder
```
*Note: Ensure you have [HMMER3](http://hmmer.org/) installed on your system.*

### Option 2: Conda/Mamba (Full Environment)
Best for scientific reproducibility, as it installs all dependencies (including HMMER3):
```bash
git clone https://github.com/LaBiOmicS/humanin-finder
cd humanin-finder
mamba env create -f environment.yml
mamba activate humanin_env
```

---

## ⚡ Quick Start

To scan a mitochondrial genome and identify Humanin candidates:

```bash
humanin-finder predict --input genome.fasta --output results --hmm --rescue
```

---

## 🌟 Key Features

- **Hybrid AI Engine:** ESM-2 structural embeddings + Biophysical analysis.
- **Evolutionary Rescue:** Detects non-canonical starts and pseudogenic relics.
- **Smart Filtering:** Automatically removes technical windowing artifacts.
- **AI Research Agent:** Expert interpretation of results via local LLMs (Ollama).

---

## 🤖 AI Research Agent (Optional)

Consult the integrated AI specialist for biological insights:
```bash
# Install agent support
pip install "humaninfinder[agent]"
# Run interpretation
humanin-finder agent --results results_csv.csv
```

---

## 📖 Main Commands

- `setup`: Verify environment and prerequisites.
- `predict`: Run the discovery and classification pipeline.
- `agent`: Interpret results with the specialized AI assistant.

---
Developed by **LaBiOmicS, UMC, Brazil**.
