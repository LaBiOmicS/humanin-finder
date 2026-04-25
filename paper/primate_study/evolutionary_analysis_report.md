# Evolutionary Dynamics of Humanin-like Peptides in Primates: A Hybrid AI Discovery Approach

**Authors:** Fabiano Bezerra Menegidio¹  
**Affiliation:** ¹LaBiOmicS, University of Mogi das Cruzes (UMC), Brazil  
**Date:** April 25, 2026

---

## Abstract
Mitochondrial-derived peptides (MDPs), such as Humanin, play a vital role in cytoprotection and metabolic regulation. However, their identification across divergent lineages is hampered by non-canonical translation signals and pseudogenic decay. Using `HumaninFinder`, we analyzed 61 primate mitochondrial genomes through a Hybrid AI Engine (ESM-2 embeddings + biophysical properties). We identified a high conservation of canonical Humanin in Hominidae and successfully "rescued" hundreds of non-canonical and pseudogenic relics in more distant lineages. Our results demonstrate that the Humanin locus is an evolutionary hotspot, maintaining structural signatures even when traditional ORF-finding methods fail.

---

## 1. Introduction
Humanin (HN) is a 21-amino acid peptide encoded within the mitochondrial 16S rRNA gene (MT-RNR2). Since its discovery, HN has been recognized for its neuroprotective effects against Alzheimer’s disease and its role as a systemic metabolic regulator. Evolutionarily, small Open Reading Frames (sORFs) like HN are subject to intense selective pressures, leading to "evolutionary tuning" where the peptide sequence adapts to the metabolic needs of the species.

Traditional bioinformatics tools often miss these sequences due to:
1.  **Alternative Start Codons:** Frequent use of GTG or ATT in mitochondria.
2.  **Degeneracy:** Mutilated sequences (pseudogenes) that still retain functional or structural relevance in evolutionary studies.

This study utilizes `HumaninFinder` to map the evolutionary trajectory of Humanin across the primate order, providing a comprehensive view of its conservation and decay.

---

## 2. Methodology
We analyzed **61 complete mitochondrial genomes** representing the major primate clades (Hominoids, Old World Monkeys, New World Monkeys, and Prosimians).

### 2.1. Hybrid AI Engine
The detection followed a three-layered approach:
*   **Structural Layer:** Mean-pooled embeddings from the ESM-2 transformer model (`esm2_t6_8M_UR50D`) to capture the "structural fingerprint" of the peptide.
*   **Biophysical Layer:** Explicit calculation of Charge, Isoelectric Point (pI), and Hydrophobicity.
*   **HMM Layer:** HMMER3-based localization of the 16S rRNA locus to provide genomic context.

### 2.2. Discovery Modes
Two analysis modes were employed:
1.  **Adaptive Selection:** Identification of the most viable (canonical) candidate per species.
2.  **Exhaustive Rescue:** An all-candidate sliding window scan to detect non-canonical starts and pseudogenic relics (internal stops).

---

## 3. Results

### 3.1. Taxonomic Distribution and Conservation
Across the 61 primate mitochondrial genomes, `HumaninFinder` identified a functional or vestigial Humanin signal in 100% of the samples. The distribution of classes revealed a clear evolutionary gradient:

#### 3.1.1. Standard Mode (Best Candidate Selection)
In the primary analysis (one best candidate per species), the tool achieved the following distribution:
*   **Canonical (90.16%, n=55):** Predominant in Hominidae (Great Apes) and most Cercopithecidae. These sequences maintain a perfect 21-AA ORF with scores averaging **0.942**.
*   **Non-canonical (9.84%, n=6):** Identified in lineages where the primary start codon was substituted (e.g., *AB371092.1* and *AJ309866.1*). These "rescued" sequences maintained high AI confidence scores (**>0.910**), despite being invisible to standard ORF-finding algorithms.

#### 3.1.2. Exhaustive Mode (The Non-Redundant Mitochondrial Sorfome)
By applying a **Non-Redundant Overlap Filter** (discarding candidates with >50% overlap on the same strand), we identified a refined landscape of **5,198 independent loci** across the 61 genomes:
*   **Pseudogenic (53.61%, n=2,787):** These represent true evolutionary relics—genomic regions that maintain a structural Humanin signature (ESM-2) but contain internal stop codons or frame-shift mutations.
*   **Non-canonical (11.70%, n=608):** Independent alternative loci or frames that lack standard start/stop signals but are recognized as viable peptides by the Hybrid AI Engine.
*   **Canonical (34.69%, n=1,803):** High-confidence ORFs, including the primary Humanin sequence and other structurally similar segments within the mitochondrial genome.

### 3.2. Detailed Findings by Clade
*   **Hominoids:** Showed the highest stability. The sequence `MAPRGFSCLLLLTSEIDLPVK` was invariant in 95% of the samples, with a mean score of **0.990**.
*   **New World Monkeys (Platyrrhines):** Displayed increased variance in the N-terminal region, often shifting to `MATR...` variants, successfully captured by the AI engine.
*   **Prosimians:** Represented the most challenging cases. In species like *Lemur catta*, the HMM locus was identified, but the functional peptide was often only detectable through the **Evolutionary Rescue Mode**, showing scores between **0.75 and 0.82**.

---

## 4. Discussion

### 4.1. From Fragments to Loci: Biological Validity
The implementation of a non-redundant filter was essential to distinguish biological reality from technical artifacts. Initial raw scans produced over 66,000 overlapping fragments; however, our refined analysis shows that primates harbor approximately 85 independent "Humanin-like" structural signals per mitochondrial genome. 

The fact that over 50% of these signals are **Pseudogenic** highlights the "Mitochondrial Ghost" phenomenon: the mitochondrial genome retains structural archetypes of protective peptides even when they are no longer actively translated. This suggests a reservoir of evolutionary potential where pseudogenes could be "re-activated" through minimal mutational events.

### 4.2. Structural vs. Sequence Conservation
Our data shows that while the DNA sequence of the Humanin locus may drift (especially in Prosimians), the **structural signature** remains remarkably stable. The ~2,700 pseudogenic signals found indicate that the 16S rRNA gene maintains a "protein-like" structural environment that favors the existence of Humanin-like embeddings, even if the translation is suppressed.

---

## 5. Conclusion
`HumaninFinder` represents a paradigm shift in sORF discovery. By integrating deep learning with biophysical analysis, we provided the first exhaustive map of Humanin evolution in primates. Our findings confirm that Humanin is not just a single peptide, but a family of structural signatures that evolve along a spectrum of functionality—from perfectly conserved canonical ORFs to non-canonical variants and pseudogenic relics. This work provides the foundation for exploring the "mitochondrial sorfome" in other taxonomic groups.

---
## References
*   Lin, Z., et al. (2023). Evolutionary-scale prediction of atomic-level protein structure with a language model. *Science*.
*   Lee, C., et al. (2016). The mitochondrial-derived peptide humanin protects against amyloid-beta neurotoxicity. *Journal of Biological Chemistry*.
*   Eddy, S. R. (2011). Accelerated Profile HMM Searches. *PLOS Computational Biology*.
