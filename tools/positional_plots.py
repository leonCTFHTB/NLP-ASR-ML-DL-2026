"""Recalcula únicamente gráficos deterministas de PE, sin entrenar modelos."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parents[1]/'docs/assets/figures'
root.mkdir(parents=True,exist_ok=True)
tokens='el perro corre en el parque verde'.split();d=32
pos=np.arange(len(tokens));freq=10000.0**(-np.arange(0,d,2)/d)
pe=np.zeros((len(tokens),d));pe[:,0::2]=np.sin(pos[:,None]*freq);pe[:,1::2]=np.cos(pos[:,None]*freq)
assert pe.shape==(7,32) and np.allclose(pe[:,0::2]**2+pe[:,1::2]**2,1)
plt.rcParams.update({'figure.facecolor':'#111c30','axes.facecolor':'#17243b','text.color':'#e6e9f1','axes.labelcolor':'#c6d2e3','xtick.color':'#b8c7db','ytick.color':'#b8c7db','axes.edgecolor':'#65718a','font.size':10,'savefig.facecolor':'#111c30'})
fig,axes=plt.subplots(3,2,figsize=(14,9),layout='constrained')
cont=np.linspace(0,6,500)
for i in range(3):
 for j,fn in enumerate([np.sin,np.cos]):
  ax=axes[i,j];dim=2*i+j
  ax.plot(cont,fn(cont*freq[i]),color='#b4a1f2' if j==0 else '#d9c58f');ax.scatter(pos,pe[:,dim],color='#91b9e3',zorder=3)
  ax.set_title(f'Dimensión {dim} · {"seno" if j==0 else "coseno"} · divisor {1/freq[i]:.4f} · período {2*np.pi/freq[i]:.2f}')
  ax.set_ylim(-1.2,1.2);ax.set_xticks(pos, [f'{p}\n{t}' for p,t in enumerate(tokens)]);ax.grid(alpha=.2)
fig.suptitle('PE con d = 32 · Las seis primeras columnas (tres parejas de frecuencia)',fontsize=16)
fig.savefig(root/'pe-37.png',dpi=145);plt.close(fig)
fig,axes=plt.subplots(2,1,figsize=(14,7),layout='constrained')
for j,ax in enumerate(axes):
 im=ax.imshow(pe[:,j::2],vmin=-1,vmax=1,cmap='coolwarm',aspect='auto');ax.set_yticks(pos,[f'{p}: {t}' for p,t in enumerate(tokens)]);ax.set_xticks(np.arange(16),[str(x) for x in range(j,d,2)]);ax.set_xlabel('Índice de dimensión');ax.set_title('Seno: dimensiones pares' if j==0 else 'Coseno: dimensiones impares');fig.colorbar(im,ax=ax)
fig.suptitle('Matriz PE completa · 7 posiciones × 32 dimensiones',fontsize=16)
fig.savefig(root/'pe-39.png',dpi=145);plt.close(fig)
fig,axes=plt.subplots(7,1,figsize=(14,15),sharex=True,layout='constrained')
for p,ax in enumerate(axes):
 ax.vlines(np.arange(d),0,pe[p],color='#91b9e3');ax.scatter(np.arange(d),pe[p],c=['#b4a1f2' if k%2==0 else '#d9c58f' for k in range(d)],s=20);ax.set_ylim(-1.2,1.2);ax.set_title(f'Posición {p} · {tokens[p]}',loc='left');ax.grid(alpha=.15)
axes[-1].set_xticks(np.arange(d));axes[-1].set_xlabel('Dimensión 0–31 · pares: seno · impares: coseno')
fig.suptitle('Cada token recibe una fila completa de 32 valores PE',fontsize=16)
fig.savefig(root/'pe-41.png',dpi=145);plt.close(fig)
print('PE verificado: 7×32, 3 gráficos deterministas.')
