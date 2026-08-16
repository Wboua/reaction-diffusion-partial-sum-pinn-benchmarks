# Numerical figure consistency corrections

- Rebuilt the reference/PINN field comparison with identical colour limits within each component.
- Added both u and v absolute-error maps for FDM and FEM; the prior presentation showed only the first-component classical errors.
- FDM and FEM now share the same error scale within u and within v, enabling direct visual comparison.
- PINN error maps are displayed separately because their magnitude is roughly two orders larger; this prevents a common all-method scale from erasing the classical error structure.
- Added componentwise RMSE values to the Results text: FDM (u=6.966e-5, v=1.733e-4), FEM (u=4.723e-5, v=1.162e-4), median PINN seed 29 (u=1.848e-3, v=4.154e-3).
- Changed Results floats from forced [H] placement to journal-friendlier [!htbp] placement.
- Added a regeneration script and the source `solutions.npz` to the supplementary reproducibility material.
