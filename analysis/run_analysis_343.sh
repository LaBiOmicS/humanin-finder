#!/usr/bin/env bash
# ==============================================================================
# HumaninFinder: Workflow de Descoberta Evolutiva em 343 Mitogenomas de Primatas
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# Configuração de Ambiente
PYTHON_BIN="${PYTHON_BIN:-$(which python3)}"
if [ -f "/home/dayhoff/.micromamba/envs/humanin_env/bin/python" ]; then
    PYTHON_BIN="/home/dayhoff/.micromamba/envs/humanin_env/bin/python"
    export PATH="/home/dayhoff/.micromamba/envs/humanin_env/bin:${PATH}"
fi

export PYTHONPATH="${REPO_ROOT}/src:${PYTHONPATH:-}"

# Parâmetros Padrão
MODE="standard"
CPUS="$(nproc 2>/dev/null || echo 4)"
THRESHOLD="0.7"
INPUT_FASTA="${SCRIPT_DIR}/primates_343.fasta"
METADATA_FILE="${SCRIPT_DIR}/primates_343_metadata.tsv"
RESULTS_DIR="${SCRIPT_DIR}/results"
REPORTS_DIR="${SCRIPT_DIR}/reports"

# Parse CLI flags
while [[ $# -gt 0 ]]; do
    case "$1" in
        --mode|-m)
            MODE="$2"
            shift 2
            ;;
        --cpus|-c)
            CPUS="$2"
            shift 2
            ;;
        --threshold|-t)
            THRESHOLD="$2"
            shift 2
            ;;
        --help|-h)
            echo "Uso: $0 [opções]"
            echo "Opções:"
            echo "  --mode, -m        Modo de execução: 'standard' (melhor hit), 'exhaustive' (todos os loci) ou 'both' (default: standard)"
            echo "  --cpus, -c        Número de núcleos de processamento (default: $(nproc))"
            echo "  --threshold, -t   Limiar de confiança (default: 0.7)"
            echo "  --help, -h        Exibe esta mensagem de ajuda"
            exit 0
            ;;
        *)
            echo "Opção desconhecida: $1"
            exit 1
            ;;
    esac
done

mkdir -p "${RESULTS_DIR}" "${REPORTS_DIR}"

echo "================================================================================"
echo " HumaninFinder: Análise de 343 Genomas Mitocondriais de Primatas"
echo "================================================================================"
echo "[*] Python Interpreter: ${PYTHON_BIN}"
echo "[*] CPUs alocados:     ${CPUS}"
echo "[*] Modo selecionado:   ${MODE}"
echo "[*] Limiar de corte:    ${THRESHOLD}"
echo "[*] Arquivo de entrada: ${INPUT_FASTA}"
echo "================================================================================"

START_TIME=$(date +%s)

# 1. Pré-checagem de dependências
echo -e "\n[*] [Etapa 1/4] Verificando dependências do sistema..."
${PYTHON_BIN} -m humaninfinder.cli setup

# 2. Execução da Descoberta
if [[ "${MODE}" == "standard" || "${MODE}" == "both" ]]; then
    echo -e "\n[*] [Etapa 2/4] Executando Modo Padrão (Adaptive Selection - 1 melhor candidato/espécie)..."
    OUTPUT_PREFIX="${RESULTS_DIR}/primates_343_standard"
    ${PYTHON_BIN} -m humaninfinder.cli predict \
        --input "${INPUT_FASTA}" \
        --output "${OUTPUT_PREFIX}" \
        --table 2 \
        --hmm \
        --rescue \
        --threshold "${THRESHOLD}" \
        --cpus "${CPUS}"

    echo -e "\n[*] [Etapa 3/4] Gerando relatório estatístico e síntese por clado..."
    ${PYTHON_BIN} "${SCRIPT_DIR}/scripts/summarize_primates.py" \
        --results "${OUTPUT_PREFIX}_results.csv" \
        --metadata "${METADATA_FILE}" \
        --output-dir "${REPORTS_DIR}/standard"
fi

if [[ "${MODE}" == "exhaustive" || "${MODE}" == "both" ]]; then
    echo -e "\n[*] Executando Modo Exaustivo (All Candidates - Sorfoma mitocondrial completo)..."
    OUTPUT_PREFIX_ALL="${RESULTS_DIR}/primates_343_exhaustive"
    ${PYTHON_BIN} -m humaninfinder.cli predict \
        --input "${INPUT_FASTA}" \
        --output "${OUTPUT_PREFIX_ALL}" \
        --table 2 \
        --hmm \
        --rescue \
        --all-candidates \
        --cpus "${CPUS}"

    echo -e "\n[*] Gerando relatório estatístico do Sorfoma Exaustivo..."
    ${PYTHON_BIN} "${SCRIPT_DIR}/scripts/summarize_primates.py" \
        --results "${OUTPUT_PREFIX_ALL}_results.csv" \
        --metadata "${METADATA_FILE}" \
        --output-dir "${REPORTS_DIR}/exhaustive"
fi

# 4. Agente IA (Opcional se Ollama estiver ativo)
echo -e "\n[*] [Etapa 4/4] Verificando disponibilidade do Agente IA (Ollama)..."
if command -v ollama &>/dev/null && pgrep -x "ollama" &>/dev/null; then
    echo "[+] Ollama detectado e ativo. Solicitando síntese do Agente Especialista..."
    TARGET_CSV="${RESULTS_DIR}/primates_343_standard_results.csv"
    if [ -f "${TARGET_CSV}" ]; then
        ${PYTHON_BIN} -m humaninfinder.cli agent --results "${TARGET_CSV}" > "${REPORTS_DIR}/ai_agent_insights.txt" || true
        echo "[+] Insights salvos em: ${REPORTS_DIR}/ai_agent_insights.txt"
    fi
else
    echo "[-] Ollama não está em execução em segundo plano. Pulando interpretação por LLM (opcional)."
    echo "    (Para ativar: 'ollama serve &' e execute 'humanin-finder agent --results ...')"
fi

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

echo -e "\n================================================================================"
echo " [+] Workflow finalizado com sucesso em ${ELAPSED} segundos!"
echo " [+] Arquivos de resultados: ${RESULTS_DIR}/"
echo " [+] Relatórios e tabelas:   ${REPORTS_DIR}/"
echo "================================================================================"
