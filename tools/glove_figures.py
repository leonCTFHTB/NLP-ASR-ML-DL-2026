"""Diagramas vectoriales de GloVe con datos y geometría explícitos."""
from pathlib import Path
from html import escape
import math

DEST=Path(__file__).resolve().parents[1]/'docs/assets/glove'
DEST.mkdir(parents=True,exist_ok=True)
BG='#111318'; PANEL='#191d26'; LINE='#343b4b'; TEXT='#e5e7eb'; MUTED='#a8b0c1'; BLUE='#91b9e3'; GOLD='#d9c58f'; LAV='#b8a5ee'; RED='#e3a19c'

class Diagram:
    def __init__(self,title,sub=''):
        self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="650" viewBox="0 0 1200 650" role="img" aria-label="{escape(title)}"><rect width="1200" height="650" rx="20" fill="{BG}"/><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="{BLUE}"/></marker></defs>']
        self.text(45,60,title,32,LAV,700);self.text(45,102,sub,21,MUTED)
    def text(self,x,y,t,size=24,color=TEXT,weight=400,anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="DejaVu Sans,sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">{escape(str(t))}</text>')
    def box(self,x,y,w,h,title='',color=LINE):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{PANEL}" stroke="{color}" stroke-width="2"/>')
        if title:self.text(x+20,y+36,title,23,GOLD,600)
    def line(self,x1,y1,x2,y2,color=LINE,width=2,arrow=False,dash=False):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'+(' marker-end="url(#arrow)"' if arrow else '')+(' stroke-dasharray="7 7"' if dash else '')+'/>')
    def circle(self,x,y,r,label='',color=BLUE):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{PANEL}" stroke="{color}" stroke-width="3"/>')
        if label:self.text(x,y+8,label,22,color,600,'middle')
    def foot(self,t):self.text(45,614,t,20,MUTED)
    def save(self,name):
        (DEST/(name+'.svg')).write_text(''.join(self.parts)+'</svg>')

def make():
    d=Diagram('Anatomía de GloVe','Del corpus a los conteos; de los conteos a dos tablas de vectores.')
    for x,t,a,b in [(60,'Corpus','el hielo es sólido','el vapor es gas'),(450,'Coocurrencias X','centro × contexto','solo pares observados'),(840,'Representaciones','vectores W y U','embedding: W + U')]:
        d.box(x,170,300,300,t);d.text(x+25,390,a,23);d.text(x+25,430,b,21,MUTED)
    for yy,w in [(250,170),(280,220),(310,140)]:d.line(85,yy,85+w,yy,BLUE,7)
    for i in range(4):
        for j in range(4):d.box(480+j*53,225+i*32,38,23,color=BLUE if (i+j)%3==0 else LINE)
    for i,(x,y) in enumerate([(905,260),(1070,290),(965,335)]):d.line(900,340,x,y,[BLUE,GOLD,LAV][i],4,True)
    d.line(365,315,440,315,BLUE,3,True);d.line(755,315,830,315,BLUE,3,True)
    d.text(65,540,'Objetivo: puntuación aprendida ≈ logaritmo del conteo observado',27,GOLD)
    d.foot('La estadística es global por agregación; la ventana que construye X sigue siendo local.');d.save('portada')

    d=Diagram('2.1 · Skip-gram y CBOW','Una misma oración; dos direcciones de predicción.')
    d.box(45,140,535,400,'Skip-gram · centro → contexto');d.box(620,140,535,400,'CBOW · contexto → centro')
    d.circle(170,340,60,'gato')
    for y,t in [(250,'el'),(420,'duerme')]:d.circle(445,y,68,t,GOLD);d.line(232,340,375,y,BLUE,3,True)
    d.circle(1020,340,60,'gato')
    for y,t in [(250,'el'),(420,'duerme')]:d.circle(750,y,68,t,GOLD);d.line(818,y,951,340,BLUE,3,True)
    d.foot('«el gato duerme» · el contexto excluye la palabra central; CBOW combina sus representaciones.');d.save('fig-01')

    d=Diagram('2.2 · Un corpus, dos formas de aprender','Ambos métodos incorporan evidencia de muchas ventanas del corpus.')
    for x,t in [(50,'Word2Vec'),(640,'GloVe')]:d.box(x,145,510,395,t)
    for k,y in enumerate([235,300,365]):
        d.text(75,y,['gato → duerme','gato → duerme','gato → duerme'][k],25,BLUE);d.line(290,y-8,340,y-8,BLUE,3,True)
        d.circle(380,y-8,15,'',LAV)
    d.text(75,480,'Actualizaciones a partir de ejemplos',22)
    d.text(670,250,'(gato, duerme) → x = 3',29,BLUE)
    d.line(890,280,890,345,BLUE,4,True);d.box(685,365,415,110);d.text(715,430,'Ajuste al objetivo log(3)',25)
    d.foot('Negative sampling evita el softmax completo; GloVe añade el costo de construir y guardar X.');d.save('fig-02')

    d=Diagram('2.3 · El archivo de coocurrencias','Ejemplo exacto: «el gato duerme», radio 1, peso 1 y sin cruzar oraciones.')
    labels=['el','gato','duerme'];values=[[0,1,0],[1,0,1],[0,1,0]]
    for j,l in enumerate(labels):d.text(300+j*150,190,l,23,GOLD,600,'middle')
    for i,l in enumerate(labels):
        d.text(75,265+i*90,l,24,GOLD)
        for j,v in enumerate(values[i]):d.box(230+j*150,215+i*90,140,75,color=BLUE if v else LINE);d.text(300+j*150,265+i*90,v,28,BLUE if v else MUTED,600,'middle')
    d.box(760,185,380,300,'Fila «gato»');d.text(790,270,'xᵢ = 1 + 0 + 1 = 2',26)
    d.text(790,330,'P(el | gato) = 1/2',24,BLUE);d.text(790,380,'P(duerme | gato) = 1/2',22,BLUE)
    d.text(75,545,'Fila = centro i · columna = contexto j',25)
    d.foot('Con pesos 1/distancia los conteos pueden ser fraccionarios; xᵢ suma eventos de contexto.');d.save('fig-03')

    d=Diagram('2.4 · Comparar con la misma pregunta','Cambian los centros: ice / steam. Se mantiene el contexto: solid.')
    d.circle(230,265,77,'ice',BLUE);d.circle(230,455,77,'steam',LAV)
    d.box(555,255,360,175,'Pregunta común');d.text(590,360,'¿Contexto solid?',30,GOLD)
    d.line(315,265,545,305,BLUE,3,True);d.line(315,455,545,385,BLUE,3,True)
    d.text(75,165,'Centro',24,MUTED);d.text(375,245,'1,9 × 10⁻⁴',23,BLUE);d.text(375,465,'2,2 × 10⁻⁵',23,LAV)
    d.text(640,520,'R(solid) ≈ 8,64',32,GOLD,600)
    d.foot('Cociente calculado con probabilidades redondeadas de la tabla 1 de Pennington et al. (2014).');d.save('fig-04')

    d=Diagram('2.5 · De tres palabras a una relación','Dos vectores de centro y un vector del mismo contexto.')
    d.box(55,160,490,350,'Geometría aprendida');d.text(90,250,'vᵢ = vector de ice',27,BLUE);d.text(90,305,'vⱼ = vector de steam',27,LAV)
    d.text(90,380,'uₖ = vector de solid',27,GOLD);d.text(90,455,'Δ = (vᵢ − vⱼ)ᵀuₖ',30)
    d.line(555,340,650,340,BLUE,4,True)
    d.box(665,160,480,350,'Estadística del corpus');d.text(710,260,'P(solid | ice)',30,BLUE);d.line(705,287,1080,287,GOLD,2);d.text(710,335,'P(solid | steam)',30,LAV)
    d.text(710,445,'Una relación escalar',26)
    d.foot('La diferencia de vectores contiene d componentes; el producto punto las resume en un escalar.');d.save('fig-05')

    d=Diagram('2.6 · De la diferencia al cociente','Identidad exacta: exp(a − b) = exp(a) / exp(b).')
    d.box(55,160,1090,125);d.text(600,240,'exp[(vᵢ − vⱼ)ᵀuₖ] = exp(vᵢᵀuₖ) / exp(vⱼᵀuₖ)',34,BLUE,600,'middle')
    for x,a,b,c in [(65,'Δ > 0','exp(Δ) > 1','Favorece al centro i'),(440,'Δ = 0','exp(Δ) = 1','Puntuaciones iguales'),(815,'Δ < 0','0 < exp(Δ) < 1','Favorece al centro j')]:
        d.box(x,335,320,185,a);d.text(x+20,425,b,26,GOLD);d.text(x+20,475,c,21)
    d.foot('Para el modelo final: log Rₖ ≈ (vᵢ − vⱼ)ᵀuₖ + bᵢ − bⱼ − log xᵢ + log xⱼ.');d.save('fig-06')

    d=Diagram('2.7 · Cuatro sondas para comparar','Cocientes recalculados con los valores redondeados de la tabla original.')
    headers=['Contexto k','P(k | ice)','P(k | steam)','Cociente Rₖ'];xs=[65,355,620,925]
    for x,h in zip(xs,headers):d.text(x,180,h,24,GOLD,600)
    rows=[('solid','1,9 × 10⁻⁴','2,2 × 10⁻⁵','8,64'),('gas','6,6 × 10⁻⁵','7,8 × 10⁻⁴','0,0846'),('water','3,0 × 10⁻³','2,2 × 10⁻³','1,36'),('fashion','1,7 × 10⁻⁵','1,8 × 10⁻⁵','0,944')]
    for k,row in enumerate(rows):
        y=255+k*72;d.line(60,y+25,1140,y+25)
        for x,t in zip(xs,row):d.text(x,y,t,25,BLUE if k<2 else TEXT)
    d.foot('Ratios publicados: 8,9; 0,085; 1,36; 0,96. Un ratio cercano a 1 indica poca discriminación.');d.save('fig-07')

    d=Diagram('2.8 · Vectores y sesgos','Ejemplo numérico didáctico para un solo par observado.')
    d.box(55,160,500,340,'Producto punto');d.text(85,255,'vᵢ = (1; 2)     uⱼ = (0,2; 0,4)',24,BLUE)
    d.text(85,320,'vᵢᵀuⱼ = 1 × 0,2 + 2 × 0,4',25);d.text(85,390,'= 1,0',34,GOLD,600)
    d.box(610,160,535,340,'Puntuación total');d.text(640,255,'bᵢ = 0,4        cⱼ = 0,6',26,LAV)
    d.text(640,325,'ŷᵢⱼ = 1,0 + 0,4 + 0,6 = 2,0',25)
    d.text(640,405,'Objetivo: log(xᵢⱼ)',29,GOLD)
    d.foot('El producto punto depende de normas y ángulo. Los sesgos son parámetros escalares aprendidos.');d.save('fig-08')

    d=Diagram('2.9 · De una predicción a la pérdida','Ejemplo didáctico: x = 4, xₘₐₓ = 5 y α = 0,75.')
    for x,t,a,b in [(55,'1 · Objetivo','log(4) ≈ 1,3863','ŷ = 2,0'),(440,'2 · Residual','r = 2 − 1,3863','r ≈ 0,6137'),(825,'3 · Peso','h(4) = (4/5)⁰·⁷⁵','h(4) ≈ 0,8459')]:
        d.box(x,175,320,220,t);d.text(x+20,270,a,23,BLUE);d.text(x+20,335,b,23)
    d.box(140,445,920,110);d.text(600,515,'ℓᵢⱼ = h(xᵢⱼ) rᵢⱼ² ≈ 0,8459 × 0,6137² ≈ 0,3186',29,GOLD,600,'middle')
    d.foot('La pérdida global suma estas contribuciones solo sobre pares con xᵢⱼ > 0.');d.save('fig-09')

    d=Diagram('2.10 · Ponderar sin evaluar log(0)','h(x) = min[1, (x/xₘₐₓ)ᵅ] · curva con xₘₐₓ = 5 y α = 0,75.')
    d.line(100,490,690,490,BLUE,3,True);d.line(100,490,100,180,BLUE,3,True)
    pts=' '.join(f'{100+56*x:.1f},{490-280*min(1,(x/5)**.75):.1f}' for x in [i/10 for i in range(101)])
    d.parts.append(f'<polyline points="{pts}" fill="none" stroke="{GOLD}" stroke-width="5"/>')
    d.line(380,490,380,200,MUTED,2,False,True);d.text(380,530,'5 = xₘₐₓ',22,GOLD,400,'middle');d.text(65,220,'1',23);d.text(100,530,'0',23);d.text(675,530,'x',25)
    d.box(770,175,365,340,'Orden correcto');d.text(795,265,'1. Seleccionar x > 0',24,BLUE)
    d.text(795,325,'2. Calcular log(x)',24,BLUE);d.text(795,385,'3. Aplicar h(x)',24,BLUE);d.text(795,455,'0 × log(0) no es seguro.',22,RED)
    d.foot('La saturación limita el peso a 1; no limita el residual ni garantiza gradientes pequeños.');d.save('fig-10')

    d=Diagram('2.11 · Un regulador del error','Analogía: una perilla ajusta una puntuación hasta acercarla a una marca objetivo.')
    d.line(150,350,1050,350,MUTED,5);d.line(750,280,750,420,GOLD,5);d.text(750,245,'Objetivo log(x)',27,GOLD,600,'middle')
    d.circle(350,350,24,'',BLUE);d.line(390,350,705,350,BLUE,5,True);d.text(350,455,'ŷ por debajo',26,BLUE,400,'middle')
    d.circle(980,350,24,'',LAV);d.line(940,380,790,380,BLUE,5,True);d.text(980,455,'ŷ por encima',26,LAV,400,'middle')
    d.text(600,540,'Se corrige el residual r = ŷ − log(x)',30)
    d.foot('No son resortes entre puntos: la pérdida depende del producto punto y de los sesgos.');d.save('fig-11')

    for name,number,sign in [('fig-12','2.12',-1),('fig-13','2.13',1)]:
        d=Diagram(number+' · '+('Aumentar' if sign<0 else 'Reducir')+' la puntuación','Paso de descenso simple para un par; contexto uⱼ fijo y sin reescala adaptativa.')
        d.line(145,490,640,490,MUTED,2,True);d.line(145,490,145,175,MUTED,2,True)
        d.line(145,490,520,280,GOLD,4,True);d.text(545,275,'uⱼ',30,GOLD)
        d.line(145,490,300,280,BLUE,4,True);d.text(280,250,'vᵢ',28,BLUE)
        ex,ey=(450,196) if sign<0 else (205,333)
        d.line(300,280,ex,ey,BLUE,5,True);d.text(ex+8,ey-15,'vᵢ nuevo',24,LAV)
        d.box(720,170,420,345,'Residual '+('negativo' if sign<0 else 'positivo'))
        d.text(745,270,'r < 0' if sign<0 else 'r > 0',33,BLUE)
        d.text(745,340,'Δvᵢ = −2η h(x) r uⱼ',26)
        d.text(745,410,'Dirección: +uⱼ' if sign<0 else 'Dirección: −uⱼ',28,GOLD)
        d.foot('El cambio del producto punto es −2η h(x) r ‖uⱼ‖²; cambia su signo con r.');d.save(name)

    d=Diagram('2.14 · Peso y residual son factores distintos','El peso modula una contribución; no es una garantía de estabilidad global.')
    for x,t,weight,r in [(65,'Par A · peso pequeño',.2,2),(645,'Par B · peso saturado',1,2)]:
        d.box(x,165,490,330,t);d.text(x+30,255,f'h(x) = {weight:g}      r = {r}',28,BLUE)
        d.text(x+30,325,f'|2 h(x) r| = {2*weight*r:g}',29,GOLD)
        d.line(x+35,405,x+35+100*weight*2,405,BLUE,4,True)
    d.text(600,550,'Si r = 0, el gradiente de ese par es cero.',29,TEXT,500,'middle')
    d.foot('Otros pares aún modifican los parámetros compartidos; h(x) = 1 no limita el valor de r.');d.save('fig-14')

    d=Diagram('2.15 · Del residual al paso de AdaGrad','Primero se acumula el gradiente; después el optimizador calcula la actualización.')
    for x,t,a,b in [(55,'Peso','h(xᵢⱼ)','cuánto pondera'),(440,'Residual','rᵢⱼ','error con signo'),(825,'Dirección','uⱼ','vector de contexto')]:
        d.box(x,160,320,185,t);d.text(x+160,260,a,33,BLUE,600,'middle');d.text(x+160,315,b,22,TEXT,400,'middle')
    d.text(600,400,'gᵢ = 2 Σⱼ: xᵢⱼ > 0 h(xᵢⱼ) rᵢⱼ uⱼ',32,GOLD,500,'middle')
    d.box(75,450,1050,110);d.text(600,495,'Gₜ = Gₜ₋₁ + gₜ ⊙ gₜ',28,LAV,400,'middle')
    d.text(600,535,'θₜ₊₁ = θₜ − η gₜ / (√Gₜ + ε)',28,BLUE,400,'middle')
    d.foot('Operaciones por coordenada. Una coordenada con menor acumulado conserva una tasa efectiva mayor.');d.save('fig-15')

    d=Diagram('2.16 · Dos roles, una representación de salida','Una misma palabra tiene una fila como centro y otra como contexto.')
    for x,t,vals,col in [(65,'W · centros',[.2,.5,-.1],BLUE),(455,'U · contextos',[.3,-.1,.4],LAV),(845,'E = W + U',[.5,.4,.3],GOLD)]:
        d.box(x,175,290,330,t)
        for j,val in enumerate(vals):
            d.text(x+30,285+j*70,f'{val:+.1f}',27,col)
            d.line(x+190,250+j*70,x+190,292+j*70,MUTED,1)
            d.line(x+190,275+j*70,x+190+100*val,275+j*70,col,8)
    d.text(405,360,'+',42,GOLD,600,'middle');d.text(795,360,'=',42,GOLD,600,'middle')
    d.foot('La simetría de X no obliga a W = U. Sumar es una elección de extracción, no una restricción.');d.save('fig-16')

if __name__=='__main__':make()
