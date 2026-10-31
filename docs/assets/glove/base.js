(() => {
  const $ = s => document.querySelector(s);
  $('#expand')?.addEventListener('click',()=>document.querySelectorAll('.source-code').forEach(d=>d.open=true));
  $('#collapse')?.addEventListener('click',()=>document.querySelectorAll('.source-code').forEach(d=>d.open=false));
  $('#print')?.addEventListener('click',()=>{document.querySelectorAll('.source-code').forEach(d=>d.open=true);window.print();});
  $('#menu')?.addEventListener('click',e=>{const state=document.body.classList.toggle('nav-open');e.currentTarget.setAttribute('aria-expanded',String(state));});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){document.body.classList.remove('nav-open');$('#menu')?.setAttribute('aria-expanded','false');}});
  document.querySelectorAll('.copy-code').forEach(b=>b.addEventListener('click',async()=>{
    const value=b.parentElement.querySelector('pre')?.innerText||'';
    try {
      if(navigator.clipboard&&window.isSecureContext)await navigator.clipboard.writeText(value);
      else {const ta=document.createElement('textarea');ta.value=value;document.body.append(ta);ta.select();if(!document.execCommand('copy'))throw Error('copy');ta.remove();}
      b.textContent='Copiado';setTimeout(()=>b.textContent='Copiar código',1800);
    }catch {b.textContent='Seleccioná y copiá el código';}
  }));
  const progress=()=>{const h=document.documentElement;const p=$('.progress');if(p)p.style.width=(h.scrollHeight>h.clientHeight?100*h.scrollTop/(h.scrollHeight-h.clientHeight):100)+'%';};
  window.addEventListener('scroll',progress,{passive:true});progress();
  document.querySelectorAll('.load-video').forEach(button=>button.addEventListener('click',async()=>{
    const video=button.nextElementSibling;button.disabled=true;button.textContent='Cargando video…';
    try {
      const parts=await Promise.all(video.dataset.videoParts.split('|').map(async path=>{const r=await fetch(path);if(!r.ok)throw Error('video');return r.arrayBuffer();}));
      video.src=URL.createObjectURL(new Blob(parts,{type:'video/mp4'}));video.load();button.remove();
    }catch {button.disabled=false;button.textContent='Reintentar carga del video';}
  }));
})();

