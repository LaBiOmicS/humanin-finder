#!/usr/bin/env python3
"""
Summarize HumaninFinder results across the 343 primate mitogenomes dataset.
Generates statistical metrics, category breakdowns, and a markdown report.
"""

import argparse
import json
import os
import pandas as pd


def get_primate_group(genus):
    """Map major primate genera to their higher taxonomic groups."""
    hominoids = {
        "Homo", "Pan", "Gorilla", "Pongo", "Hylobates", "Symphalangus",
        "Nomascus", "Hoolock"
    }
    cercopithecoids = {
        "Macaca", "Papio", "Mandrillus", "Theropithecus", "Cercocebus",
        "Lophocebus", "Rungwecebus", "Chlorocebus", "Erythrocebus", "Cercopithecus",
        "Miopithecus", "Allenopithecus", "Colobus", "Piliocolobus", "Procolobus",
        "Semnopithecus", "Trachypithecus", "Presbytis", "Pygathrix", "Rhinopithecus",
        "Nasalis", "Simias"
    }
    platyrrhines = {
        "Callithrix", "Mico", "Cebuella", "Leontocebus", "Saguinus", "Leontopithecus",
        "Callimico", "Cebus", "Sapajus", "Saimiri", "Aotus", "Pithecia", "Chiropotes",
        "Cacajao", "Callicebus", "Cheracebus", "Plecturocebus", "Alouatta", "Ateles",
        "Brachyteles", "Lagothrix", "Oreonax"
    }
    strepsirrhines = {
        "Lemur", "Eulemur", "Varecia", "Hapalemur", "Prolemur", "Lepilemur",
        "Cheirogaleus", "Microcebus", "Mirza", "Allocebus", "Phaner", "Indri",
        "Propithecus", "Avahi", "Daubentonia", "Loris", "Nycticebus", "Xanthonycticebus",
        "Perodicticus", "Pseudopotto", "Arctocebus", "Galago", "Galagoides", "Paragalago",
        "Otolemur", "Euoticus"
    }
    tarsiiformes = {"Tarsius", "Carlito", "Cephalopachus"}

    if genus in hominoids:
        return "Hominoidea"
    elif genus in cercopithecoids:
        return "Cercopithecoidea (Old World Monkeys)"
    elif genus in platyrrhines:
        return "Platyrrhini (New World Monkeys)"
    elif genus in strepsirrhines:
        return "Strepsirrhini (Lemurs & Lorises)"
    elif genus in tarsiiformes:
        return "Tarsiiformes (Tarsiers)"
    return "Other Primates"


def main():
    parser = argparse.ArgumentParser(description="Summarize HumaninFinder predictions for 343 primates.")
    parser.add_argument("--results", "-r", required=True, help="Path to HumaninFinder results CSV file.")
    parser.add_argument("--metadata", "-m", required=True, help="Path to primates_343_metadata.tsv.")
    parser.add_argument("--output-dir", "-o", default="analysis/reports", help="Output directory for reports.")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    df_results = pd.read_csv(args.results)
    df_meta = pd.read_csv(args.metadata, sep="\t")

    # Clean accession IDs for merging (strip version if needed)
    df_results["accession_base"] = df_results["id"].apply(lambda x: str(x).split(".")[0])
    df_meta["accession_base"] = df_meta["accession"].apply(lambda x: str(x).split(".")[0])

    # Extract Genus
    df_meta["genus"] = df_meta["organism"].apply(lambda x: str(x).split()[0])
    df_meta["clade_group"] = df_meta["genus"].apply(get_primate_group)

    # Merge
    merged = pd.merge(df_results, df_meta, on="accession_base", how="left")

    total_species = len(df_meta)
    detected_species = df_results["accession_base"].nunique()

    # Metrics
    status_counts = df_results["status"].value_counts().to_dict()
    mean_score = float(df_results["score"].mean())
    median_score = float(df_results["score"].median())
    high_conf_hits = int((df_results["score"] >= 0.85).sum())

    group_summary = (
        merged.groupby("clade_group")
        .agg(
            total_loci=("id", "count"),
            unique_species=("accession_base", "nunique"),
            mean_score=("score", "mean"),
            canonical_count=("status", lambda x: (x == "Canonical").sum()),
            non_canonical_count=("status", lambda x: (x == "Non-canonical").sum()),
            pseudogenic_count=("status", lambda x: (x == "Pseudogenic").sum()),
        )
        .reset_index()
    )

    # Save CSV summary
    summary_csv_path = os.path.join(args.output_dir, "summary_by_clade.csv")
    group_summary.to_csv(summary_csv_path, index=False)

    # Save JSON metrics
    metrics = {
        "total_primates_evaluated": total_species,
        "species_with_hits": detected_species,
        "detection_rate_pct": round(detected_species / total_species * 100, 2),
        "total_candidates": len(df_results),
        "status_distribution": status_counts,
        "mean_confidence_score": round(mean_score, 4),
        "median_confidence_score": round(median_score, 4),
        "high_confidence_hits_ge_0.85": high_conf_hits,
    }
    json_path = os.path.join(args.output_dir, "summary_metrics.json")
    with open(json_path, "w") as f:
        json.dump(metrics, f, indent=2)

    # Save Markdown report
    md_report_path = os.path.join(args.output_dir, "primate_analysis_summary.md")
    with open(md_report_path, "w") as f:
        f.write("# HumaninFinder: Relatório da Análise de 343 Mitogenomas de Primatas\n\n")
        f.write("## 1. Visão Geral dos Resultados\n\n")
        f.write(f"- **Total de Espécies Avaliadas:** {total_species}\n")
        f.write(f"- **Espécies com Loci Detectados:** {detected_species} ({metrics['detection_rate_pct']}%)\n")
        f.write(f"- **Total de Candidatos Mapeados:** {len(df_results)}\n")
        f.write(f"- **Score Médio de Confiança:** {mean_score:.3f} (Mediana: {median_score:.3f})\n")
        f.write(f"- **Hits de Alta Confiança (Score >= 0.85):** {high_conf_hits}\n\n")

        f.write("## 2. Distribuição por Status Biológico\n\n")
        f.write("| Status | Frequência | Proporção (%) |\n")
        f.write("| :--- | :---: | :---: |\n")
        for status, count in status_counts.items():
            pct = count / len(df_results) * 100
            f.write(f"| **{status}** | {count} | {pct:.2f}% |\n")

        f.write("\n## 3. Síntese por Grupo Taxonômico\n\n")
        f.write("| Clado | Espécies Únicas | Total Loci | Score Médio | Canônicos | Não-Canônicos | Pseudogenes |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |\n")
        for _, row in group_summary.iterrows():
            f.write(
                f"| {row['clade_group']} | {row['unique_species']} | {row['total_loci']} | "
                f"{row['mean_score']:.3f} | {row['canonical_count']} | {row['non_canonical_count']} | "
                f"{row['pseudogenic_count']} |\n"
            )

        f.write("\n---\n*Gerado automaticamente pelo pipeline de análise HumaninFinder.*\n")

    print(f"[+] Summary generated successfully:")
    print(f"    - Table: {summary_csv_path}")
    print(f"    - JSON:  {json_path}")
    print(f"    - Report: {md_report_path}")


if __name__ == "__main__":
    main()
