# Reaction-diffusion partial-sum PINN benchmarks

Reproducibility package for the numerical experiments accompanying the associated Mediterranean Journal of Mathematics manuscript. It contains the FDM, FEM and PINN implementations, the archived numerical outputs used in the reported results, and scripts for validation diagnostics and figure regeneration.

## Contents

- `simulations/src/` — complete FDM, P1 Galerkin FEM and PINN solvers; study, convergence, ablation and diagnostic runners.
- `simulations/scripts/` — additional output-based diagnostics and error-figure regeneration.
- `simulations/outputs/` — archived CSV and NPZ outputs used in the numerical study.

## Reproduction

Create a fresh Python environment, then install the dependencies:

```bash
pip install -r simulations/src/requirements.txt
```

Run a quick end-to-end check:

```bash
python simulations/src/run_study.py --mode quick
```

Use `--mode publication` for the main five-seed PINN study. Recreated artifacts are written to `simulations/outputs/`.

## Archived outputs

The archived outputs include common-grid reference/FDM/FEM/PINN fields, accuracy and runtime metrics, manufactured-solution refinements, three-component benchmark fields and metrics, and coercivity and initial-condition diagnostics. They remain the source of record for the numerical values reported in the associated manuscript.

## Archive and citation

The software record is archived on Zenodo.

- Version `v1.0.0`: [10.5281/zenodo.21968286](https://doi.org/10.5281/zenodo.21968286)
- Concept DOI for all versions: [10.5281/zenodo.21968285](https://doi.org/10.5281/zenodo.21968285)
