/* Visualizaciones locales de las salidas guardadas, sin servicios externos. */
(() => {
  'use strict';
  const payload = JSON.parse(document.getElementById('glove-data').textContent);
  const NS = 'http://www.w3.org/2000/svg';
  const palette = ['#91b9e3','#b8a5ee','#d9c58f','#9bc9b0','#e3a19c','#9dcdd1'];
  const create = (name, attrs = {}, text = '') => {
    const el = document.createElementNS(NS, name);
    for (const [key,val] of Object.entries(attrs)) el.setAttribute(key,String(val));
    if (text) el.textContent=text;
    return el;
  };
  const line = (svg,x1,y1,x2,y2,color='#343b4b',width=1) => svg.append(create('line',{x1,y1,x2,y2,stroke:color,'stroke-width':width}));
  const label = (svg,x,y,text,fill='#a8b0c1',size=17,anchor='start') => svg.append(create('text',{x,y,fill,'font-size':size,'font-family':'system-ui,sans-serif','text-anchor':anchor},text));
  const fmt = value => Number(value).toLocaleString('es-AR',{maximumFractionDigits:4});

  // Mapa de calor y tabla: valores exactos de la ventana del ejemplo.
  const {words,values} = payload.matrix;
  const heat = create('svg',{viewBox:'0 0 1000 1000',role:'img','aria-label':'Matriz de coocurrencias: filas centro y columnas contexto'});
  const cell=30, offsetX=240,offsetY=220,max=Math.max(...values.flat());
  words.forEach((word,i) => {
    label(heat,offsetX-12,offsetY+i*cell+22,word,'#e5e7eb',17,'end');
    const text=create('text',{transform:`translate(${offsetX+i*cell+20},${offsetY-12}) rotate(-55)`,fill:'#e5e7eb','font-family':'system-ui,sans-serif','font-size':17},word);heat.append(text);
    values[i].forEach((value,j) => {
      const intensity=value/max;
      const color=value ? `rgb(${Math.round(35+110*intensity)},${Math.round(48+137*intensity)},${Math.round(66+160*intensity)})`:'#15181f';
      const rect=create('rect',{x:offsetX+j*cell,y:offsetY+i*cell,width:cell-2,height:cell-2,fill:color,tabindex:0,role:'img','aria-label':`${word}, ${words[j]}: ${fmt(value)}`});
      rect.append(create('title',{},`${word} → ${words[j]}: ${fmt(value)}`));
      const show=()=>{document.getElementById('heat-status').textContent=`Centro «${word}» · contexto «${words[j]}» · xᵢⱼ = ${fmt(value)}`;};
      rect.addEventListener('pointerenter',show);rect.addEventListener('focus',show);rect.addEventListener('click',show);heat.append(rect);
    });
  });
  label(heat,offsetX,990,`0 = no observado · máximo = ${fmt(max)} · radio 2 · peso 1/distancia`,'#d9c58f',18);
  document.getElementById('heatmap').append(heat);
  const weight=create('svg',{viewBox:'0 0 900 340',role:'img','aria-label':'h(x) con x máximo 5 y alfa 0,75. Peso 0 en x=0 y 1 desde x=5.'});
  line(weight,70,275,850,275,'#a8b0c1',2);line(weight,70,275,70,40,'#a8b0c1',2);
  const wpath=Array.from({length:201},(_,i)=>{const x=i/20;return `${i?'L':'M'}${70+76*x},${275-210*Math.min(1,(x/5)**.75)}`;}).join(' ');
  weight.append(create('path',{d:wpath,fill:'none',stroke:'#d9c58f','stroke-width':4}));
  const boundary=create('line',{x1:450,x2:450,y1:65,y2:275,stroke:'#91b9e3','stroke-dasharray':'6 6'});weight.append(boundary);
  label(weight,65,300,'0');label(weight,450,310,'xₘₐₓ = 5','#91b9e3',19,'middle');label(weight,830,310,'10');label(weight,45,72,'1');label(weight,80,30,'h(x) = min[1, (x/5)⁰·⁷⁵]','#e5e7eb',21);
  document.getElementById('weight-curve').append(weight);
  const table=document.createElement('table');
  const cap=document.createElement('caption');cap.textContent='Coocurrencias ponderadas xᵢⱼ';table.append(cap);
  const head=document.createElement('thead'),hr=document.createElement('tr');
  ['Centro / contexto',...words].forEach(w=>{const th=document.createElement('th');th.textContent=w;th.scope='col';hr.append(th);});head.append(hr);table.append(head);
  const body=document.createElement('tbody');
  words.forEach((w,i)=>{const row=document.createElement('tr');const th=document.createElement('th');th.textContent=w;th.scope='row';row.append(th);values[i].forEach(v=>{const td=document.createElement('td');td.textContent=fmt(v);row.append(td);});body.append(row);});table.append(body);document.getElementById('cooc-table').append(table);

  // Animación: los 200 estados proceden de la salida guardada del notebook.
  const {names,points,loss}=payload.animation;
  const input=document.getElementById('glove-step'), select=document.getElementById('glove-word');
  names.forEach((word,i)=>{const option=document.createElement('option');option.value=i;option.textContent=word;select.append(option);});
  select.value=names.indexOf('hielo');
  const all=points.flat();
  const xmin=Math.min(...all.map(p=>p[0]))-.25,xmax=Math.max(...all.map(p=>p[0]))+.25;
  const ymin=Math.min(...all.map(p=>p[1]))-.25,ymax=Math.max(...all.map(p=>p[1]))+.25;
  const sx=x=>70+(x-xmin)/(xmax-xmin)*570, sy=y=>470-(y-ymin)/(ymax-ymin)*360;
  const lx=i=>755+i/199*365, ly=v=>470-v/(Math.max(...loss)*1.05)*360;
  let timer=null;
  const draw=()=>{
    const step=Number(input.value)-1,selected=Number(select.value),host=document.getElementById('glove-chart');
    host.replaceChildren();
    const svg=create('svg',{viewBox:'0 0 1200 570',role:'img','aria-label':`Actualización ${step+1}. Pérdida ${fmt(loss[step])}. Palabra seleccionada: ${names[selected]}.`});
    label(svg,70,42,'Vectores combinados eᵢ = vᵢ + uᵢ','#e5e7eb',24);label(svg,755,42,'Pérdida ponderada J','#e5e7eb',24);
    for(let k=0;k<=4;k++){
      const x=xmin+k/4*(xmax-xmin),y=ymin+k/4*(ymax-ymin);
      line(svg,sx(x),110,sx(x),470);line(svg,70,sy(y),640,sy(y));
      label(svg,sx(x),500,x.toFixed(1),'#a8b0c1',16,'middle');label(svg,60,sy(y)+5,y.toFixed(1),'#a8b0c1',16,'end');
      const val=k/4*Math.max(...loss)*1.05;line(svg,755,ly(val),1120,ly(val));label(svg,745,ly(val)+5,val.toFixed(1),'#a8b0c1',16,'end');
    }
    line(svg,sx(0),110,sx(0),470,'#a8b0c1');line(svg,70,sy(0),640,sy(0),'#a8b0c1');
    points[step].forEach(([x,y],i)=>{
      const color=palette[i%palette.length],active=i===selected;
      if(active){
        const path=points.slice(0,step+1).map((frame,k)=>`${k?'L':'M'} ${sx(frame[i][0])},${sy(frame[i][1])}`).join(' ');
        svg.append(create('path',{d:path,fill:'none',stroke:color,'stroke-width':2,'stroke-dasharray':'4 5',opacity:.65}));
        line(svg,sx(0),sy(0),sx(x),sy(y),color,3);
      }
      const circle=create('circle',{cx:sx(x),cy:sy(y),r:active?9:5,fill:color,opacity:active?1:.7,tabindex:0,role:'button','aria-label':`${names[i]}: ${fmt(x)}, ${fmt(y)}`});
      circle.append(create('title',{},`${names[i]} · (${fmt(x)}, ${fmt(y)})`));
      const activate=()=>{select.value=i;draw();};circle.addEventListener('click',activate);circle.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();activate();}});svg.append(circle);
      if(active)label(svg,Math.max(82,Math.min(580,sx(x)+12)),Math.max(95,sy(y)-12),names[i],color,22);
    });
    const path=loss.slice(0,step+1).map((value,i)=>`${i?'L':'M'}${lx(i)},${ly(value)}`).join(' ');
    svg.append(create('path',{d:path,fill:'none',stroke:'#d9c58f','stroke-width':4}));svg.append(create('circle',{cx:lx(step),cy:ly(loss[step]),r:6,fill:'#d9c58f'}));
    for(const i of [0,49,99,149,199])label(svg,lx(i),500,String(i+1),'#a8b0c1',16,'middle');
    label(svg,355,540,'Dimensión 1 / Dimensión 2','#91b9e3',18,'middle');label(svg,937,540,'Actualización','#91b9e3',18,'middle');
    host.append(svg);document.getElementById('glove-count').value=String(step+1);
    document.getElementById('loss-status').textContent=`Actualización ${step+1} de 200 · J = ${fmt(loss[step])} · ${names[selected]} = (${fmt(points[step][selected][0])}; ${fmt(points[step][selected][1])}).`;
  };
  const pause=()=>{clearInterval(timer);timer=null;};
  document.getElementById('play-glove').addEventListener('click',()=>{
    pause();if(Number(input.value)===200)input.value=1;
    timer=setInterval(()=>{if(Number(input.value)>=200){pause();return;}input.value=Number(input.value)+1;draw();},100);
  });
  document.getElementById('pause-glove').addEventListener('click',pause);input.addEventListener('input',()=>{pause();draw();});select.addEventListener('change',draw);draw();

  // Ampliación accesible de los diagramas; conserva el enlace como alternativa.
  const dialog=document.createElement('dialog'),close=document.createElement('button'),image=document.createElement('img');
  close.type='button';close.textContent='Cerrar ×';close.addEventListener('click',()=>dialog.close());dialog.append(close,image);document.body.append(dialog);
  dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
  document.querySelectorAll('.figure-zoom').forEach(a=>a.addEventListener('click',e=>{e.preventDefault();image.src=a.querySelector('img').src;image.alt=a.querySelector('img').alt;dialog.showModal();}));
})();
