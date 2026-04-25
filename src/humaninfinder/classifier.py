import logging
import os
import warnings

import joblib
import numpy as np
import peptides
import torch
from transformers import AutoTokenizer, EsmModel
from transformers import logging as transformers_logging

# Silence warnings
warnings.filterwarnings("ignore")
transformers_logging.set_verbosity_error()
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

# Extra silence for HF Hub
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)


class HumaninClassifier:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = os.path.join(os.path.dirname(__file__), "models/humanin_detector_hybrid.joblib")

        self.data = joblib.load(model_path)
        self.clf = self.data["classifier"]
        self.scaler = self.data["scaler"]
        self.model_name = self.data["model_name"]

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.esm_model = EsmModel.from_pretrained(self.model_name).to(self.device)
        self.esm_model.eval()

    def get_physicochemical_features(self, seq):
        p = peptides.Peptide(seq.upper().replace("X", "").replace("*", ""))
        return [p.charge(pH=7.4), p.isoelectric_point(), p.hydrophobicity(), p.aliphatic_index()]

    def predict(self, sequences, batch_size=32):
        if not sequences:
            return []

        # Unique sequences only to speed up ESM-2
        unique_seqs = list(set(str(s).upper().replace("X", "").replace("*", "") for s in sequences))
        seq_to_score = {}

        for i in range(0, len(unique_seqs), batch_size):
            batch = unique_seqs[i : i + batch_size]
            features = []

            with torch.no_grad():
                inputs = self.tokenizer(batch, return_tensors="pt", padding=True, truncation=True).to(self.device)
                outputs = self.esm_model(**inputs)

                # Masked Mean Pooling: Ignore padding tokens in the average
                attention_mask = inputs["attention_mask"]  # (batch, seq_len)
                token_embeddings = outputs.last_hidden_state  # (batch, seq_len, hidden_dim)

                # Expand mask for element-wise multiplication
                input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()

                # Sum embeddings, ignoring pads, then divide by actual sequence length
                # We also exclude the first (<cls>) and last (<eos>) tokens for a pure protein signature
                # by zeroing them out in the mask
                input_mask_expanded[:, 0, :] = 0  # Remove <cls>
                for b_idx in range(len(batch)):
                    # Find last non-pad token index
                    last_idx = attention_mask[b_idx].nonzero()[-1].item()
                    input_mask_expanded[b_idx, last_idx, :] = 0  # Remove <eos>

                sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
                sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
                esm_embeddings = (sum_embeddings / sum_mask).cpu().numpy()

                for j, seq in enumerate(batch):
                    bio_features = self.get_physicochemical_features(seq)
                    features.append(np.concatenate([esm_embeddings[j], bio_features]))

            X = np.array(features)
            X_scaled = self.scaler.transform(X)
            probs = self.clf.predict_proba(X_scaled)[:, 1]

            for j, seq in enumerate(batch):
                seq_to_score[seq] = probs[j]

        # Map back to original order
        final_probs = [seq_to_score.get(str(s).upper().replace("X", "").replace("*", ""), 0.0) for s in sequences]
        return np.array(final_probs)
