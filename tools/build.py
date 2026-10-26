"""Convierte los ZIP docentes en HTML estático sin ejecutar celdas.

Uso: python tools/build.py --inputs ../extracted --external ../external
Requiere los ZIP originales extraídos, preserva sus salidas y registra cambios.
"""
from pathlib import Path
import argparse, base64, copy, hashlib, html, io, json, mimetypes, re, unicodedata
from bs4 import BeautifulSoup
from PIL import Image
from markdown_it import MarkdownIt
from latex2mathml.converter import convert
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from corrections import correct, PE, ROPE
from figures import FIGURES, MAP, write as write_figures

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs';ASSETS=DOCS/'assets';PAGES=DOCS/'nlp'
for p in [ASSETS,PAGES,ROOT/'reports']:p.mkdir(parents=True,exist_ok=True)
args=argparse.ArgumentParser();args.add_argument('--inputs',required=True);args.add_argument('--external',required=True)
args=args.parse_args();INPUT=Path(args.inputs);EXTERNAL=Path(args.external)
md=MarkdownIt('commonmark',{'html':True,'breaks':False}).enable('table')
stats={'notebooks':0,'text_corrections':0,'figure_replacements':0,'setup_cells_removed':0,'math':0,'math_errors':[],'missing':[],'external':[]}
changes=[];asset_cache={}
LI='https://www.linkedin.com/in/lic-jacobo-leon-juarez/'
GH='https://github.com/leonCTFHTB/NLP-ASR-ML-DL-2026'
NOTION='https://app.notion.com/p/leon-ctf/Portafolio-4034120b17c880048026ec0abf21f685'
AUTHOR='Jacobo León Juárez'
CATALOG={1:'Introducción al NLP · Bases',2:'Word2Vec',3:'GloVe',4:'fastText',5:'Redes convolucionales',6:'Mecanismos de atención · Parte 1',7:'Mecanismos de atención · Parte 2',8:'Mecanismos de atención · Parte 3',9:'Mecanismos de atención · Parte 4',10:'Introducción a Transformers · Parte 1',11:'Introducción a Transformers · Parte 2',12:'GPT y codificación posicional · Parte 1',13:'GPT y RoPE · Parte 2',14:'Introducción a ASR · Parte 1',15:'Introducción a ASR · Parte 2',16:'FFT Radix-2'}

def join(value):return ''.join(value) if isinstance(value,list) else str(value)
def slug(s):return re.sub('[^a-z0-9]+','-',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip('-')
def asset(data,kind='png'):
    digest=hashlib.sha256(data).hexdigest()
    if digest in asset_cache:return asset_cache[digest]
    if kind not in ('svg','gif','wav','mp3','ogg','webm','mp4'):
        try:
            im=Image.open(io.BytesIO(data))
            if not getattr(im,'is_animated',False):
                out=io.BytesIO();im.save(out,format='WEBP',lossless=True,method=4);data=out.getvalue();kind='webp'
        except Exception:pass
    name=hashlib.sha256(data).hexdigest()[:24]+'.'+kind
    (ASSETS/name).write_bytes(data);asset_cache[digest]='../assets/'+name
    return asset_cache[digest]

external_map={u:p for u,p,e in json.loads((EXTERNAL/'map.json').read_text())} if (EXTERNAL/'map.json').exists() else {}
def remote(url):
    if external_map.get(url):
        data=Path(external_map[url]).read_bytes()
        kind='svg' if b'<svg' in data[:1000] else ('gif' if data.startswith(b'GIF') else 'png')
        return asset(data,kind)
    stats['external'].append(url)
    return url

def local_image(folder,name):
    if (str(folder),name) in MAP:
        stats['figure_replacements']+=1
        key=MAP[(str(folder),name)]
        return '../assets/figures/'+key+'.svg'
    matches=list(INPUT.glob(f'*-images-NLP/clase-{folder}/{name}'))
    # Algunas clases reutilizan imágenes sin copiarlas al ZIP siguiente.
    if not matches and str(folder)=='12' and name.startswith('a'):
        matches=list(INPUT.glob(f'*-images-NLP/clase-11/{name}'))
    if not matches and str(folder)=='15' and name.startswith('a'):
        matches=list(INPUT.glob(f'*-images-NLP/clase-14/{name}'))
    if not matches and str(folder)=='16':
        matches=list(INPUT.glob(f'*-images-NLP/clase-15/{name}'))
        if not matches and name=='a0.png':matches=list(INPUT.glob('*-images-NLP/clase-14/a0.png'))
    if matches:return asset(matches[0].read_bytes(),matches[0].suffix.lstrip('.'))
    return None

def math_html(src,display=False):
    raw=src.strip().replace('\u200b','').replace('⊤',r'\top').replace('−','-')
    raw=re.sub(r'\\label\{[^}]*\}|\\tag\{[^}]*\}','',raw)
    raw=re.sub(r'\\begin\{(align\*?|equation\*?|gather\*?)\}',r'\\begin{aligned}',raw)
    raw=re.sub(r'\\end\{(align\*?|equation\*?|gather\*?)\}',r'\\end{aligned}',raw)
    # Evita interpretar un corchete matemático inicial como argumento opcional.
    raw=raw.replace(r'\begin{aligned}',r'\begin{aligned}{} ')
    raw=raw.replace(r'\mathbf{N}',r'\mathbf{N}')
    try:
        result=convert(raw,display='block' if display else 'inline')
        result=result.replace('<math ',f'<math aria-label="{html.escape(src,quote=True)}" ')
        stats['math']+=1;return result
    except Exception as e:
        stats['math_errors'].append({'formula':src,'error':str(e)})
        return '<code class="math-fallback">'+html.escape(src)+'</code>'

def markdown(text):
    protected={}
    def save(value):
        key='ZXQPROTECTED'+str(len(protected))+'QXZ';protected[key]=value;return key
    text=re.sub(r'```[\s\S]*?```',lambda m:save(m[0]),text)
    text=re.sub(r'\$\$([\s\S]*?)\$\$',lambda m:save(math_html(m[1],True)),text)
    text=re.sub(r'\\\[([\s\S]*?)\\\]',lambda m:save(math_html(m[1],True)),text)
    text=re.sub(r'\\begin\{(align\*?|equation\*?|gather\*?)\}[\s\S]*?\\end\{\1\}',lambda m:save(math_html(m[0],True)),text)
    text=re.sub(r'(?<!\\)\$([^$\n]+?)(?<!\\)\$',lambda m:save(math_html(m[1])),text)
    # Restaurar bloques de código antes del renderizado; MathML después.
    for k,v in protected.items():
        if v.startswith('```'):text=text.replace(k,v)
    rendered=md.render(text)
    for k,v in protected.items():
        if not v.startswith('```'):rendered=rendered.replace(k,v)
    return rendered

def sanitize(fragment):
    soup=BeautifulSoup(fragment,'html.parser')
    for wrapper in soup.find_all(['html','head','body']):wrapper.unwrap()
    for im in soup.find_all(['img','source','audio','video']):
        src=im.get('src','')
        if src.startswith('data:'):
            m=re.match(r'data:([^;,]+)(;base64)?,(.*)',src,re.S)
            if m:
                try:
                    data=base64.b64decode(m[3]) if m[2] else __import__('urllib.parse',fromlist=['unquote_to_bytes']).unquote_to_bytes(m[3])
                    ext=mimetypes.guess_extension(m[1]) or '.bin';ext={'svg+xml':'.svg'}.get(m[1].split('/')[-1],ext)
                    im['src']=asset(data,ext.lstrip('.'))
                except Exception: pass
        elif src.startswith('http') and im.name=='img':im['src']=remote(src)
        if im.name=='img':
            im['loading']='lazy';im['decoding']='async'
            if not im.get('alt'):im['alt']='Figura conservada del notebook original'
            if im.get('src') and im['src'].startswith('http'):im['data-external']='true'
    for script in soup.find_all('script'):
        # Las salidas que dependen de un kernel se conservan como texto/imagen.
        # Plotly autónomo se permite; scripts de configuración de Colab se omiten.
        if 'google.colab' in script.text:script.decompose()
    return str(soup)

def output_html(outputs):
    out=[]
    for o in outputs:
        d=o.get('data',{})
        if 'image/svg+xml' in d:
            src=asset(join(d['image/svg+xml']).encode(),'svg');out.append(f'<img src="{src}" alt="Gráfico guardado del notebook" loading="lazy">')
        elif 'image/png' in d or 'image/jpeg' in d:
            typ='image/png' if 'image/png' in d else 'image/jpeg';src=asset(base64.b64decode(join(d[typ])),typ.split('/')[1]);out.append(f'<img src="{src}" alt="Gráfico guardado del notebook" loading="lazy">')
        elif 'text/html' in d:out.append(sanitize(join(d['text/html'])))
        elif 'text/latex' in d:out.append(markdown(join(d['text/latex'])))
        elif 'text/plain' in d:
            t=join(d['text/plain'])
            if not re.match(r'^<(?:IPython|PIL|Figure|matplotlib)',t):out.append('<pre>'+html.escape(t)+'</pre>')
        elif o.get('output_type')=='stream':
            t=join(o.get('text',''))
            if not re.search('Mounted at|drive.mount|UPATECO',t,re.I):out.append('<pre>'+html.escape(t)+'</pre>')
        elif o.get('output_type')=='error':out.append('<details class="saved-error"><summary>Error registrado en la ejecución original</summary><pre>'+html.escape(o.get('ename','')+': '+o.get('evalue',''))+'</pre></details>')
    return '<div class="output">'+''.join(out)+'</div>' if out else ''

files=[]
for path in INPUT.rglob('*.ipynb'):
    if '-images-' in str(path):continue
    m=re.search(r'Clase (\d+)',str(path))
    if not m or int(m[1])>16:continue
    files.append({'path':path,'class':int(m[1]),'title':path.stem,'slug':slug(path.stem),'annex':('Recursos' in str(path) or 'Anexos' in str(path))})
files.sort(key=lambda f:(f['class'],f['annex'],f['title']))
used={}
for f in files:
    name=f"clase-{f['class']:02d}-{f['slug']}"
    used[name]=used.get(name,0)+1
    if used[name]>1:name+='-recurso-'+str(used[name])
    f['filename']=name+'.html'

def sidebar(active='',prefix=''):
    links=[]
    for num,title in CATALOG.items():
        group=[f for f in files if f['class']==num]
        if not group:links.append('<div class="chapter pending">01 · Introducción al NLP <small>Material pendiente</small></div>');continue
        rows=''.join(f'<a class="{"active" if f["filename"]==active else ""}" href="{prefix}{f["filename"]}">{html.escape(f["title"])}{ " <small>Complemento</small>" if f["annex"] else ""}</a>' for f in group)
        links.append(f'<details class="chapter" {"open" if any(f["filename"]==active for f in group) else ""}><summary>{num:02d} · {html.escape(title)}</summary>{rows}</details>')
    return '<nav aria-label="Clases">'+''.join(links)+'</nav>'

def layout(title,body,active='',root=False):
    prefix='' if root else '../';nlp='nlp/' if root else ''
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Portafolio docente de {AUTHOR}. Notebooks de NLP y reconocimiento del habla, con teoría, código y visualizaciones."><title>{html.escape(title)} · {AUTHOR}</title><link rel="stylesheet" href="{prefix}assets/site.css"><link rel="icon" type="image/svg+xml" href="{prefix}assets/favicon.svg"></head><body><a class="skip" href="#contenido">Saltar al contenido</a><div class="progress"></div><button id="menu" aria-expanded="false" aria-controls="library-nav">☰ Índice</button><aside id="library-nav"><a class="brand" href="{prefix}index.html">PORTAFOLIO DOCENTE</a><h2>Lenguaje natural<br><span>y reconocimiento<br>del habla</span></h2><p class="note">{AUTHOR} · 2026</p><a href="{prefix}index.html#buscar" class="search-link">⌕ Buscar en el libro</a>{sidebar(active,nlp)}<div class="aside-links"><a href="{GH}">GitHub ↗</a><a href="{LI}">LinkedIn ↗</a><a href="{NOTION}">Notion ↗</a></div></aside><main id="contenido">{body}<footer><p>© 2026 {AUTHOR}. Material docente propio: <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. Código propio: Apache 2.0. Los materiales de terceros conservan sus autores y condiciones.</p><p><a href="{prefix}citar.html">Cómo citar · BibTeX</a> · <a href="{GH}/archive/refs/heads/main.zip">Descargar repositorio</a></p></footer></main><script src="{prefix}assets/site.js"></script></body></html>'''

write_figures(ASSETS/'figures')
search=[]
for f in files:
    n=json.loads(f['path'].read_text());parts=[];folder='';plain=[]
    for c in n['cells']:
        s=join(c.get('source',''));m=re.search(r'clase-(\d+)',s)
        if 'root_class_path' in s and m:folder=m[1]
    for i,c in enumerate(n['cells']):
        src=join(c.get('source',''));typ=c['cell_type']
        if typ=='code' and re.search(r'drive\.mount|root_(?:class_)?path\s*=|^%?from google\.colab',src,re.M):
            stats['setup_cells_removed']+=1;continue
        if typ=='markdown' and i<7 and re.search('Preparación del Entorno|Importación de Librerías',src,re.I):
            stats['setup_cells_removed']+=1;continue
        if typ=='code' and i<9 and (src.strip().startswith(('!','%')) or re.match(r'^from IPython.display import Image[^\n]*$',src.strip())):
            stats['setup_cells_removed']+=1;continue
        text,changed=correct(f['title'],i,src,typ)
        if changed:
            stats['text_corrections']+=1;changes.append({'notebook':str(f['path'].relative_to(INPUT)),'cell':i,'type':typ,'before':src,'after':text})
        rendered=''
        if typ=='markdown':rendered=sanitize(markdown(text));plain.append(re.sub(r'data:[^\s)]+','',text))
        elif typ=='code':
            imgcall=re.fullmatch(r'\s*(?:display\()?Image\([\s\S]*?\)\)?\s*',src)
            if imgcall:
                match=re.search(r'/([^/\"\']+\.(?:png|jpg|jpeg|svg|webp))',src)
                image_src=local_image(folder,match[1]) if match and 'http' not in src else None
                if image_src:rendered=f'<figure><img src="{image_src}" alt="Ilustración de la sección" loading="lazy"></figure>'
                else:
                    rendered=output_html(c.get('outputs',[]))
                    if not rendered:
                        url=re.search(r'https?://[^\"\']+',src)
                        if url:rendered=f'<img src="{remote(url[0])}" alt="Figura externa del notebook" loading="lazy">'
                        else:stats['missing'].append({'notebook':f['title'],'cell':i,'source':src})
            else:
                code=highlight(text,PythonLexer(),HtmlFormatter())
                rendered=f'<details class="source-code"><summary>Código Python · celda {i+1}</summary><button type="button" class="copy-code">Copiar código</button>{code}</details>'
                if f['title'] in (PE,ROPE) and i in (37,39,41):
                    rendered+=f'<img src="../assets/figures/pe-{i}.png" alt="Codificación posicional calculada para 32 dimensiones" loading="lazy">'
                elif f['title']==ROPE and i==63:
                    rendered+='<img src="../assets/figures/ape.svg" alt="Efecto de sumar posiciones a vectores sintéticos">'
                else:rendered+=output_html(c.get('outputs',[]))
        parts.append(f'<section class="cell" id="celda-{i+1}" data-cell="{i}">{rendered}</section>')
    content=BeautifulSoup(''.join(parts),'html.parser');toc=[]
    for j,h in enumerate(content.find_all(re.compile('^h[1-6]$'))):
        h['id']='seccion-'+str(j)
        if int(h.name[1])<=2 and len(toc)<55:toc.append(f'<a href="#{h["id"]}">{html.escape(h.get_text(" ",strip=True))}</a>')
    idx=files.index(f);prev=files[idx-1] if idx else None;nxt=files[idx+1] if idx+1<len(files) else None
    pager='<div class="pager">'+(f'<a href="{prev["filename"]}">← {html.escape(prev["title"])}</a>' if prev else '<span></span>')+(f'<a href="{nxt["filename"]}">{html.escape(nxt["title"])} →</a>' if nxt else '')+'</div>'
    hero=f'<header class="hero"><div class="eyebrow">Procesamiento del Lenguaje Natural y Reconocimiento del Habla · Clase {f["class"]:02d}</div><h1>{html.escape(f["title"])}</h1><p class="note">Contenido convertido sin ejecutar Python. Se conservan las salidas guardadas; las figuras matemáticas sustituidas y los gráficos de PE están identificados en el registro de revisión.</p><div class="toolbar"><button id="expand">Mostrar código</button><button id="collapse">Plegar código</button><button id="print">Imprimir / PDF</button><a href="{f["filename"]}" download>Descargar HTML</a></div><details class="page-toc"><summary>En esta página</summary>{"".join(toc)}</details></header>'
    page=layout(f['title'],hero+str(content)+pager,f['filename'])
    page=re.sub('UPATECO','institución',page,flags=re.I)
    (PAGES/f['filename']).write_text(page)
    search.append({'title':f['title'],'class':f['class'],'url':'nlp/'+f['filename'],'text':BeautifulSoup(' '.join(plain),'html.parser').get_text(' ',strip=True)})
    stats['notebooks']+=1;print('Rendered',f['filename'],flush=True)

sections=[]
for num,title in CATALOG.items():
    group=[f for f in files if f['class']==num]
    links=''.join(f'<li><a href="nlp/{f["filename"]}">{html.escape(f["title"])}</a>{" <span class=\"label\">Complemento</span>" if f["annex"] else ""}</li>' for f in group)
    sections.append(f'<article class="catalog-row" id="clase-{num:02d}"><span class="number">{num:02d}</span><div><h3>{html.escape(title)}</h3>{"<ul>"+links+"</ul>" if links else "<p class=\"note\">Material pendiente. La carpeta recibida no contiene un notebook.</p>"}</div></article>')
hero=f'''<header class="hero home"><div class="eyebrow">Teoría · Código · Visualizaciones</div><h1>Del lenguaje<br>a la representación.</h1><p class="lead">Un recorrido por el procesamiento del lenguaje natural y el reconocimiento del habla. Clases para leer como un libro, con notebooks, ejemplos numéricos y código desplegable.</p><p class="author">{AUTHOR} <span>· Docencia en Inteligencia Artificial</span></p><div class="chips"><span>Embeddings</span><span>Atención</span><span>Transformers</span><span>Audio</span></div><div class="hero-actions"><a class="primary" href="nlp/{files[0]['filename']}">Comenzar a leer →</a><a href="{LI}">Perfil profesional ↗</a></div></header><section class="intro-grid"><div><div class="eyebrow">01 / Biblioteca disponible</div><h2>Lenguaje natural<br>y reconocimiento del habla</h2><p>29 notebooks de las clases 2–16 y sus complementos. La clase 1 está pendiente de incorporar.</p></div><div><div class="eyebrow">02 / Otra materia</div><h2>Machine Learning Avanzado<br>y Aprendizaje Profundo</h2><p>El catálogo de esta materia puede consultarse en el portafolio de Notion.</p><a href="{NOTION}">Abrir portafolio de Notion ↗</a></div></section><section id="buscar"><h2>Buscar en el libro</h2><label for="search">Tema, concepto o nombre del notebook</label><input id="search" type="search" placeholder="Por ejemplo: softmax, GloVe, Fourier…" autocomplete="off"><div id="search-status" role="status" aria-live="polite"></div><div id="search-results"></div></section><section id="indice"><h2>Índice de clases</h2>{''.join(sections)}</section>'''
home=layout('Portafolio docente',hero,root=True).replace('</body>','<script src="assets/search-index.js"></script><script src="assets/search.js"></script></body>')
(DOCS/'index.html').write_text(home)
(ASSETS/'search-index.js').write_text('window.BOOK_SEARCH='+json.dumps(search,ensure_ascii=False)+';')
(ROOT/'reports/revision.json').write_text(json.dumps(stats,indent=2,ensure_ascii=False))
(ROOT/'reports/correcciones.json').write_text(json.dumps(changes,indent=2,ensure_ascii=False))
(ROOT/'reports/catalogo.json').write_text(json.dumps([{k:str(v) for k,v in f.items() if k!='path'} for f in files],indent=2,ensure_ascii=False))
print(json.dumps(stats,ensure_ascii=False,indent=2))
