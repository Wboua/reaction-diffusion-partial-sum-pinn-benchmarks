import argparse,csv,json,platform,time,tracemalloc
from dataclasses import asdict
from pathlib import Path
import numpy as np
from scipy.interpolate import RegularGridInterpolator
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model import Config,quick_config
from classical_solvers import fdm,fem
from pinn_solver import train,residual

OUT=Path(__file__).resolve().parent.parent/'outputs'
def timed(fn):
    tracemalloc.start(); t=time.perf_counter(); val=fn(); elapsed=time.perf_counter()-t; peak=tracemalloc.get_traced_memory()[1]/1048576; tracemalloc.stop(); return val,elapsed,peak
def interp(sol,t,x):
    ts,xs,U,V=sol; T,X=np.meshgrid(t,x,indexing='ij'); pts=np.c_[T.ravel(),X.ravel()]
    fun=lambda z: RegularGridInterpolator((ts,xs),z)(pts).reshape(T.shape)
    return fun(U),fun(V)
def metric(method,seed,u,v,ur,vr,x,elapsed,mem,test_residual=float('nan'),train_residual=float('nan'),inference_seconds=float('nan')):
    e=np.r_[u.ravel()-ur.ravel(),v.ravel()-vr.ravel()]; r=np.r_[ur.ravel(),vr.ravel()]; mass=np.trapezoid(u+v,x,axis=1)
    return dict(method=method,seed=seed,rmse=np.sqrt(np.mean(e*e)),relative_l2=np.linalg.norm(e)/np.linalg.norm(r),min_value=min(u[:,1:-1].min(),v[:,1:-1].min()),test_residual=test_residual,train_residual=train_residual,inference_seconds=inference_seconds,max_mass_increase=np.maximum(np.diff(mass),0).max(initial=0),runtime_seconds=elapsed,peak_memory_mb=mem)
def write(path,rows):
    with path.open('w',newline='',encoding='utf8') as f: w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
def figures(t,x,ur,vr,fields,hist):
    fig,ax=plt.subplots(2,3,figsize=(12,7),constrained_layout=True); ext=[0,1,0,t[-1]]
    panels=[(ur,'Reference u'),(vr,'Reference v'),(fields['PINN'][0],'PINN u'),(fields['PINN'][1],'PINN v'),(fields['FDM'][0]-ur,'FDM error u'),(fields['FEM'][0]-ur,'FEM error u')]
    for a,(z,title) in zip(ax.ravel(),panels): im=a.imshow(z,origin='lower',aspect='auto',extent=ext,cmap='viridis'); a.set(title=title,xlabel='x',ylabel='t'); fig.colorbar(im,ax=a)
    fig.savefig(OUT/'solution_comparison.png',dpi=220); plt.close(fig)
    fig,ax=plt.subplots(figsize=(6,4))
    for seed,h in hist.items(): a=np.asarray(h); ax.semilogy(a[:,0],a[:,1],label=f'seed {seed}')
    ax.set(xlabel='epoch',ylabel='total loss',title='PINN convergence'); ax.grid(alpha=.3); ax.legend(); fig.tight_layout(); fig.savefig(OUT/'loss_convergence.png',dpi=220); plt.close(fig)
    fig,ax=plt.subplots(2,1,figsize=(7,6),sharex=True,gridspec_kw={'height_ratios':[2,1]})
    mass_ref=np.trapezoid(ur+vr,x,axis=1)
    styles={'FDM':dict(color='C0',ls='-',marker='o'),'FEM':dict(color='C2',ls='--',marker='s'),'PINN':dict(color='C3',ls='-.',marker='^')}
    ax[0].plot(t,mass_ref,color='k',ls=':',lw=2.4,label='Reference',zorder=1)
    for rank,(name,(u,v)) in enumerate(fields.items(),start=2):
        mass=np.trapezoid(u+v,x,axis=1); st=styles[name]
        ax[0].plot(t,mass,lw=1.45,markevery=5,ms=4,mfc='white',label=name,zorder=rank,**st)
        ax[1].plot(t,mass-mass_ref,lw=1.45,markevery=5,ms=4,mfc='white',label=name,**st)
    ax[0].set(ylabel='total mass',title='Positivity-compatible mass-control diagnostic')
    ax[1].axhline(0,color='k',ls=':',lw=1); ax[1].set(xlabel='t',ylabel='mass error')
    for a in ax: a.grid(alpha=.25); a.legend(frameon=False,ncol=2)
    fig.tight_layout(); fig.savefig(OUT/'mass_control.png',dpi=220,bbox_inches='tight'); plt.close(fig)
def main():
    p=argparse.ArgumentParser(); p.add_argument('--mode',choices=['quick','publication'],default='quick'); a=p.parse_args(); cfg=quick_config() if a.mode=='quick' else Config(); OUT.mkdir(exist_ok=True)
    ref,rt,rm=timed(lambda:fdm(cfg,cfg.ref_nx,cfg.ref_dt)); t=np.linspace(0,cfg.T,cfg.eval_nt); x=np.linspace(0,1,cfg.eval_nx); ur,vr=interp(ref,t,x)
    rows=[]; fields={}; histories={}; pinn_fields={}
    sol,sec,mem=timed(lambda:fdm(cfg)); u,v=interp(sol,t,x); fields['FDM']=(u,v); rows.append(metric('FDM','deterministic',u,v,ur,vr,x,sec,mem))
    sol,sec,mem=timed(lambda:fem(cfg)); u,v=interp(sol,t,x); fields['FEM']=(u,v); rows.append(metric('FEM','deterministic',u,v,ur,vr,x,sec,mem))
    T,X=np.meshgrid(t,x,indexing='ij'); tx=np.c_[T.ravel(),X.ravel()].astype('float32'); test_rng=np.random.default_rng(2025); common_test_tx=np.c_[test_rng.random(5000)*cfg.T,test_rng.random(5000)].astype('float32')
    for seed in cfg.seeds:
        tracemalloc.start(); net,h,sec=train(cfg,seed); mem=tracemalloc.get_traced_memory()[1]/1048576; tracemalloc.stop(); tic=time.perf_counter(); y=net(tx).numpy(); infer=time.perf_counter()-tic; u=y[:,0].reshape(T.shape); v=y[:,1].reshape(T.shape); rr=residual(net,__import__('tensorflow').constant(common_test_tx),cfg); test_res=float(np.sqrt(np.mean(rr[0].numpy()**2+rr[1].numpy()**2))); train_res=float(np.sqrt(h[-1][2])); rows.append(metric('PINN',seed,u,v,ur,vr,x,sec,mem,test_res,train_res,infer)); pinn_fields[seed]=(u,v); histories[seed]=h
        with (OUT/f'loss_seed_{seed}.csv').open('w',newline='') as f: w=csv.writer(f); w.writerow(['epoch','total','pde','initial']); w.writerows(h)
    pinn_rows=[r for r in rows if r['method']=='PINN']; median_rmse=float(np.median([r['rmse'] for r in pinn_rows])); representative_seed=min(pinn_rows,key=lambda r:abs(r['rmse']-median_rmse))['seed']; fields['PINN']=pinn_fields[representative_seed]
    write(OUT/'metrics.csv',rows); summary=[]
    for name in ['FDM','FEM','PINN']:
        s=[r for r in rows if r['method']==name]; d={'method':name}
        for k in ['rmse','relative_l2','min_value','test_residual','train_residual','inference_seconds','max_mass_increase','runtime_seconds','peak_memory_mb']:
            z=np.array([r[k] for r in s]); count=int(np.sum(~np.isnan(z))); d[k+'_mean']=float(np.nanmean(z)) if count else float('nan'); d[k+'_std']=float(np.nanstd(z,ddof=1)) if count>1 else 0.0
        summary.append(d)
    write(OUT/'summary.csv',summary); archived={f'{n.lower()}_{q}':z for n,(u,v) in fields.items() for q,z in [('u',u),('v',v)]}; archived.update({f'pinn_seed_{seed}_{q}':z for seed,(u,v) in pinn_fields.items() for q,z in [('u',u),('v',v)]}); np.savez_compressed(OUT/'solutions.npz',t=t,x=x,u_ref=ur,v_ref=vr,**archived); figures(t,x,ur,vr,fields,histories)
    (OUT/'metadata.json').write_text(json.dumps(dict(mode=a.mode,config=asdict(cfg),reference_runtime=rt,reference_memory_mb=rm,python=platform.python_version(),platform=platform.platform(),processor=platform.processor(),machine=platform.machine(),numpy=np.__version__,scipy=__import__('scipy').__version__,tensorflow=__import__('tensorflow').__version__,float_precision='float32 (PINN), float64 (FDM/FEM)',independent_test_seed=2025,representative_pinn_seed=representative_seed),indent=2),encoding='utf8'); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
