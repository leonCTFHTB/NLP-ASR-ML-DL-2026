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
catalog={x['filename']:x for x in json.loads((root/'reports/catalogo.json').read_text())}
numbering_errors=[]
for p,s in soups.items():
    redirect=s.find('meta',attrs={'name':'class-redirect'})
    if redirect:
        target=redirect.get('content','')
        if target not in catalog or p.parent.name!='nlp':numbering_errors.append([p.name,'invalid class redirect'])
        continue
    if s.select('nav .chapter.pending'):
        numbering_errors.append([str(p.relative_to(docs)),'unpublished navigation entry'])
    nav=s.select_one('nav[aria-label="Clases"]')
    if nav:
        names={Path(urlsplit(a['href']).path).name for a in nav.select('a[href]')}
        if names!=set(catalog):numbering_errors.append([str(p.relative_to(docs)),'navigation/catalog mismatch'])
        for a in nav.select('a[href]'):
            name=Path(urlsplit(a['href']).path).name
            if name not in catalog:continue
            item=catalog[name];label=item.get('class_label',f"{int(item['class']):02d}")
            chapter=a.find_parent('details',class_='chapter')
            if not a.get_text(' ',strip=True).startswith(item['title']):numbering_errors.append([str(p.relative_to(docs)),name,'sidebar title mismatch'])
            if chapter and not chapter.summary.get_text(' ',strip=True).startswith(label+' · '):numbering_errors.append([str(p.relative_to(docs)),name,'sidebar number mismatch'])
    if p.parent.name=='nlp':
        item=catalog.get(p.name);match=re.match(r'clase-(\d+)-',p.name)
        if not item or not match or int(match[1])!=int(item['class']):
            numbering_errors.append([p.name,'filename/catalog number mismatch']);continue
        label=item.get('class_label',f"{int(item['class']):02d}")
        if not item['title'].startswith(label+' · ') or s.h1.get_text(' ',strip=True)!=item['title'] or not s.title.get_text().startswith(item['title']+' · '):numbering_errors.append([p.name,'HTML title/catalog mismatch'])
home=soups[docs/'index.html']
if any(not row.find('a') for row in home.select('#indice .catalog-row')):numbering_errors.append(['index.html','unpublished index entry'])
if {Path(urlsplit(a['href']).path).name for a in home.select('#indice a[href]')}!=set(catalog):numbering_errors.append(['index.html','index/catalog mismatch'])
errors.extend(numbering_errors)
result={'html_pages':len(files),'notebook_pages':len(catalog),'class_redirects':sum(bool(s.find('meta',attrs={'name':'class-redirect'})) for s in soups.values()),'formula_instances':formulas,'image_instances':images,'class_numbering_verified':not numbering_errors,'errors':errors,'external_media':external,'python_training_executed':False}
(root/'reports/validacion.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
print(json.dumps(result,indent=2,ensure_ascii=False));sys.exit(bool(errors))
