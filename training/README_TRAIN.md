# Model Training & Reproducibility

This folder contains the complete pipeline used to create the AI model for `HumaninFinder`.

## Contents
- `train_model.py`: The main training script (HMMer + ESM-2 + Biophysics).
- `datasets/`: 
    - `humanin_pos.fasta`: Curated positive sequences.
    - `negatives_ref.fasta`: Non-Humanin peptide sequences from Swiss-Prot.

## How to Replicate

To retrain the model and reproduce the results:

1.  Activate the environment:
    ```bash
    mamba activate humanin_env
    ```
2.  Run the training script:
    ```bash
    cd training/
    python train_model.py
    ```

The script will automatically use your GPU (if available) to extract ESM-2 embeddings and save the updated model to `src/humaninfinder/models/`.

## Logic
The training uses **Strict Group Splitting**. Sequences are clustered at 80% identity, and clusters are kept whole during the train/test split to prevent data leakage and ensure the model learns biological signatures rather than specific sequences.
