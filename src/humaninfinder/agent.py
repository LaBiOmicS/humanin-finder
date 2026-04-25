import click
import pandas as pd
import sys

class HumaninAgent:
    def __init__(self, model="llama3"):
        self.model = model
        try:
            import ollama
            self.client = ollama
        except ImportError:
            click.secho("Error: 'ollama' package not found.", fg="red")
            click.echo("Please install it with: pip install ollama")
            sys.exit(1)

    def analyze_results(self, csv_path, query=None):
        """Analyze the results CSV and provide AI-powered insights."""
        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            click.secho(f"Error loading CSV: {e}", fg="red")
            return

        # Basic summary statistics to feed the context
        stats = df['status'].value_counts().to_dict()
        top_scores = df.nlargest(5, 'score')[['id', 'status', 'score']].to_dict(orient='records')
        
        # Specialized Scientific Context
        context = f"""
        You are the HumaninFinder AI Specialist, an expert in mitochondrial-derived peptides (MDPs), 
        proteomics, and evolutionary biology. Your core expertise is the Humanin (HN) peptide and its 
        role in mitochondrial signaling, cytoprotection, and metabolic regulation.

        Scientific Background for your analysis:
        - Humanin is a 21-AA peptide encoded in the 16S rRNA gene (MT-RNR2).
        - It is a potent neuroprotective and cytoprotective factor, antagonizing apoptosis-inducing proteins like Bax.
        - It plays a crucial role in Aging biology, protecting against Alzheimer's disease and cardiovascular decay.
        - Evolutionarily, HN is subject to "evolutionary tuning"—sequence variations often correlate with species-specific lifespans and metabolic rates.
        - Pseudogenic relics (loci with internal stops) are genomic "ghosts" that still hold structural information about ancient MDPs.

        Current Study Results (after scanning mitochondrial genomes):
        - Total Loci Identified: {len(df)}
        - Class Distribution: {stats}
        - Top 5 Highest Confidence Hits: {top_scores}

        Analyze these results with scientific rigor. Focus on how these findings might impact our 
        understanding of mitochondrial health, longevity, and the evolution of MDPs.
        """

        if query:
            full_prompt = f"{context}\n\nUser Question: {query}"
        else:
            full_prompt = f"{context}\n\nPlease summarize the biological significance of these findings, focusing on evolutionary conservation and potential functional relics (pseudogenes)."

        click.echo(f"[*] Consulting AI Agent ({self.model})...")
        try:
            response = self.client.generate(model=self.model, prompt=full_prompt)
            return response['response']
        except Exception as e:
            click.secho(f"AI Agent error: {e}", fg="red")
            click.echo("Ensure Ollama is running ('ollama serve') and the model is downloaded ('ollama pull llama3').")
            return None
