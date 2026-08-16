"""Generate article diagnostics from archived outputs without rerunning solvers."""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent.parent/'outputs'

def snapshots(d):
    t,x=d['t'],d['x']; methods=(('Reference','ref','k'),('FDM','fdm','C0'),('FEM','fem','C2'),('PINN (seed 29)','pinn','C3'))
    fig,ax=plt.subplots(2,3,figsize=(12,6.7),sharex=True)
    for col,target in enumerate((.05,.15,.25)):
        q=int(np.argmin(abs(t-target)))
        for label,key,color in methods:
            for row,var in enumerate(('u','v')):
                ax[row,col].plot(x,d[f'{var}_{key}' if key=='ref' else f'{key}_{var}'][q],color=color,lw=2 if key=='ref' else 1.35,label=label)
        ax[0,col].set_title(fr'$t={t[q]:.2f}$'); ax[1,col].set_xlabel('x')
        for row in range(2): ax[row,col].grid(alpha=.22)
    ax[0,0].set_ylabel('u(t,x)'); ax[1,0].set_ylabel('v(t,x)'); ax[0,2].legend(frameon=False,fontsize=8)
    fig.suptitle('Temporal snapshots on the common evaluation grid'); fig.tight_layout()
    fig.savefig(OUT/'temporal_snapshots.png',dpi=220,bbox_inches='tight'); plt.close(fig)

def mass_control(d):
    t,x=d['t'],d['x']
    mass_ref=np.trapezoid(d['u_ref']+d['v_ref'],x,axis=1)
    methods=(('FDM','fdm','C0','-','o'),('FEM','fem','C2','--','s'),('PINN (seed 29)','pinn','C3','-.','^'))
    fig,ax=plt.subplots(2,1,figsize=(7,6),sharex=True,gridspec_kw={'height_ratios':[2,1]})
    ax[0].plot(t,mass_ref,color='k',ls=':',lw=2.4,label='Reference',zorder=1)
    for rank,(label,key,color,ls,marker) in enumerate(methods,start=2):
        mass=np.trapezoid(d[f'{key}_u']+d[f'{key}_v'],x,axis=1)
        style=dict(color=color,ls=ls,marker=marker,lw=1.45,markevery=5,ms=4,mfc='white')
        ax[0].plot(t,mass,label=label,zorder=rank,**style)
        ax[1].plot(t,mass-mass_ref,label=label,**style)
    ax[0].set(ylabel='total mass',title='Positivity-compatible mass-control diagnostic')
    ax[1].axhline(0,color='k',ls=':',lw=1); ax[1].set(xlabel='t',ylabel='mass error')
    for a in ax: a.grid(alpha=.25); a.legend(frameon=False,ncol=2)
    fig.tight_layout(); fig.savefig(OUT/'mass_control.png',dpi=220,bbox_inches='tight'); plt.close(fig)
def energy_diagnostic(d,d1=0.1):
    """Check the continuous u-energy identity on the archived evaluation grid."""
    t,x=d['t'],d['x']
    methods=(('Reference','ref','k',':'),('FDM','fdm','C0','-'),('FEM','fem','C2','--'),('PINN (seed 29)','pinn','C3','-.'))
    fig,ax=plt.subplots(1,2,figsize=(10,3.8)); rows=[]
    for label,key,color,ls in methods:
        u=d['u_ref'] if key=='ref' else d[f'{key}_u']
        ux=np.gradient(u,x,axis=1,edge_order=2)
        energy=.5*np.trapezoid(u*u,x,axis=1)
        dissipation=np.trapezoid(d1*ux*ux+u*u*ux*ux,x,axis=1)
        cumulative=np.zeros_like(t)
        cumulative[1:]=np.cumsum(.5*(dissipation[1:]+dissipation[:-1])*np.diff(t))
        defect=energy+cumulative-energy[0]
        ax[0].plot(t,energy,color=color,ls=ls,lw=1.8,label=label)
        ax[1].plot(t,defect/energy[0],color=color,ls=ls,lw=1.8,label=label)
        rows.append(dict(method=label,initial_energy=energy[0],terminal_energy=energy[-1],max_abs_defect=np.max(np.abs(defect)),max_relative_defect=np.max(np.abs(defect))/energy[0]))
    ax[0].set(xlabel='t',ylabel='$E_u(t)$',title='First-component energy')
    ax[1].axhline(0,color='0.4',lw=.8); ax[1].set(xlabel='t',ylabel='normalized balance defect',title='Energy-identity diagnostic')
    for a in ax: a.grid(alpha=.25); a.legend(frameon=False,fontsize=8)
    fig.tight_layout(); fig.savefig(OUT/'energy_diagnostic.png',dpi=220,bbox_inches='tight'); plt.close(fig)
    pd.DataFrame(rows).to_csv(OUT/'energy_diagnostic.csv',index=False)
def validation():
    conv=pd.read_csv(OUT/'convergence.csv'); abl=pd.read_csv(OUT/'ablations.csv'); summary=pd.read_csv(OUT/'summary.csv')
    fig,ax=plt.subplots(1,3,figsize=(13,3.8)); usable=conv[conv.rmse>0]
    ax[0].loglog(usable.nx,usable.rmse,'o-',color='C0'); ax[0].set(xlabel='spatial points $N_x$',ylabel='RMSE vs. finest run',title='Reference refinement')
    nf=abl.setting.str.extract(r'(\d+)')[0].astype(int); right=ax[1].twinx()
    ax[1].plot(nf,abl.rmse,'o-',color='C3',label='field RMSE'); right.plot(nf,abl.test_residual,'s--',color='C4',label='test residual')
    ax[1].set(xlabel='$N_f$',ylabel='field RMSE',title='Collocation ablation'); right.set_ylabel('independent residual')
    lines=ax[1].lines+right.lines; ax[1].legend(lines,[z.get_label() for z in lines],frameon=False,fontsize=8)
    for _,row in summary.iterrows():
        ax[2].scatter(row.runtime_seconds_mean,row.rmse_mean,s=55); ax[2].annotate(row.method,(row.runtime_seconds_mean,row.rmse_mean),xytext=(5,4),textcoords='offset points')
    ax[2].set_xscale('log'); ax[2].set_yscale('log'); ax[2].set(xlabel='solve/train time (s)',ylabel='RMSE',title='Accuracy--cost diagnostic')
    for a in ax: a.grid(alpha=.22,which='both')
    fig.tight_layout(); fig.savefig(OUT/'validation_diagnostics.png',dpi=220,bbox_inches='tight'); plt.close(fig)

if __name__=='__main__':
    data=np.load(OUT/'solutions.npz'); snapshots(data); mass_control(data); energy_diagnostic(data); validation(); print('Wrote article diagnostics')
