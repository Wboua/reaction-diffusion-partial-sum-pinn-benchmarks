import os,time
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL','2')
import numpy as np
import tensorflow as tf
from model import initial_data

class Network(tf.keras.Model):
    def __init__(self,cfg):
        super().__init__(); self.cfg=cfg; self.hidden=[tf.keras.layers.Dense(cfg.width,activation='tanh',kernel_initializer='glorot_normal') for _ in range(cfg.layers)]; self.out=tf.keras.layers.Dense(2)
    def call(self,tx):
        z=tf.concat([2*tx[:,:1]/self.cfg.T-1,2*tx[:,1:]-1],1)
        for layer in self.hidden: z=layer(z)
        x=tx[:,1:]; return x*(1-x)*tf.nn.softplus(self.out(z))

def residual(model,tx,cfg):
    t=tx[:,:1]; x=tx[:,1:]
    with tf.GradientTape(persistent=True) as g2:
        g2.watch([t,x])
        with tf.GradientTape(persistent=True) as g1:
            g1.watch([t,x]); y=model(tf.concat([t,x],1)); u=y[:,:1]; v=y[:,1:]
        ut=g1.gradient(u,t); vt=g1.gradient(v,t); ux=g1.gradient(u,x); vx=g1.gradient(v,x)
    uxx=g2.gradient(ux,x); vxx=g2.gradient(vx,x); del g1,g2
    r1=ut-cfg.d1*uxx+u*ux**2
    r2=vt-cfg.d2*vxx-u*ux**2+v*vx**2
    return r1,r2

def train(cfg,seed):
    tf.keras.backend.clear_session(); tf.keras.utils.set_random_seed(seed); rng=np.random.default_rng(seed)
    tx=tf.constant(np.c_[rng.random(cfg.nf)*cfg.T,rng.random(cfg.nf)].astype('float32'))
    x0=np.linspace(0,1,cfg.nic,dtype='float32')[:,None]; tx0=tf.constant(np.c_[np.zeros_like(x0),x0]); u0,v0=initial_data(x0); y0=tf.constant(np.c_[u0[:,0],v0[:,0]].astype('float32'))
    net=Network(cfg); net(tf.zeros((1,2))); opt=tf.keras.optimizers.Adam(cfg.lr)
    @tf.function
    def step():
        with tf.GradientTape() as tape:
            r1,r2=residual(net,tx,cfg); lp=tf.reduce_mean(r1**2+r2**2); li=tf.reduce_mean((net(tx0)-y0)**2); total=lp+20*li
        grad=tape.gradient(total,net.trainable_variables); opt.apply_gradients(zip(grad,net.trainable_variables)); return total,lp,li
    hist=[]; start=time.perf_counter()
    for epoch in range(1,cfg.epochs+1):
        vals=step()
        if epoch==1 or epoch%50==0 or epoch==cfg.epochs: hist.append((epoch,*[float(z) for z in vals]))
    return net,hist,time.perf_counter()-start
