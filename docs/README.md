# HumaninFinder Documentation

Welcome to the technical documentation for **HumaninFinder**.

## Table of Contents
1. [Architecture & Technical Design](architecture.md)
2. [Quickstart Guide](quickstart.md)
3. [CLI Reference](cli_reference.md)

---

## Architecture at a Glance

```text
               +----------------------------------+
               | Mitochondrial DNA Genome (FASTA) |
               +----------------------------------+
                                 |
                                 v
               +----------------------------------+
               | 16S Locus Detection (nhmmer /   |
               | conserved anchor fallback)       |
               +----------------------------------+
                                 |
        +------------------------+------------------------+
        |                                                 |
        v                                                 v
+-----------------------+                         +-----------------------+
| Canonical sORF Scan   |                         | Evolutionary Rescue   |
| (NCBI Translation     |                         | (Sliding Window Scan, |
|  Tables 1 - 33)       |                         |  Window=21, Step=3)   |
+-----------------------+                         +-----------------------+
        |                                                 |
        +------------------------+------------------------+
                                 |
                                 v
               +----------------------------------+
               | Hybrid AI Scoring Engine:        |
               | - ESM-2 (8M) Embeddings          |
               | - Biophysical Features           |
               | - Profile HMM Verification       |
               +----------------------------------+
                                 |
                                 v
               +----------------------------------+
               | Biological Redundancy Filter     |
               | (Non-Maximum Suppression > 50%)  |
               +----------------------------------+
                                 |
                                 v
               +----------------------------------+
               | Output Results: CSV and FASTA    |
               | + Optional Ollama AI Agent       |
               +----------------------------------+
```
