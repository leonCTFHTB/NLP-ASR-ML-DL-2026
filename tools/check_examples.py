"""Pruebas pequeñas de los ejemplos publicados, sin descargar datos ni entrenar."""
from pathlib import Path
import ast,json
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1];PAGES=ROOT/'docs/nlp'
checks=[]
def ok(name):checks.append(name)
def cell(prefix,n):
    p=next(PAGES.glob(prefix+'*.html'));s=BeautifulSoup(p.read_text(),'html.parser')
    return s.find(id=f'celda-{n}').select_one('details.source-code pre').get_text()
def definitions(code,ns,names=None):
    tree=ast.parse(code)
    tree.body=[x for x in tree.body if isinstance(x,(ast.ClassDef,ast.FunctionDef)) and (names is None or x.name in names)]
    exec(compile(tree,'<ejemplo publicado>','exec'),ns)
def run():
    torch.manual_seed(23);ns={'torch':torch,'nn':nn,'F':F,'np':np}
    prefix='clase-06-6-mecanismos-de-atencion-parte-2'
    for n in [81,90,143,148,150]:definitions(cell(prefix,n),ns)
    for cls,kwargs in [('BahdanauAttention',{'attention_dim':5}),('LuongAttention',{'method':'general'}),('LocalAttention',{}),('HardAttention',{})]:
        for batch in [1,2]:
            model=ns[cls](query_dim=4,key_dim=4,**kwargs).eval()
            q=torch.randn(batch,4,requires_grad=True);k=torch.randn(batch,6,4,requires_grad=True)
            mask=torch.tensor([[1,1,1,0,0,0]],dtype=torch.bool).expand(batch,-1)
            ctx,w=model(q,k,mask)
            assert ctx.shape==(batch,4) and w.shape==(batch,6)
            assert torch.isfinite(ctx).all() and torch.all(w[:,3:]==0)
            assert torch.allclose(w.sum(1),torch.ones(batch),atol=1e-6)
            ctx.square().sum().backward();assert torch.isfinite(k.grad).all()
            try:model(q,k,torch.zeros_like(mask))
            except ValueError:pass
            else:raise AssertionError(cls+' aceptó una secuencia vacía')
        ok(cls+': batch 1/2, padding, pesos, gradiente y rechazo de máscara vacía')
    model=ns['LocalAttention'](4,4).eval();ctx,w=model(torch.randn(1,4),torch.randn(1,1000,4))
    assert torch.isfinite(w).all() and torch.allclose(w.sum(1),torch.ones(1),atol=1e-6)
    ok('Atenuación gaussiana: secuencia larga sin normalización nula')
    model=ns['AttentionLSTMClassifier'](3,4,2).eval()
    x=torch.randn(1,3,3);padded=torch.cat([x,torch.zeros(1,4,3)],dim=1)
    a,_=model(x,torch.ones(1,3,dtype=torch.bool))
    b,_=model(padded,torch.tensor([[1,1,1,0,0,0,0]],dtype=torch.bool))
    assert torch.allclose(a,b,atol=1e-6)
    ok('Clasificador unidireccional: invariancia al padding derecho')
    ns2={'torch':torch,'nn':nn,'F':F,'np':np}
    for n in [67,77,88]:definitions(cell('clase-09-6-mecanismos-',n),ns2)
    for name in ['DecomposableAttention','IntraAttention']:
        m=ns2[name](4,4).eval();ctx,w=m(torch.randn(1,4),torch.randn(1,5,4),torch.tensor([[1,1,0,0,0]]))
        assert ctx.shape==(1,4) and torch.isfinite(ctx).all() and torch.all(w[:,2:]==0)
        assert torch.allclose(w.sum(1),torch.ones(1),atol=1e-6)
        ok(name+': máscara y suma de pesos')
    definitions(cell('clase-05-3-3-',52),ns,names=['bbox_iou','write_results'])
    a=torch.tensor([[0.,0.,2.,2.]])
    assert torch.allclose(ns['bbox_iou'](a,a),torch.ones(1))
    assert torch.allclose(ns['bbox_iou'](a,torch.tensor([[3.,3.,4.,4.]])),torch.zeros(1))
    prediction=torch.zeros(1,3,7);prediction[0,:,0:4]=torch.tensor([5.,5.,2.,2.]);prediction[0,:,4]=.9
    prediction[0,0,5:]=torch.tensor([.9,.1]);prediction[0,1,5:]=torch.tensor([.8,.2]);prediction[0,2,5:]=torch.tensor([.1,.9])
    snapshot=prediction.clone();out=ns['write_results'](prediction,.3,2)
    assert out.shape==(2,8) and set(out[:,-1].tolist())=={0.,1.}
    assert torch.equal(prediction,snapshot)
    assert ns['write_results'](torch.zeros(2,4,7),.3,2).shape==(0,8)
    ok('IoU continua y NMS: duplicados, clases, entrada intacta y salida vacía')
    # Gradiente exacto de la pérdida softmax frente a autograd.
    u=torch.randn(5,3);v=torch.randn(3,requires_grad=True);target=2
    loss=F.cross_entropy((u@v)[None,:],torch.tensor([target]));loss.backward()
    exact=(F.softmax(u@v.detach(),0)[:,None]*u).sum(0)-u[target]
    assert torch.allclose(v.grad,exact,atol=1e-6);ok('Signo y fórmula del gradiente Word2Vec')
    theta=.7;m=2;n=5
    rot=lambda p:np.array([[np.cos(p*theta),-np.sin(p*theta)],[np.sin(p*theta),np.cos(p*theta)]])
    q=np.array([1.,.4]);k=np.array([-.2,.8])
    assert np.allclose((rot(m)@q)@(rot(n)@k),q@rot(n-m)@k)
    assert np.allclose(np.linalg.norm(rot(m)@q),np.linalg.norm(q));ok('RoPE: norma y producto relativo')
    tc=.6;threshold=lambda k:tc**2/np.sqrt(1/k+(1-1/k)*tc**2)
    assert np.isclose(threshold(1),tc**2) and np.isclose(threshold(10**9),tc)
    ok('Links: umbral en k=1 y límite asintótico')
    x=np.random.default_rng(1).normal(size=512);assert np.allclose(np.fft.irfft(np.fft.rfft(x),n=512),x)
    ok('FFT real: reconstrucción de 512 muestras')
    errors=[];count=0
    for p in PAGES.glob('*.html'):
        s=BeautifulSoup(p.read_text(),'html.parser')
        for d in s.select('details.source-code'):
            text=d.pre.get_text();lines=text.splitlines();count+=1
            # Magias válidas de notebook no son Python de un archivo .py.
            if lines and lines[0].startswith('%%'):continue
            source='\n'.join('# '+l if l.lstrip().startswith(('!','%')) else l for l in lines)
            try:ast.parse(source)
            except SyntaxError as e:errors.append([p.name,d.find_parent('section')['id'],str(e)])
    assert not errors,errors
    ok(f'Sintaxis de {count} celdas Python publicadas (magias tratadas como notebook)')
    result={'checks':checks,'passed':len(checks),'training_executed':False,'datasets_downloaded':False}
    (ROOT/'reports/pruebas-ejemplos.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
