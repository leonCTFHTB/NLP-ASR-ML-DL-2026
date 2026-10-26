"""Retira registros históricos y recursos gráficos sin referencias en la edición vigente."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
OBSOLETE_REPORTS=['auditoria-editorial.json','auditoria-figuras.json','correcciones.json','editorial-patches.json','figure-patches.json','revision.json','checks.json','theme.json']
OBSOLETE_TOOLS=['build.py','finalize.py','corrections.py','figures.py','backup.py','theme.py']
def run():
 for n in OBSOLETE_REPORTS:(ROOT/'reports'/n).unlink(missing_ok=True)
 for n in OBSOLETE_TOOLS:(ROOT/'tools'/n).unlink(missing_ok=True)
 text='\n'.join(p.read_text(errors='replace') for p in DOCS.rglob('*') if p.is_file() and p.suffix in ['.html','.css','.js','.svg'])
 removed=0
 for p in (DOCS/'assets').rglob('*'):
  if p.is_file() and not p.name.startswith('.') and p.suffix.lower() in ['.webp','.png','.jpg','.jpeg','.gif','.svg'] and p.name not in text:
   p.unlink();removed+=1
 print('Recursos gráficos sin referencias retirados:',removed)
if __name__=='__main__':run()
