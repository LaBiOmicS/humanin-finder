# Examples & Datasets

This directory contains reference mitogenomic datasets for quick-start discovery and reproduction:

- `test_sample.fasta`: Complete mitochondrial genome of *Propithecus verreauxi coquereli* (NCBI: AB286049.1), ideal for quick validation runs.
- `full_primates_collection.fasta`: Consolidated collection of 61 complete primate mitochondrial genomes representing Hominoids, Old World Monkeys, New World Monkeys, and Prosimians.

### Quick Usage:
```bash
# Run prediction on the single test sample
humanin-finder predict -i examples/test_sample.fasta -o results/propithecus --hmm --rescue

# Run prediction across all 61 primates
humanin-finder predict -i examples/full_primates_collection.fasta -o results/all_primates --hmm --rescue
```
