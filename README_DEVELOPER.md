# HumaninFinder: Developer & Maintenance Guide

This guide details the automation processes and development standards for the **HumaninFinder** project.

## 🚀 Publication Workflow (Continuous Deployment)

The project uses **Continuous Deployment (CD)** via GitHub Actions to keep PyPI always up to date with the latest stable version.

### Minor Changes (Documentation)
*   **Definition:** Updates to `README.md`, files in the `paper/` or `docs/` folders, or code comments.
*   **Procedure:** Commit and push normally.
*   **Impact:** GitHub Actions **will not** attempt to publish to PyPI. The version number in `pyproject.toml` can remain the same.

### Major Changes (Tool/Source Code)
*   **Definition:** Any alteration to files within `src/`, new dependencies, or changes to biological logic.
*   **Procedure:**
    1.  Apply changes to the source code.
    2.  **Mandatory:** Increment the version number in `pyproject.toml` (e.g., `1.0.0` -> `1.0.1`).
    3.  Push to the `main` branch.
*   **Impact:** GitHub Actions will detect the change, build the distribution package, and automatically publish the new version to PyPI.

> **Note:** If you push changes to the source code but forget to increment the version, the publication Action will skip the upload to prevent version collisions on PyPI.

---

## 🛠️ Environment Maintenance

### Synchronization
Always keep the environment configuration files synchronized when adding new dependencies:
1.  `pyproject.toml`: Core dependencies for `pip` installation.
2.  `environment.yml`: Recommended for Conda/Mamba users.
3.  `pixi.toml`: Modern development setup using Pixi.

### Testing
Always run the test suite before pushing any major changes:
```bash
pytest tests/
```

---

## 📖 Badges and Repository Links
The badges in `README.md` are linked to the official repository at `https://github.com/LaBiOmicS/humanin-finder`. If the repository is moved, ensure these image links are updated accordingly.

---
**Bioinformatics and Omics Laboratory (LaBiOmicS) - UMC**
