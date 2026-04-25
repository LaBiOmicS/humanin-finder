import re
import subprocess
import tempfile
import os
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.Data import CodonTable

def find_sorfs(seq, table=1, min_len=10, max_len=50):
    """
    Finds small ORFs (sORFs) in a DNA sequence.
    Canonical: M...*
    """
    sorfs = []
    for strand, nuc in [(1, seq), (-1, seq.reverse_complement())]:
        for frame in range(3):
            nuc_frame = nuc[frame:]
            trim_len = (len(nuc_frame) // 3) * 3
            trans = nuc_frame[:trim_len].translate(table=table)
            
            # Find all ORFs (between M and *)
            for match in re.finditer(r'M[^*]{%d,%d}\*' % (min_len-1, max_len-1), str(trans)):
                start_aa = match.start()
                end_aa = match.end()
                
                # DNA coordinates (0-based)
                start_dna = (start_aa * 3) + frame
                end_dna = (end_aa * 3) + frame
                
                if strand == 1:
                    d_start, d_end = start_dna, end_dna
                else:
                    d_end = len(seq) - start_dna
                    d_start = len(seq) - end_dna
                
                sorfs.append({
                    'seq': str(match.group()[:-1]), # Remove *
                    'start': d_start,
                    'end': d_end,
                    'strand': strand,
                    'frame': frame,
                    'status': 'Canonical'
                })
    return sorfs

def sliding_window_rescue(seq, table=1, window_size=21, step=3, target_strand=None):
    """
    High-sensitivity scan for non-canonical or pseudogenic peptides.
    target_strand: if provided, only scan that strand (1 or -1).
    """
    candidates = []
    win_bp = window_size * 3
    
    strands = [(1, seq), (-1, seq.reverse_complement())]
    if target_strand is not None:
        if target_strand == 1:
            strands = [(1, seq)]
        else:
            strands = [(-1, seq.reverse_complement())]

    for strand, nuc in strands:
        for i in range(0, len(nuc) - win_bp + 1, step):
            sub_dna = nuc[i:i+win_bp]
            pep = str(sub_dna.translate(table=table))
            
            # Status classification
            if "*" in pep:
                status = "Pseudogenic"
            elif pep.startswith("M"):
                status = "Canonical"
            else:
                status = "Non-canonical"
            
            if strand == 1:
                d_start, d_end = i, i + win_bp
            else:
                d_end = len(seq) - i
                d_start = len(seq) - (i + win_bp)
                
            candidates.append({
                'seq': pep,
                'start': d_start,
                'end': d_end,
                'strand': strand,
                'frame': i % 3,
                'status': status
            })
    return candidates

def run_hmm_search(dna_seq, hmm_path, table=2):
    """
    Translates DNA in 6 frames and runs hmmsearch.
    Returns regions (start, end, strand) with significant hits.
    """
    if not os.path.exists(hmm_path):
        return []

    hits = []
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False) as tmp_in:
        # Translate 6 frames
        for strand, nuc in [(1, dna_seq), (-1, dna_seq.reverse_complement())]:
            for frame in range(3):
                nuc_frame = nuc[frame:]
                trim_len = (len(nuc_frame) // 3) * 3
                trans = nuc_frame[:trim_len].translate(table=table)
                tmp_in.write(f">strand{strand}_frame{frame}\n{trans}\n")
        tmp_in_path = tmp_in.name

    tmp_out = tempfile.NamedTemporaryFile(suffix='.tbl', delete=False).name
    
    try:
        cmd = ["hmmsearch", "--noali", "--tblout", tmp_out, hmm_path, tmp_in_path]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Parse tblout
        with open(tmp_out, 'r') as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.split()
                if len(parts) < 18:
                    continue
                
                # In hmmsearch tblout:
                # parts[0]: target name (strandX_frameY)
                # parts[4]: E-value
                # parts[5]: score
                target_name = parts[0]
                e_value = float(parts[4])
                score = float(parts[5])
                
                if e_value < 0.1: # Reasonable threshold for localization
                    m = re.match(r"strand(-?\d)_frame(\d)", target_name)
                    if m:
                        strand = int(m.group(1))
                        frame = int(m.group(2))
                        hits.append({
                            'strand': strand,
                            'frame': frame,
                            'score': score,
                            'e_value': e_value
                        })
    finally:
        if os.path.exists(tmp_in_path): os.remove(tmp_in_path)
        if os.path.exists(tmp_out): os.remove(tmp_out)
        
    return hits

def find_16s_locus(dna_seq):
    """
    Locates the 16S rRNA gene region using conserved anchors.
    Returns (start, end) or a default range if anchor not found.
    """
    anchor = "GTTAATGTAGCTTA"
    for strand, seq in [(1, dna_seq), (-1, dna_seq.reverse_complement())]:
        match = re.search(anchor, str(seq))
        if match:
            pos = match.start()
            if strand == 1:
                return max(0, pos), min(len(dna_seq), pos + 6000)
            else:
                start_global = len(dna_seq) - (pos + 6000)
                end_global = len(dna_seq) - pos
                return max(0, start_global), min(len(dna_seq), end_global)
    return 1000, 5500

def find_16s_locus_precise(dna_seq, probe_path="16s_probe.fasta"):
    """
    Uses nhmmer to find the exact boundaries of the 16S rRNA gene.
    Returns (start, end) of the detected 16S gene.
    """
    if not os.path.exists(probe_path):
        # Fallback to the anchor-based method if probe is missing
        return find_16s_locus(dna_seq)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False) as tmp_in:
        tmp_in.write(f">query\n{dna_seq}\n")
        tmp_in_path = tmp_in.name

    tmp_out = tempfile.NamedTemporaryFile(suffix='.tbl', delete=False).name
    
    try:
        # nhmmer is specialized for DNA/RNA sequence search
        cmd = ["nhmmer", "--noali", "--tblout", tmp_out, probe_path, tmp_in_path]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        
        # Parse nhmmer tblout to find the best hit
        best_hit = None
        with open(tmp_out, 'r') as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                parts = line.split()
                # nhmmer tblout format:
                # target name [0], query name [2], alifrom [6], alito [7], evalue [12], score [13]
                score = float(parts[13])
                start = int(parts[6])
                end = int(parts[7])
                
                if best_hit is None or score > best_hit['score']:
                    best_hit = {'start': min(start, end), 'end': max(start, end), 'score': score}
        
        if best_hit and best_hit['score'] > 50: # Threshold for a valid 16S hit
            # Return coordinates with a small buffer
            return max(0, best_hit['start'] - 50), min(len(dna_seq), best_hit['end'] + 50)
            
    except Exception:
        pass
    finally:
        if os.path.exists(tmp_in_path): os.remove(tmp_in_path)
        if os.path.exists(tmp_out): os.remove(tmp_out)
        
    # Fallback if nhmmer fails
    return find_16s_locus(dna_seq)
