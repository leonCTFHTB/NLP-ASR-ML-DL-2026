"""Genera una copia de lectura local con HTML y recursos completos."""
from pathlib import Path
from bs4 import BeautifulSoup
import argparse,zipfile
root=Path(__file__).resolve().parents[1];docs=root/'docs'
p=argparse.ArgumentParser();p.add_argument('destination');args=p.parse_args()
with zipfile.ZipFile(args.destination,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in docs.rglob('*'):
  if not f.is_file() or '.part-' in f.name:continue
  if f.suffix=='.html':
   s=BeautifulSoup(f.read_text(),'html.parser')
   for v in s.select('video[data-original-src]'):
    v['src']=v['data-original-src'];v.attrs.pop('data-video-parts',None);v.attrs.pop('data-original-src',None)
   for button in s.select('.load-video'):button.decompose()
   z.writestr(str(f.relative_to(docs)),str(s))
  else:z.write(f,str(f.relative_to(docs)))
 for name in ['README.md','LICENCIAS.md','THIRD_PARTY.md','LICENSE-PLOTLY.txt']:
  z.write(root/name,'documentacion/'+name)
 z.writestr('LEEME.txt','Portafolio docente · Jacobo León Juárez\n\nDescomprimí el ZIP completo y abrí index.html.\nMantené assets/ y nlp/ junto al índice. Incluye los 29 HTML, imágenes, animaciones, audios, video y fórmulas MathML.\nEl código es de lectura: abrir el sitio no ejecuta Python.\nLas salidas que requieren un kernel de notebook pueden necesitar su entorno original.\nLa clase 1 está pendiente porque su carpeta se recibió vacía.\nCita y licencias: citar.html.\n')
print(Path(args.destination).resolve(),Path(args.destination).stat().st_size)
