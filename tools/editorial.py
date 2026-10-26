"""Aplica correcciones editoriales identificadas a HTML existente, sin ejecutar modelos."""
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

def apply_edits():
    """Aplica una vez cada parche y conserva el antes/después en el informe."""
    config=json.loads((ROOT/'reports/editorial-patches.json').read_text())
    report_path=ROOT/'reports/auditoria-editorial.json'
    history=json.loads(report_path.read_text()) if report_path.exists() else []
    cache={};failures=[]
    for patch in config:
        file=DOCS/'nlp'/patch['file'];soup=cache.setdefault(file,BeautifulSoup(file.read_text(),'html.parser'))
        cell=soup.find(id=patch['cell']);key=hashlib.sha256(json.dumps(patch,sort_keys=True).encode()).hexdigest()[:12]
        applied=cell.get('data-editorial-edits','').split('|')
        if key in applied:continue
        before=str(cell)
        if patch['mode']=='replace_text':
            hits=0
            for node in list(cell.find_all(string=True)):
                if patch['old'] in str(node):node.replace_with(str(node).replace(patch['old'],patch['new']));hits+=1
            if not hits:failures.append([patch['file'],patch['cell'],patch['old']]);continue
        else:
            heading=cell.find(re.compile('^h[1-6]$'))
            if heading:heading=heading.extract()
            cell.clear()
            if heading:cell.append(heading)
            fragment=BeautifulSoup(render(patch['markdown']),'html.parser')
            for child in list(fragment.contents):cell.append(child)
        label,url=patch['source']
        if not cell.find('a',href=url):
            note=soup.new_tag('p',attrs={'class':'note editorial-source'});note.append('Fuente de la revisión: ')
            link=soup.new_tag('a',href=url);link.string=label;note.append(link);cell.append(note)
        cell['data-editorial-edits']='|'.join([v for v in applied if v]+[key])
        history.append({'file':'docs/nlp/'+patch['file'],'cell':patch['cell'],'reason':patch['reason'],'source':url,'before':before,'after':str(cell)})
    if failures:raise RuntimeError('Parches sin coincidencia: '+json.dumps(failures,ensure_ascii=False))
    for file,soup in cache.items():file.write_text(str(soup))
    report_path.write_text(json.dumps(history,ensure_ascii=False,indent=2));print('Correcciones documentadas:',len(history))
if __name__=='__main__':apply_edits()
