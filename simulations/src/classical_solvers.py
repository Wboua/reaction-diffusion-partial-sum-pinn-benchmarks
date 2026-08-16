import numpy as np
from scipy.sparse import diags,csc_matrix
from scipy.sparse.linalg import splu
from model import initial_data,reaction

def _sample(cfg,x,advance,dt):
    ts=np.linspace(0,cfg.T,cfg.eval_nt); u,v=initial_data(x)
    U=np.empty((len(ts),len(x))); V=np.empty_like(U); U[0]=u; V[0]=v
    n=int(np.ceil(cfg.T/dt)); dt=cfg.T/n; k=1; told=0.; uold=u.copy(); vold=v.copy()
    for j in range(1,n+1):
        un,vn=advance(u,v,dt); now=j*dt
        while k<len(ts) and ts[k]<=now+1e-14:
            w=(ts[k]-told)/dt; U[k]=(1-w)*uold+w*un; V[k]=(1-w)*vold+w*vn; k+=1
        told=now; uold=un.copy(); vold=vn.copy(); u,v=un,vn
    return ts,x,U,V

def fdm(cfg,nx=None,dt=None):
    nx=nx or cfg.fdm_nx; dt=dt or cfg.fdm_dt; x=np.linspace(0,1,nx); h=x[1]-x[0]; ni=nx-2
    L=diags([np.ones(ni-1),-2*np.ones(ni),np.ones(ni-1)],[-1,0,1])/h**2
    # dt is normalized below; build factors with the normalized step.
    steps=int(np.ceil(cfg.T/dt)); dtn=cfg.T/steps
    su=splu(csc_matrix(diags(np.ones(ni))-dtn*cfg.d1*L)); sv=splu(csc_matrix(diags(np.ones(ni))-dtn*cfg.d2*L))
    def advance(u,v,d):
        ux=np.gradient(u,h,edge_order=2); vx=np.gradient(v,h,edge_order=2); f1,f2=reaction(u,v,ux,vx)
        un=np.zeros_like(u); vn=np.zeros_like(v); un[1:-1]=su.solve(u[1:-1]+d*f1[1:-1]); vn[1:-1]=sv.solve(v[1:-1]+d*f2[1:-1]); return un,vn
    return _sample(cfg,x,advance,dt)

def fem(cfg):
    """P1 Galerkin FEM; nonlinear loads assembled by 2-point Gauss quadrature."""
    x=np.linspace(0,1,cfg.fem_ne+1); h=x[1]-x[0]; n=cfg.fem_ne-1
    M=diags([h/6*np.ones(n-1),2*h/3*np.ones(n),h/6*np.ones(n-1)],[-1,0,1])
    K=diags([-np.ones(n-1)/h,2*np.ones(n)/h,-np.ones(n-1)/h],[-1,0,1])
    steps=int(np.ceil(cfg.T/cfg.fem_dt)); dt=cfg.T/steps
    su=splu(csc_matrix(M+dt*cfg.d1*K)); sv=splu(csc_matrix(M+dt*cfg.d2*K))
    gp=(-1/np.sqrt(3),1/np.sqrt(3))
    def loads(u,v):
        b1=np.zeros_like(u); b2=np.zeros_like(v)
        for e in range(cfg.fem_ne):
            ux=(u[e+1]-u[e])/h; vx=(v[e+1]-v[e])/h
            for xi in gp:
                phi=np.array([(1-xi)/2,(1+xi)/2]); uq=phi@u[e:e+2]; vq=phi@v[e:e+2]
                f1,f2=reaction(uq,vq,ux,vx); b1[e:e+2]+=h/2*f1*phi; b2[e:e+2]+=h/2*f2*phi
        return b1[1:-1],b2[1:-1]
    def advance(u,v,d):
        f1,f2=loads(u,v); un=np.zeros_like(u); vn=np.zeros_like(v)
        un[1:-1]=su.solve(M@u[1:-1]+d*f1); vn[1:-1]=sv.solve(M@v[1:-1]+d*f2); return un,vn
    return _sample(cfg,x,advance,cfg.fem_dt)
