"""Valida enlaces internos, recursos y limpieza del sitio sin ejecutar Python docente."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
import json,re,sys
root=Path(__file__).resolve().parents[1];docs=root/'docs'
errors=[];external=[];formulas=0;images=0;ids={}
files=list(docs.rglob('*.html'))
soups={p:BeautifulSoup(p.read_text(),'html.parser') for p in files}
for p,s in soups.items():ids[p]={x.get('id') for x in s.find_all(attrs={'id':True})}
for p,s in soups.items():
    text=p.read_text()
    if 'UPATECO' in text.upper():errors.append([str(p),'institutional name'])
    if s.select('.math-fallback'):errors.append([str(p),'math fallback'])
    formulas+=len(s.find_all('math'));images+=len(s.find_all('img'))
    if not s.h1:errors.append([str(p),'missing h1'])
    for v in s.select('video[data-video-parts]'):
        for part in v['data-video-parts'].split('|'):
            if not (p.parent/part).resolve().exists():errors.append([str(p),part,'missing video part'])
    for tag,attr in [('a','href'),('img','src'),('script','src'),('link','href'),('source','src'),('audio','src'),('video','src')]:
      for el in s.find_all(tag):
        value=el.get(attr,'')
        if not value:continue
        u=urlsplit(value)
        if u.scheme in ['http','https']:
            if tag in ['img','source','audio','video']:external.append([str(p.relative_to(docs)),value])
            continue
        if u.scheme or value.startswith('//'):continue
        if u.path.startswith('/NLP-ASR-ML-DL-2026/'):
            target=(docs/unquote(u.path).removeprefix('/NLP-ASR-ML-DL-2026/')).resolve()
        else:
            target=(p.parent/unquote(u.path)).resolve() if u.path else p.resolve()
        if not target.exists():errors.append([str(p.relative_to(docs)),value,'missing file']);continue
        if u.fragment and target in ids and unquote(u.fragment) not in ids[target]:errors.append([str(p.relative_to(docs)),value,'missing anchor'])
result={'html_pages':len(files),'notebook_pages':len(list((docs/'nlp').glob('*.html'))),'formula_instances':formulas,'image_instances':images,'errors':errors,'external_media':external,'python_training_executed':False}
(root/'reports/validacion.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
print(json.dumps(result,indent=2,ensure_ascii=False));sys.exit(bool(errors))
