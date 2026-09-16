# HumaninFinder v1.1.0 🧬🤖

<p align="center">
  <img src="https://raw.githubusercontent.com/LaBiOmicS/humanin-finder/main/logo.png" alt="HumaninFinder Logo" width="70%">
</p>

<!-- Institutional Badges -->
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1220989570.svg)](https://doi.org/10.5281/zenodo.1220989570)
[![University: UMC](https://img.shields.io/badge/University-UMC-0D47A1.svg)](https://www.umc.br/)
[![Laboratory: LaBiOmicS](https://img.shields.io/badge/Laboratory-LaBiOmicS-7B1FA2.svg)](https://github.com/LaBiOmicS)
[![Bioinformatics](https://img.shields.io/badge/Bioinformatics-Humanin-brightgreen.svg)](https://github.com/LaBiOmicS/humanin-finder)

<!-- Open Science Badges -->
[![PyPI Version](https://img.shields.io/pypi/v/humaninfinder.svg)](https://pypi.org/project/humaninfinder/)
[![Open Source](https://img.shields.io/badge/Open-Source-brightgreen.svg)](https://github.com/LaBiOmicS/humanin-finder)
[![Open Science](https://img.shields.io/badge/Open-Science-blue.svg)](https://github.com/LaBiOmicS/humanin-finder)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![JOSS Status](https://img.shields.io/badge/JOSS-Pre--submission-brightgreen.svg)](https://joss.theoj.org/)
[![CI Status](https://github.com/LaBiOmicS/humanin-finder/actions/workflows/ci.yml/badge.svg)](https://github.com/LaBiOmicS/humanin-finder/actions/workflows/ci.yml)

<!-- Tech & Method Badges -->
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Powered by Ollama](https://img.shields.io/badge/AI-Powered_by_Ollama-orange.svg)](https://ollama.com)
[![Deep Learning](https://img.shields.io/badge/Method-ESM--2_Embeddings-blueviolet.svg)](https://github.com/LaBiOmicS/humanin-finder)

---

`HumaninFinder` is a professional, high-performance Python framework designed for the discovery and classification of Humanin-like peptides (sORFs) within mitochondrial genomes. It employs a **Hybrid AI Engine** that integrates deep structural embeddings from the ESM-2 Protein Language Model with explicit biophysical analysis to identify functional, non-canonical, and pseudogenic sequences across any taxonomic group.

---

<p align="center">
  <img src="https://raw.githubusercontent.com/LaBiOmicS/humanin-finder/main/infografico.png" alt="HumaninFinder" width="100%">
</p>

---

## 📂 Repository Structure

```text
.
├── conda/                   # Bioconda recipe and metadata
├── deploy/                  # Containerization (Dockerfile, Singularity.def)
├── docs/                    # Technical documentation hub
│   ├── architecture.md      # Exhaustive architecture, algorithms, ML training & stack
│   ├── quickstart.md        # Installation guide and first execution steps
│   └── cli_reference.md     # Command-line parameters and subcommands reference
├── examples/                # Quick-start samples (FASTA genomes)
├── galaxy/                  # Galaxy Tool wrapper and integration
├── paper/                   # Publication manuscripts
│   ├── joss/                # Software description for JOSS
│   └── primate_study/       # Scientific case study on 343 primate mitogenomes
├── src/
│   └── humaninfinder/       # Main Python Package
│       ├── cli.py           # Subcommand-based Command-line interface
│       ├── core.py          # Locus localization and ORF finding logic
│       ├── classifier.py    # Hybrid AI Engine (ESM-2 + Biophysical)
│       ├── agent.py         # AI Research Agent (Ollama integration)
│       ├── data/            # HMM models and 16S probes
│       └── models/          # Pre-trained hybrid classifier weights
├── tests/                   # Unit and biological validation tests
├── pyproject.toml           # Build system and PyPI definitions
└── pixi.toml                # Modern environment management
```

## 🧠 Architecture & Methodology

Traditional sequence-alignment tools (such as BLASTp or standard ORF finders) fail to detect mitochondrial sORFs across diverged taxa because nucleotide sequences drift rapidly, translation initiation frequently uses non-canonical codons, and pseudogenization disrupts simple reading frames. 

`HumaninFinder` shifts the discovery paradigm from sequence-identity matching to **structural-signature and biophysical recognition** using a 6-layer architecture:
1. **Targeted 16S Locus Detection:** Restricts search to *MT-RNR2* using `nhmmer` DNA profile alignment and conserved anchors.
2. **Dual Candidate Extraction & 3-Frame Rescue:** Combines canonical sORF scans with multi-frame sliding-window rescue to capture non-canonical starts and pseudogenes.
3. **Hybrid AI Engine:** Combines deep **ESM-2** protein language model embeddings (masked mean pooling) with explicit biophysical features (net charge at pH 7.4, pI, hydrophobicity, aliphatic index), classified via a calibrated Support Vector Classifier (RBF-SVC).
4. **Orthogonal HMM Validation:** Profile HMM alignment (`hmmsearch`) provides orthogonal verification and status-based confidence penalties.
5. **Biological Non-Maximum Suppression (NMS):** Eliminates overlapping window artifacts (>50% overlap on the same strand).
6. **Built-in AI Research Agent:** Local LLM integration (via Ollama) translates predictions into biological and gerontological insights.

> 📖 **Comprehensive Technical Reference:** For algorithmic pseudo-code, mathematical formulations, anti-leakage ML training benchmarks, and the full technology stack matrix, please consult the **[Architecture & Technical Design Guide](docs/architecture.md)**.

---

## 🚀 Key Features

- **Organism Agnostic:** Supports all 33 NCBI genetic codes, enabling MDP discovery in any mitochondria-bearing taxon.
- **Deep Structural Embeddings:** Powered by Meta AI's ESM-2 transformer model for sequence-drift-resistant peptide recognition.
- **Multi-Frame Evolutionary Rescue:** Captures pseudogenic and non-canonical relics across divergent evolutionary clades.
- **Expert AI Agent:** Built-in specialist in Humanin, mitochondrial signaling, and aging biology to interpret your findings.
- **High-Throughput Ready:** Multi-core parallel processing for large genomic cohorts.
- **Validated Science:** Benchmark-verified across 343 primate mitogenomes with 100% taxonomic recovery.

---

## 🛠️ Quick Start

### 1. Installation

#### Option A: via `pip` (Fastest)
```bash
pip install "humaninfinder[agent]"
humanin-finder setup
```
*Note: Ensure [HMMER3](http://hmmer.org/) is installed on your system.*

#### Option B: via `Conda` / `Mamba` (Recommended)
Perfect for an isolated scientific environment:

```bash
# Create environment from the provided file
mamba env create -f environment.yml
mamba activate humanin_env

# Finalize setup
humanin-finder setup
```

### 2. Run Discovery Pipeline
```bash
humanin-finder predict -i examples/test_sample.fasta -o results/propithecus --hmm --rescue
```

### 3. Biological Interpretation
```bash
# Get a summary of your findings from the AI Specialist
humanin-finder agent --results results/propithecus_results.csv
```

---

## 📖 Documentation

Complete technical guides and scientific reports are hosted in the **[Documentation Hub](docs/README.md)**:

| Document | Description |
| :--- | :--- |
| 🧬 **[Architecture & Technical Design](docs/architecture.md)** | Exhaustive 6-layer architecture, algorithmic pseudo-code, ESM-2 structural embeddings, biophysical profiling, and anti-leakage ML training. |
| 🚀 **[Quickstart Guide](docs/quickstart.md)** | Step-by-step installation instructions (Pip, Conda, Pixi), first runs, and expected outputs. |
| 📋 **[CLI Reference](docs/cli_reference.md)** | Full parameter and flag reference for `setup`, `predict`, and `agent` subcommands. |
| 🔬 **[Evolutionary Analysis Report](paper/primate_study/evolutionary_analysis_report.md)** | Biological case study examining Humanin retention and pseudogenization across 343 primate mitogenomes. |

---

## 🤝 Contributing
Contributions are welcome! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
**Developed by [LaBiOmicS](https://github.com/LaBiOmicS)** - *Laboratory of Bioinformatics and Omics Sciences.*
**Institution:** [Universidade de Mogi das Cruzes (UMC)](https://www.umc.br/)
