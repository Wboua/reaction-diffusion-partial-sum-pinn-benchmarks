# AI-review-resistant revision

This revision implements the automated-review vulnerabilities identified after the hostile-review pass.

## Core corrections

1. **Documentary novelty positioning**
   - Added a publication-scope paragraph for the two earlier triangular critical-gradient references.
   - Reworked the prior-vs-present table so it does not attribute an unverified local formula or error to earlier theorems.
   - The novelty claim is now confined to the self-contained exact cross-gradient identity, the explicitly exposed full-gradient hypothesis, and the conditional removal of monotone diffusion ordering at the absorption step.

2. **Closed the reaction-sign logic**
   - Made explicit that the common nonnegative cutoff preserves quasi-positivity.
   - Added the nonnegative-cone implication for the regularized approximants.
   - Added the chain `u_{i,n} >= 0 -> U_{r,n} >= 0 -> T_k(U_{r,n}) >= 0`, hence the partial-sum sign implies a nonpositive tested reaction term.
   - Proposition 2.3 now assumes the primitive structural ingredients instead of assuming the already-multiplied sign conclusion.

3. **Explicit PINN initial-condition diagnostic**
   - Recovered the archived five-seed solution arrays.
   - Added the relative initial-data error `E_IC` to the methodology.
   - Added five-seed values: 4.024%, 3.960%, 4.816%, 3.972%, 4.445%.
   - Added mean +/- sample SD: 4.243% +/- 0.378%.
   - Added initial combined RMSE: (1.775 +/- 0.158)e-2.
   - Added `initial_condition_diagnostic.py` and `outputs/initial_condition_diagnostic.csv`.

4. **Coercivity diagnostic terminology hardened**
   - Renamed the numerical quantity to **coercivity-bound consistency diagnostic**.
   - Retained the explicit statement that it is post-processed consistency evidence, not a proof of Proposition 2.3 or a discrete energy law.

5. **MMS evidence clarified**
   - Removed the potentially tautological `manufactured residual = 0.0` claim.
   - The refinement study is now identified as the evidential code-verification result.

## Additional automated-review vulnerabilities corrected

- Normalized the diffusion claim to **any fixed positive diffusion vector, conditional on the full-gradient bounds**.
- Removed the notation collision between critical-growth control functions and gradient-bound constants by using `Gamma_i` for the former and `C_j` for the latter.
- Reduced repeated defensive disclaimers in the theoretical scope and conclusion.
- Removed prospective DOI language from Code and Data Availability.
- Restored raw PINN solution arrays and metrics to the reproducibility package so the new diagnostic is recomputable.
- Kept the PINN comparison explicitly diagnostic rather than presenting it as a state-of-the-art optimization contest.
- Preserved the structure-aware title and the scientific-architecture figure.

## Documentary verification note

The accessible bibliographic record confirms the theorem-level scope of the earlier works used for positioning. The revision deliberately does **not** invent page or equation numbers for the older papers where a full version-of-record text was not available in the working environment. The local cross-gradient calculation is therefore reproduced self-containedly in the manuscript rather than attributed to an unverifiable equation location.
