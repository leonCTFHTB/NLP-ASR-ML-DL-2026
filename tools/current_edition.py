"""Publica únicamente el material vigente y reconstruye sus índices y referencias."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,re
from review_content import SOURCES
from editorial import render
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
GROUPS={
 'embeddings':['word2vec','w2v-math','glove','adagrad','fasttext','ft-code','ft-class','embbag','adamw','ce'],
 'cnn':['conv','conv2d','padding','pool','bn','vgg','ce'],
 'attention':['attention','bahdanau','luong','hard','gumbel','lstm','parikh','cheng','ntm'],
 'positions':['attention','rope','animation'],
 'vision':['ssd','rcnn','fastrcnn','faster','maskrcnn','yolo2','yolo3','focal','augment','nms'],
 'audio':['fft','stft','nola','mel','mfcc','cqt','preemphasis','whisper','uncertainty'],
 'speakers':['ge2e','ge2e-updates','diarization','links'],
}
SOURCES['rcnn']=('Girshick et al. · R-CNN','https://arxiv.org/abs/1311.2524')
SOURCES['fastrcnn']=('Girshick · Fast R-CNN','https://arxiv.org/abs/1504.08083')
SOURCES['ge2e-updates']=('GE2E · Publicación y actualizaciones de los autores','https://google.github.io/speaker-id/publications/GE2E/')
URLS={
 'https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.Animation.to_jshtml.html':'https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.Animation.html#matplotlib.animation.Animation.to_jshtml',
 'https://librosa.org/doc/latest/generated/librosa.filters.mel.html':'https://librosa.org/doc/0.10.2/generated/librosa.filters.mel.html',
 'https://librosa.org/doc/latest/generated/librosa.feature.mfcc.html':'https://librosa.org/doc/0.10.2/generated/librosa.feature.mfcc.html',
 'https://librosa.org/doc/main/api/generated/librosa.feature.mfcc.html':'https://librosa.org/doc/0.10.2/generated/librosa.feature.mfcc.html',
 'https://librosa.org/doc/main/generated/librosa.effects.preemphasis.html':'https://librosa.org/doc/0.10.2/generated/librosa.effects.preemphasis.html',
}
def refs_for(p):
 n=p.name
 if n.startswith(('clase-02','clase-03','clase-04')):return GROUPS['embeddings']
 if n.startswith('clase-05-1'):return GROUPS['cnn']
 if n.startswith('clase-05-3'):return GROUPS['vision']
 if n.startswith(('clase-12','clase-13')):return GROUPS['positions']
 if n.startswith('clase-14-1-2'):return GROUPS['speakers']
 if n.startswith(('clase-14','clase-15','clase-16')):return GROUPS['audio']
 return GROUPS['attention']
def source_list(keys):
 return '\n'.join(f'- [{SOURCES[k][0]}]({URLS.get(SOURCES[k][1],SOURCES[k][1])})' for k in keys)
def run():
 coverage=[]
 for p in sorted(DOCS.rglob('*.html')):
  s=BeautifulSoup(p.read_text(),'html.parser')
  for n in list(s.select('.figure-revision')):n.decompose()
  for n in s.find_all(True):
   for attr in ['data-original-src','data-editorial-edits']:
    if n.name=='video' and attr=='data-original-src':continue
    n.attrs.pop(attr,None)
  for n in s.select('.editorial-source'):
   for t in list(n.find_all(string=True)):
    if 'Fuente de la revisión:' in t:t.replace_with(str(t).replace('Fuente de la revisión:','Referencia:'))
   n['class']=['note','source-reference']
  for a in s.find_all('a',href=True):
   a['href']=URLS.get(a['href'],a['href'])
   if a['href'].endswith('revision.html'):a.string='Bibliografía y criterios del material'
  for t in list(s.find_all(string=True)):
   if t.find_parent(['script','style','pre','code','math']):continue
   val=str(t).replace('En la RNN de la versión anterior,','En el ejemplo de RNN,')
   if val!=str(t):t.replace_with(val)
  if p.parent.name=='nlp':
   keys=refs_for(p);body=source_list(keys)
   found=False
   for c in s.select('section.cell'):
    title=c.get_text(' ',strip=True)
    if not title.lower().startswith(('bibliografía','bibliografia','referencias bibliográficas')):continue
    if c.find('pre') and not c.find(re.compile('^h[1-6]$')):continue
    old_h=c.find(re.compile('^h[1-6]$'))
    if old_h:old_h.extract()
    c.clear()
    if old_h:c.append(old_h)
    else:
     h=s.new_tag('h2');h.string='Bibliografía';c.append(h)
    fragment=BeautifulSoup(render(body),'html.parser')
    for n in list(fragment.contents):c.append(n)
    found=True
   block=s.find(id='bibliografia-del-tema')
   if not found and block is None:
    block=s.new_tag('section',id='bibliografia-del-tema',attrs={'class':'cell'})
    block.append(BeautifulSoup(render('## Bibliografía del tema\n\n'+body),'html.parser'))
    anchor=s.select_one('.pager') or s.select_one('footer')
    if anchor:anchor.insert_before(block)
    else:s.main.append(block)
   # Las figuras vectoriales propias tienen atribución al material actual.
   for im in s.select('img[src*="/figures/"]'):
    container=im.find_parent('section')
    for text in list(container.find_all(string=True)):
     if text.find_parent(['pre','code','script','math']):continue
     val=str(text)
     if re.search(r'Fig(?:ura|\.)?\s+tomada de',val,re.I):
      text.replace_with('Figura de elaboración didáctica. Referencias en la bibliografía del tema.')
   coverage.append({'page':str(p.relative_to(DOCS)),'title':s.h1.get_text(' ',strip=True),'references':[URLS.get(SOURCES[k][1],SOURCES[k][1]) for k in keys],'text_cells':len(s.select('section.cell')),'images':len(s.find_all('img'))})
  p.write_text(str(s))
 allkeys=list(dict.fromkeys(k for ks in GROUPS.values() for k in ks))
 bibliography='''# Bibliografía y criterios del material

El libro reúne 29 páginas de clases sobre embeddings, redes convolucionales, atención, Transformers, posiciones, audio y diarización. Las explicaciones distinguen definiciones matemáticas, elecciones de implementación y ejemplos ilustrativos.

## Fuentes

Las referencias principales son artículos de sus autores, documentación oficial y el texto de Dive into Deep Learning. Cada tema incluye su bibliografía y las explicaciones revisadas enlazan su fuente.

'''+source_list(allkeys)+'''

## Convenciones y ejemplos

Las fórmulas declaran ejes, dimensiones, índices y supuestos cuando afectan el resultado. Las analogías acompañan al cálculo y no sustituyen una definición. Las gráficas sintéticas indican sus parámetros; no se presentan como resultados de un entrenamiento. Las cifras publicadas se interpretan dentro del experimento que las produjo.

Los ejemplos de atención incluyen máscaras y el tratamiento explícito de secuencias sin claves válidas. La variante gaussiana didáctica calcula scores globales y no representa una implementación dispersa. La autoatención bilineal del laboratorio es una adaptación y no una reproducción de la recurrencia LSTMN.

## Comprobaciones

Se comprueban enlaces y recursos internos, fórmulas MathML y sintaxis del código. Las pruebas pequeñas ejecutan atención, padding, IoU y NMS, y verifican identidades de Word2Vec, RoPE, Links y FFT. No se han repetido los entrenamientos completos, las descargas de datasets ni los benchmarks de GPU; estas comprobaciones no certifican el rendimiento de los modelos.

Las animaciones se inspeccionan mediante fotogramas representativos. Los códigos, recursos y referencias vigentes forman parte del repositorio. Las modificaciones se documentan en sus commits.

## Autoría y licencias

Las aportaciones propias y los materiales de terceros conservan sus condiciones de uso y atribución. Las adaptaciones de D2L mantienen su licencia específica. Consultá [cómo citar y las licencias](citar.html).
'''
 (ROOT/'reports/REVISION.md').write_text(bibliography)
 (ROOT/'reports/cobertura.json').write_text(json.dumps({'pages':coverage,'notebook_pages':len(coverage)},ensure_ascii=False,indent=2))
 print('Páginas con bibliografía:',len(coverage))
if __name__=='__main__':run()
