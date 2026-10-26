"""Normaliza roles de color y títulos en HTML exportado; no ejecuta celdas."""
from pathlib import Path
from collections import Counter
import json,re
from bs4 import BeautifulSoup,NavigableString
ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/'docs'
TONES={'#91b9e3':'context','#00acc1':'context','#60a5fa':'context','#d9c58f':'emphasis','#fcf78d':'emphasis','#de9f68':'emphasis','#d6a487':'emphasis','#ffab8f':'emphasis'}

def apply_theme():
    """Migra font a estilos semánticos, preservando IDs y fórmulas."""
    counts=Counter()
    for path in sorted(DOCS.rglob('*.html')):
        soup=BeautifulSoup(path.read_text(),'html.parser')
        for tag in soup.find_all('font'):
            tone=TONES.get(tag.get('color','').lower(),'accent');tag.name='span'
            for attr in ('color','face','size'):tag.attrs.pop(attr,None)
            tag['class']=list(dict.fromkeys(tag.get('class',[])+['tone-'+tone]));counts['font_tags_migrated']+=1
        for p in soup.select('section.cell p'):
            if p.find_parent(['pre','blockquote']):continue
            match=re.match(r'^\s*(#{1,6})\s+\S',p.get_text())
            if not match or len(p.get_text())>240:continue
            for node in p.descendants:
                if isinstance(node,NavigableString) and node.strip():
                    node.replace_with(re.sub(r'^\s*#{1,6}\s+','',str(node)));break
            p.name='h'+str(len(match[1]));p['id']='titulo-'+p.find_parent('section')['id'];counts['markdown_headings_repaired']+=1
        active=soup.select_one('nav a.active')
        if active:active['aria-current']='page'
        toc=soup.select_one('.page-toc')
        if toc:
            summary=toc.find('summary').extract();toc.clear();toc.append(summary)
            for h in soup.select('section.cell h1,section.cell h2,section.cell h3'):
                if not h.get('id'):continue
                a=soup.new_tag('a',href='#'+h['id']);a.string=h.get_text(' ',strip=True);toc.append(a)
        if path.name=='404.html':
            for el in soup.select('[href],[src]'):
                for attr in ('href','src'):
                    value=el.get(attr,'')
                    if value and not value.startswith(('http:','https:','/','#','data:','mailto:')):el[attr]='/NLP-ASR-ML-DL-2026/'+value.removeprefix('./')
        path.write_text(str(soup));counts['html_pages']+=1
    replacements={'#111c30':'#191d26','#1a2942':'#222733','#3d4c67':'#3b4354','#e6e9f1':'#e5e7eb','#a7b4c9':'#a8b0c1'}
    for path in (DOCS/'assets/figures').glob('*.svg'):
        svg=path.read_text()
        for old,new in replacements.items():svg=svg.replace(old,new)
        path.write_text(svg);counts['own_svg_figures']+=1
    report=ROOT/'reports/theme.json'
    if not report.exists() or counts['font_tags_migrated']:report.write_text(json.dumps(dict(counts),ensure_ascii=False,indent=2))
    print(json.dumps(dict(counts),ensure_ascii=False))
if __name__=='__main__':apply_theme()
