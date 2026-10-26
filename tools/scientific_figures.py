"""Gráficas científicas deterministas de los ejemplos numéricos."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/assets/figures'
plt.rcParams.update({'font.size':12,'svg.fonttype':'none','figure.facecolor':'#191d26','axes.facecolor':'#222733','text.color':'#e5e7eb','axes.labelcolor':'#e5e7eb','xtick.color':'#c8d0df','ytick.color':'#c8d0df','axes.edgecolor':'#75829b','savefig.facecolor':'#191d26'})
def save(fig,name):
 fig.savefig(OUT/(name+'.svg'),bbox_inches='tight');plt.close(fig)
def softmax(x):
 e=np.exp(x-np.max(x,axis=-1,keepdims=True));return e/e.sum(axis=-1,keepdims=True)
def run():
 OUT.mkdir(exist_ok=True)
 scores=np.array([1.,3.,2.,0.]);positions=np.arange(4)
 global_w=softmax(scores)
 local_w=softmax(scores-(positions-2.)**2/(2*.7**2))
 hard=np.eye(4)[np.argmax(scores)]
 weights=np.stack([global_w,local_w,hard]);assert np.allclose(weights.sum(1),1)
 fig,ax=plt.subplots(figsize=(11,3.8));im=ax.imshow(weights,vmin=0,vmax=1,cmap='viridis',aspect='auto')
 for i in range(3):
  for j in range(4):ax.text(j,i,f'{weights[i,j]:.4f}',ha='center',va='center',color='white' if weights[i,j]<.5 else '#111827',fontsize=14)
 ax.set_xticks(range(4),['Posición 0','Posición 1','Posición 2','Posición 3'])
 ax.set_yticks(range(3),['Softmax global','Gaussiana + softmax','Selección argmax'])
 ax.set_title('Ejemplo sintético: pesos de atención, sin entrenamiento',pad=18)
 fig.colorbar(im,ax=ax,label='Peso');fig.text(.12,.005,'Scores [1, 3, 2, 0] · Gaussiana: centro 2, σ=0.7 · Cada fila suma 1.',fontsize=11)
 fig.tight_layout(rect=[0,.07,1,1]);save(fig,'attention-weights')
 fig,ax=plt.subplots(figsize=(7,6));theta=.6;q=np.array([1.,.4])
 for p in range(4):
  a=p*theta;r=np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])@q
  ax.arrow(0,0,*r,width=.008,length_includes_head=True,color=plt.cm.viridis(.2+p*.22))
  ax.text(*(r*1.1),f'p={p}',ha='center')
 t=np.linspace(0,2*np.pi,300);norm=np.linalg.norm(q);ax.plot(norm*np.cos(t),norm*np.sin(t),'--',color='#75829b')
 ax.set(xlim=(-1.4,1.4),ylim=(-1.4,1.4),xlabel='Coordenada 1',ylabel='Coordenada 2',title='RoPE: rotar una pareja de contenido fijo')
 ax.set_aspect('equal');ax.grid(alpha=.15);fig.text(.04,.02,'q=(1, 0.4), θ=0.6 rad/posición · La norma se conserva; no mide significado.',fontsize=10)
 save(fig,'rope-rotation')
 fs=8000;t=np.arange(fs)/fs
 x=np.sin(2*np.pi*600*t)*(t<.5)+np.sin(2*np.pi*1000*t)*(t>=.5)
 fig,axes=plt.subplots(2,1,figsize=(11,6),sharex=True)
 for ax,w in zip(axes,[128,512]):
  h=32;nfft=512;frames=np.lib.stride_tricks.sliding_window_view(x,w)[::h]
  spec=np.abs(np.fft.rfft(frames*np.hanning(w),n=nfft,axis=1)).T**2
  db=10*np.log10(np.maximum(spec,1e-12)/spec.max())
  centers=(np.arange(frames.shape[0])*h+(w-1)/2)/fs
  im=ax.imshow(db,origin='lower',aspect='auto',extent=[centers[0],centers[-1],0,fs/2],vmin=-65,vmax=0,cmap='magma')
  ax.set(ylim=(0,1600),ylabel='Frecuencia (Hz)',title=f'Ventana Hann: {1000*w/fs:.0f} ms · salto 4 ms · FFT 512 puntos')
 axes[1].set_xlabel('Tiempo (s)');fig.suptitle('Señal sintética: cambio de 600 a 1000 Hz en t=0.5 s')
 fig.colorbar(im,ax=axes,label='Potencia relativa (dB)',fraction=.025,pad=.03)
 fig.subplots_adjust(top=.86,hspace=.45,bottom=.12,right=.86)
 save(fig,'time-frequency')
 fig,ax=plt.subplots(figsize=(11,4));f=np.linspace(0,8000,513)
 mel=lambda f:2595*np.log10(1+f/700)
 edges=700*(10**(np.linspace(mel(0),mel(8000),14)/2595)-1)
 for a,b,c in zip(edges[:-2],edges[1:-1],edges[2:]):
  filt=np.maximum(0,np.minimum((f-a)/(b-a),(c-f)/(c-b)));ax.plot(f,filt)
 ax.set(xlabel='Frecuencia (Hz)',ylabel='Peso (pico uno)',title='Banco Mel ilustrativo: 12 filtros, convención HTK')
 ax.grid(alpha=.15);fig.text(.08,.005,'Cada filtro suma potencia ponderada. El logaritmo se aplica después, con suelo positivo.',fontsize=11)
 fig.tight_layout(rect=[0,.06,1,1]);save(fig,'mel-bank')
if __name__=='__main__':run()
