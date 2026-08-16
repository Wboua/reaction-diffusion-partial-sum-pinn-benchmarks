# Codex brief — formatting + GitHub publication

Work on this repository without changing any scientific numerical value unless it is recomputed from the archived source-of-record data.

## Priorities

1. Preserve `manuscript/Main.tex` scientific content and MJM/Birkhäuser structure.
2. Make only requested presentation/formatting modifications.
3. Keep every figure traceable to `simulations/outputs/` where possible.
4. Do not fabricate missing simulation code or numerical results.
5. Inspect the original project for missing solver/training scripts. If found, copy and normalize them under `simulations/src/` and document exact commands.
6. Create `requirements.txt` / environment documentation from the real imports and versions.
7. Add a top-level reproduction script only after all dependencies and source scripts are present.
8. Prepare the repository for GitHub with a concise README, repository tree, and reproducibility instructions.
9. After the GitHub URL is known, update the manuscript's Code and Data Availability section with that exact URL. Do not invent a URL.
10. Optionally prepare a Zenodo-ready release after the GitHub repository is complete.

## Integrity rule

Archived CSV/NPZ files are the source of record for the paper. If a rerun differs, report and investigate the discrepancy; do not silently overwrite published values.
