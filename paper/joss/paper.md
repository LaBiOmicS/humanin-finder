---
title: 'HumaninFinder: A Hybrid AI Engine for the Evolutionary Discovery of Humanin-like Peptides'
tags:
  - Python
  - Bioinformatics
  - Deep Learning
  - ESM-2
  - Mitochondria
  - sORF
  - Mitochondrial-Derived Peptides (MDPs)
authors:
  - name: Fabiano Bezerra Menegidio
    orcid: 0000-0002-XXXX-XXXX
    affiliation: 1
affiliations:
  - name: LaBiOmicS, University of Mogi das Cruzes (UMC), Brazil
    index: 1
date: 25 April 2026
bibliography: paper.bib
---

# Summary

Mitochondrial-derived peptides (MDPs) are a newly discovered class of bioactive molecules encoded within mitochondrial genes. Among them, Humanin (HN)—encoded within the 16S rRNA gene (MT-RNR2)—is a critical cytoprotective factor with roles in aging, neuroprotection, and metabolic signaling. 

`HumaninFinder` is an organism-agnostic bioinformatics framework designed to automate the discovery and classification of Humanin orthologs. By integrating deep structural embeddings from the ESM-2 Protein Language Model [@Lin2023] with explicit biophysical analysis, the tool enables researchers to identify functional and degenerated peptides across any taxonomic group, supporting all 33 NCBI genetic codes.

# Statement of Need

Small Open Reading Frames (sORFs) represent the "dark matter" of the genome. Their identification is plagued by high sequence divergence, non-canonical signals (e.g., GTG, ATT start codons), and pseudogenization. Traditional tools rely on rigid rules and sequence identity, which often fail over large evolutionary distances. `HumaninFinder` addresses these challenges by shifting the discovery paradigm from sequence-identity to **structural-signature recognition**.

# Technical Innovation and Implementation

The core innovation of `HumaninFinder` lies in its **Hybrid AI Engine**, which combines deep structural embeddings with traditional biophysical metrics. The software features a modular, subcommand-based architecture implemented in Python, leveraging:
-   **Locus Localization:** HMMER3 [@Eddy2011] for pinpointing the MT-RNR2 region.
-   **Neural Inference:** PyTorch [@Paszke2019] and ESM-2 transformer models [@Lin2023] for structural fingerprinting.
-   **Evolutionary Rescue:** High-sensitivity scans with automatic biological de-multiplexing to ensure independent evolutionary signals.

The tool provides an intuitive CLI via the `click` library, including a `setup` command for environment verification and a `predict` command for genomic scanning.

# Research Applicability

`HumaninFinder` is designed for broad research use:
-   **Evolutionary Genomics:** Mapping the degradation and rescue of MDPs, as demonstrated in our primate case study (identifying >5,000 signals).
-   **Aging and Endocrinology:** Identification of species-specific Humanin variants to study metabolic adaptation.
-   **Genomic Annotation:** Integration into high-throughput pipelines to refine mitochondrial "sorfomes."

# Mentions

This work was supported by the Laboratory of Bioinformatics and Omics (LaBiOmics) at the University of Mogi das Cruzes (UMC).

# References
