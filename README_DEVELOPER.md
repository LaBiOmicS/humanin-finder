# HumaninFinder: Developer & Maintenance Guide

Este guia detalha os processos de automação e padrões de desenvolvimento do projeto **HumaninFinder**.

## 🚀 Fluxo de Trabalho de Publicação (CD)

O projeto utiliza **Continuous Deployment** através do GitHub Actions para manter o PyPI sempre atualizado.

### Mudanças Menores (Documentação)
*   **O que são:** Mudanças no `README.md`, arquivos na pasta `paper/`, `docs/`, ou comentários.
*   **Procedimento:** Realize o commit e push normalmente.
*   **Impacto:** O GitHub Actions **não** tentará publicar no PyPI. O número da versão no `pyproject.toml` pode permanecer o mesmo.

### Mudanças Maiores (Ferramenta/Código)
*   **O que são:** Qualquer alteração em `src/`, novas dependências ou mudanças na lógica biológica.
*   **Procedimento:**
    1.  Realize as alterações no código.
    2.  **Obrigatório:** Aumente o número da versão no arquivo `pyproject.toml` (ex: `1.0.0` -> `1.0.1`).
    3.  Realize o push para a branch `main`.
*   **Impacto:** O GitHub Actions detectará a mudança, fará o build do pacote e publicará automaticamente a nova versão no PyPI.

> **Nota:** Se você realizar uma mudança no código mas esquecer de aumentar a versão, a Action de publicação falhará silenciosamente (skip) para evitar colisões no PyPI.

---

## 🛠️ Manutenção de Ambientes

### Sincronização
Mantenha sempre os arquivos de ambiente sincronizados quando adicionar uma nova dependência:
1.  `pyproject.toml`: Dependências para instalação via `pip`.
2.  `environment.yml`: Dependências para usuários de Conda/Mamba.
3.  `pixi.toml`: Configurações para desenvolvimento moderno com Pixi.

### Testes
Sempre execute os testes antes de realizar um push de mudança maior:
```bash
pytest tests/
```

---

## 📖 Badges e Documentação
Os badges no `README.md` são sincronizados com os workflows do repositório oficial em `https://github.com/LaBiOmicS/humanin-finder`. Ao trocar de repositório, certifique-se de atualizar os links das imagens no README.

---
**Laboratório de Bioinformática e Ômicas (LaBiOmicS) - UMC**
