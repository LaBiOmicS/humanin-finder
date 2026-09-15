import pytest
import numpy as np
from humaninfinder.classifier import HumaninClassifier


@pytest.fixture(scope="module")
def classifier():
    return HumaninClassifier()


def test_classifier_initialization(classifier):
    assert classifier.clf is not None
    assert classifier.scaler is not None
    assert classifier.tokenizer is not None
    assert classifier.esm_model is not None


def test_physicochemical_features(classifier):
    seq = "MAPRGFSCLLLLTSEIDLPVKRRA"
    features = classifier.get_physicochemical_features(seq)
    assert len(features) == 4
    # features: [charge(pH=7.4), pI, hydrophobicity, aliphatic_index]
    assert all(isinstance(f, (int, float, np.floating)) for f in features)
    assert features[1] > 0  # pI > 0
    assert features[3] > 0  # aliphatic index > 0


def test_predict_canonical_humanin(classifier):
    # Canonical human Humanin sequence (24-AA)
    humanin_24 = "MAPRGFSCLLLLTSEIDLPVKRRA"
    # Canonical human Humanin sequence (21-AA)
    humanin_21 = "MAPRGFSCLLLLTSEIDLPVK"

    probs = classifier.predict([humanin_24, humanin_21])
    assert len(probs) == 2
    assert probs[0] > 0.80, f"Expected high probability for canonical 24-AA Humanin, got {probs[0]}"
    assert probs[1] > 0.80, f"Expected high probability for canonical 21-AA Humanin, got {probs[1]}"


def test_predict_negative_sequence(classifier):
    # Unrelated peptides
    negatives = [
        "AAAAAAAAAAAAAA",
        "KKKKRRRRKKKKRRRR",
        "WEEEDDDEEEDDDW",
    ]
    probs = classifier.predict(negatives)
    assert len(probs) == 3
    for p in probs:
        assert p < 0.50, f"Expected low probability for negative control, got {p}"


def test_predict_edge_cases(classifier):
    # Empty list
    assert len(classifier.predict([])) == 0

    # Sequences with stop codon (*) or unknown amino acids (X)
    seqs_with_special = ["MAPRGFSCLLLL*TSEIDLPVK", "MAPRGFSCLLLLXTSEIDLPVK"]
    probs = classifier.predict(seqs_with_special)
    assert len(probs) == 2
    assert probs[0] > 0.5
