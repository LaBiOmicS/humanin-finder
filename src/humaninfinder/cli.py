import argparse
import os
import pandas as pd
import concurrent.futures
from Bio import SeqIO
from humaninfinder.core import find_sorfs, sliding_window_rescue, run_hmm_search, find_16s_locus_precise
from humaninfinder.classifier import HumaninClassifier

def process_single_record(record, args, hmm_path):
    """Targeted processing: Detect 16S locus PRECISELY using nhmmer, then search Humanin."""
    # 1. Precise Locus Detection (Discovery Mode)
    probe_path = os.path.join(os.path.dirname(__file__), "data/16s_probe.fasta")
    if not os.path.exists(probe_path):
        probe_path = "16s_probe.fasta"

    locus_start, locus_end = find_16s_locus_precise(record.seq, probe_path=probe_path)
    
    targeted_seq = record.seq[locus_start:locus_end]

    # 2. HMM Locus Localization (within the discovered targeted sequence)
    hmm_hits = []
    if args.hmm:
        hmm_hits = run_hmm_search(targeted_seq, hmm_path, table=args.table)

    # 3. Candidate Generation (ONLY in the discovered zone)
    # Search standard ORFs in the 16S fragment
    local_candidates = find_sorfs(targeted_seq, table=args.table)

    if args.rescue:
        # High-sensitivity scan in the discovered locus
        local_candidates.extend(sliding_window_rescue(targeted_seq, table=args.table))

    # 4. Map coordinates back to the global genome
    final_candidates = []
    for cand in local_candidates:
        cand['start'] += locus_start
        cand['end'] += locus_start
        final_candidates.append(cand)

    return record.id, record.description, final_candidates, hmm_hits

def main():
    parser = argparse.ArgumentParser(description="HumaninFinder: Discovery tool for Humanin-like peptides.")
    parser.add_argument("--input", required=True, help="Input FASTA file.")
    parser.add_argument("--output", required=True, help="Output prefix.")
    parser.add_argument("--threshold", type=float, default=0.7, help="Confidence threshold (0.0-1.0). Default: 0.7.")
    parser.add_argument("--table", type=int, default=2, help="NCBI Genetic Table (Default: 2 - Vertebrate Mitochondrial).")
    parser.add_argument("--hmm", action="store_true", help="Enable HMM-based locus localization.")
    parser.add_argument("--rescue", action="store_true", help="Enable Evolutionary Rescue (Sliding Window).")
    parser.add_argument("--cpus", type=int, default=os.cpu_count(), help="Number of CPUs to use for parallel processing.")
    parser.add_argument("--all-candidates", action="store_true", help="Output all detected candidates, not just the best one.")
    
    args = parser.parse_args()
    
    hmm_path = os.path.join(os.path.dirname(__file__), "data/humanin.hmm")
    
    print(f"[*] Loading sequences from {args.input}...")
    records = list(SeqIO.parse(args.input, "fasta"))
    
    print("[*] Initializing Hybrid AI Engine (ESM-2 + Biophysical)...")
    clf = HumaninClassifier()
    
    print(f"\n{'-'*80}")
    print(f"{'ID':<25} | {'Status':<15} | {'Coordinates':<20} | {'Score'}")
    print(f"{'-'*80}")

    final_results_list = []
    
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.cpus) as executor:
        futures = [executor.submit(process_single_record, r, args, hmm_path) for r in records]
        
        for future in futures:
            rec_id, rec_desc, candidates, hmm_hits = future.result()
            
            if not candidates:
                print(f"{rec_id:<25} | >> No candidates found in 16S locus.")
                continue

            # Classify candidates
            sequences = [c['seq'] for c in candidates]
            probs = clf.predict(sequences, batch_size=256)
            
            scored_candidates = []
            for i, cand in enumerate(candidates):
                prob = probs[i]
                
                # SCIENTIFIC SCORING V6: Adaptive Thresholding
                score = prob
                
                cand_hit = next((h for h in hmm_hits if h['strand'] == cand['strand'] and h['frame'] == cand['frame']), None)
                
                # Boost confidence based on locus and HMM evidence
                score = max(score, 0.65) # Higher floor since we are in the precise 16S
                if cand_hit:
                    score = min(0.99, score + 0.15)
                else:
                    score = min(0.95, score + 0.05)

                if cand['status'] == 'Non-canonical':
                    score *= 0.95 
                elif cand['status'] == 'Pseudogenic':
                    score *= 0.75

                cand.update({
                    'id': rec_id,
                    'score': score,
                    'ai_score': prob,
                    'hmm_score': cand_hit['score'] if cand_hit else 0.0,
                    'locus_tag': "16S-Locus"
                })
                scored_candidates.append(cand)

            # NON-REDUNDANT FILTER (Biological Sense)
            # Sort by score to keep the best representative of each locus
            scored_candidates.sort(key=lambda x: x['score'], reverse=True)
            non_redundant = []
            for cand in scored_candidates:
                is_redundant = False
                for accepted in non_redundant:
                    # Check overlap on the same strand
                    if cand['strand'] == accepted['strand']:
                        overlap_start = max(cand['start'], accepted['start'])
                        overlap_end = min(cand['end'], accepted['end'])
                        if overlap_start < overlap_end:
                            overlap_len = overlap_end - overlap_start
                            # If overlap is > 50% of the candidate length, it's redundant
                            if overlap_len > (0.5 * (cand['end'] - cand['start'])):
                                is_redundant = True
                                break
                if not is_redundant:
                    non_redundant.append(cand)
            
            scored_candidates = non_redundant

            # ADAPTIVE SELECTION LOGIC
            if args.all_candidates:
                # Save everything that was found
                for cand in scored_candidates:
                    print(f"{rec_id:<25} | {cand['status']:<15} | {cand['start']}-{cand['end']:<20} | {cand['score']:.3f}")
                    final_results_list.append(cand)
            else:
                # Original Adaptive Logic: find the single best candidate
                # 1. Try Primary Threshold (Default 0.7)
                primary_results = [c for c in scored_candidates if c['score'] >= args.threshold]
                
                # 2. Try Fallback Threshold (0.5) if Primary fails
                final_selection = []
                is_low_conf = False
                
                if primary_results:
                    final_selection = primary_results
                else:
                    # Fallback to 0.5 because we have "evidence" (we are in the 16S locus)
                    fallback_results = [c for c in scored_candidates if c['score'] >= 0.5]
                    if fallback_results:
                        final_selection = fallback_results
                        is_low_conf = True

                if final_selection:
                    status_priority = {'Canonical': 3, 'Non-canonical': 2, 'Pseudogenic': 1}
                    best_cand = sorted(final_selection, key=lambda x: (x['score'], status_priority.get(x['status'], 0)), reverse=True)[0]
                    
                    # Visual Tags
                    hmm_tag = " (!No HMM)" if best_cand['hmm_score'] == 0 else ""
                    conf_tag = " (?LowConf)" if is_low_conf else ""
                    
                    m_idx = best_cand['seq'].find('M')
                    if m_idx != -1:
                        best_cand['seq'] = best_cand['seq'][m_idx:]
                        if best_cand['strand'] == 1:
                            best_cand['start'] += (m_idx * 3)
                        else:
                            best_cand['end'] -= (m_idx * 3)
                    
                    status_str = f"{best_cand['status']}{hmm_tag}{conf_tag}"
                    print(f"{rec_id:<25} | {status_str:<15} | {best_cand['start']}-{best_cand['end']:<20} | {best_cand['score']:.3f}")
                    final_results_list.append(best_cand)
                else:
                    print(f"{rec_id:<25} | >> No reliable candidates (below 0.5).")

    if final_results_list:
        df = pd.DataFrame(final_results_list)
        df.to_csv(f"{args.output}_results.csv", index=False)
        with open(f"{args.output}_results.fasta", "w") as f:
            for _, row in df.iterrows():
                header = f">{row['id']}_{row['status']}_{row['start']}_{row['end']}_score_{row['score']:.3f}"
                f.write(f"{header}\n{row['seq']}\n")
        print(f"\n[+] Done. Results: {args.output}_results.[csv/fasta]")
    else:
        print("\n[-] No candidates found.")

if __name__ == "__main__":
    main()
