"""PINN ablations: hard constraints, collocation size, and arithmetic precision."""
import csv,time
from pathlib import Path
import numpy as np
import tensorflow as tf
from dataclasses import replace
from model import Config
from pinn_solver import train,residual
from classical_solvers import fdm
from scipy.interpolate import RegularGridInterpolator

def reference(cfg):
    t,x,u,v=fdm(cfg,cfg.ref_nx,cfg.ref_dt); return t,x,u,v

def evaluate(net,cfg,ref,seed):
    t=np.linspace(0,cfg.T,cfg.eval_nt); x=np.linspace(0,1,cfg.eval_nx); T,X=np.meshgrid(t,x,indexing='ij'); pts=np.c_[T.ravel(),X.ravel()]
    tr,xr,ur0,vr0=ref; ur=RegularGridInterpolator((tr,xr),ur0)(pts).reshape(T.shape); vr=RegularGridInterpolator((tr,xr),vr0)(pts).reshape(T.shape)
    y=net(pts.astype('float32')).numpy(); u=y[:,0].reshape(T.shape); v=y[:,1].reshape(T.shape); e=np.r_[(u-ur).ravel(),(v-vr).ravel()]
    rng=np.random.default_rng(seed+500); q=np.c_[rng.random(5000)*cfg.T,rng.random(5000)].astype('float32'); r=residual(net,tf.constant(q),cfg); res=np.sqrt(np.mean(r[0].numpy()**2+r[1].numpy()**2))
    return np.sqrt(np.mean(e*e)),res,min(u[:,1:-1].min(),v[:,1:-1].min())

def main():
    out=Path(__file__).resolve().parent.parent/'outputs'; out.mkdir(exist_ok=True)
    base=Config(epochs=1200,seeds=(11,)); ref=reference(base); rows=[]
    for nf in (1000,3000,6000):
        cfg=replace(base,nf=nf); net,h,sec=train(cfg,11); rmse,res,mn=evaluate(net,cfg,ref,11); rows.append(dict(experiment='collocation',setting=f'Nf={nf}',rmse=rmse,test_residual=res,min_interior=mn,runtime_seconds=sec))
    with (out/'ablations.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
    print(rows)
if __name__=='__main__': main()
