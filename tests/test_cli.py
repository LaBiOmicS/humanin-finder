import os
import pandas as pd
from click.testing import CliRunner
from humaninfinder.cli import main


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "HumaninFinder" in result.output
    assert "predict" in result.output
    assert "setup" in result.output
    assert "agent" in result.output


def test_cli_setup():
    runner = CliRunner()
    result = runner.invoke(main, ["setup"])
    assert result.exit_code == 0
    assert "Verifying prerequisites" in result.output
    assert "Setup complete" in result.output


def test_cli_predict_e2e(tmp_path):
    runner = CliRunner()
    repo_root = os.path.dirname(os.path.dirname(__file__))
    sample_fasta = os.path.join(repo_root, "examples", "test_sample.fasta")
    if not os.path.exists(sample_fasta):
        sample_fasta = os.path.join(repo_root, "test_sample.fasta")
    out_prefix = str(tmp_path / "test_out")

    result = runner.invoke(
        main,
        ["predict", "-i", sample_fasta, "-o", out_prefix, "--hmm", "--rescue", "-c", "1"],
    )
    assert result.exit_code == 0
    assert "Done. Results:" in result.output

    csv_file = f"{out_prefix}_results.csv"
    fasta_file = f"{out_prefix}_results.fasta"

    assert os.path.exists(csv_file)
    assert os.path.exists(fasta_file)

    df = pd.read_csv(csv_file)
    expected_cols = {"seq", "start", "end", "strand", "frame", "status", "id", "score", "ai_score", "hmm_score", "locus_tag"}
    assert expected_cols.issubset(set(df.columns))
    assert len(df) > 0


def test_cli_agent_missing_file():
    runner = CliRunner()
    result = runner.invoke(main, ["agent", "-r", "non_existent_file.csv"])
    assert result.exit_code != 0 or "Error" in result.output
