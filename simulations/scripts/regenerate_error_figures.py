import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'Supplementary' / 'reproducibility_outputs' / 'solutions.npz'
FIG = ROOT / 'figures'
z = np.load(DATA)
t, x = z['t'], z['x']
extent = [x.min(), x.max(), t.min(), t.max()]
u_ref, v_ref = z['u_ref'], z['v_ref']
fdm_u, fdm_v = z['fdm_u'], z['fdm_v']
fem_u, fem_v = z['fem_u'], z['fem_v']
pinn_u, pinn_v = z['pinn_seed_29_u'], z['pinn_seed_29_v']

# Reference/PINN fields with shared scale within each component.
fig, axes = plt.subplots(2, 2, figsize=(8.2, 6.0), constrained_layout=True)
u_min, u_max = min(u_ref.min(), pinn_u.min()), max(u_ref.max(), pinn_u.max())
v_min, v_max = min(v_ref.min(), pinn_v.min()), max(v_ref.max(), pinn_v.max())
for ax, arr, title, lo, hi in [
    (axes[0,0],u_ref,'Reference $u$',u_min,u_max),
    (axes[0,1],pinn_u,'PINN $u$ (seed 29)',u_min,u_max),
    (axes[1,0],v_ref,'Reference $v$',v_min,v_max),
    (axes[1,1],pinn_v,'PINN $v$ (seed 29)',v_min,v_max),
]:
    im=ax.imshow(arr,origin='lower',aspect='auto',extent=extent,vmin=lo,vmax=hi)
    ax.set_title(title); ax.set_xlabel('$x$'); ax.set_ylabel('$t$'); fig.colorbar(im,ax=ax)
fig.savefig(FIG/'reproducible_solution_comparison.png',dpi=350,bbox_inches='tight')
plt.close(fig)

# FDM/FEM absolute errors with a shared scale within each component.
eu_fdm, ev_fdm = np.abs(fdm_u-u_ref), np.abs(fdm_v-v_ref)
eu_fem, ev_fem = np.abs(fem_u-u_ref), np.abs(fem_v-v_ref)
u_max=max(eu_fdm.max(),eu_fem.max()); v_max=max(ev_fdm.max(),ev_fem.max())
fig, axes=plt.subplots(2,2,figsize=(8.0,6.0),constrained_layout=True)
for ax,arr,title,vmax in [
    (axes[0,0],eu_fdm,'FDM: $|u-u_{ref}|$',u_max),
    (axes[0,1],ev_fdm,'FDM: $|v-v_{ref}|$',v_max),
    (axes[1,0],eu_fem,'FEM: $|u-u_{ref}|$',u_max),
    (axes[1,1],ev_fem,'FEM: $|v-v_{ref}|$',v_max),
]:
    im=ax.imshow(arr,origin='lower',aspect='auto',extent=extent,vmin=0,vmax=vmax)
    ax.set_title(title); ax.set_xlabel('$x$'); ax.set_ylabel('$t$'); fig.colorbar(im,ax=ax)
fig.savefig(FIG/'reproducible_classical_error_comparison.png',dpi=350,bbox_inches='tight')
plt.close(fig)

# PINN absolute errors displayed separately because of the much larger magnitude.
fig, axes=plt.subplots(1,2,figsize=(8.0,3.2),constrained_layout=True)
for ax,arr,title in [
    (axes[0],np.abs(pinn_u-u_ref),'PINN: $|u-u_{ref}|$'),
    (axes[1],np.abs(pinn_v-v_ref),'PINN: $|v-v_{ref}|$'),
]:
    im=ax.imshow(arr,origin='lower',aspect='auto',extent=extent,vmin=0,vmax=arr.max())
    ax.set_title(title); ax.set_xlabel('$x$'); ax.set_ylabel('$t$'); fig.colorbar(im,ax=ax)
fig.savefig(FIG/'reproducible_pinn_error_comparison.png',dpi=350,bbox_inches='tight')
plt.close(fig)
