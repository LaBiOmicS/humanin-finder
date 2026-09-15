# Análise Mitogenômica Expandida: 343 Primatas

Este diretório contém o conjunto consolidado de genomas mitocondriais completos exclusivamente da ordem **Primates**, filtrados a partir da base mitogenômica evolutiva (`/home/dayhoff/workdir/omics/evolution/`):

## Arquivos Disponíveis

- **`primates_343.fasta`**: Arquivo multi-FASTA contendo os **343 genomas mitocondriais completos** de primatas (tamanho: ~5.55 MB).
  - Todos os 4 outgroups (*Tupaia*, *Galeopterus*, *Ornithorhynchus*, *Oryctolagus*) foram excluídos.
- **`primates_343_metadata.tsv`**: Tabela de metadados das 343 espécies (organismo, accession NCBI, comprimento em bp, conteúdo GC e anotações).

## Fluxos de Trabalho Automatizados

O pipeline pode ser executado de forma totalmente automatizada via **Script Bash** ou **Snakemake**:

### Opção 1: Script Bash Integrado (Recomendado)
O script [`run_analysis_343.sh`](file:///home/dayhoff/workdir/bioinformatics/humanin-finder/analysis/run_analysis_343.sh) orquestra todas as etapas (verificação, predição, geração de relatórios e consulta ao Agente IA):

```bash
# Execução padrão (utiliza todos os núcleos disponíveis)
./analysis/run_analysis_343.sh

# Execução customizada (modo exaustivo com 4 núcleos)
./analysis/run_analysis_343.sh --mode exhaustive --cpus 4

# Execução completa (gera tanto o modo padrão quanto o sorfoma exaustivo)
./analysis/run_analysis_343.sh --mode both
```

### Opção 2: Pipeline Snakemake
Para ambientes com Snakemake:

```bash
cd analysis
snakemake --cores 4
```

---

## Estrutura de Diretórios Gerada

```text
analysis/
├── primates_343.fasta              # Multi-FASTA de entrada (343 mitogenomas)
├── primates_343_metadata.tsv       # Tabela de metadados das 343 espécies
├── run_analysis_343.sh             # Pipeline executável de ponta a ponta
├── Snakefile                       # Definição do fluxo para Snakemake
├── scripts/
│   └── summarize_primates.py       # Script de geração de relatórios e métricas por clado
├── results/                        # Tabelas CSV e arquivos FASTA gerados
└── reports/                        # Relatórios Markdown, JSONs e sumários por clado
```
