# Architecture & Technical Design

`HumaninFinder` is built on a modular, multi-layered architecture designed to solve a fundamental challenge in computational biology: **the identification of small Open Reading Frames (sORFs) across vast evolutionary distances where primary sequence identity decays, but structural and biophysical properties persist.**

---

## 🏗️ High-Level Architectural Diagram

```text
               +-------------------------------------------------------------+
               |             Input Mitochondrial Genome (FASTA)              |
               +-------------------------------------------------------------+
                                              |
                                              v
               +-------------------------------------------------------------+
               |            LAYER 1: Targeted 16S Locus Detection            |
               |  - nhmmer DNA/RNA profile alignment (16s_probe.fasta)       |
               |  - Heuristic fallback: conserved anchor 5'-GTTAATGTAGCTTA   |
               |  - Restricts 17 kbp genome to ~1.6 kbp MT-RNR2 search space |
               +-------------------------------------------------------------+
                                              |
                             +----------------+----------------+
                             |                                 |
                             v                                 v
               +----------------------------+   +----------------------------+
               | LAYER 2A: Canonical sORFs  |   | LAYER 2B: Evolutionary     |
               | - Regex: M[^*]{9,49}*      |   |   Rescue (Multi-frame)     |
               | - NCBI Tables 1 to 33      |   | - 3 reading frames (0, 1,2)|
               | - Standard Met initiation  |   | - Sliding window (21 aa)   |
               +----------------------------+   +----------------------------+
                             |                                 |
                             +----------------+----------------+
                                              |
                                              v
               +-------------------------------------------------------------+
               |               LAYER 3: Hybrid AI Scoring Engine             |
               |  +-------------------------------------------------------+  |
               |  |  Deep Structural Representation (ESM-2 Transformer)  |  |
               |  |  - Masked Mean-Pooled Embeddings (320 dimensions)     |  |
               |  +-------------------------------------------------------+  |
               |  |  Biophysical & Physicochemical Descriptors           |  |
               |  |  - Net Charge (pH 7.4) & Isoelectric Point (pI)       |  |
               |  |  - Kyte-Doolittle Hydrophobicity & Aliphatic Index    |  |
               |  +-------------------------------------------------------+  |
               |  |  Calibrated Extra Trees Ensemble Classifier           |  |
               |  |  - 100 randomized estimators, StandardScaler          |  |
               |  +-------------------------------------------------------+  |
               +-------------------------------------------------------------+
                                              |
                                              v
               +-------------------------------------------------------------+
               |            LAYER 4: Orthogonal Validation & Penalty         |
               |  - Profile HMM verification (hmmsearch against humanin.hmm) |
               |  - Synergistic boost (+0.15 for significant HMM hits)       |
               |  - Status weighting: Non-canonical (0.95x), Pseudogene(0.75x)|
               +-------------------------------------------------------------+
                                              |
                                              v
               +-------------------------------------------------------------+
               |     LAYER 5: Biological Non-Maximum Suppression (NMS)       |
               |  - Eliminates overlapping technical window artifacts (> 50%)|
               |  - Priority hierarchy: Canonical > Non-canonical > Pseudo   |
               |  - Output modes: Adaptive Best-Hit vs. Exhaustive Sorfome   |
               +-------------------------------------------------------------+
                                              |
                                              v
               +-------------------------------------------------------------+
               |            LAYER 6: Outputs & Expert AI Interpretation      |
               |  - Structured Tabular Output (.csv) & Peptide FASTA (.fasta)|
               |  - Built-in Local LLM Research Agent (via Ollama / Llama 3) |
               +-------------------------------------------------------------+
```

---

## 🔍 Detailed Component Walkthrough

### 1. Layer 1: Precision 16S Locus Targeting (`find_16s_locus_precise`)

Scanning an entire 16,000–17,000 bp mitochondrial genome across 6 reading frames generates thousands of spurious open reading frames that clutter classifier inference. Humanin is known biologically to reside exclusively within the mitochondrial 16S ribosomal RNA gene (*MT-RNR2*).

* **Profile HMM DNA Alignment:** Using `nhmmer` (from the HMMER3 suite), the genome is scanned against a curated DNA profile of the 16S rRNA core (`src/humaninfinder/data/16s_probe.fasta`).
* **Coordinate Extraction:** The best alignment ($S > 50$) defines the locus boundaries with a 50 bp buffer, reducing the search space from ~17,000 bp down to ~1,600 bp.
* **Resilient Heuristic Fallback:** If `nhmmer` is unavailable or the genome is highly divergent, the tool automatically scans for the ultraconserved oligonucleotide anchor:
  $$\text{5'-GTTAATGTAGCTTA-3'}$$
  If found, an extended window of 6,000 bp downstream is targeted. If no anchor matches, a default window (bp 1,000–5,500) is used.

---

### 2. Layer 2: Dual Candidate Extraction Engine

Humanin orthologs exhibit diverse translational behaviors across the tree of life:

#### A. Canonical sORF Scanning (`find_sorfs`)
* Scans both forward ($+1$) and reverse-complement ($-1$) strands under the specified NCBI translation table (supporting **Tables 1 through 33**; default: **Table 2 - Vertebrate Mitochondrial**).
* Identifies strict open reading frames starting with Met (`M`), containing no internal stops, and ending with a stop codon (`*`), with lengths between 10 and 50 amino acids.
* Labeled as **`Canonical`**.

#### B. Multi-Frame Evolutionary Sliding Window Rescue (`sliding_window_rescue`)
Standard ORF finders miss sequences with alternative initiation codons (e.g., AUA, AUU, GUG) or pseudogenes that have sustained premature nonsense mutations (e.g., codon 5 mutating to `AGG`, which is a Stop codon in vertebrate mitochondria).
* **3-Frame Systematic Iteration:** Iterates through all **three reading frames** ($f \in \{0, 1, 2\}$) on both strands ($\pm 1$):
  $$i_{s, f, k} = f + 3k \quad \text{where } k \in \mathbb{N}_0, \quad i + 63 \le L_{\text{locus}}$$
* **Fixed Window Size:** Evaluates $21$ amino acid windows ($63$ nucleotides), stepping by $3$ nucleotides (codon-by-codon).
* **Heuristic Biological Labeling:**
  * **`Pseudogenic`**: Contains one or more internal stop codons (`*`).
  * **`Canonical`**: Begins with Met (`M`) and contains no internal stops.
  * **`Non-canonical`**: Does not begin with Met (`M`) and contains no internal stops (rescuing alternative starts).

---

### 3. Layer 3: Hybrid AI Scoring Engine (`HumaninClassifier`)

The classifier combines deep language model representations with explicit biophysical profiling to form a 324-dimensional feature vector $\mathbf{x} \in \mathbb{R}^{324}$.

#### A. Deep Structural Embeddings (ESM-2 Transformer)
* Utilizes Meta AI's **ESM-2** (`esm2_t6_8M_UR50D`, 8 million parameters, 6 layers, embedding dimension $d=320$).
* **Masked Mean Pooling:** To ensure unbiased representations, special delimiter tokens (`<cls>` and `<eos>`) and padding tokens (`[PAD]`) are excluded from pooling:
  $$\mathbf{v}_{\text{ESM}} = \frac{\sum_{t=1}^{T} m_t \cdot \mathbf{h}_t}{\sum_{t=1}^{T} m_t}$$
  where $m_t$ is the attention mask and $\mathbf{h}_t$ is the token representation in the final transformer layer.
* **Pseudogene Normalization:** Stop codons (`*`) and ambiguous letters (`X`) are temporarily stripped during tokenization to enable seamless transformer inference.

#### B. Biophysical & Physicochemical Profiling
Four analytical properties known to govern Humanin's amphipathic alpha-helical structure and membrane/receptor interaction are computed:
1. **Net Charge ($q$):** At physiological pH ($7.4$) via Henderson-Hasselbalch with Lehninger $pK_a$ values.
2. **Isoelectric Point ($pI$):** The pH at which net charge is zero.
3. **Mean Hydrophobicity ($H$):** Kyte-Doolittle scale average.
4. **Aliphatic Index ($AI$):** Relative volume occupied by aliphatic side chains (Ala, Val, Ile, Leu).

$$\mathbf{x} = \left[ \mathbf{v}_{\text{ESM}} \,\|\, q \,\|\, pI \,\|\, H \,\|\, AI \right] \in \mathbb{R}^{324}$$

#### C. Ensemble Classifier
* A calibrated **Extra Trees Classifier** (100 estimators) trained on experimental and synthetic Humanin orthologs contrasted against length-matched mitochondrial background noise.
* Outputs the raw posterior probability $P_{\text{AI}} \in [0.0, 1.0]$.

---

### 4. Layer 4: Orthogonal Profile HMM & Score Calibration

1. **Profile HMM Verification:** In parallel, the translated locus is scanned using `hmmsearch` against `humanin.hmm`. Candidates matching the HMM profile ($E < 0.1$) receive an additive confidence boost:
   $$\text{Score}_{\text{base}} = \min(0.99, \, P_{\text{AI}} + 0.15)$$
2. **Biological Penalty Weighting:** To account for translational uncertainty while preserving structural value:
   $$\text{Score}_{\text{final}} = \begin{cases}
   \text{Score}_{\text{base}}, & \text{Canonical} \\
   \text{Score}_{\text{base}} \times 0.95, & \text{Non-canonical} \\
   \text{Score}_{\text{base}} \times 0.75, & \text{Pseudogenic}
   \end{cases}$$

---

### 5. Layer 5: Biological Non-Maximum Suppression (NMS)

Because a sliding window with a 3 bp step produces overlapping variants of the same biological locus:
* Candidates are sorted by $\text{Score}_{\text{final}}$ in descending order.
* Any lower-scoring candidate sharing **$> 50\%$ coordinate overlap on the same strand** with an accepted candidate is suppressed.
* **Adaptive Mode:** Selects the top non-redundant candidate per species ($\ge 0.70$, fallback $\ge 0.50$).
* **Exhaustive Mode (`--all-candidates`):** Retains all independent non-redundant loci exceeding the threshold, generating a comprehensive mitochondrial "sorfome".

---

### 6. Layer 6: Offline AI Research Agent (`humaninfinder agent`)

An integrated scientific reasoning agent connects directly to local LLMs (via **Ollama**, e.g., Llama 3):
* Operates 100% locally and offline—no external API keys or cloud dependencies.
* Loaded with domain-specific knowledge on Humanin's interactions with BAX, IGFBP-3, gp130/WSX-1/CNTFR receptor complexes, and longevity genetics.
* Automatically synthesizes results tables into biological hypotheses and suggests experimental validations.
