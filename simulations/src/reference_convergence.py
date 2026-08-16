import csv,time
from pathlib import Path
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from model import Config
from classical_solvers import fdm
cfg=Config(); grids=[(101,2e-4),(201,1e-4),(401,2.5e-5),(801,1.25e-5)]; sol=[]
OUT=Path(__file__).resolve().parent.parent/'outputs'
OUT.mkdir(exist_ok=True)
for nx,dt in grids:
    start=time.perf_counter(); s=fdm(cfg,nx,dt); sol.append((nx,dt,s,time.perf_counter()-start))
t,x,U,V=sol[-1][2]; T,X=np.meshgrid(t,x,indexing='ij'); pts=np.c_[T.ravel(),X.ravel()]; ref=np.r_[U.ravel(),V.ravel()]; rows=[]
for nx,dt,(tc,xc,uc,vc),sec in sol:
    if nx==801: ui,vi=U,V
    else:
        ui=RegularGridInterpolator((tc,xc),uc)(pts).reshape(U.shape); vi=RegularGridInterpolator((tc,xc),vc)(pts).reshape(V.shape)
    e=np.r_[(ui-U).ravel(),(vi-V).ravel()]; rows.append(dict(nx=nx,dt=dt,rmse=np.sqrt(np.mean(e*e)),relative_l2=np.linalg.norm(e)/np.linalg.norm(ref),runtime_seconds=sec))
with (OUT/'convergence.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
print(rows)
