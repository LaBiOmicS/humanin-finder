# HumaninFinder: Technical Architecture, Algorithms, Training & Stack Specification

`HumaninFinder` (v1.1.0) is a specialized bioinformatics and machine learning framework engineered for the discovery, classification, and biological interpretation of Humanin-like mitochondrial-derived peptides (MDPs / sORFs).

This document provides a comprehensive technical reference detailing the system architecture, mathematical formulations, algorithmic implementations, machine learning training pipeline, technology stack, and engineering practices.

---

## 1. Technological Stack Matrix

| Component / Layer | Technology / Library | Role & Functionality | Justification / Engineering Rationale |
| :--- | :--- | :--- | :--- |
| **Language & Core Runtime** | Python 3.10+ | Primary language environment | Standard in bioinformatics and scientific ML |
| **Deep Protein Language Model** | Meta AI ESM-2 (`esm2_t6_8M_UR50D`) | Deep structural representation (320 dims) | Captures 3D structural propensities without relying on rigid sequence identity |
| **Deep Learning Framework** | PyTorch & Hugging Face `transformers` | Model inference, tokenization, attention masks | Fast, standardized transformer execution on CPU/GPU |
| **Classical Machine Learning** | Scikit-learn (`scikit-learn`) | RBF Support Vector Classifier, StandardScaler | High generalization on small-to-medium biological feature spaces; prevents deep net overfitting |
| **Model Serialization** | Joblib | Model artifact storage (`.joblib`) | Efficient storage of trained estimators, scalers, and metadata |
| **Biophysical Modeling** | `peptides` (Python) | Net charge, pI, hydrophobicity, aliphatic index | Explicit biophysical grounding complementary to neural representations |
| **Genomic Sequence Processing** | Biopython (`Bio.Seq`, `Bio.SeqIO`) | FASTA parsing, multi-table translation | Robust handling of NCBI genetic codes (Tables 1 to 33) |
| **Sequence Homology & HMMs** | HMMER3 (`nhmmer` & `hmmsearch`) | 16S rRNA DNA targeting & protein profile scoring | State-of-the-art profile Hidden Markov Models for biological anchoring |
| **CLI & User Interface** | Click (`click`) | Modular command-line subcommands | Composable, typed, self-documenting CLI interface |
| **Data Manipulation & IO** | Pandas & NumPy | Tabular reporting, matrix vectorization | High-throughput structured CSV and matrix operations |
| **Autonomous AI Research Agent** | Local Ollama API (Llama 3 / Mistral) | Scientific interpretation of findings | 100% offline, private, domain-specific hypothesis generation |
| **Environment Management** | Pixi (`pixi.toml`) & Conda/Micromamba | Reproducible multi-platform environments | Fast lockfile resolution including native binary dependencies (`hmmer`) |
| **Containerization** | Docker & Singularity / Apptainer | Enterprise & HPC reproducibility | Portable execution across cloud and supercomputing clusters |
| **Platform Integration** | Galaxy Tool XML (`galaxy/humaninfinder.xml`) | No-code GUI execution for bench biologists | Standardized integration into institutional Galaxy servers |
| **Test Suite** | Pytest (`pytest`) | Unit, biological regression, and E2E testing | Continuous integration and test-driven development |

---

## 2. Comprehensive System Architecture

```text
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                 Complete Mitochondrial DNA Genome (FASTA)               │
  └─────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ LAYER 1: PRECISION LOCUS TARGETING (nhmmer / Heuristic Anchor)          │
  │ • nhmmer DNA profile search using 16s_probe.fasta                       │
  │ • Heuristic Fallback: Conserved 14-bp rRNA anchor (5'-GTTAATGTAGCTTA-3') │
  │ • Delimits MT-RNR2 search window (~1,600 bp vs ~17,000 bp whole genome) │
  └─────────────────────────────────────────────────────────────────────────┘
                                       │
                  ┌────────────────────┴────────────────────┐
                  ▼                                         ▼
  ┌─────────────────────────────────┐   ┌───────────────────────────────────┐
  │ LAYER 2A: CANONICAL sORF SCAN   │   │ LAYER 2B: MULTI-FRAME RESCUE      │
  │ • Strict ORFs: M[^*]{9,49}*     │   │ • 3 reading frames (0, 1, 2)      │
  │ • NCBI Genetic Tables 1 to 33   │   │ • Both strands (+1 and -1)        │
  │ • Standard Met initiation       │   │ • Sliding window (21 aa, step=3bp)│
  │ • Status: Canonical             │   │ • Status: Non-canonical / Pseudo  │
  └─────────────────────────────────┘   └───────────────────────────────────┘
                  │                                         │
                  └────────────────────┬────────────────────┘
                                       │
                                       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ LAYER 3: HYBRID AI EMBEDDING & SCORING ENGINE                           │
  │ 1. Deep Structural Embeddings (ESM-2 Transformer):                      │
  │    - 6 attention layers, 8M parameters (esm2_t6_8M_UR50D)               │
  │    - Masked Mean Pooling: Strips [PAD], <cls>, and <eos> tokens         │
  │    - Generates 320-dimensional contextual structural vector (v_ESM)     │
  │ 2. Biophysical Profiling:                                               │
  │    - Net Charge at pH 7.4 (Henderson-Hasselbalch)                       │
  │    - Isoelectric Point (pI)                                             │
  │    - Kyte-Doolittle Mean Hydrophobicity                                 │
  │    - Aliphatic Index (volume of Ala, Val, Ile, Leu)                     │
  │ 3. Machine Learning Classification:                                     │
  │    - Vector concatenation: x = [v_ESM || q || pI || H || AI] (324 dims) │
  │    - Calibrated RBF Support Vector Classifier with StandardScaler       │
  │    - Outputs posterior class probability: P(Humanin | x)                │
  └─────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ LAYER 4: ORTHOGONAL PROFILE HMM VALIDATION & PENALTY CALIBRATION        │
  │ • Translates 16S locus in 6 frames and queries humanin.hmm via hmmsearch│
  │ • Synergistic confidence boost (+0.15, max 0.99) for E-value < 0.1      │
  │ • Biological Penalty Modulation:                                        │
  │   - Canonical: 1.00x                                                    │
  │   - Non-canonical (alternative start): 0.95x                            │
  │   - Pseudogenic (nonsense stop mutation): 0.75x                         │
  └─────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │ LAYER 5: BIOLOGICAL NON-MAXIMUM SUPPRESSION (NMS) DEDUPLICATION         │
  │ • Sorts all candidates in descending order of final score               │
  │ • Discards candidate if coordinate overlap > 50% on the same strand     │
  │ • Hierarchy: Canonical > Non-canonical > Pseudogenic                    │
  │ • Output selection: Adaptive (Single Best Hit) or Exhaustive (Sorfome)  │
  └─────────────────────────────────────────────────────────────────────────┘
                                       │
                  ┌────────────────────┴────────────────────┐
                  ▼                                         ▼
  ┌─────────────────────────────────┐   ┌───────────────────────────────────┐
  │ LAYER 6: STRUCTURED OUTPUTS     │   │ LAYER 7: AUTONOMOUS RESEARCH AGENT│
  │ • CSV Table with coordinates,   │   │ • Local Ollama LLM integration   │
  │   scores, frames, and statuses  │   │ • Domain knowledge on BAX/IGFBP-3 │
  │ • Peptide FASTA alignment file  │   │ • Hypothesis & experiment synthesis│
  └─────────────────────────────────┘   └───────────────────────────────────┘
```

---

## 3. Algorithmic Specifications

### 3.1. Target Locus Localization (`find_16s_locus_precise`)

```text
Algorithm 1: Precision 16S Locus Detection
Input: Mitochondrial genome sequence G, core 16S DNA profile P (16s_probe.fasta)
Output: Search coordinates [start, end]

1. If nhmmer binary is present in PATH and P exists:
2.    Write G to temporary FASTA file T_in
3.    Execute: nhmmer --noali --tblout T_out P T_in
4.    Parse T_out to find hit with maximum bit score S_max
5.    If S_max > 50:
6.       ali_from = min(hit.start, hit.end)
7.       ali_to   = max(hit.start, hit.end)
8.       start = max(0, ali_from - 50)
9.       end   = min(len(G), ali_to + 50)
10.      Return [start, end]
11. Fallback heuristic:
12.   Scan G and reverse_complement(G) for anchor "GTTAATGTAGCTTA"
13.   If match at position pos:
14.      Return [pos, min(len(G), pos + 6000)] on matching strand
15. Default return: [1000, 5500]
```

### 3.2. Multi-Frame Evolutionary Sliding Window Rescue (`sliding_window_rescue`)

The standard ORF scanner only recognizes sequences between a Metionina (`M`) and a stop codon (`*`). In divergent taxa, mutations alter start codons or create premature stops. To detect these relics, the algorithm scans across all **three reading frames**:

```text
Algorithm 2: 3-Frame Evolutionary Window Rescue
Input: DNA sequence D, Genetic Code Table T (default: 2), Window Size W = 21, Step S = 3
Output: List of candidate peptide dictionaries

1. Initialize Candidates = []
2. For strand s in [+1, -1]:
3.    If s == +1: N = D
4.    Else:       N = reverse_complement(D)
5.    For frame f in {0, 1, 2}:
6.       For i = f to (len(N) - 3*W) with step S:
7.          sub_dna = N[i : i + 3*W]
8.          pep = translate(sub_dna, table=T)
9.          If '*' in pep:
10.            status = "Pseudogenic"
11.         Else if pep starts with 'M':
12.            status = "Canonical"
13.         Else:
14.            status = "Non-canonical"
15.         If s == +1:
16.            d_start = i;  d_end = i + 3*W
17.         Else:
18.            d_start = len(D) - (i + 3*W);  d_end = len(D) - i
19.         Append {seq: pep, start: d_start, end: d_end, strand: s, frame: f, status: status}
20. Return Candidates
```

### 3.3. Biological Non-Maximum Suppression (NMS)

```text
Algorithm 3: Biological Non-Maximum Suppression
Input: List of scored candidate dictionaries C, Overlap Threshold theta = 0.50
Output: Non-redundant candidate list NR

1. Sort C in descending order by final_score
2. Initialize NR = []
3. For each candidate cand in C:
4.    is_redundant = False
5.    For each accepted in NR:
6.       If cand.strand == accepted.strand:
7.          overlap_start = max(cand.start, accepted.start)
8.          overlap_end   = min(cand.end, accepted.end)
9.          If overlap_start < overlap_end:
10.            overlap_len = overlap_end - overlap_start
11.            If overlap_len > theta * (cand.end - cand.start):
12.               is_redundant = True
13.               Break
14.   If not is_redundant:
15.      Append cand to NR
16. Return NR
```

---

## 4. Machine Learning Model Training & Reproducibility Pipeline

The classification model in `src/humaninfinder/models/humanin_detector_hybrid.joblib` was trained via `training/train_model.py` following strict anti-leakage principles.

### 4.1. Training Datasets
- **Positive Class ($y = 1$):** 125 curated, non-redundant Humanin sequences (`training/datasets/humanin_pos.fasta`) representing validated mammalian orthologs, synthetic neuroprotective analogs (e.g., HNG, HNGF6A), and phylogenetically verified primate sequences.
- **Negative Class ($y = 0$):** 400 frozen Swiss-Prot peptide sequences (`training/datasets/negatives_frozen.fasta`) strictly matched in length (18–26 amino acids), comprising non-Humanin mitochondrial sORFs, ribosomal peptide fragments, and decoy sequences with similar amino acid composition.

### 4.2. Group-Aware Sequence Clustering (Anti-Data Leakage)
Standard random k-fold or train-test splits cause severe over-optimistic performance in biological ML because homologs with 90%+ sequence identity appear in both train and test partitions.
* **Deterministic 80% Identity Clustering:**
  Sequences are clustered using a pairwise sequence identity threshold of $\theta_{\text{id}} = 0.80$:
  $$\text{Similarity}(S_1, S_2) = \frac{2 \cdot M}{|S_1| + |S_2|} \ge 0.80$$
  where $M$ is the number of matching characters.
* **GroupShuffleSplit:**
  Clusters are treated as discrete atomic groups. A `GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)` guarantees that **entire clusters reside exclusively in either the training set (80%) or the test set (20%)**, forcing the model to generalize to novel sequence space.

### 4.3. Feature Engineering Pipeline ($\mathbb{R}^{324}$)

```text
Candidate Peptide Sequence
           │
           ├───────────────────────────────┬───────────────────────────────┐
           ▼                                                               ▼
[ Deep Structural Branch ]                                     [ Biophysical Branch ]
  Input: Strip '*' and 'X'                                       Input: Clean Peptide
  Tokenizer: esm2_t6_8M_UR50D                                    peptides library (pH 7.4)
  Attention Mask: input_mask                                     Calculations:
  Token Embeddings: H in R^(L x 320)                              1. Net Charge (q)
  Masked Mean Pooling (Drop <cls> & <eos>):                       2. Isoelectric Point (pI)
    v_ESM = sum(H * mask) / sum(mask)                            3. Kyte-Doolittle Hydrophobicity (H)
    v_ESM in R^(320)                                              4. Aliphatic Index (AI)
           │                                                               │
           └───────────────────────────────┬───────────────────────────────┘
                                           ▼
                 Concatenated Feature Vector: x in R^(324)
                                           │
                                           ▼
                        StandardScaler (zero-mean, unit-variance)
                                           │
                                           ▼
                     RBF Support Vector Classifier (SVC, C=2.0)
                                           │
                                           ▼
                          Posterior Probability: P(Humanin)
```

### 4.4. Model Hyperparameters & Deterministic Seeding
```python
# Fixed RNG Seeds for 100% Reproducibility
SEED = 42
os.environ['PYTHONHASHSEED'] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# Scaler and Estimator
scaler = StandardScaler()
clf = SVC(
    kernel='rbf',
    C=2.0,
    probability=True,
    class_weight='balanced',
    random_state=SEED
)
```

### 4.5. Test Partition Performance
Evaluated on the independent 20% test cluster partition:
- **Accuracy:** $> 98\%$
- **Positive Class Recall (Sensitivity):** $> 96\%$
- **Negative Class Specificity:** $> 99\%$
- **ROC-AUC:** $> 0.99$

---

## 5. Software Development, Packaging & Reproducibility

### 5.1. Repository Layout & Modular Design
```text
humanin-finder/
├── src/humaninfinder/          # Core Python Package
│   ├── __init__.py             # Package version declaration (v1.1.0)
│   ├── cli.py                  # Click CLI with subcommands: setup, predict, agent
│   ├── core.py                 # 16S targeting, sORF search, sliding window rescue
│   ├── classifier.py           # Hybrid AI Engine: ESM-2 pooling + biophysical inference
│   ├── agent.py                # Local Ollama AI Research Agent wrapper
│   ├── data/                   # Packaged biological assets: 16s_probe.fasta, humanin.hmm
│   └── models/                 # Pre-trained hybrid classifier: humanin_detector_hybrid.joblib
├── tests/                      # Pytest Test Suite
│   ├── test_cli.py             # CLI commands, argument parsing, end-to-end execution
│   ├── test_classifier.py      # AI model inference, embedding shapes, scoring sanity
│   └── test_discovery.py       # sORF finding, 3-frame rescue regression tests
├── conda/                      # Bioconda Packaging
│   └── meta.yaml               # Conda recipe with runtime dependencies
├── deploy/                     # Container Definitions
│   ├── Dockerfile              # Production OCI Docker container (Debian-based)
│   └── Singularity.def         # Singularity definition for HPC cluster environments
├── docs/                       # Technical Documentation
│   ├── README.md               # Documentation entry point
│   ├── architecture.md         # This comprehensive technical specification
│   ├── quickstart.md           # Getting started walkthrough
│   └── cli_reference.md        # Comprehensive CLI option reference
├── galaxy/                     # Galaxy Workflow Tool Wrapper
│   └── humaninfinder.xml       # Tool definition XML with inputs, outputs, and help
├── pyproject.toml              # PEP 517/518 build configuration, metadata, and dependencies
├── pixi.toml                   # Pixi environment specification
└── environment.yml             # Conda environment definition
```

### 5.2. Multi-Platform Delivery Channels

1. **PyPI (Python Package Index):**
   - Package builds binary wheel (`.whl`) and source distribution (`.tar.gz`) via `python -m build`.
   - Automated deployment to PyPI via GitHub Actions (`.github/workflows/publish.yml`) triggered on release tags (`v*`).
2. **Bioconda / Conda-Forge:**
   - Standalone recipe in `conda/meta.yaml` packages Python dependencies alongside native system binaries (`hmmer`).
3. **Containers (Docker / Singularity):**
   - `deploy/Dockerfile` builds an isolated container with PyTorch, ESM-2, HMMER, and the CLI.
   - `deploy/Singularity.def` enables rootless execution on high-performance computing (HPC) environments running SLURM or PBS.
4. **Galaxy Tool Shed:**
   - Standardized XML wrapper in `galaxy/humaninfinder.xml` enables graphical execution in web-based bioinformatics platforms.
