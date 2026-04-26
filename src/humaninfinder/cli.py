import concurrent.futures
import os

import click
import pandas as pd
from Bio import SeqIO

from humaninfinder.classifier import HumaninClassifier
from humaninfinder.core import find_16s_locus_precise, find_sorfs, run_hmm_search, sliding_window_rescue


def process_single_record(record, table, hmm, rescue, hmm_path):
    """Targeted processing: Detect 16S locus PRECISELY using nhmmer, then search Humanin."""
    probe_path = os.path.join(os.path.dirname(__file__), "data/16s_probe.fasta")
    if not os.path.exists(probe_path):
        probe_path = "16s_probe.fasta"

    locus_start, locus_end = find_16s_locus_precise(record.seq, probe_path=probe_path)
    targeted_seq = record.seq[locus_start:locus_end]

    hmm_hits = []
    if hmm:
        hmm_hits = run_hmm_search(targeted_seq, hmm_path, table=table)

    local_candidates = find_sorfs(targeted_seq, table=table)
    if rescue:
        local_candidates.extend(sliding_window_rescue(targeted_seq, table=table))

    final_candidates = []
    for cand in local_candidates:
        cand["start"] += locus_start
        cand["end"] += locus_start
        final_candidates.append(cand)

    return record.id, record.description, final_candidates, hmm_hits


@click.group()
@click.version_option(version="1.0.8")
def main():
    """HumaninFinder: Discovery tool for Humanin-like peptides using Hybrid AI."""
    pass


@main.command()
@click.option("--results", "-r", required=True, type=click.Path(exists=True), help="Path to results CSV file.")
@click.option("--model", "-m", default="llama3", help="Ollama model to use. Default: llama3.")
@click.option("--query", "-q", help="Specific question about the results.")
def agent(results, model, query):
    """AI-powered interpretation of HumaninFinder results."""
    from humaninfinder.agent import HumaninAgent

    ai = HumaninAgent(model=model)
    response = ai.analyze_results(results, query=query)
    if response:
        click.echo("\n" + "=" * 80)
        click.echo("AI AGENT INSIGHTS")
        click.echo("=" * 80)
        click.echo(response)
        click.echo("=" * 80)


@main.command()
def setup():
    """Initialize and verify the environment."""
    click.echo("[*] Verifying prerequisites...")

    # Check HMMER
    import subprocess

    try:
        subprocess.run(["hmmsearch", "-h"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        click.secho("[+] HMMER3 is installed and accessible.", fg="green")
    except FileNotFoundError:
        click.secho("[-] HMMER3 not found. Please install it via Conda or system package manager.", fg="yellow")

    # Check ESM-2 Cache (simulated check)
    click.echo("[*] Verifying AI Model connectivity...")
    try:
        import transformers  # noqa: F401

        # This only checks if the library is there; it doesn't download the 30MB model until first run
        click.secho("[+] Transformers library is ready.", fg="green")
    except ImportError:
        click.secho("[-] Transformers library not found.", fg="red")

    click.secho("\n[!] Setup complete. You can now use 'humanin-finder predict'.", fg="blue", bold=True)


@main.command()
@click.option("--input", "-i", required=True, type=click.Path(exists=True), help="Input FASTA file.")
@click.option("--output", "-o", required=True, help="Output prefix.")
@click.option("--threshold", "-t", type=float, default=0.7, help="Confidence threshold (0.0-1.0). Default: 0.7.")
@click.option("--table", "-g", type=int, default=2, help="NCBI Genetic Table (Default: 2 - Vertebrate Mitochondrial).")
@click.option("--hmm", is_flag=True, help="Enable HMM-based locus localization.")
@click.option("--rescue", is_flag=True, help="Enable Evolutionary Rescue (Sliding Window).")
@click.option("--cpus", "-c", type=int, default=os.cpu_count(), help="Number of CPUs for parallel processing.")
@click.option("--all-candidates", is_flag=True, help="Output all detected candidates, not just the best one.")
def predict(input, output, threshold, table, hmm, rescue, cpus, all_candidates):
    """Scan genomes to identify and classify Humanin-like peptides."""
    hmm_path = os.path.join(os.path.dirname(__file__), "data/humanin.hmm")

    click.echo(f"[*] Loading sequences from {input}...")
    records = list(SeqIO.parse(input, "fasta"))

    click.echo("[*] Initializing Hybrid AI Engine (ESM-2 + Biophysical)...")
    clf = HumaninClassifier()

    click.echo(f"\n{'-' * 80}")
    click.echo(f"{'ID':<25} | {'Status':<15} | {'Coordinates':<20} | {'Score'}")
    click.echo(f"{'-' * 80}")

    final_results_list = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=cpus) as executor:
        futures = [executor.submit(process_single_record, r, table, hmm, rescue, hmm_path) for r in records]

        for future in futures:
            rec_id, rec_desc, candidates, hmm_hits = future.result()

            if not candidates:
                click.echo(f"{rec_id:<25} | >> No candidates found in 16S locus.")
                continue

            # Classify candidates
            sequences = [c["seq"] for c in candidates]
            probs = clf.predict(sequences, batch_size=256)

            scored_candidates = []
            for i, cand in enumerate(candidates):
                prob = probs[i]
                score = prob

                cand_hit = next(
                    (h for h in hmm_hits if h["strand"] == cand["strand"] and h["frame"] == cand["frame"]), None
                )

                score = max(score, 0.65)
                if cand_hit:
                    score = min(0.99, score + 0.15)
                else:
                    score = min(0.95, score + 0.05)

                if cand["status"] == "Non-canonical":
                    score *= 0.95
                elif cand["status"] == "Pseudogenic":
                    score *= 0.75

                cand.update(
                    {
                        "id": rec_id,
                        "score": score,
                        "ai_score": prob,
                        "hmm_score": cand_hit["score"] if cand_hit else 0.0,
                        "locus_tag": "16S-Locus",
                    }
                )
                scored_candidates.append(cand)

            scored_candidates.sort(key=lambda x: x["score"], reverse=True)
            non_redundant = []
            for cand in scored_candidates:
                is_redundant = False
                for accepted in non_redundant:
                    if cand["strand"] == accepted["strand"]:
                        overlap_start = max(cand["start"], accepted["start"])
                        overlap_end = min(cand["end"], accepted["end"])
                        if overlap_start < overlap_end:
                            overlap_len = overlap_end - overlap_start
                            if overlap_len > (0.5 * (cand["end"] - cand["start"])):
                                is_redundant = True
                                break
                if not is_redundant:
                    non_redundant.append(cand)

            scored_candidates = non_redundant

            if all_candidates:
                for cand in scored_candidates:
                    msg = (
                        f"{rec_id:<25} | {cand['status']:<15} | {cand['start']}-{cand['end']:<20} | {cand['score']:.3f}"
                    )
                    click.echo(msg)
                    final_results_list.append(cand)
            else:
                primary_results = [c for c in scored_candidates if c["score"] >= threshold]
                final_selection = []
                is_low_conf = False

                if primary_results:
                    final_selection = primary_results
                else:
                    fallback_results = [c for c in scored_candidates if c["score"] >= 0.5]
                    if fallback_results:
                        final_selection = fallback_results
                        is_low_conf = True

                if final_selection:
                    status_priority = {"Canonical": 3, "Non-canonical": 2, "Pseudogenic": 1}
                    best_cand = sorted(
                        final_selection, key=lambda x: (x["score"], status_priority.get(x["status"], 0)), reverse=True
                    )[0]

                    hmm_tag = " (!No HMM)" if best_cand["hmm_score"] == 0 else ""
                    conf_tag = " (?LowConf)" if is_low_conf else ""

                    m_idx = best_cand["seq"].find("M")
                    if m_idx != -1:
                        best_cand["seq"] = best_cand["seq"][m_idx:]
                        if best_cand["strand"] == 1:
                            best_cand["start"] += m_idx * 3
                        else:
                            best_cand["end"] -= m_idx * 3

                    status_str = f"{best_cand['status']}{hmm_tag}{conf_tag}"
                    msg = (
                        f"{rec_id:<25} | {status_str:<15} | "
                        f"{best_cand['start']}-{best_cand['end']:<20} | {best_cand['score']:.3f}"
                    )
                    click.echo(msg)
                    final_results_list.append(best_cand)
                else:
                    click.echo(f"{rec_id:<25} | >> No reliable candidates (below 0.5).")

    if final_results_list:
        df = pd.DataFrame(final_results_list)
        df.to_csv(f"{output}_results.csv", index=False)
        with open(f"{output}_results.fasta", "w") as f:
            for _, row in df.iterrows():
                header = f">{row['id']}_{row['status']}_{row['start']}_{row['end']}_score_{row['score']:.3f}"
                f.write(f"{header}\n{row['seq']}\n")
        click.echo(f"\n[+] Done. Results: {output}_results.[csv/fasta]")
    else:
        click.echo("\n[-] No candidates found.")


if __name__ == "__main__":
    main()
