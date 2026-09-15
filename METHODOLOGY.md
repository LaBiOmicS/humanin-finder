# Metodologia de Desenvolvimento e Arquitetura do HumaninFinder (v1.1.0)

**Autor:** Fabiano Bezerra Menegidio  
**Afiliação:** Laboratório de Bioinformática e Ômicas (LaBiOmicS), Universidade de Mogi das Cruzes (UMC)  
**Data:** 15 de Setembro de 2026  
**Versão da Ferramenta:** HumaninFinder 1.1.0  

---

## 1. Visão Geral e Fundamentação Teórica

Os Peptídeos Derivados de Mitocôndrias (MDPs, do inglês *Mitochondrial-Derived Peptides*) constituem uma classe essencial de moléculas sinalizadoras codificadas em pequenas fases de leitura abertas (sORFs) aninhadas no genoma mitocondrial. Entre eles, o peptídeo **Humanina (HN)**, composto classicamente por 21 a 24 aminoácidos e transcrito a partir do gene de RNA ribossomal 16S (*MT-RNR2*), exerce funções neuroprotetoras, citoprotetoras e reguladoras do metabolismo energético e da longevidade.

A identificação bioinformática de ortólogos e relíquias evolutivas de Humanina em linhagens divergentes enfrenta obstáculos severos quando abordada por ferramentas tradicionais de anotação e alinhamento primário (como BLASTp ou preditores estritos de ORFs):
1. **Divergência de Iniciação da Tradução:** O sistema mitocondrial utiliza frequentemente códons de início alternativos (ex.: AUA, AUU, GUG);
2. **Deriva Mutacional e Pseudogenização:** Mutações pontuais (como substituições nonsense gerando códons de parada prematuros) interrompem a ORF primária, mesmo quando a região conserva o perfil estrutural e biofísico ancestral;
3. **Restrições Duplas de Codificação:** A sequência de DNA do locus da Humanina sobrepõe-se a estruturas secundárias e terciárias críticas do rRNA 16S, impondo padrões evolutivos que desviam dos modelos convencionais de substituição de aminoácidos.

O **HumaninFinder (v1.1.0)** foi desenvolvido como um framework bioinformático de alta sensibilidade que redefine a busca por Humanina: substituindo a dependência estrita de identidade de sequência por um **reconhecimento de assinatura estrutural e biofísica mediado por Inteligência Artificial Híbrida**, aliado a um motor de **Resgate Evolutivo Multiframe** e ancoramento genômico ortogonal.

---

## 2. Arquitetura Geral do Pipeline

O pipeline processa genomas mitocondriais completos em formato FASTA através de cinco módulos sequenciais e integrados:

```text
       +-------------------------------------------------------------+
       |           Mitogenoma Completo de Entrada (FASTA)            |
       +-------------------------------------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       |   Módulo 1: Delimitação Genômica de Precisão (16S rRNA)     |
       |   - Alinhamento de perfil HMM de DNA via nhmmer             |
       |   - Fallback heurístico por âncoras conservadas de rRNA     |
       +-------------------------------------------------------------+
                                      |
                     +----------------+----------------+
                     |                                 |
                     v                                 v
       +----------------------------+   +----------------------------+
       | Módulo 2A: Varredura de    |   | Módulo 2B: Resgate         |
       | sORFs Canônicos (find_sorfs|   | Evolutivo Multiframe       |
       | - Tabelas de Tradução 1-33 |   | - 3 fases (Frames 0, 1, 2) |
       | - Início Metionina (M...*) |   | - Janela deslizante (21 aa)|
       +----------------------------+   +----------------------------+
                     |                                 |
                     +----------------+----------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       |    Módulo 3: Motor de Classificação Híbrido (Hybrid AI)     |
       |    - Embeddings Estruturais Profundos (ESM-2 Transformer)   |
       |    - Descritores Físico-Químicos e Biofísicos Explícitos     |
       |    - Extra Trees Classifier Calibrado                       |
       |    - Validação Ortogonal por HMM Profile (hmmsearch)        |
       +-------------------------------------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       | Módulo 4: Desreplicação e Supressão de Não-Máximos (NMS)    |
       | - Filtro de sobreposição (> 50%) na mesma fita              |
       | - Hierarquia: Canônico > Não-canônico > Pseudogênico        |
       +-------------------------------------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       | Módulo 5: Exportação de Resultados e Interpretação IA        |
       | - Tabela Estruturada (.CSV) e Alinhamento FASTA (.fasta)    |
       | - Agente IA Especialista Integrado (Ollama / Llama 3)       |
       +-------------------------------------------------------------+
```

---

## 3. Detalhamento dos Módulos Metodológicos

### 3.1. Módulo 1: Delimitação Genômica de Precisão do Locus 16S

Para evitar o ruído biológico decorrente da tradução indiscriminada de todo o mitogenoma (16.000–17.000 pb) em 6 fases de leitura, o HumaninFinder restringe o espaço de busca primário às coordenadas do gene de rRNA 16S (*MT-RNR2*).

1. **Varredura HMM de Nucleotídeos (`find_16s_locus_precise`):**
   - Utiliza a ferramenta `nhmmer` (integrada ao pacote HMMER3) para alinhar o genoma contra uma sonda conservada de DNA/RNA ribossomal (`16s_probe.fasta`).
   - Extrai as coordenadas de início e fim da região homóloga com limiar de pontuação $S > 50$, aplicando uma margem de segurança de $\pm 50$ pb.
   - Reduz o comprimento do alvo de processamento de ~17.000 pb para ~1.600 pb, conferindo um ganho de velocidade computacional de mais de $10\times$.

2. **Mecanismo de Resiliência (*Fallback Anchor*):**
   - Caso o `nhmmer` não esteja instalado no ambiente ou a sonda não localize o gene em genomas altamente atípicos, o sistema aciona a função `find_16s_locus`, que busca pela assinatura oligonucleotídica ultraconservada `5'-GTTAATGTAGCTTA-3'`.
   - Se nenhuma âncora for identificada, aplica uma janela padrão heurística (posições $1000$ a $5500$).

---

### 3.2. Módulo 2: Algoritmos de Extração de Candidatos e Resgate Evolutivo

O sistema combina duas estratégias complementares de amostragem peptídica no locus 16S:

#### A. Extração Canônica de sORFs (`find_sorfs`)
- Executa a tradução conceitual das fitas *forward* ($+1$) e *reverse complement* ($-1$) utilizando a tabela de código genético informada pelo usuário (suporte integral às Tabelas NCBI 1 a 33, tendo como padrão a **Tabela 2 - Código Mitocondrial de Vertebrados**).
- Seleciona regiões delimitadas por um códon de início canônico (Metionina, `M`) seguido por um segmento contínuo sem paradas internas e finalizado por um códon de parada (`*`), com comprimento restrito entre 10 e 50 aminoácidos:
  $$\text{Padrão Regex: } M[\hat{~}^*]^{L-1}* \quad \text{onde } 10 \le L \le 50$$
- Classificação preliminar: **`Canonical`**.

#### B. Resgate Evolutivo Multiframe Atualizado (`sliding_window_rescue`)
Para superar a cegueira algorítmica frente a inícios não canônicos e eventos de pseudogenização precoce (como a observada no gênero *Mirza*), o algoritmo de janela deslizante foi atualizado para iterar formalmente em **todas as 3 fases de leitura** e em ambas as fitas:
- **Tamanho da Janela:** $w = 21$ aminoácidos ($63$ nucleotídeos);
- **Passo (*step*):** $3$ nucleotídeos (avanço em nível de códon);
- **Varredura Multiframe:** Para cada fita $s \in \{+1, -1\}$ e cada fase $f \in \{0, 1, 2\}$, o índice nucleotídico inicial varia conforme:
  $$i = f + 3k, \quad k \in \mathbb{N}_0, \quad i + 63 \le |nuc|$$
- **Classificação Biológica Heurística do Segmento Traduzido:**
  $$\text{Status} = \begin{cases} 
  \text{Pseudogenic}, & \text{se o peptídeo contiver um ou mais códons de parada } (*) \\
  \text{Canonical}, & \text{se } * \notin \text{pep e o peptídeo iniciar com Metionina } (M) \\
  \text{Non-canonical}, & \text{se } * \notin \text{pep e o peptídeo iniciar sem } M
  \end{cases}$$

---

### 3.3. Módulo 3: Motor de Inteligência Artificial Híbrido (Hybrid AI Engine)

Cada peptídeo candidato extraído é submetido a uma vetorização híbrida multidimensional, que combina semântica biológica profunda com propriedades físico-químicas calculadas deterministicamente.

#### 1. Vetorização Estrutural Profunda (ESM-2 Transformer)
- Emprega o modelo de linguagem de proteínas em larga escala **ESM-2** (*Evolutionary Scale Modeling*, arquitetura `esm2_t6_8M_UR50D`, 8 milhões de parâmetros, 6 camadas de atenção).
- **Tratamento de Tokens Especiais e Paradas:** Símbolos de pseudogenes (`*`) e incógnitas (`X`) são suprimidos na fase de tokenização para permitir a inferência contínua na rede neural.
- **Masked Mean Pooling:** O vetor de representação contextual $\mathbf{v}_{\text{ESM}} \in \mathbb{R}^{320}$ é extraído da última camada oculta, aplicando-se uma média ponderada sobre a máscara de atenção (excluindo tokens de preenchimento `[PAD]` e delimitadores `<cls>` / `<eos>`):
  $$\mathbf{v}_{\text{ESM}} = \frac{\sum_{t=1}^{T} m_t \cdot \mathbf{h}_t}{\sum_{t=1}^{T} m_t}$$
  onde $m_t \in \{0, 1\}$ é o identificador de validade do resíduo e $\mathbf{h}_t$ é a representação vetorial na posição $t$.

#### 2. Extração Físico-Química e Biofísica
Simultaneamente, quatro propriedades biofísicas canônicas da Humanina são computadas utilizando a biblioteca `peptides`:
1. **Carga Líquida ($\mathbf{q}$):** Calculada em pH fisiológico ($7.4$) através da equação de Henderson-Hasselbalch com constantes de dissociação de Lehninger.
2. **Ponto Isoelétrico ($\text{pI}$):** pH no qual a carga líquida total do peptídeo anula-se.
3. **Hidrofobicidade Média ($\mathbf{H}$):** Média ponderada pela escala de hidrofobicidade de Kyte-Doolittle.
4. **Índice Alifático ($\mathbf{AI}$):** Volume relativo ocupado por cadeias laterais alifáticas (Alanina, Valina, Isoleucina e Leucina).

O vetor final de características do candidato $\mathbf{x} \in \mathbb{R}^{324}$ é composto pela concatenação:
$$\mathbf{x} = \left[ \mathbf{v}_{\text{ESM}} \,\|\, \text{Carga} \,\|\, \text{pI} \,\|\, \text{Hidrofobicidade} \,\|\, \text{Índice Alifático} \right]$$

#### 3. Classificação Supervisionada por *Extra Trees Ensemble*
- As características são normalizadas via `StandardScaler`.
- Um modelo de florestas extremamente randomizadas (*Extra Trees Classifier*, 100 estimadores) infere a probabilidade posterior $P(\text{Humanin} \mid \mathbf{x})$.
- O modelo foi treinado em conjunto com validação cruzada estratificada sobre ortólogos experimentais e sintéticos de Humanina contrastados com ruído proteômico mitocondrial e sORFs não-relacionados de mesma extensão.

---

### 3.4. Módulo 4: Integração HMM, Penalização e Supressão de Não-Máximos

#### 1. Validação Ortogonal via Perfil HMM (`run_hmm_search`)
- O fragmento 16S é traduzido em 6 fases e escaneado pelo `hmmsearch` utilizando o perfil `humanin.hmm` (construído a partir de alinhamento múltiplo curado de Humaninas canônicas).
- Loci com hit estatisticamente significativo ($E\text{-value} < 0.1$) recebem um acréscimo de confiança no escore final:
  $$\text{Score}_{\text{ajustado}} = \min\left(0.99, \, \text{Score}_{\text{IA}} + 0.15\right)$$

#### 2. Ponderação Evolutiva de Penalidade por Status
Peptídeos resgatados sem os sinais canônicos completos recebem coeficientes de atenuação para refletir incerteza tradricional sem desconsiderar seu valor estrutural:
$$\text{Score}_{\text{final}} = \begin{cases}
\text{Score}_{\text{ajustado}}, & \text{se Status} = \text{Canonical} \\
\text{Score}_{\text{ajustado}} \times 0.95, & \text{se Status} = \text{Non-canonical} \\
\text{Score}_{\text{ajustado}} \times 0.75, & \text{se Status} = \text{Pseudogenic}
\end{cases}$$

#### 3. Filtro de Sobreposição Biológica e Seleção Adaptativa
Para evitar a multiplicação redundante de janelas sobrepostas originadas do passo de 3 nucleotídeos:
1. Os candidatos são ordenados de forma decrescente por $\text{Score}_{\text{final}}$.
2. Aplica-se **Supressão de Não-Máximos (NMS)**: um candidato $C_j$ é descartado se compartilhar mais de $50\%$ de sobreposição com um candidato de maior pontuação $C_i$ na mesma fita.
3. **Modo Padrão (*Adaptive Selection*):** Retém o candidato com maior pontuação por genoma que satisfaça o limiar $\ge 0.70$ (ou fallback $\ge 0.50$).
4. **Modo Exaustivo (*All-Candidates / Sorfoma*):** Exporta todos os loci não-redundantes que superem o limiar de qualidade.

---

### 3.5. Módulo 5: Exportação e Agente de Interpretação por LLM

1. **Saídas Padronizadas:**
   - Arquivo `.csv` estruturado contendo: sequência peptídica, coordenadas genômicas (início/fim), fita, fase, status biológico, identificador, score final, probabilidade da rede neural (ai_score), pontuação HMM e tag de anotação.
   - Arquivo `.fasta` com cabeçalho informando clado, coordenadas e escore de predição.

2. **Agente Especialista Integrado (`humaninfinder agent`):**
   - Integrado localmente ao servidor **Ollama** via interface `humaninfinder.agent`.
   - Modela um agente analítico com *prompt* de sistema especializado em gerontologia, neurodegeneração e dinâmica evolutiva de sORFs, permitindo ao usuário consultar interpretações biológicas diretamente via terminal.

---

## 4. Validação Experimental: Estudo com 343 Mitogenomas de Primatas

### 4.1. Coleta e Curadoria do Conjunto de Dados
Foram analisados **343 mitogenomas completos de primatas** abrangendo 6 agrupamentos taxonômicos principais:
* **Hominoidea** (Grandes símios e humanos): 33 genomas
* **Cercopithecoidea** (Macacos do Velho Mundo): 91 genomas
* **Platyrrhini** (Macacos do Novo Mundo): 112 genomas
* **Strepsirrhini** (Lêmures, Lorises e Gálagos): 91 genomas
* **Tarsiiformes** (Társios): 6 genomas
* **Outros Primatas / Linhagens Basais**: 10 genomas

### 4.2. Eficácia e Taxa de Detecção Global
Com a implementação do resgate multiframe em 3 fases, o HumaninFinder atingiu **100% de taxa de detecção** ($343/343$ genomas):

| Status Classificado | Frequência Absoluta | Proporção (%) | Média de Escore |
| :--- | :---: | :---: | :---: |
| **Canonical** | **291** | **84.84%** | $0.942$ |
| **Non-canonical** | **31** | **9.04%** | $0.923$ |
| **Pseudogenic** | **21** | **6.12%** | $0.728$ |
| **Total Global** | **343** | **100.0%** | **0.927** |

---

### 4.3. Estudo de Caso Resolutivo: Pseudogenização no Gênero *Mirza*

A importância do escaneamento em 3 fases foi demonstrada diretamente na análise de *Mirza zaza* (`NC_035606.1`) e *Mirza coquereli* (`NC_035656.1`):

```text
Alinhamento do Locus 16S (Posições 2084 a 2147):

Cheirogaleus crossleyi (Lêmure de cauda gorda - Canônico):
  DNA:   ATG GCT ACA CGA GGT TTC AAC TGT CTC TTA CTT TTA ATC AGT GAA ATT GAC CTT CCC GTG AAG
  Prot:   M   A   T   R   G   F   N   C   L   L   L   L   I   S   E   I   D   L   P   V   K
  Score: 0.990 (Status: Canonical)

Mirza zaza (Lêmure-rato-gigante-do-norte - Pseudogene):
  DNA:   ATG GCT ACA CGA AGG TTC AAC TGT CTC TTA CTT TCA GTC AGT GAA ATT GAC CTT CCC GTG AAG
  Prot:   M   A   T   R   *   F   N   C   L   L   L   S   V   S   E   I   D   L   P   V   K
                          ^
              Mutação: GGT -> AGG (Códon Stop na Tabela Mitocondrial 2)
  Score Bruto da Rede Neural ESM-2: 0.9732
  Score Final Ponderado: 0.7425 (Status: Pseudogenic)
```

- **Mecanismo da Falha Tradicional:** O códon 5 sofreu transição para `AGG`, que na Tabela 2 do NCBI codifica para Parada (*Stop*). Métodos de busca de ORF convencional geravam apenas o tetrapeptídeo `MATR*`, descartado por filtros de tamanho mínimo.
- **Resgate pela Metodologia Multiframe:** A varredura na fase $+2$ permitiu à janela de 21 aminoácidos abranger toda a extensão da sequência degenerada. O ESM-2 reconheceu o domínio hidrofóbico central conservado (`FNCLLLSVSEIDLPVK`), classificando-o com **97,3% de confiança**, permitindo o resgate bem-sucedido de uma relíquia molecular até então invisível.

---

## 5. Reprodutibilidade e Disponibilidade

O código-fonte completo, modelos treinados, testes unitários automatizados e os relatórios da análise mitogenômica estão disponíveis publicamente:
- **Repositório GitHub:** [https://github.com/LaBiOmicS/humanin-finder](https://github.com/LaBiOmicS/humanin-finder)
- **Tabelas e Dados Brutos:** [`analysis/results/primates_343_standard_results.csv`](../analysis/results/primates_343_standard_results.csv)
- **Sumário Estatístico por Clado:** [`analysis/reports/standard/summary_by_clade.csv`](../analysis/reports/standard/summary_by_clade.csv)
- **Suíte de Testes Automatizados:** [`tests/`](../tests/)
