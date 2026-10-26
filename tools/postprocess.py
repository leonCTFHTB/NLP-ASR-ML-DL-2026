"""Repara multimedia y reconstruye búsqueda y documentación de revisión."""
from pathlib import Path
from urllib.parse import urlsplit
import copy,html,json,re
import xml.etree.ElementTree as ET
from PIL import Image
from bs4 import BeautifulSoup
from editorial import render
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs';ASSETS=DOCS/'assets'

def run():
    """Prepara los exportados para servir desde /docs en GitHub Pages."""
    search=[];videos=0;dimensions={}
    catalog={x['filename']:x for x in json.loads((ROOT/'reports/catalogo.json').read_text())}
    for path in sorted(DOCS.rglob('*.html')):
        soup=BeautifulSoup(path.read_text(),'html.parser')
        # Reservar el espacio de imágenes lazy evita desplazar un ancla al
        # cargar ilustraciones que aparecen antes de ella en páginas largas.
        for im in soup.find_all('img'):
            src=im.get('src','')
            if urlsplit(src).scheme or src.startswith('/'):continue
            asset=(path.parent/src).resolve()
            if asset not in dimensions:
                if asset.suffix=='.svg':
                    svg=ET.parse(asset).getroot();box=svg.get('viewBox','').split()
                    if len(box)==4:dimensions[asset]=(float(box[2]),float(box[3]))
                    else:
                        width=re.match(r'^[0-9.]+',svg.get('width',''));height=re.match(r'^[0-9.]+',svg.get('height',''))
                        dimensions[asset]=(float(width[0]),float(height[0])) if width and height else None
                else:
                    with Image.open(asset) as bitmap:dimensions[asset]=bitmap.size
            size=dimensions[asset]
            if size and not im.get('width') and not im.get('height'):
                im['width']=str(round(size[0]));im['height']=str(round(size[1]))
        for video in soup.find_all('video'):
            source=video.find('source');src=video.get('src') or (source.get('src') if source else '')
            if not src:continue
            name=Path(urlsplit(src).path).stem
            parts=sorted(ASSETS.glob(name+'.part-*.bin'),key=lambda p:int(p.stem.rsplit('-',1)[1]))
            if not parts:continue
            if [int(p.stem.rsplit('-',1)[1]) for p in parts]!=list(range(len(parts))):raise ValueError('Video incompleto: '+name)
            video['data-original-src']=src;video['data-video-parts']='|'.join('../assets/'+p.name for p in parts)
            video.attrs.pop('src',None);video['preload']='none';video['controls']='';video['aria-label']='Video didáctico de convolución'
            for el in list(video.find_all('source')):el.decompose()
            if not video.find_previous_sibling('button',class_='load-video'):
                button=soup.new_tag('button',attrs={'type':'button','class':'load-video'});button.string=f'Cargar video ({sum(p.stat().st_size for p in parts)/1e6:.1f} MB)';video.insert_before(button)
            videos+=1
        # Ortografía de rótulos; no se renombran URLs públicas.
        for node in list(soup.find_all(string=True)):
            if node.parent.name in ('script','style','pre','code') or node.find_parent(['pre','code','math']):continue
            value=str(node).replace('Inotroducción','Introducción').replace('inotroducción','introducción').replace('Mecanísmos','Mecanismos')
            if value!=str(node):node.replace_with(value)
        toc=soup.select_one('.page-toc')
        if toc:
            summary=toc.find('summary').extract();toc.clear();toc.append(summary)
            for heading in soup.select('section.cell h1,section.cell h2,section.cell h3'):
                if heading.get('id'):
                    a=soup.new_tag('a',href='#'+heading['id']);a.string=heading.get_text(' ',strip=True);toc.append(a)
        # Exportar un HTML suelto no incluye los assets relativos.
        for a in soup.select('.toolbar a[download]'):
            a.string='Descargar página HTML';a['title']='Requiere los recursos del repositorio para visualizarse sin conexión.'
        if path.parent.name=='nlp':
            item=catalog[path.name];copy_soup=BeautifulSoup(str(soup.main),'html.parser')
            for node in copy_soup.select('script,style,.source-code,footer,.hero,.pager'):node.decompose()
            for m in copy_soup.find_all('math'):m.replace_with(m.get('aria-label',m.get_text(' ',strip=True)))
            search.append({'title':soup.h1.get_text(' ',strip=True),'class':int(item['class']),'url':'nlp/'+path.name,'text':copy_soup.get_text(' ',strip=True)})
        for footer in soup.select('footer'):
            prefix='../' if path.parent.name=='nlp' else ''
            if path.name=='404.html':prefix='/NLP-ASR-ML-DL-2026/'
            if not footer.find('a',href=prefix+'revision.html'):
                p=soup.new_tag('p');a=soup.new_tag('a',href=prefix+'revision.html');a.string='Revisión técnica y criterios editoriales';p.append(a);footer.append(p)
        path.write_text(str(soup))
    (ASSETS/'search-index.js').write_text('window.BOOK_SEARCH='+json.dumps(search,ensure_ascii=False)+';\n')
    # Una página legible ofrece acceso al informe y a las fuentes.
    base=BeautifulSoup((DOCS/'index.html').read_text(),'html.parser');base.title.string='Revisión técnica y diseño · Jacobo León Juárez'
    for script in list(base.find_all('script')):
        if 'search' in script.get('src',''):script.decompose()
    base.main.clear();base.main.append(BeautifulSoup(render((ROOT/'reports/REVISION.md').read_text()),'html.parser'))
    (DOCS/'revision.html').write_text(str(base))
    print('Índice actualizado:',len(search),'notebooks; videos reparados:',videos)
if __name__=='__main__':run()
