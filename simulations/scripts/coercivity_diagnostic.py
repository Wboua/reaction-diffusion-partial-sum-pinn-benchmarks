from pathlib import Path
import csv
import numpy as np

HERE = Path(__file__).resolve().parent
OUT = HERE / 'outputs'
DATA = np.load(OUT / 'three_component_solutions.npz')

t = DATA['t']
x = DATA['x']
d3 = 0.3
C1 = 1.2
C2 = 0.0708984375
YOUNG = (7/30)*C1 + (7/12)*C2


def phi_k(s, k):
    a = np.abs(s)
    return np.where(a <= k, 0.5*s*s, k*a - 0.5*k*k)


def compute(u, v, w, k):
    U = u + v + w
    Tk = np.clip(U, -k, k)
    gx = np.gradient(Tk, x, axis=1, edge_order=2)
    spatial = np.trapezoid(gx*gx, x, axis=1)
    lhs = 0.5*d3*np.trapezoid(spatial, t)
    initial = np.trapezoid(phi_k(U[0], k), x)
    rhs = initial + YOUNG
    return lhs, initial, rhs, lhs/rhs

rows = []
for method, keys in {
    'Reference': ('u_ref', 'v_ref', 'w_ref'),
    'FDM': ('fdm_u', 'fdm_v', 'fdm_w'),
    'FEM': ('fem_u', 'fem_v', 'fem_w'),
}.items():
    u, v, w = (DATA[k] for k in keys)
    for k in (0.25, 0.5, 1.0, 2.0):
        lhs, initial, rhs, ratio = compute(u, v, w, k)
        rows.append({
            'method': method, 'k': k,
            'coercivity_lhs': lhs,
            'initial_phi': initial,
            'young_remainder': YOUNG,
            'analytical_bound': rhs,
            'lhs_over_bound': ratio,
        })

with (OUT / 'coercivity_diagnostic.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader(); writer.writerows(rows)

print('Wrote', OUT / 'coercivity_diagnostic.csv')
for row in rows:
    print(row)
