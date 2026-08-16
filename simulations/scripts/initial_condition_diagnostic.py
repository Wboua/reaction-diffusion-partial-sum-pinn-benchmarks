from pathlib import Path
import csv
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
z = np.load(OUT / "solutions.npz")
x = z["x"].astype(float)
u0 = z["u_ref"][0].astype(float)
v0 = z["v_ref"][0].astype(float)
den = np.sqrt(np.sum(u0*u0 + v0*v0))
mass0 = np.trapezoid(u0+v0, x)
rows=[]
for seed in [11,29,47,71,101]:
    u=z[f"pinn_seed_{seed}_u"][0].astype(float)
    v=z[f"pinn_seed_{seed}_v"][0].astype(float)
    rel=np.sqrt(np.sum((u-u0)**2+(v-v0)**2))/den
    rmse=np.sqrt(np.sum((u-u0)**2+(v-v0)**2)/(2*len(x)))
    mass=np.trapezoid(u+v,x)
    rows.append({"seed":seed,"initial_relative_l2":rel,"initial_rmse":rmse,"initial_mass":mass,"initial_mass_error":mass-mass0})
with open(OUT/"initial_condition_diagnostic.csv","w",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
print("wrote", OUT/"initial_condition_diagnostic.csv")
