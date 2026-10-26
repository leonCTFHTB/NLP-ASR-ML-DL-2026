(() => {
  const field=document.querySelector('#search'),out=document.querySelector('#search-results'),status=document.querySelector('#search-status');
  if(!field)return;
  const norm=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  const index=(window.BOOK_SEARCH||[]).map(p=>({...p,normalized:norm(p.title+' '+p.text)}));
  function search(){
    out.replaceChildren();const q=norm(field.value.trim());
    if(q.length<2){status.textContent='Escribí al menos dos caracteres.';return;}
    const terms=q.split(/\s+/),hits=index.filter(p=>terms.every(t=>p.normalized.includes(t))).sort((a,b)=>Number(norm(b.title).includes(q))-Number(norm(a.title).includes(q)));
    status.textContent=hits.length+' notebook'+(hits.length===1?'':'s')+' encontrado'+(hits.length===1?'':'s')+'.';
    for(const p of hits){
      const row=document.createElement('article');row.className='search-result';const h=document.createElement('h3'),a=document.createElement('a');a.href=p.url;a.textContent='Clase '+p.class+' · '+p.title;h.append(a);row.append(h);
      const snip=document.createElement('p');const pos=norm(p.text).indexOf(terms[0]);const start=Math.max(0,pos-80);snip.textContent=(start?'…':'')+p.text.slice(start,start+260)+'…';row.append(snip);out.append(row);
    }
  }
  field.addEventListener('input',search);search();
})();
