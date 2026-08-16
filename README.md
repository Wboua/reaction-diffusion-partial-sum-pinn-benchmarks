# MJM Reaction–Diffusion / PINN manuscript repository

This repository is organized for the Mediterranean Journal of Mathematics submission and for reproducibility/GitHub archiving.

## Structure

- `manuscript/` — current MJM `birkjour` manuscript source, bibliography, compiled PDF and publication figures.
- `simulations/outputs/` — archived numerical outputs used in the manuscript (`CSV` and `NPZ`).
- `simulations/scripts/` — analysis/diagnostic and figure-regeneration scripts available in the current revision workspace.
- `docs/` — Birkhäuser template documentation and revision/audit notes.

## Source-of-record numerical outputs

The numerical values reported in the manuscript are backed by the files in `simulations/outputs/`, including:

- `solutions.npz` — two-component reference/FDM/FEM/PINN fields.
- `three_component_solutions.npz` — three-component reference/FDM/FEM fields.
- `metrics.csv`, `summary.csv` — main accuracy/runtime/PINN metrics.
- `mms_fdm_spatial.csv`, `mms_fem_spatial.csv`, `mms_temporal.csv` — manufactured-solution verification.
- `three_component_metrics.csv`, `three_component_reference_check.csv` — non-monotone benchmark metrics.
- `coercivity_diagnostic.csv` — coercivity-bound consistency diagnostic.
- `initial_condition_diagnostic.csv` — PINN initial-condition diagnostic.

## Available scripts

- `coercivity_diagnostic.py`
- `initial_condition_diagnostic.py`
- `regenerate_error_figures.py`

The archived outputs above are the source of record for the values in the manuscript.

### Reproducibility

The complete original two-component FDM, FEM and PINN solver/training workflow has been restored under `simulations/src/`. Install `simulations/src/requirements.txt`, then run `python simulations/src/run_study.py --mode quick` for a pipeline check or use `--mode publication` for the five-seed study. Recreated artifacts are written to `simulations/outputs/`.

The restored package includes `classical_solvers.py` (FDM and P1 Galerkin FEM), `model.py` and `pinn_solver.py`, plus the main study, convergence, ablation and diagnostic runners. Existing archived outputs remain the source of record for the manuscript values.

## Suggested GitHub repository name

`reaction-diffusion-partial-sum-pinn-benchmarks`

## Recommended citation in the manuscript

After publishing the repository, replace the repository placeholder in the Code and Data Availability statement with the permanent GitHub URL. For archival reproducibility, create a Zenodo release from the GitHub repository and cite the DOI once available.
