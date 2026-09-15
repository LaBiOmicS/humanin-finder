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
├── docs/                    # Technical documentation and user guides
├── examples/                # Quick-start samples (FASTA genomes)
├── galaxy/                  # Galaxy Tool wrapper and integration
├── paper/                   # Publication manuscripts
│   ├── joss/                # Software description for JOSS
│   └── primate_study/       # Scientific case study on 61 primate genomes
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

## 🧠 Architecture & Methodological Design

Traditional sequence-alignment tools (BLASTp, standard ORF finders) fail to detect mitochondrial sORFs across diverged taxa because primary nucleotide sequence drifts rapidly, translation frequently starts at non-canonical codons, and pseudogenization disrupts simple reading frames. `HumaninFinder` shifts the discovery paradigm from sequence-identity matching to **structural-signature and biophysical recognition**.

```text
  [ Complete Mitogenome (FASTA) ]
                 │
                 ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │ Layer 1: Targeted 16S Locus Detection                           │
  │ • nhmmer DNA profile alignment (16s_probe.fasta)                │
  │ • Fallback anchor: 5'-GTTAATGTAGCTTA-3'                         │
  │ • Restricts search space from ~17 kbp to ~1.6 kbp MT-RNR2 locus  │
  └─────────────────────────────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
  ┌───────────────┐ ┌───────────────────────────────────────────────┐
  │ Layer 2A:     │ │ Layer 2B: Multi-Frame Evolutionary Rescue     │
  │ Canonical     │ │ • Scans all 3 reading frames (0, 1, 2) on     │
  │ sORFs         │ │   both strands (±1)                           │
  │ • M...* ORFs  │ │ • Sliding window (21 aa, step=3 bp)           │
  │ • NCBI 1 - 33 │ │ • Identifies Non-canonical & Pseudogenes      │
  └───────────────┘ └───────────────────────────────────────────────┘
        │                 │
        └────────┬────────┘
                 ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │ Layer 3: Hybrid AI Scoring Engine                               │
  │ • ESM-2 Transformer (esm2_t6_8M_UR50D): Masked Mean Pooling     │
  │ • Explicit Biophysics: Charge (pH 7.4), pI, Hydrophobicity, AI  │
  │ • Calibrated Extra Trees Ensemble Classifier (100 estimators)   │
  └─────────────────────────────────────────────────────────────────┘
                 │
                 ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │ Layer 4: Orthogonal Validation & Penalization                   │
  │ • Profile HMM alignment (hmmsearch against humanin.hmm)         │
  │ • Synergistic confidence boost (+0.15 for significant hits)     │
  │ • Status weighting: Canonical (1.0x), Non-canon (0.95x),        │
  │   Pseudogenic (0.75x)                                           │
  └─────────────────────────────────────────────────────────────────┘
                 │
                 ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │ Layer 5: Biological Non-Maximum Suppression (NMS)               │
  │ • Suppresses overlapping window artifacts (> 50% overlap)       │
  │ • Prioritization: Canonical > Non-canonical > Pseudogenic       │
  │ • Output modes: Adaptive Single Best Hit vs. Exhaustive Sorfome │
  └─────────────────────────────────────────────────────────────────┘
                 │
                 ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │ Layer 6: Offline AI Research Agent (Ollama / Llama 3)           │
  │ • Local LLM synthesis of biological & gerontological insights   │
  └─────────────────────────────────────────────────────────────────┘
```

### 🧩 The Five Layers Explained

1. **Precision 16S Locus Targeting:** Employs `nhmmer` to pinpoint the exact boundaries of the 16S rRNA gene (*MT-RNR2*) using a conserved DNA probe (`16s_probe.fasta`), with automatic fallback to conserved oligonucleotide anchors. This reduces false positives and accelerates inference by $>10\times$.
2. **Dual Candidate Extraction & 3-Frame Rescue:** Combines strict canonical sORF discovery (`find_sorfs`) with a systematic **3-reading-frame sliding window scan** (`sliding_window_rescue`). This rescues sequences with alternative start codons or premature stop mutations (such as mitochondrial `AGG` stop codons in pseudogenized lineages).
3. **Hybrid AI Scoring Engine:** Vectorizes candidate peptides into a 324-dimensional space combining **ESM-2** deep transformer embeddings (masked mean-pooled, stripping special tokens) with four key biophysical descriptors (isoelectric point, net charge at pH 7.4, Kyte-Doolittle hydrophobicity, and aliphatic index). A calibrated Extra Trees classifier computes the posterior probability.
4. **Orthogonal Validation & Status Weighting:** Cross-validates candidates against a curated Humanin profile HMM (`humanin.hmm`). Confirmed hits receive an additive boost ($+0.15$), while non-canonical ($0.95\times$) and pseudogenic ($0.75\times$) candidates receive proportional biological penalties.
5. **Biological Non-Maximum Suppression (NMS):** Eliminates technical windowing redundancy by suppressing candidates sharing $>50\%$ overlap on the same strand, producing clean, independent genomic loci.
6. **Built-in AI Research Agent:** An integrated offline assistant powered by **Ollama** (e.g., Llama 3) that translates raw prediction tables into biological hypotheses regarding mitochondrial signaling, BAX/IGFBP-3 interactions, and aging biology.

📖 *For complete mathematical formulations and benchmark metrics, see the **[Architecture & Technical Design Guide](docs/architecture.md)**.*

---


## 🚀 Key Features

- **Organism Agnostic:** Supports all 33 NCBI genetic codes, enabling MDP discovery in any mitochondria-bearing taxon.
- **Expert AI Agent:** Built-in specialist in Humanin, mitochondrial signaling, and aging biology to interpret your findings.
- **High-Throughput Ready:** Parallelized processing and optimized inference for large genomic collections.
- **Validated Science:** Built-in reproduction of the 61-primate evolutionary case study.

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
Detailed technical documentation and reports are available:
- 🚀 **[Quickstart Guide](docs/quickstart.md)**: Step-by-step setup and common use cases.
- 📋 **[CLI Reference](docs/cli_reference.md)**: Detailed parameter reference for all subcommands.
- 🧬 **[Architecture & Technical Design](docs/architecture.md)**: In-depth technical guide covering all pipeline layers, neural embeddings, and biophysical scoring.
- 🛠️ **[Software Paper](paper/joss/paper.md)**: Software description and methodology draft for JOSS.
- 🏗️ **[Scientific Report](paper/primate_study/evolutionary_analysis_report.md)**: Evolutionary dynamics of Humanin in 61 Primates.

---

## 🤝 Contributing
Contributions are welcome! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
**Developed by [LaBiOmicS](https://github.com/LaBiOmicS)** - *Laboratory of Bioinformatics and Omics Sciences.*
**Institution:** [Universidade de Mogi das Cruzes (UMC)](https://www.umc.br/)
