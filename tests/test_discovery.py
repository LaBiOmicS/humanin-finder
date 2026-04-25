import pytest
from Bio.Seq import Seq
from humaninfinder.core import find_sorfs, sliding_window_rescue, find_16s_locus_precise

def test_find_sorfs_canonical():
    # Humanin canonical sequence (H. sapiens)
    dna = Seq("ATGGCCACCCGAGGTTTCAGCTGTCTCTTACTTTTAACCAGTGAAATTGACCTGCCCGTGAAGTAA")
    results = find_sorfs(dna, table=2)
    assert len(results) >= 1
    assert results[0]['status'] == 'Canonical'
    assert results[0]['seq'].startswith('M')

def test_sliding_window_rescue_logic():
    # Sequence with a stop codon in the middle (Pseudogenic candidate)
    dna = Seq("ATGGCCACCCGAGGTTTCAGCTGTTAGCTTACTTTTAACCAGTGAAATTGACCTGCCCGTGAAG")
    # TAA (Stop) inserted at pos 33-35
    results = sliding_window_rescue(dna, window_size=21, step=3)
    
    # Check if any candidate is marked as Pseudogenic
    pseudogenes = [r for r in results if r['status'] == 'Pseudogenic']
    assert len(pseudogenes) > 0
    assert "*" in pseudogenes[0]['seq']

def test_non_canonical_detection():
    # Sequence starting without M (Non-canonical candidate)
    dna = Seq("GGCACCCGAGGTTTCAGCTGTCTCTTACTTTTAACCAGTGAAATTGACCTGCCCGTGAAGTAA")
    results = sliding_window_rescue(dna, window_size=20, step=3)
    
    non_canonical = [r for r in results if r['status'] == 'Non-canonical']
    assert len(non_canonical) > 0
    assert not non_canonical[0]['seq'].startswith('M')
    assert "*" not in non_canonical[0]['seq']

def test_16s_locus_fallback():
    # Test if locus detection returns coordinates even with random DNA
    dna = Seq("A" * 10000)
    start, end = find_16s_locus_precise(dna, probe_path="non_existent.fasta")
    assert start < end
    assert start >= 0
    assert end <= 10000
