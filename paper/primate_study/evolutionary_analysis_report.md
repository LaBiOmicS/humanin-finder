# Evolutionary Dynamics of Humanin-like Peptides in Primates: A Hybrid AI Discovery Approach Across 343 Mitogenomes

**Authors:** Fabiano Bezerra Menegidio¹  
**Affiliation:** ¹LaBiOmicS, University of Mogi das Cruzes (UMC), Brazil  
**Date:** September 15, 2026  
**Dataset:** 343 complete primate mitochondrial genomes (*NCBI RefSeq/GenBank*)

---

## Abstract

Mitochondrial-derived peptides (MDPs), such as Humanin, play vital roles in cytoprotection, neuroprotection, and metabolic regulation. However, identifying their orthologs across divergent evolutionary lineages is challenging due to alternative initiation codons, frame drifts, and pseudogenic decay. Using `HumaninFinder` (v1.1.0)—a specialized framework coupling ESM-2 transformer embeddings with biophysical profiling and multi-frame evolutionary rescue—we conducted a comprehensive scan of **343 complete primate mitochondrial genomes** spanning all major lineages (Hominoidea, Cercopithecoidea, Platyrrhini, Strepsirrhini, and Tarsiiformes). 

`HumaninFinder` achieved a **100.0% detection rate** (343 out of 343 species). The biological distribution revealed **291 canonical loci (84.84%)**, **31 non-canonical loci (9.04%)**, and **21 pseudogenic relics (6.12%)**, with a mean confidence score of **0.927** (median: 0.990) and 278 high-confidence hits ($\ge 0.85$). We highlight the evolutionary trajectory of Humanin conservation, demonstrating absolute canonical invariance in Hominoidea (100%), gradual diversification in Old and New World monkeys, and lineage-specific pseudogenization in prosimians. Notably, in the giant mouse lemurs (*Mirza zaza* and *Mirza coquereli*), a point mutation converting codon 5 to `AGG` (a stop codon under the vertebrate mitochondrial code, Table 2) caused premature termination (`MATR*`); our multi-frame sliding-window rescue successfully identified this cryptic pseudogenic relic with high structural confidence (raw neural score: 0.973, penalized score: 0.742). These findings establish that the Humanin locus maintains robust structural signatures across the entire primate order, even in the presence of severe primary sequence decay.

---

## 1. Introduction

Humanin (HN) is a 21-amino acid cytoprotective peptide originally identified from a cDNA library of surviving neurons in patients with Alzheimer’s disease. It is transcribed from a short Open Reading Frame (sORF) nested within the mitochondrial 16S ribosomal RNA gene (*MT-RNR2*). Beyond its neuroprotective activity, Humanin functions systemically as an insulin sensitizer, an inhibitor of apoptosis via direct interaction with BAX and IGFBP-3, and a biomarker of metabolic fitness and longevity.

From an evolutionary standpoint, mitochondrial sORFs face unique selective pressures:
1. **Dual Coding Constraints:** The sequence overlaps functional secondary structures of the 16S rRNA.
2. **Alternative Initiation:** Mitochondrial translation frequently initiates at non-standard start codons (e.g., AUA, AUU, GUG).
3. **Pseudogenic Drift and Decay:** Nonsense mutations or small indels can disrupt translation while the surrounding locus retains structural or transcriptional activity.

Standard bioinformatics tools (e.g., blastp, rigid ORF finders) routinely fail to detect such divergent or damaged loci. `HumaninFinder` addresses these limitations through a **Hybrid AI Engine** combining protein language models (ESM-2) with biophysical descriptors, profile HMM genomic anchoring, and 3-frame evolutionary window rescue.

---

## 2. Materials and Methods

### 2.1. Dataset Composition
We compiled **343 complete primate mitochondrial genomes** from NCBI RefSeq and GenBank, curated with taxonomic metadata representing:
* **Hominoidea** (Apes & Humans): 33 species
* **Cercopithecoidea** (Old World Monkeys): 91 species
* **Platyrrhini** (New World Monkeys): 112 species
* **Strepsirrhini** (Lemurs, Lorises, Galagos): 91 species
* **Tarsiiformes** (Tarsiers): 6 species
* **Other Primates / Basal Taxa**: 10 species

### 2.2. Computational Pipeline (`HumaninFinder v1.1.0`)
Genomes were analyzed using the standard adaptive prediction pipeline with the following parameters:
- **Genetic Code:** NCBI Table 2 (Vertebrate Mitochondrial).
- **Locus Localization:** `nhmmer` alignment against a conserved 16S rRNA core probe to define the search window.
- **Candidate Generation:** Dual strategy utilizing:
  1. `find_sorfs`: Extraction of canonical ORFs ($M \dots *$, 10–50 aa).
  2. `sliding_window_rescue`: High-sensitivity 3-reading-frame scan ($21$ aa window, 3 bp step across frames 0, 1, and 2 on both strands) to capture non-canonical starts and internal stop mutations.
- **Hybrid AI Scoring:** Candidates were vectorized using ESM-2 (`esm2_t6_8M_UR50D`) masked mean-pooled embeddings and four biophysical metrics (charge at pH 7.4, isoelectric point, hydrophobicity, aliphatic index). A calibrated Extra Trees ensemble generated raw class probabilities.
- **Penalty & Selection:** Scores were modulated by biological category (Non-canonical: $0.95\times$; Pseudogenic: $0.75\times$) and boosted by profile HMM agreement ($+0.15$, max $0.99$). The highest-scoring candidate per species was selected.

---

## 3. Results

### 3.1. Global Detection and Classification
`HumaninFinder` identified Humanin-related loci in **343 of 343 species (100.0%)**:

| Status | Total Count | Proportion (%) | Biological Description |
| :--- | :---: | :---: | :--- |
| **Canonical** | **291** | **84.84%** | Intact 21–24 aa ORF starting with Met (ATG/ATA/ATT) and normal stop |
| **Non-canonical** | **31** | **9.04%** | Viable peptide lacking standard Met start, rescued by sliding window |
| **Pseudogenic** | **21** | **6.12%** | Disrupted sequence with internal stop codon(s) retaining AI structural signature |
| **Total** | **343** | **100.0%** | **Universal detection across the Primate order** |

- **Mean Confidence Score:** $0.927$
- **Median Confidence Score:** $0.990$
- **High-Confidence Hits ($\ge 0.85$):** $278$ species ($81.05\%$)

---

### 3.2. Taxonomic and Clade-Specific Dynamics

| Taxonomic Clado | Espécies Analisadas | Loci Detectados | Score Médio | Canônicos | Não-Canônicos | Pseudogenes |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Hominoidea** | 33 | 33 (100%) | **0.990** | 33 (100%) | 0 | 0 |
| **Cercopithecoidea** | 91 | 91 (100%) | **0.946** | 82 (90.1%) | 6 (6.6%) | 3 (3.3%) |
| **Platyrrhini** | 112 | 112 (100%) | **0.932** | 95 (84.8%) | 11 (9.8%) | 6 (5.4%) |
| **Strepsirrhini** | 91 | 91 (100%) | **0.885** | 69 (75.8%) | 11 (12.1%) | 11 (12.1%) |
| **Tarsiiformes** | 6 | 6 (100%) | **0.864** | 4 (66.7%) | 2 (33.3%) | 0 (0.0%) |
| **Outros Primatas** | 10 | 10 (100%) | **0.928** | 8 (80.0%) | 1 (10.0%) | 1 (10.0%) |

#### Key Clade Observations:
1. **Hominoidea:** Complete structural conservation. The sequence `MAPRGFSCLLLLTSEIDLPVK` (or identical single-point homologs) is 100% canonical with maximum model confidence ($0.990$).
2. **Cercopithecoidea:** High conservation ($90.1\%$ canonical). A small fraction exhibits N-terminal truncation or frame shifts rescued in non-canonical forms (e.g., *Colobus*, *Trachypithecus*).
3. **Platyrrhini:** Strong conservation ($84.8\%$ canonical), with widespread transition to the `MATRGFNCLL...` motif.
4. **Strepsirrhini:** The highest evolutionary plasticity. Approximately $24.2\%$ of prosimian species exhibit non-canonical or pseudogenic states, reflecting extensive divergence in the lemuriform radiation.

---

### 3.3. Case Study: Pseudogenization in Giant Mouse Lemurs (*Mirza*)

In prosimians of the genus *Mirza* (*Mirza zaza*, `NC_035606.1`; *Mirza coquereli*, `NC_035656.1`), the canonical Humanin ORF is interrupted by a premature stop mutation:

```text
Cheirogaleus crossleyi (Canonical, Score: 0.990):
  DNA:   ATG GCT ACA CGA GGT TTC AAC TGT CTC TTA CTT TTA ATC AGT GAA ATT GAC CTT CCC GTG AAG
  Prot:   M   A   T   R   G   F   N   C   L   L   L   L   I   S   E   I   D   L   P   V   K

Mirza zaza (Pseudogenic, Raw AI: 0.973, Final Score: 0.742):
  DNA:   ATG GCT ACA CGA AGG TTC AAC TGT CTC TTA CTT TCA GTC AGT GAA ATT GAC CTT CCC GTG AAG
  Prot:   M   A   T   R   *   F   N   C   L   L   L   S   V   S   E   I   D   L   P   V   K
                          ^
              Codon 5: GGA/GGT -> AGG (Stop codon in Table 2)
```

Because codon 5 mutated from Glycine (`GGT/GGA`) to `AGG` (which codes for Stop `*` in vertebrate mitochondrial translation), traditional ORF finders discard this locus as an unviable 4-amino acid fragment (`MATR*`). 

However, `HumaninFinder`'s multi-frame sliding window scan extracted the full 21-amino acid frame (`MATR*FNCLLLSVSEIDLPVK`). The ESM-2 hybrid classifier recognized the conserved biophysical and structural core (`FNCLLLSVSEIDLPVK`), awarding a raw neural probability of **97.3%**. With the pseudogenic penalty applied, the final confidence score reached **0.742**, successfully rescuing the locus as a bona fide pseudogene.

---

## 4. Discussion

### 4.1. Universal Evolutionary Retention of Humanin Architecture
Our analysis across 343 primate mitogenomes demonstrates that Humanin is universally present in primates. Even where point mutations disrupt the translation reading frame (such as in *Mirza* or *Lepilemur*), the underlying nucleotide region maintains the secondary and tertiary structural propensity recognized by ESM-2. This supports the hypothesis of a **"Mitochondrial Ghost Sorfome"**, where structural templates of cytoprotective peptides persist in non-coding or pseudogenic forms.

### 4.2. Methodological Implications: Beyond Rigid Sequence Identity
Homology searches based exclusively on BLAST or simple ORF thresholds miss up to $15.2\%$ of primate Humanin loci ($31$ non-canonical + $21$ pseudogenes = $52$ species). By combining machine learning embeddings, biophysical profiling, and comprehensive 3-frame evolutionary scanning, `HumaninFinder` recovers these otherwise hidden loci, providing an accurate, complete evolutionary map.

---

## 5. Availability and Reproducibility

- **Repository:** `https://github.com/LaBiOmicS/humanin-finder`
- **Results CSV:** [`analysis/results/primates_343_standard_results.csv`](file:///home/dayhoff/workdir/bioinformatics/humanin-finder/analysis/results/primates_343_standard_results.csv)
- **FASTA Alignments:** [`analysis/results/primates_343_standard_results.fasta`](file:///home/dayhoff/workdir/bioinformatics/humanin-finder/analysis/results/primates_343_standard_results.fasta)
- **Clade Summary Table:** [`analysis/reports/standard/summary_by_clade.csv`](file:///home/dayhoff/workdir/bioinformatics/humanin-finder/analysis/reports/standard/summary_by_clade.csv)
- **Summary Metrics JSON:** [`analysis/reports/standard/summary_metrics.json`](file:///home/dayhoff/workdir/bioinformatics/humanin-finder/analysis/reports/standard/summary_metrics.json)
