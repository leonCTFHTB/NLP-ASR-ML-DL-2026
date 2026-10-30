"""Convierte el notebook Whisper y sus ZIP sin ejecutar el código docente.

Uso: python tools/import_whisper.py notebook.ipynb directorio_de_zips
"""
from pathlib import Path
import argparse, base64, copy, hashlib, html, json, re, zipfile
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
from editorial import render, ROOT, DOCS
from latex2mathml.converter import convert

FILENAME = 'clase-17-whisper-datasets-entrenamiento-inferencia.html'
TITLE = '17 · Whisper: datasets, entrenamiento e inferencia'
ASSET = DOCS / 'assets' / 'whisper'
COLORS = {'#de9f68':'tone-emphasis', '#a79fe3':'tone-accent',
          '#d6a487':'tone-emphasis', '#dfc5cf':'tone-accent',
          '#a091e3':'tone-accent', '#91b9e3':'tone-context',
          '#d9c58f':'tone-emphasis', '#fcf78d':'tone-emphasis', '#b9cbea':'tone-context'}

def fragment(value):
    return BeautifulSoup(value, 'html.parser')

def portable_paths(source):
    source = re.sub(r'root_path = r?"/content/drive/[^\n]+', 'root_path = r"/content/images"', source)
    return source.replace('/content/drive/MyDrive/1_UPATECO/src/', '/content/audio/')

def markdown(source):
    # Proteger el código del conversor de fórmulas y colorearlo como las demás páginas.
    protected = {}
    def save(match):
        key = f'CODIGOWHISPER{len(protected)}FINAL'
        code = match[2] if match[2] is not None else match[3]
        value = highlight(code, PythonLexer(), HtmlFormatter()) if match[2] is not None else '<code>'+html.escape(code)+'</code>'
        protected[key] = value
        return '\n\n'+key+'\n\n' if match[2] is not None else key
    source = re.sub(r'^```([^\n]*)\n([\s\S]*?)^```\s*$|`([^`\n]+)`', save, source, flags=re.M)
    # El notebook contiene dos entornos align sin delimitadores $. CommonMark
    # interpretaría su signo igual como un encabezado en vez de una ecuación.
    def align(match):
        key = f'CODIGOWHISPER{len(protected)}FINAL'
        latex = match[0]
        protected[key] = convert(latex.replace(r'\_', '_'), display='block').replace('<math ', '<math aria-label="'+html.escape(latex,quote=True)+'" ')
        return key
    source = re.sub(r'\\begin\{align\}[\s\S]*?\\end\{align\}', align, source)
    source = source.replace('**/font>', '**</font>')
    value = render(source)
    for key, code in protected.items():
        value = value.replace('<p>'+key+'</p>', code).replace(key, code)
    soup = fragment(value)
    for font in soup.find_all('font'):
        font.name = 'span'
        font['class'] = COLORS.get(font.get('color','').lower(), 'tone-emphasis')
        font.attrs.pop('color', None)
    return str(soup)

def main(notebook, zip_dir):
    raw = notebook.read_bytes()
    nb = json.loads(raw)
    ASSET.mkdir(parents=True, exist_ok=True)
    archive_images = {}
    for path in sorted(zip_dir.glob('*.zip')):
        with zipfile.ZipFile(path) as archive:
            for name in archive.namelist():
                if re.fullmatch(r'clase-\d+/[\w-]+\.png', name):
                    data = archive.read(name)
                    if name in archive_images and archive_images[name] != data:
                        raise ValueError('Imagen duplicada diferente: '+name)
                    archive_images[name] = data
    base = fragment((DOCS/'nlp/clase-16-16-radix-2.html').read_text())
    base.title.string = TITLE+' · Jacobo León Juárez'
    main_tag = base.main
    hero = copy.deepcopy(main_tag.select_one('.hero'))
    footer = copy.deepcopy(main_tag.footer)
    main_tag.clear()
    main_tag.append(hero)
    hero.h1.string = TITLE
    hero.select_one('.eyebrow').string = 'Procesamiento del Lenguaje Natural y Reconocimiento del Habla · Clase 17'
    hero.select_one('p.note').string = 'Contenido convertido sin ejecutar Python. Se conservan el texto, el código y las salidas guardadas del notebook; los tiempos y resultados corresponden a su ejecución original. Las rutas personales de Google Drive se muestran como /content/images y /content/audio.'
    hero.select_one('.toolbar a')['href'] = FILENAME
    toc = hero.select_one('.page-toc')
    toc.clear()
    toc.append(fragment('<summary>En esta página</summary>'))
    image_class = None
    image_refs = []
    heading_count = 0
    output_count = 0
    for index, cell in enumerate(nb['cells']):
        source = ''.join(cell['source'])
        section = base.new_tag('section', attrs={'class':'cell','id':f'celda-{index+1}','data-cell':str(index)})
        main_tag.append(section)
        if cell['cell_type'] == 'markdown':
            section.append(fragment(markdown(source)))
            for heading in section.find_all(re.compile(r'^h[1-6]$')):
                heading['id'] = f'seccion-{heading_count}'
                heading_count += 1
                if heading.name in ('h1','h2','h3'):
                    link = base.new_tag('a', href='#'+heading['id'])
                    link.string = heading.get_text(' ',strip=True)
                    toc.append(link)
            continue
        match = re.search(r'root_class_path\s*=.*?/(clase-\d+)', source)
        if match:
            image_class = match[1]
        # Una ruta personal de Colab no es necesaria para entender el ejemplo.
        shown = portable_paths(source)
        details = base.new_tag('details', attrs={'class':'source-code'})
        details.append(fragment(f'<summary>Código Python · celda {index+1}</summary><button class="copy-code" type="button">Copiar código</button>'))
        details.append(fragment(highlight(shown, PythonLexer(), HtmlFormatter())))
        section.append(details)
        image_match = re.fullmatch(r'\s*Image\(f[\"\']\{root_class_path\}/([^\"\']+)[\"\']\)\s*', source)
        if image_match:
            key = image_class+'/'+image_match[1]
            if key not in archive_images:
                raise ValueError('Falta imagen en los ZIP: '+key)
            target = ASSET/key
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive_images[key])
            previous = section.find_previous(re.compile(r'^h[1-6]$'))
            label = previous.get_text(' ',strip=True) if previous else key
            section.append(fragment(f'<figure><img loading="lazy" src="../assets/whisper/{key}" alt="{html.escape(label,quote=True)}"/></figure>'))
            image_refs.append(key)
            output_count += 1
            continue
        for oi, output in enumerate(cell.get('outputs', [])):
            data = output.get('data', {})
            out = base.new_tag('div', attrs={'class':'output'})
            if output['output_type'] == 'stream':
                pre = base.new_tag('pre'); pre.string = portable_paths(''.join(output.get('text',[]))); out.append(pre)
            elif 'image/png' in data:
                target = ASSET/f'salida-{index+1}-{oi}.png'
                target.write_bytes(base64.b64decode(''.join(data['image/png'])))
                out.append(fragment(f'<figure><img loading="lazy" src="../assets/whisper/{target.name}" alt="Gráfica guardada del notebook, celda {index+1}"/></figure>'))
            elif 'text/html' in data:
                saved = fragment(''.join(data['text/html']))
                for script in saved.select('script,iframe'):
                    script.decompose()
                for audio in saved.select('audio'):
                    audio['preload'] = 'none'
                    audio['aria-label'] = 'Muestra de audio guardada del dataset MINDS-14'
                for media in saved.select('[src]'):
                    match = re.fullmatch(r'data:audio/[^;]+;base64,([\s\S]+)', media['src'])
                    if match:
                        target = ASSET/f'audio-{index+1}-{oi}.wav'
                        target.write_bytes(base64.b64decode(match[1]))
                        media['src'] = '../assets/whisper/'+target.name
                out.append(saved)
            elif 'text/plain' in data and not any(k.startswith('application/') for k in data):
                pre = base.new_tag('pre'); pre.string = ''.join(data['text/plain']); out.append(pre)
            else:
                continue  # Metadatos interactivos de Colab sin representación estática.
            section.append(out)
            output_count += 1
    pager = fragment('<div class="pager"><a href="clase-16-16-radix-2.html">← 16 - Radix-2</a></div>')
    main_tag.append(pager)
    main_tag.append(footer)
    (DOCS/'nlp'/FILENAME).write_text(str(base))
    catalog_path = ROOT/'reports/catalogo.json'
    catalog = json.loads(catalog_path.read_text())
    if not any(x['filename']==FILENAME for x in catalog):
        catalog.append({'class':'17','title':TITLE,'slug':'whisper-datasets-entrenamiento-inferencia','annex':'False','filename':FILENAME})
    catalog_path.write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n')
    for path in DOCS.rglob('*.html'):
        soup = fragment(path.read_text())
        nav = soup.select_one('nav[aria-label="Clases"]')
        if not nav:
            continue
        prefix = '' if path.parent.name=='nlp' else 'nlp/'
        if path.name=='404.html':
            prefix='/NLP-ASR-ML-DL-2026/nlp/'
        for old in nav.select('[data-whisper]'):
            old.decompose()
        entry = fragment(f'<details class="chapter" data-whisper=""><summary>17 · Whisper</summary><a href="{prefix+FILENAME}">{TITLE}</a></details>')
        if path.name==FILENAME:
            for opened in nav.select('details[open]'):opened.attrs.pop('open',None)
            for active in nav.select('a.active'):
                active['class']=[];active.attrs.pop('aria-current',None)
            entry.details['open']=''
            entry.a['class']='active';entry.a['aria-current']='page'
        nav.append(entry)
        if path.name=='clase-16-16-radix-2.html':
            pager=soup.select_one('.pager')
            if not pager.find('a',href=FILENAME):pager.append(fragment(f'<a href="{FILENAME}">{TITLE} →</a>'))
        if path.name=='index.html':
            old=soup.select_one('#clase-17')
            if old:old.decompose()
            soup.select_one('#indice').append(fragment(f'<article class="catalog-row" id="clase-17"><span class="number">17</span><div><h3>Whisper: datasets, entrenamiento e inferencia</h3><ul><li><a href="nlp/{FILENAME}">{TITLE}</a></li></ul></div></article>'))
        path.write_text(str(soup))
    report = {'source_notebook':notebook.name,'source_sha256':hashlib.sha256(raw).hexdigest(),
              'html':'nlp/'+FILENAME,'cells':len(nb['cells']),
              'markdown_cells':sum(c['cell_type']=='markdown' for c in nb['cells']),
              'code_cells':sum(c['cell_type']=='code' for c in nb['cells']),
              'archive_images':image_refs,'saved_output_blocks':output_count,
              'python_training_executed':False,
              'adaptations':['Rutas personales de Google Drive mostradas como /content/images y /content/audio.',
                             'Colores del notebook adaptados al tema existente.',
                             'Dos entornos align sin delimitadores renderizados como MathML y una etiqueta font mal cerrada reparada.',
                             'Widgets de progreso de Colab omitidos; texto, audio y gráficas conservados.']}
    (ROOT/'reports/importacion-whisper.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(report,indent=2,ensure_ascii=False))

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('notebook',type=Path)
    parser.add_argument('zip_dir',type=Path)
    args=parser.parse_args()
    main(args.notebook,args.zip_dir)
