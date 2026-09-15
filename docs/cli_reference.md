# CLI Reference

`HumaninFinder` provides three main subcommands: `setup`, `predict`, and `agent`.

---

## `humanin-finder setup`
Validates that external binaries (HMMER3 / `hmmsearch`, `nhmmer`) and deep learning dependencies are correctly configured in your environment.

```bash
humanin-finder setup
```

---

## `humanin-finder predict`
Performs sORF discovery, evolutionary rescue, and hybrid AI classification on mitochondrial FASTA sequences.

```bash
humanin-finder predict [OPTIONS]
```

### Options:
- `-i, --input PATH`: Path to input multi-FASTA file (required).
- `-o, --output TEXT`: Output prefix for resulting CSV and FASTA files (required).
- `-t, --threshold FLOAT`: Confidence threshold between 0.0 and 1.0 (default: `0.7`).
- `-g, --table INTEGER`: NCBI genetic translation table (default: `2` - Vertebrate Mitochondrial).
- `--hmm`: Enable profile HMM-based locus localization and orthogonal scoring bonus.
- `--rescue`: Enable evolutionary rescue mode (sliding-window scan for non-canonical starts and pseudogenes).
- `-c, --cpus INTEGER`: Number of CPU workers for parallel genome processing (default: all CPUs).
- `--all-candidates`: Output all non-redundant candidates, rather than only the top candidate per genome.

---

## `humanin-finder agent`
Interprets discovery results using a local LLM via Ollama with specialized scientific context in mitochondrial biology and aging.

```bash
humanin-finder agent [OPTIONS]
```

### Options:
- `-r, --results PATH`: Path to results CSV file (required).
- `-m, --model TEXT`: Ollama model to use (default: `llama3`).
- `-q, --query TEXT`: Optional custom scientific question about the results.
