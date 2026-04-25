import torch
import numpy as np
import random
import os
import joblib
import peptides
from Bio import SeqIO
from transformers import AutoTokenizer, EsmModel
from sklearn.model_selection import GroupShuffleSplit
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from difflib import SequenceMatcher

# 1. TOTAL REPRODUCIBILITY SEEDS
SEED = 42
os.environ['PYTHONHASHSEED'] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# Config
script_dir = os.path.dirname(os.path.abspath(__file__))
MODEL_NAME = "facebook/esm2_t6_8M_UR50D"
POS_FASTA = os.path.join(script_dir, "datasets/humanin_pos.fasta")
NEG_FASTA = os.path.join(script_dir, "datasets/negatives_frozen.fasta")
IDENTITY_THRESHOLD = 0.8

def get_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def cluster_sequences(sequences, threshold):
    clusters = np.zeros(len(sequences), dtype=int)
    current_cluster = 1
    for i in range(len(sequences)):
        if clusters[i] == 0:
            clusters[i] = current_cluster
            for j in range(i + 1, len(sequences)):
                if get_similarity(sequences[i], sequences[j]) >= threshold:
                    clusters[j] = current_cluster
            current_cluster += 1
    return clusters

def get_physicochemical_features(seq):
    p = peptides.Peptide(seq.upper().replace("X", "").replace("*", ""))
    return [p.charge(pH=7.4), p.isoelectric_point(), p.hydrophobicity(), p.aliphatic_index()]

def get_hybrid_embeddings(sequences, model, tokenizer, device):
    model.eval()
    all_features = []
    with torch.no_grad():
        for seq in sequences:
            clean_seq = str(seq).upper().replace("X", "").replace("*", "")
            inputs = tokenizer(clean_seq, return_tensors="pt", padding=True, truncation=True).to(device)
            outputs = model(**inputs)
            esm_emb = outputs.last_hidden_state.mean(dim=1).cpu().numpy().flatten()
            bio_features = get_physicochemical_features(clean_seq)
            all_features.append(np.concatenate([esm_emb, bio_features]))
    return np.array(all_features)

def train():
    print(f"[*] Starting reproducible training (Seed: {SEED})")
    
    # Load frozen datasets
    pos_seqs = sorted(list(set(str(r.seq).upper() for r in SeqIO.parse(POS_FASTA, "fasta"))))
    neg_seqs = sorted(list(set(str(r.seq).upper() for r in SeqIO.parse(NEG_FASTA, "fasta"))))
    
    print(f"[*] Positives: {len(pos_seqs)} | Negatives: {len(neg_seqs)}")

    # Deterministic Clustering
    pos_clusters = cluster_sequences(pos_seqs, IDENTITY_THRESHOLD)
    neg_clusters = np.arange(len(pos_clusters) + 1, len(pos_clusters) + 1 + len(neg_seqs))

    X_all_seqs = pos_seqs + neg_seqs
    y = np.array([1] * len(pos_seqs) + [0] * len(neg_seqs))
    groups = np.concatenate([pos_clusters, neg_clusters])

    # Feature Extraction
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = EsmModel.from_pretrained(MODEL_NAME).to(device)
    X_hybrid = get_hybrid_embeddings(X_all_seqs, model, tokenizer, device)

    # Train/Test Split
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEED)
    train_idx, test_idx = next(gss.split(X_hybrid, y, groups=groups))

    X_train, X_test = X_hybrid[train_idx], X_hybrid[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    # Scaler and Classifier
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    clf = SVC(kernel='rbf', probability=True, class_weight='balanced', C=2.0, random_state=SEED)
    clf.fit(X_train_scaled, y_train)

    # Final validation print
    y_pred = clf.predict(X_test_scaled)
    print("\nDeterministic Evaluation:")
    print(classification_report(y_test, y_pred))

    # SAVE THE FINAL MODEL
    model_data = {
        'classifier': clf,
        'scaler': scaler,
        'model_name': MODEL_NAME,
        'features': 'hybrid_esm2_plus_bio',
        'seed': SEED,
        'software_versions': {
            'torch': torch.__version__,
            'sklearn': '1.8.0', # We fix this based on your env
            'numpy': np.__version__
        }
    }
    output_path = os.path.join(os.path.dirname(script_dir), "src/humaninfinder/models/humanin_detector_hybrid.joblib")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump(model_data, output_path)
    print(f"\n[REPRODUCIBILITY SUCCESS] Model saved to {output_path}")

if __name__ == "__main__":
    train()
