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

Small Open Reading Frames (sORFs) represent the "dark matter" of the genome. Their identification is plagued by:
1.  **Sequence Divergence:** sORFs drift much faster than large genes, rendering BLAST-based methods ineffective over large evolutionary distances.
2.  **Non-canonical Signals:** Mitochondrial genomes frequently use alternative start codons (GTG, ATT, ATC) that are ignored by standard annotation pipelines.
3.  **Pseudogenization:** Functional sequences often transition into "pseudogenic relics" that still maintain structural relevance but lack canonical markers.

`HumaninFinder` addresses these challenges by shifting the discovery paradigm from **sequence-identity** to **structural-signature recognition**.

# Technical Innovation: Beyond the Sequence

The core innovation of `HumaninFinder` lies in its **Hybrid AI Engine**. Unlike traditional tools that rely on rigid codon rules or position-weight matrices, `HumaninFinder` leverages:
-   **Deep Structural Embeddings:** Using ESM-2 transformer-derived vectors to capture the high-dimensional biophysical "essence" of a peptide. This allows the tool to detect "structural ghosts"—regions where the DNA sequence has drifted significantly, but the underlying protein-like structure is still recognizable by the AI.
-   **Evolutionary Rescue Mode:** A high-sensitivity sliding-window scanner that explores all potential reading frames. 
-   **Biological De-multiplexing:** A specialized non-redundant filter that deduplicates technical windowing artifacts into independent evolutionary loci. This ensures that the results provide a biologically accurate map of a locus's evolutionary history.

# Research Applicability

`HumaninFinder` is designed for broad applicability in various scientific domains:
-   **Evolutionary Genomics:** Researchers can use the "Exhaustive Mode" to map the degradation and "rescue" of MDPs across millions of years, as demonstrated in our primate evolution case study.
-   **Aging and Endocrinology:** Identification of species-specific Humanin variants ("tuned" peptides) can provide insights into metabolic adaptations and longevity.
-   **Genomic Annotation:** The tool can be integrated into larger pipelines (via Docker, Singularity, or Galaxy) to refine the annotation of mitochondrial "sorfomes" in non-model organisms, from fungi to endangered vertebrates.

# State of the Field

Classic tools like **ORFfinder** or **getorf** are restricted to canonical ORF detection and cannot handle the high mutation rates of mitochondrial sORFs. While specialized sORF finders exist, they typically require extensive organism-specific training. `HumaninFinder` bridges this gap by using a protein language model trained on evolutionary-scale data, providing a truly organism-agnostic solution with high sensitivity for both functional and degenerated peptides.

# Mentions

This work was supported by the Laboratory of Bioinformatics and Omics (LaBiOmics) at the University of Mogi das Cruzes (UMC).

# References
