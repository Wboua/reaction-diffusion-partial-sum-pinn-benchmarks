# Reproducible numerical study

This directory contains the complete numerical supplement. The common problem is

    u_t - d1 u_xx = -u (u_x)^2,
    v_t - d2 v_xx =  u (u_x)^2 - v (v_x)^2,

on `(0,0.25) x (0,1)` with homogeneous Dirichlet data. For nonnegative states, `f1 <= 0` and `f1+f2 <= 0`; the example is quasi-positive, has partial-sum mass control, and has quadratic gradient growth.

## Environment

Create a fresh environment and install `requirements.txt`. The submitted local virtual environment is not needed.

## Reproduction

Pipeline check:

    python run_study.py --mode quick

Main five-seed experiment:

    python run_study.py --mode publication

Reference refinement:

    python reference_convergence.py

Collocation ablation:

    python run_ablations.py

Article diagnostics from the archived outputs (no solver rerun):

    python make_article_diagnostics.py
Outputs are written to `outputs/`: raw and summary metrics, independent residuals, loss histories, convergence and ablation tables, compressed fields, metadata, and figures. The article-diagnostics script generates temporal snapshots and a refinement/ablation/accuracy--cost panel from those archived files. No reported numerical value is hard-coded in a plotting routine.

## Method notes

The FDM and FEM use identical data and semi-implicit time treatment. The FEM nonlinear loads are assembled elementwise by two-point Gauss quadrature. The PINN enforces nonnegativity and homogeneous Dirichlet values through its output map. Five seeds are trained; a common set of 5000 independently sampled points (seed 2025) evaluates every network. The median-RMSE realization is used in field figures, while aggregate values report the sample standard deviation. The article-diagnostics script also evaluates the continuous first-component energy identity on the archived common grid.
