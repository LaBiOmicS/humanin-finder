# Primate Evolution Case Study Data

This directory contains the supplementary data for the primate evolution case study performed with `HumaninFinder`.

## Files

- `evolutionary_analysis_report.md`: Complete scientific report detailing the findings, methodology, and evolutionary discussion.
- `full_primate_study_results.csv`: Standard analysis results containing the best Humanin candidate for each of the 61 primate genomes.
- `full_primate_study_results.fasta`: Peptide sequences of the candidates in the standard analysis.
- `full_primate_study_all_results.csv`: Exhaustive non-redundant analysis containing all independent Humanin-like loci (Canonical, Non-canonical, and Pseudogenic) identified across the genomes.
- `full_primate_study_all_results.fasta`: Peptide sequences of all candidates in the exhaustive analysis.

## Reproduction

To reproduce these results, run the following command from the project root:

```bash
bash run_final_analysis.sh
```

## Data Integrity

Verification hashes (SHA256) are provided in the `checksums.txt` file at the root of the repository.
