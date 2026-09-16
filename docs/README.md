# HumaninFinder Documentation Hub

Welcome to the technical documentation for **HumaninFinder**, an organism-agnostic framework combining deep protein language models (ESM-2) with biophysical analysis for the discovery and evolutionary characterization of Humanin-like peptides.

---

## 📚 Documentation Index

| Document | Description |
| :--- | :--- |
| 🏗️ **[Architecture & Technical Design](architecture.md)** | Exhaustive technical specification: 6-layer pipeline, algorithmic pseudo-code, ESM-2 masked mean pooling, RBF-SVC machine learning training, data-leakage prevention via 80% clustering, and full technology stack. |
| 🚀 **[Quickstart Guide](quickstart.md)** | Step-by-step installation instructions (Pixi, Conda, Pip) and first execution walkthrough. |
| 📋 **[CLI Reference](cli_reference.md)** | Detailed parameter and flag reference for all subcommands (`setup`, `predict`, `agent`). |

---

## 🧭 Pipeline Flowchart

```text
[ Mitochondrial FASTA ] 
          │
          ▼
[ Layer 1: 16S Locus Targeting (nhmmer / 16s_probe.fasta) ]
          │
    ┌─────┴─────┐
    ▼           ▼
[ Layer 2A: Canonical sORF Scan ]   [ Layer 2B: 3-Frame Evolutionary Rescue ]
    │                                   │
    └───────────────┬───────────────────┘
                    ▼
[ Layer 3: Hybrid AI Engine (ESM-2 8M Embeddings + Biophysical Descriptors) ]
                    │
                    ▼
[ Layer 4: Orthogonal Validation (hmmsearch / humanin.hmm) & Penalties ]
                    │
                    ▼
[ Layer 5: Biological Non-Maximum Suppression (NMS > 50% overlap) ]
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
[ Layer 6A: Structured Outputs (CSV/FASTA) ]   [ Layer 6B: Local AI Agent (Ollama) ]
```

---

For inquiries, bug reports, and contributions, please visit our [GitHub Repository](https://github.com/LaBiOmicS/humanin-finder).
