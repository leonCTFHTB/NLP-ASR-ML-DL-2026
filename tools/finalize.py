"""Completa licencias, repara fórmulas y empaqueta la versión ya convertida."""
from pathlib import Path
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from latex2mathml.converter import convert
import html, json, re, shutil
from figures import panel

root=Path(__file__).resolve().parents[1];docs=root/'docs';assets=docs/'assets'
bn=panel('Batch normalization: estadística y parámetros aprendidos',[
 ('Durante el entrenamiento',['Media μ y varianza σ²','estimadas sobre el lote.','En una CNN, por canal,','agregando lote y posiciones.']),
 ('Normalizar y transformar',['x̂ = (x − μ) / √(σ² + ε)','y = γ x̂ + β','γ y β se aprenden.','Inferencia: estadísticas móviles.'])], 'El comportamiento de inferencia depende de la configuración; BatchNorm no elimina por sí sola todo cambio de distribución.')
(assets/'figures/batchnorm.svg').write_text(bn)
report=json.loads((root/'reports/revision.json').read_text());repaired=0
for p in docs.rglob('*.html'):
    soup=BeautifulSoup(p.read_text(),'html.parser')
    for tag in ('html','head','body'):
        for nested in soup.find_all(tag)[1:]:nested.unwrap()
    for script in list(soup.find_all('script')):
        src=script.get('src','')
        if 'mathjax' in src.lower() or ('MathJax.Hub' in script.text and 'Plotly' not in script.text):
            script.decompose()
        elif 'cdn.plot.ly/plotly-' in src:
            script['src']=('../' if p.parent.name=='nlp' else '')+'assets/plotly-2.35.2.min.js'
    for el in soup.select('.math-fallback'):
        src=el.get_text();raw=re.sub(r'\\begin\{(align\*?|equation\*?|gather\*?)\}',lambda m:r'\begin{aligned}{} ',src)
        raw=re.sub(r'\\end\{(align\*?|equation\*?|gather\*?)\}',lambda m:r'\end{aligned}',raw)
        try:el.replace_with(BeautifulSoup(convert(raw,display='block'),'html.parser'));repaired+=1
        except Exception as e:print('Unrepaired formula',p,repr(src),repr(e))
    for im in soup.find_all('img'):
        if 'batch-normalization-768x479' in im.get('src',''):
            im['src']='../assets/figures/batchnorm.svg';im['alt']='Esquema propio de batch normalization';im.attrs.pop('data-external',None)
            im.insert_after(BeautifulSoup('<p class="note">Esquema propio de reemplazo. La referencia de la ilustración original se conserva debajo.</p>','html.parser'))
    # Un aviso local aclara la excepción de licencia, también en el respaldo.
    if soup.footer and not soup.footer.find(class_='third-party-notice'):
        link='../citar.html' if p.parent.name=='nlp' else 'citar.html'
        el=soup.new_tag('p',attrs={'class':'third-party-notice'});el.append('Los pasajes adaptados de Dive into Deep Learning conservan CC BY-SA 4.0 y su código MIT modificada. ')
        a=soup.new_tag('a',href=link);a.string='Créditos y condiciones de las fuentes';el.append(a);soup.footer.append(el)
    p.write_text(str(soup))
report['math']+=repaired;report['math_errors_repaired']=repaired
if repaired==len(report['math_errors']):report['math_errors']=[]
report['external']=[u for u in report['external'] if 'batch-normalization-768x479' not in u]
(root/'reports/revision.json').write_text(json.dumps(report,indent=2,ensure_ascii=False))
# Registro sin las rutas privadas de los originales.
changes=json.loads((root/'reports/correcciones.json').read_text())
for item in changes:
    item['before']=re.sub(r'([rR]?[\"\'])/content/(?:drive/)?MyDrive/[^\n\"\']*([\"\'])',r'\1[RUTA LOCAL OMITIDA]\2',item['before'])
    item['before']=re.sub('UPATECO','[INSTITUCIÓN OMITIDA]',item['before'],flags=re.I)
(root/'reports/correcciones.json').write_text(json.dumps(changes,indent=2,ensure_ascii=False))
md=MarkdownIt('commonmark',{'html':True}).enable('table')
base=BeautifulSoup((docs/'index.html').read_text(),'html.parser')
base.title.string='Cómo citar y licencias · Jacobo León Juárez'
for s in base.find_all('script'):
    if 'search' in s.get('src',''):s.decompose()
main=base.main;main.clear()
content='<header class="hero"><div class="eyebrow">Autoría · Reutilización</div><h1>Cómo citar este material</h1><p>Jacobo León Juárez · Portafolio docente · 2026</p></header>'
content+='<h2>Cita BibTeX</h2><pre>'+html.escape((root/'CITATION.bib').read_text())+'</pre><p><a href="CITATION.bib" download>Descargar CITATION.bib</a> · <a href="CITATION.cff" download>Descargar CITATION.cff</a></p>'
content+=md.render((root/'LICENCIAS.md').read_text())+md.render((root/'THIRD_PARTY.md').read_text())
main.append(BeautifulSoup(content,'html.parser'));(docs/'citar.html').write_text(str(base))
for n in ['CITATION.bib','CITATION.cff','LICENSE','LICENSE-CONTENT.txt','LICENSE-D2L-CONTENT.txt','LICENSE-D2L-SAMPLECODE.txt']:
    if (root/n).exists():shutil.copyfile(root/n,docs/n)
page=BeautifulSoup((docs/'index.html').read_text(),'html.parser');page.title.string='Página no encontrada · Jacobo León Juárez';page.main.clear();page.main.append(BeautifulSoup('<h1>Página no encontrada</h1><p>Volvé al <a href="./index.html">índice del portafolio</a> para elegir una clase.</p>','html.parser'));(docs/'404.html').write_text(str(page))
print('Finalizado: fórmulas reparadas',repaired,'; notebooks',report['notebooks'])

# Divide recursos de video grandes sin recodificar; se cargan a demanda.
for video_path in assets.glob('*.mp4'):
    if video_path.stat().st_size < 25000000:continue
    video_bytes=video_path.read_bytes();parts=[]
    for index,offset in enumerate(range(0,len(video_bytes),1000000)):
        part=video_path.with_name(video_path.stem+f'.part-{index}.bin')
        part.write_bytes(video_bytes[offset:offset+1000000]);parts.append('../assets/'+part.name)
    for page_path in (docs/'nlp').glob('*.html'):
        page=BeautifulSoup(page_path.read_text(),'html.parser');changed=False
        for video in page.find_all('video'):
            if video_path.name in video.get('src',''):
                video['data-original-src']=video['src'];video['data-video-parts']='|'.join(parts)
                video.attrs.pop('src',None);video['preload']='none';video['controls']=''
                button=page.new_tag('button',attrs={'type':'button','class':'load-video'});button.string='Cargar video (50 MB)';video.insert_before(button);changed=True
        if changed:page_path.write_text(str(page))
