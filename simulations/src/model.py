from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Config:
    T: float=.25; d1: float=.10; d2: float=.50
    eval_nx: int=101; eval_nt: int=51
    ref_nx: int=401; ref_dt: float=2.5e-5
    fdm_nx: int=101; fdm_dt: float=2e-4
    fem_ne: int=100; fem_dt: float=2e-4
    layers: int=4; width: int=48; nf: int=3000; nic: int=200
    epochs: int=2000; lr: float=1e-3; seeds: tuple=(11,29,47,71,101)

def quick_config():
    return Config(ref_nx=161,ref_dt=1e-4,fdm_nx=81,fdm_dt=5e-4,
        fem_ne=80,fem_dt=5e-4,layers=3,width=32,nf=1200,nic=100,
        epochs=300,seeds=(11,))

def initial_data(x):
    return .8*np.sin(np.pi*x)**2, .55*np.sin(2*np.pi*x)**2

def reaction(u,v,ux,vx):
    a=u*ux**2; b=v*vx**2
    return -a,a-b
