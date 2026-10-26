"""Renderizador de Markdown y fórmulas MathML para las páginas docentes."""
from pathlib import Path
import hashlib,html,json,re
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from latex2mathml.converter import convert
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
md=MarkdownIt('commonmark',{'html':True}).enable('table')

def render(text):
    """Protege ecuaciones y genera MathML accesible sin un CDN."""
    formulas={}
    def save(m,display):
        key='FORMULAEDITORIAL'+str(len(formulas))+'FINAL'
        val=convert(m[1],display='block' if display else 'inline')
        val=val.replace('<math ',f'<math aria-label="{html.escape(m[1],quote=True)}" ')
        formulas[key]=val;return key
    text=re.sub(r'\$\$([\s\S]+?)\$\$',lambda m:save(m,True),text)
    text=re.sub(r'(?<!\\)\$([^\n$]+?)\$',lambda m:save(m,False),text)
    result=md.render(text)
    for key,val in formulas.items():result=result.replace(key,val)
    return result
