"""Diagramas específicos y verificables para la clase 02 de Word2Vec.

Genera SVG nativos, reemplaza las figuras y ajusta sus explicaciones.
Los ejemplos numéricos son ilustrativos; no representan un entrenamiento.
"""
from pathlib import Path
import copy, hashlib, html, json, math
from bs4 import BeautifulSoup
from editorial import render

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/'docs/nlp/clase-02-1-introduccion-al-nlp-parte-1-word2vec.html'
OUT=ROOT/'docs/assets/figures/word2vec'
BG='#111318'; PANEL='#191d26'; LINE='#414a5d'; TEXT='#e5e7eb'
BLUE='#91b9e3'; GOLD='#d9c58f'; PURPLE='#b8a5ee'; GREEN='#a9cbb5'; RED='#e6a09d'; MUTED='#a8b0c1'
WORDS=['the','man','loves','his','son']

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def softmax(scores):
    exps=[math.exp(s-max(scores)) for s in scores]
    return [x/sum(exps) for x in exps]
def loss(v,u,target):
    scores=[dot(row,v) for row in u];m=max(scores)
    return m+math.log(sum(math.exp(s-m) for s in scores))-scores[target]
def grad(v,u,target):
    p=softmax([dot(row,v) for row in u])
    return [sum(p[j]*u[j][k] for j in range(len(u)))-u[target][k] for k in range(len(v))]

U=[[1.,0.],[0.,1.],[-1.,0.]]
PROBS=softmax([1.,0.,-1.])
START=[.2,.4];G=grad(START,U,0);END=[START[k]-.5*G[k] for k in range(2)]
P_START=softmax([dot(row,START) for row in U])
EXPECTED=[sum(P_START[j]*U[j][k] for j in range(3)) for k in range(2)]
CONTEXT=[[1.,0.],[0.,1.],[1.,1.],[2.,0.]]
MEAN=[sum(v[k] for v in CONTEXT)/4 for k in range(2)]
CBOW_U=[[1.,1.],[1.,0.],[0.,1.],[-1.,0.],[0.,-1.]]
CBOW_WORDS=['loves','the','man','his','son']
CBOW_SCORES=[dot(v,MEAN) for v in CBOW_U]
CBOW_P=softmax(CBOW_SCORES)
CBOW_G=grad(MEAN,CBOW_U,0)

def fmt(v,n=3):return f'{v:.{n}f}'.replace('-', '−')
def vector(v):return '('+', '.join(fmt(x) for x in v)+')'

class Drawing:
    """Primitivas SVG con texto accesible, proporciones y flechas explícitas."""
    def __init__(self,title,note='',height=620):
        self.height=height
        self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 {height}" role="img" aria-labelledby="title desc">',
            '<title id="title">'+html.escape(title)+'</title><desc id="desc">'+html.escape(note)+'</desc>',
            '<defs>'+''.join(f'<marker id="{name}" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0,0 L9,4.5 L0,9 Z" fill="{color}"/></marker>' for name,color in [('blue',BLUE),('gold',GOLD),('purple',PURPLE),('red',RED),('green',GREEN)])+'</defs>',
            f'<rect width="1040" height="{height}" rx="16" fill="{BG}"/>']
        self.text(38,49,title,30,GOLD,weight=650)
        self.line(38,73,1002,73)
        if note:self.text(38,height-24,note,18,MUTED)
    def text(self,x,y,value,size=23,color=TEXT,anchor='start',weight=400):
        self.parts.append(f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" font-family="DejaVu Sans,Arial,sans-serif">{html.escape(str(value))}</text>')
    def lines(self,x,y,values,size=22,color=TEXT,gap=32):
        for i,v in enumerate(values):self.text(x,y+i*gap,v,size,color)
    def rect(self,x,y,w,h,fill=PANEL,stroke=LINE,rx=9):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    def line(self,x1,y1,x2,y2,color=LINE,width=2,dash=False):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="7 6"' if dash else '')+'/>')
    def arrow(self,x1,y1,x2,y2,color='blue',width=3):
        colors={'blue':BLUE,'gold':GOLD,'purple':PURPLE,'red':RED,'green':GREEN}
        self.parts.append(f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{colors[color]}" stroke-width="{width}" marker-end="url(#{color})"/>')
    def circle(self,x,y,r=6,color=BLUE):self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{color}"/>')
    def node(self,x,y,w,h,label,color=BLUE,size=24):
        self.rect(x,y,w,h,stroke=color);self.text(x+w/2,y+h/2+size*.35,label,size,color,'middle')
    def matrix(self,x,y,rows,labels=None,cell=57,selected=None):
        for i,row in enumerate(rows):
            if labels:self.text(x-14,y+i*cell+cell*.66,labels[i],20,MUTED,'end')
            for j,value in enumerate(row):
                fill='#38334c' if i==selected else PANEL
                self.rect(x+j*cell,y+i*cell,cell-3,cell-3,fill,PURPLE if i==selected else LINE,3)
                self.text(x+j*cell+cell/2,y+i*cell+cell*.65,str(value),23,PURPLE if i==selected else TEXT,'middle')
    def bars(self,x,y,labels,values,width=300,scale=1,color=BLUE,step=65):
        for i,(label,value) in enumerate(zip(labels,values)):
            yy=y+i*step;self.text(x-15,yy+23,label,22,TEXT,'end')
            self.rect(x,yy,width,32,fill=PANEL,rx=3)
            if value>0:self.rect(x,yy,width*value/scale,32,fill=color,stroke=color,rx=3)
            self.text(x+width+12,yy+23,fmt(value),20,TEXT)
    def plane(self,x,y,size,low,high):
        def pos(v):return (x+(v[0]-low)/(high-low)*size,y+size-(v[1]-low)/(high-low)*size)
        for k in range(math.ceil(low),math.floor(high)+1):
            a,b=pos((k,low)),pos((k,high));self.line(*a,*b)
            a,b=pos((low,k)),pos((high,k));self.line(*a,*b)
        a,b=pos((low,0)),pos((high,0));self.line(*a,*b,MUTED)
        a,b=pos((0,low)),pos((0,high));self.line(*a,*b,MUTED)
        ox,oy=pos((0,0));self.text(ox-10,oy+25,'0',18,MUTED)
        self.text(x+size+10,oy+8,'x',19,MUTED);self.text(ox+8,y-10,'y',19,MUTED)
        return pos
    def window(self,y,center,masked=False):
        for j,word in enumerate(WORDS):
            color=GOLD if j==center else BLUE if abs(j-center)<=2 else MUTED
            self.node(65+j*185,y,165,72,'?' if masked and j==center else word,color,29)
            self.text(147+j*185,y+101,str(j),18,MUTED,'middle')
    def save(self,name):
        path=OUT/name;path.write_text(''.join(self.parts)+'</svg>');return path

FIGURES=[]
def figure(number,cell,caption_cell,source,title,caption,explanation,note='',height=620):
    d=Drawing(title,note,height)
    FIGURES.append({'number':number,'cell':cell,'caption_cell':caption_cell,'original_image':source,
                    'file':f'fig-1-{number:02d}.svg','title':title,'caption':caption,'explanation':explanation})
    return d

def generate():
    OUT.mkdir(parents=True,exist_ok=True);FIGURES.clear()
    d=figure(2,18,19,'a1.png','One-hot: del token al vector aprendido',
        'El one-hot selecciona una fila de la tabla de embeddings.',
        'Cada fila de la matriz de la izquierda identifica un token distinto. El índice de «gato» selecciona la segunda fila de $E$; el resultado es un vector de dos componentes, no un indicador ortogonal. Los valores de $E$ son ilustrativos. La consulta $E[i]$ evita construir explícitamente el one-hot.',
        'Ejemplo ilustrativo: N = 4 tokens; d = 2 componentes.')
    d.text(110,120,'Indicadores: matriz identidad',25,BLUE);d.matrix(160,160,[[int(i==j) for j in range(4)] for i in range(4)],['perro','gato','coche','manzana'],selected=1)
    d.arrow(420,258,550,258,'gold');d.text(485,232,'índice 1',20,GOLD,'middle')
    d.text(630,120,'Tabla E',25,PURPLE);d.matrix(650,160,[[.4,.1],[.3,.2],[-.2,.8],[.1,-.5]],['perro','gato','coche','manzana'],selected=1,cell=57)
    d.node(580,450,355,68,'E[1] = (0.3, 0.2)',PURPLE);d.arrow(707,397,707,442,'purple');d.text(110,493,'e₁ = (0, 1, 0, 0)',25,BLUE);d.save(FIGURES[-1]['file'])

    d=figure(3,21,22,'a2.png','One-hot: todas las parejas distintas empatan',
        'Los indicadores distintos tienen coseno 0 y distancia √2.',
        'La diagonal de la matriz vale 1 porque cada indicador se compara consigo mismo. Fuera de la diagonal, todos los cosenos valen 0; las tres barras muestran la misma distancia. Esta geometría no expresa relaciones lingüísticas. Una transformación aprendida posterior sí puede distinguirlas.')
    d.text(120,128,'Matriz de cosenos',26,BLUE);d.matrix(165,185,[[1,0,0],[0,1,0],[0,0,1]],['perro','gato','coche'],cell=80)
    for j,t in enumerate(['perro','gato','coche']):d.text(205+j*80,165,t,19,MUTED,'middle')
    d.text(590,128,'Distancia entre indicadores',25,GOLD)
    d.bars(680,205,['perro / gato','perro / coche','gato / coche'],[math.sqrt(2)]*3,width=225,scale=2,color=GOLD,step=90)
    d.text(680,505,'Todas: √2 ≈ 1.414',24,GOLD);d.save(FIGURES[-1]['file'])

    d=figure(4,25,26,'a3.png','Coseno: comparar dirección, no longitud',
        'Escalar positivamente un vector conserva su dirección y su coseno.',
        'A la izquierda, $x=(2,2)$ e $y=(4,4)$ tienen longitudes distintas. Al dividir cada vector por su norma, ambos terminan en el mismo punto de la circunferencia unidad. Por eso su coseno vale 1. Esto describe una igualdad de direcciones; la interpretación semántica requiere un modelo y una tarea.',
        'En cada plano, x e y usan la misma escala.')
    d.text(80,120,'Vectores originales',25,BLUE);p=d.plane(90,160,350,0,4.5)
    d.arrow(*p((0,0)),*p((4,4)),'gold',4);d.arrow(*p((0,0)),*p((2,2)),'blue',5)
    d.text(*p((2.1,1.6)),'x',27,BLUE);d.text(*p((3.4,4.15)),'y',27,GOLD)
    d.arrow(465,320,555,320,'purple');d.text(510,285,'÷ norma',19,PURPLE,'middle')
    d.text(625,120,'Vectores unitarios',25,PURPLE);p=d.plane(615,160,300,0,1.15);q=1/math.sqrt(2)
    d.arrow(*p((0,0)),*p((q,q)),'purple',5);d.text(625,510,'x / ‖x‖ = y / ‖y‖',24,PURPLE);d.text(625,550,'cos(x, y) = 1',26,GOLD);d.save(FIGURES[-1]['file'])

    d=figure(5,28,29,'a4.png','Tres relaciones geométricas del coseno',
        'Coseno 1, 0 y −1: misma dirección, ortogonalidad y oposición.',
        'Cada panel compara dos vectores no nulos de la misma longitud. El ángulo determina el coseno indicado. Los rótulos describen geometría: no deben sustituirse por «sinónimos», «sin relación» y «antónimos». En particular, compartir contextos puede acercar palabras con significados opuestos.')
    for i,(angle,label,value) in enumerate([(0,'Misma dirección','1'),(90,'Ortogonalidad','0'),(180,'Dirección opuesta','−1')]):
        x=185+i*335;y=315;d.text(x,135,label,23,TEXT,'middle');d.line(x-110,y,x+115,y);d.line(x,y-115,x,y+110)
        d.arrow(x,y,x+100,y,'blue',6);r=math.radians(angle);d.arrow(x,y,x+100*math.cos(r),y-100*math.sin(r),'gold',3)
        d.text(x,485,f'θ = {angle}°',26,TEXT,'middle');d.text(x,530,'cos θ = '+value,29,GOLD,'middle')
    d.save(FIGURES[-1]['file'])

    d=figure(6,31,32,'a5.png','Búsqueda por coseno: un ranking ilustrativo',
        'Las coordenadas definen el ranking; los nombres no prueban una relación semántica.',
        'La consulta apunta hacia $(1,0)$. Todos los candidatos tienen norma 1: su coordenada horizontal coincide aquí con su coseno respecto a la consulta. El orden obtenido es 0.8, 0 y −0.6. Son coordenadas construidas para explicar el cálculo, no resultados aprendidos ni garantías sobre esas palabras.',
        'Coordenadas sintéticas; no son embeddings entrenados.')
    p=d.plane(90,160,390,-1.2,1.2)
    for v,label,color,dy in [((1,0),'consulta: perro','gold',-15),((.8,.6),'gato','blue',-15),((0,1),'manzana','purple',-10),((-.6,.8),'nube','green',-15)]:
        d.arrow(*p((0,0)),*p(v),color,3);x,y=p(v)
        if label.startswith('consulta'):d.text(x-15,y+40,label,20,GOLD,'end')
        else:d.text(x-5,y+dy,label,20,dict(gold=GOLD,blue=BLUE,purple=PURPLE,green=GREEN)[color])
    d.text(630,140,'Coseno con la consulta',25,GOLD)
    # Barras centradas en cero para distinguir valores positivos y negativos.
    x0=785;d.line(x0,190,x0,500,MUTED)
    for i,(name,v) in enumerate([('gato',.8),('manzana',0),('nube',-.6)]):
        y=220+i*105;d.text(600,y+23,name,23);d.rect(min(x0,x0+v*170),y,max(2,abs(v)*170),34,BLUE,BLUE,3);d.text(1000,y+23,fmt(v),20,TEXT,'end')
    d.save(FIGURES[-1]['file'])

    d=figure(7,34,35,'a6.png','Dos direcciones de predicción',
        'Skip-gram parte del centro; CBOW combina los contextos.',
        'En Skip-gram se forman pares entre «loves» y cada vecino. En CBOW se reúnen los cuatro vecinos para predecir la palabra central. Las flechas indican qué dato entra y qué objetivo se predice. No representan una causalidad del lenguaje ni aseguran que el contexto determine una única palabra.')
    d.text(260,130,'Skip-gram',29,BLUE,'middle');d.text(780,130,'CBOW',29,PURPLE,'middle')
    d.node(55,280,155,75,'loves',GOLD)
    for i,w in enumerate(['the','man','his','son']):
        y=170+i*95;d.node(340,y,130,60,w,BLUE);d.arrow(215,317,332,y+30,'blue')
        d.node(555,y,130,60,w,BLUE);d.arrow(690,y+30,825,317,'purple')
    d.node(835,280,150,75,'loves',GOLD);d.text(260,555,'centro → vecinos',24,BLUE,'middle');d.text(780,555,'vecinos → centro',24,PURPLE,'middle');d.save(FIGURES[-1]['file'])

    d=figure(8,38,39,'a8.png','La ventana avanza y respeta los bordes',
        'Radio m = 2: cuatro vecinos en el centro y tres junto al borde.',
        'La fila superior centra la ventana en «loves»: se usan los índices 0, 1, 3 y 4. Al avanzar a «his», solo quedan los índices 1, 2 y 4 dentro de la secuencia. El centro se excluye siempre. El radio $m=2$ permite hasta $2m$ contextos, no exige que existan cuatro en todos los casos.')
    d.text(65,126,'Centro = loves · contextos = 4',25,GOLD);d.window(165,2)
    d.arrow(505,295,690,330,'purple');d.text(550,285,'+1 posición',20,PURPLE)
    d.text(65,375,'Centro = his · contextos = 3',25,GOLD);d.window(410,3);d.save(FIGURES[-1]['file'])

    d=figure(9,43,44,'a9.png','Skip-gram: un centro, varios objetivos',
        'Cada flecha representa un par centro–contexto observado.',
        '«Loves» proporciona la entrada compartida. Las cuatro salidas son objetivos de entrenamiento distintos: «the», «man», «his» y «son». La distribución de candidatos se calcula a partir del mismo centro. Observar varios vecinos no obliga a que una sola salida softmax los convierta simultáneamente en una etiqueta one-hot.')
    d.node(80,255,210,100,'loves',GOLD,34)
    for i,w in enumerate(['the','man','his','son']):
        y=100+i*110;d.rect(740,y,240,90,stroke=BLUE);d.text(860,y+32,w,29,BLUE,'middle');d.text(860,y+69,f'P({w} | loves)',21,PURPLE,'middle');d.arrow(300,305,725,y+45,'blue')
    d.save(FIGURES[-1]['file'])

    d=figure(10,46,47,'a10.png','De una ventana a cuatro pares positivos',
        'La posición central no forma un par consigo misma.',
        'La fila superior conserva el orden del texto. La tabla inferior enumera los cuatro ejemplos positivos que salen de esa ventana: el centro se repite y cambia el objetivo. Los índices corresponden a este vocabulario de cinco tokens; no son distancias ni puntuaciones del modelo.')
    d.window(120,2);d.text(170,285,'Entrada: índice central',23,GOLD);d.text(610,285,'Objetivo: índice de contexto',23,BLUE)
    for i,(j,w) in enumerate([(0,'the'),(1,'man'),(3,'his'),(4,'son')]):
        y=310+i*56;d.node(150,y,250,44,'2 · loves',GOLD,22);d.arrow(420,y+22,580,y+22,'purple');d.node(600,y,280,44,f'{j} · {w}',BLUE,22)
    d.save(FIGURES[-1]['file'])

    d=figure(11,49,50,'a11.png','La independencia condicional es una hipótesis',
        'El modelo factoriza la verosimilitud del contexto dado el centro.',
        'Con el centro fijado, el modelo multiplica las probabilidades asignadas a los vecinos observados. Los cuatro valores del ejemplo dejan probabilidad para otros candidatos y su producto vale 0.0009. La factorización es una decisión del modelo: no afirma que las palabras del lenguaje sean independientes.',
        'Probabilidades ilustrativas; las cuatro no agotan el vocabulario.')
    d.node(370,110,300,65,'centro: loves',GOLD)
    for i,(w,p) in enumerate(zip(['the','man','his','son'],[.15,.2,.1,.3])):
        x=50+i*255;d.arrow(520,182,x+105,260,'blue');d.node(x,275,210,70,w,BLUE,28);d.text(x+105,390,fmt(p,2),30,PURPLE,'middle')
    d.text(520,490,'0.15 × 0.20 × 0.10 × 0.30 = 0.0009',30,GOLD,'middle');d.save(FIGURES[-1]['file'])

    d=figure(12,52,53,'a12.png','Skip-gram: vectores → scores → probabilidades',
        'El softmax completo normaliza sobre los tres tokens del ejemplo.',
        'Se fija $v_c=(1,0)$ para «loves». Los vectores de salida de «man», «loves» y «son» son $(1,0)$, $(0,1)$ y $(-1,0)$: sus productos punto valen 1, 0 y −1. Tras exponenciar y normalizar se obtiene aproximadamente 0.665, 0.245 y 0.090. Este es un ejemplo independiente de las ventanas anteriores.',
        'Ejemplo numérico independiente con vocabulario {man, loves, son}.')
    d.node(40,130,240,78,'v_c = (1, 0)',GOLD);d.arrow(290,170,375,170,'purple');d.node(390,130,250,78,'scores = U v_c',PURPLE,25)
    d.text(100,290,'Salida U',25,BLUE);d.matrix(100,325,[[1,0],[0,1],[-1,0]],['man','loves','son'],cell=58)
    d.text(400,290,'scores',25,PURPLE);d.matrix(420,325,[[1],[0],[-1]],cell=58)
    d.arrow(500,410,605,410,'purple');d.text(700,285,'softmax',27,GOLD)
    d.bars(715,325,['man','loves','son'],PROBS,width=190,color=BLUE,step=75);d.save(FIGURES[-1]['file'])

    d=figure(13,56,57,'a13.png','Un mayor score no implica un menor ángulo',
        'El producto punto depende de la dirección y de las normas.',
        'Con $v_c=(1,0)$, el candidato A tiene norma 1 y ángulo 0°: su score es 1. El candidato B tiene norma 3 y ángulo 60°: su score es 1.5, aunque su coseno es menor. El numerador usa la exponencial de ese score. Por tanto, ordenar por producto punto no equivale a ordenar por coseno.',
        'A = (1, 0); B = (1.5, √6.75); v_c = (1, 0).')
    p=d.plane(80,150,370,0,3);d.arrow(*p((0,0)),*p((1,0)),'gold',6);d.arrow(*p((0,0)),*p((1.5,math.sqrt(6.75))))
    x,y=p((1,0));d.text(x-20,y-18,'A = v_c',23,GOLD);x,y=p((1.5,math.sqrt(6.75)));d.text(x+12,y,'B',25,BLUE)
    d.text(600,135,'Candidato',22,MUTED);d.text(760,135,'coseno',22,MUTED);d.text(925,135,'score',22,MUTED)
    for y,name,co,sc in [(240,'A','1.0','1.0'),(345,'B','0.5','1.5')]:
        d.node(590,y-40,105,65,name);d.text(790,y,co,32,BLUE,'middle');d.text(950,y,sc,32,GOLD,'middle')
    d.text(610,465,'exp(1.5) > exp(1.0)',27,PURPLE);d.save(FIGURES[-1]['file'])

    d=figure(14,59,60,'a14.png','El denominador reúne a todos los candidatos',
        'Z suma pesos positivos y los convierte en una distribución.',
        r'Los pesos $e^1$, $e^0$ y $e^{-1}$ suman $Z\approx4.086$. Dividir cada uno por esa misma suma produce el reparto inferior, cuya suma es 1. El denominador incluye también el candidato observado y todos los demás tokens del vocabulario, incluido «loves». Negative sampling usa un objetivo distinto.',
        'Mismo ejemplo de tres tokens que en la Fig. 1.12.')
    d.text(120,125,'Pesos antes de normalizar',25,BLUE)
    d.bars(200,170,['man','loves','son'],[math.exp(1),1,math.exp(-1)],width=280,scale=3,color=BLUE,step=70)
    d.node(650,210,310,90,'Z = '+fmt(sum(math.exp(x) for x in [1,0,-1])),GOLD,30);d.arrow(565,265,630,255,'gold')
    x=75
    for w,p,color in zip(['man','loves','son'],PROBS,[BLUE,PURPLE,GREEN]):
        d.rect(x,440,890*p,65,color,color,0);d.text(x+890*p/2,480,w,21,BG,'middle',650);x+=890*p
    d.text(520,550,'Σ p_j = 1',30,GOLD,'middle');d.save(FIGURES[-1]['file'])

    d=figure(15,64,65,'a15.png','Verosimilitud: recorrer los pares del corpus',
        'La productoria es una verosimilitud del modelo, no una pérdida.',
        r'Este corpus de tres tokens y radio 1 produce cuatro pares: uno en cada borde y dos en el centro. Los valores se agrupan por la posición central y después se multiplican: $\mathcal{L}=0.2(0.3\cdot0.4)0.5=0.012$. Maximizar esa verosimilitud equivale a minimizar su logaritmo negativo.',
        'Corpus ilustrativo: [the, man, loves]; radio m = 1.')
    for i,(center,context,p) in enumerate([('the','man','0.20'),('man','the, loves','0.30 × 0.40'),('loves','man','0.50')]):
        y=140+i*115;d.node(55,y,170,65,center,GOLD);d.arrow(235,y+32,325,y+32);d.node(340,y,250,65,context,BLUE);d.text(665,y+42,p,29,PURPLE)
    d.text(520,545,'ℒ = 0.20 × (0.30 × 0.40) × 0.50 = 0.012',29,GOLD,'middle');d.save(FIGURES[-1]['file'])

    d=figure(16,68,69,'a16.png','Del producto de probabilidades a la suma de pérdidas',
        'El logaritmo negativo convierte los cuatro factores en cuatro sumandos.',
        r'Cada flecha aplica $-\log$ a una probabilidad. La fila inferior suma aproximadamente 1.609 + 1.204 + 0.916 + 0.693 = 4.423. Es el mismo objetivo que $-\log(0.012)$. Para el cálculo estable se trabaja con log-softmax o log-sum-exp, sin formar primero una productoria minúscula.',
        'Se usa logaritmo natural; redondeo a tres decimales.')
    values=[.2,.3,.4,.5]
    for i,p in enumerate(values):
        x=45+i*255;d.node(x,140,205,75,fmt(p,2),BLUE,32);d.arrow(x+102,230,x+102,325,'gold');d.text(x+102,285,'−log',24,GOLD,'middle');d.node(x,340,205,75,fmt(-math.log(p)),PURPLE,32)
    d.text(520,520,'L = −log ℒ = '+fmt(-math.log(math.prod(values))),33,GOLD,'middle');d.save(FIGURES[-1]['file'])

    d=figure(17,72,73,'a17.png','Un paso de descenso del gradiente',
        'Se resta el gradiente de la pérdida, manteniendo U fijo en este ejemplo.',
        rf'El punto inicial es {vector(START)} y el gradiente de la pérdida es {vector(G)}. Con una tasa $\eta=0.5$, el paso termina en {vector(END)}. Las barras muestran la pérdida calculada antes y después. La flecha de actualización va en sentido opuesto al gradiente; no representa una fuerza física ni asegura descenso para cualquier tasa.',
        'Ejemplo numérico: U = [(1,0), (0,1), (−1,0)]; objetivo = fila 0.')
    p=d.plane(75,150,390,-.8,1.2);a=p(START);b=p(END);op=p([START[k]+.5*G[k] for k in range(2)])
    d.arrow(*a,*op,'red',3);d.arrow(*a,*b,'gold',5);d.circle(*a,7,BLUE);d.circle(*b,7,GOLD)
    d.text(a[0]+12,a[1]+25,'v inicial',21,BLUE);d.text(b[0]+10,b[1]+22,'v actualizado',21,GOLD);d.text(op[0]-10,op[1]-12,'+ η∇L',21,RED)
    d.text(650,145,'Pérdida del par',27,GOLD)
    d.bars(660,245,['antes','después'],[loss(START,U,0),loss(END,U,0)],width=230,scale=1.5,color=PURPLE,step=115);d.save(FIGURES[-1]['file'])

    d=figure(18,75,76,'a18.png','El gradiente como diferencia de vectores',
        'Gradiente de L = esperado bajo p − vector del objetivo.',
        rf'La flecha dorada es el vector observado $u_o=(1,0)$. La azul representa el promedio ponderado $\sum_jp_j u_j={vector(EXPECTED)}$. La flecha entre sus puntas es su diferencia, $\nabla L={vector(G)}$. Para la log-verosimilitud, el signo se invierte. La suma recorre todo el vocabulario, incluido el objetivo.',
        'Mismos U y v inicial que en la Fig. 1.17; valores calculados con softmax.')
    p=d.plane(80,160,390,-.6,1.3);o=p((0,0));a=p(U[0]);b=p(EXPECTED)
    d.arrow(*o,*a,'gold',5);d.arrow(*o,*b,'blue',5);d.arrow(*a,*b,'red',4)
    d.text(a[0]-30,a[1]+35,'u_o',24,GOLD);d.text(b[0]+12,b[1]-18,'Σ p_j u_j',22,BLUE);d.text(370,200,'∇L',25,RED)
    d.text(635,155,'Probabilidades actuales',24,PURPLE)
    d.bars(715,210,['fila 0','fila 1','fila 2'],P_START,width=185,color=PURPLE,step=75)
    d.text(600,500,'∇ℓ = −∇L',30,GOLD);d.save(FIGURES[-1]['file'])

    d=figure(19,100,101,'c2.png','Dos arquitecturas: entradas y tablas aprendidas',
        'Ambas usan tablas de entrada y salida; cambia cómo se construye el predictor.',
        r'En Skip-gram se consulta una fila de $V$ para el centro y se calculan $U v_c$. En CBOW se consultan las filas de los vecinos y se promedian antes de calcular $U\bar v$. Las tablas $V$ y $U$ tienen forma $N\times d$; las puntuaciones tienen $N$ componentes. Aquí $v$ nombra vectores de entrada y $u$ vectores de salida en ambas rutas.')
    for y,label,inp,lookup,predict,color in [(165,'Skip-gram','índice c','V[c] → v_c','U v_c','blue'),(370,'CBOW','C índices','media de V[ids]','U v̄','purple')]:
        co=BLUE if color=='blue' else PURPLE;d.text(55,y-30,label,27,co)
        for x,w,t in [(55,190,inp),(340,300,lookup),(750,220,predict)]:d.node(x,y,w,85,t,co,24)
        d.arrow(255,y+42,325,y+42,color);d.arrow(652,y+42,735,y+42,color)
        d.text(855,y+125,'N scores → softmax',21,GOLD,'middle')
    d.save(FIGURES[-1]['file'])

    d=figure(20,103,104,'c3.png','CBOW: ocultar el centro, conservar sus vecinos',
        'El token objetivo se excluye de los datos de entrada.',
        'Los cuatro tokens azules son la entrada. El hueco dorado marca la posición cuyo token se debe predecir: «loves». Al avanzar la ventana se repite el mismo procedimiento con un nuevo centro. La cantidad $C$ de vecinos disponibles puede disminuir junto a los extremos de la secuencia.')
    d.window(145,2,True)
    for j in [0,1,3,4]:d.arrow(147+j*185,230,520,360,'blue')
    d.node(320,375,400,80,'contexto: the, man, his, son',BLUE,24);d.arrow(520,465,520,500,'gold');d.text(520,545,'objetivo: loves',30,GOLD,'middle');d.save(FIGURES[-1]['file'])

    d=figure(21,106,107,'c4.png','CBOW: sumar y dividir por la cantidad real',
        'Cuatro vectores de entrada producen el promedio (1, 0.5).',
        'Las filas ilustrativas suman $(4,2)$; dividir por $C=4$ da $(1,0.5)$. El punto dorado queda dentro de la región convexa de los cuatro vectores. Promediar combina componentes, pero no garantiza un «significado central» perfecto. Si el borde deja tres vecinos, el divisor pasa a ser 3.',
        'Vectores ilustrativos de the, man, his y son; no resultados entrenados.')
    d.matrix(150,140,[[1,0],[0,1],[1,1],[2,0]],['the','man','his','son'],cell=65)
    d.node(95,450,330,65,'(4, 2) / 4 = (1, 0.5)',GOLD,25)
    p=d.plane(590,160,350,-.3,2.3)
    for v,name in zip(CONTEXT,['the','man','his','son']):
        d.arrow(*p((0,0)),*p(v),'blue',2);x,y=p(v);d.text(x+8,y-12,name,20,BLUE)
    x,y=p(MEAN);d.circle(x,y,10,GOLD);d.text(x+15,y+25,'media',23,GOLD);d.save(FIGURES[-1]['file'])

    d=figure(22,109,110,'c5.png','CBOW: puntuar todas las palabras candidatas',
        'El promedio se compara con cinco vectores de salida y se normaliza.',
        r'Se usa $\bar v=(1,0.5)$ y, en el orden mostrado, $U=[(1,1),(1,0),(0,1),(-1,0),(0,-1)]$. Los scores son 1.5, 1, 0.5, −1 y −0.5. El softmax da las probabilidades dibujadas. «Loves» es el máximo en este ejemplo, pero recibe una probabilidad menor que 1.',
        'Vocabulario: the, man, loves, his, son; contexto de la Fig. 1.21.')
    d.node(45,150,310,80,'v̄ = (1, 0.5)',GOLD,28);d.arrow(365,190,505,190,'purple');d.text(430,165,'U v̄',24,PURPLE,'middle')
    d.text(630,115,'p(candidato | contexto)',25,BLUE)
    d.bars(680,155,CBOW_WORDS,CBOW_P,width=220,color=BLUE,step=70)
    d.lines(70,335,['scores:', '(1.5, 1, 0.5, −1, −0.5)', 'exp → suma → división'],23,PURPLE,45);d.save(FIGURES[-1]['file'])

    d=figure(23,113,114,'c6.png','CBOW: objetivo one-hot y predicción softmax',
        'La pérdida usa la probabilidad del centro observado.',
        rf'La etiqueta señala una sola palabra central: «loves». La distribución predicha reparte masa entre los cinco candidatos y asigna al objetivo aproximadamente {fmt(CBOW_P[0])}. La pérdida de esta ventana es $L=-\log p_c\approx{fmt(-math.log(CBOW_P[0]))}$. La etiqueta one-hot no obliga a que los ceros y el uno aparezcan exactamente en la salida softmax con logits finitos.',
        'Misma distribución que en la Fig. 1.22.')
    d.text(230,135,'Etiqueta objetivo',27,GOLD,'middle');d.text(760,135,'Predicción del modelo',27,BLUE,'middle')
    d.bars(165,190,CBOW_WORDS,[1,0,0,0,0],width=230,color=GOLD,step=62)
    d.bars(690,190,CBOW_WORDS,CBOW_P,width=230,color=BLUE,step=62)
    d.text(520,550,'L = −log p(loves | contexto) = '+fmt(-math.log(CBOW_P[0])),27,PURPLE,'middle');d.save(FIGURES[-1]['file'])

    d=figure(24,118,119,'c7.png','CBOW: repartir el gradiente del promedio',
        'Cada aparición recibe 1/C del gradiente que llega al vector promedio.',
        rf'Para el ejemplo anterior, $\nabla_{{\bar v}}L={vector(CBOW_G)}$. Como $C=4$, cada aparición recibe {vector([v/4 for v in CBOW_G])}. El Jacobiano del promedio respecto de cada entrada es $I_d/C$. Si un token aparece varias veces, su fila compartida acumula las contribuciones de todas sus apariciones. Para maximizar la log-verosimilitud se usa el signo opuesto.',
        'Gradientes de la pérdida negativa; U se mantiene fijo en este cálculo.')
    d.node(245,110,550,75,'∇L respecto de v̄ = '+vector(CBOW_G),GOLD,25)
    d.arrow(520,195,520,245,'purple');d.node(370,260,300,65,'Jacobiano: I / 4',PURPLE,27)
    for j,name in enumerate(['the','man','his','son']):
        x=35+j*255;d.arrow(520,335,x+100,400,'blue');d.node(x,415,220,65,'∇v_'+name,BLUE,23);d.text(x+110,525,vector([v/4 for v in CBOW_G]),20,TEXT,'middle')
    d.save(FIGURES[-1]['file'])

    d=figure(25,121,None,'c8.png','La misma ventana, dos lotes de entrenamiento',
        'Skip-gram produce cuatro pares; CBOW produce un contexto y un centro.',
        'Con los índices the=0, man=1, loves=2, his=3 y son=4, Skip-gram repite 2 como entrada y usa cuatro objetivos. CBOW reúne [0,1,3,4] en una entrada y usa 2 como objetivo. Estas son formas de lote de un ejemplo mínimo; no prueban por sí solas qué arquitectura será más rápida o mejor en otra tarea.',
        'Sin negativos ni padding; ventana completa de radio m = 2.')
    d.text(260,130,'Skip-gram',28,BLUE,'middle');d.text(780,130,'CBOW',28,PURPLE,'middle')
    d.text(80,190,'X: centros',22,GOLD);d.text(330,190,'y: contextos',22,BLUE)
    d.matrix(125,215,[[2],[2],[2],[2]],cell=66);d.matrix(375,215,[[0],[1],[3],[4]],cell=66)
    d.arrow(210,340,345,340,'blue');d.text(260,530,'X: (4,) · y: (4,)',24,BLUE,'middle')
    d.text(600,190,'X: un contexto',22,PURPLE);d.matrix(580,240,[[0,1,3,4]],cell=66)
    d.arrow(710,335,710,390,'purple');d.node(620,415,180,65,'y = [2]',GOLD,28);d.text(780,530,'X: (1, 4) · y: (1,)',24,PURPLE,'middle');d.save(FIGURES[-1]['file'])

    # Sustituye la portada de CBOW que duplicaba la palabra «Anatomía».
    d=Drawing('CBOW: aprender a predecir el centro',
              'El contexto proporciona la entrada; el centro observado proporciona el objetivo.',440)
    for i,name in enumerate(['the','man','his','son']):
        x=80;y=100+i*72
        d.node(x,y,180,55,name,BLUE,27);d.arrow(x+190,y+27,465,240,'blue')
    d.node(480,195,230,90,'promedio',PURPLE,29);d.arrow(720,240,800,240,'gold');d.node(815,195,180,90,'loves',GOLD,30)
    d.save('cbow-intro.svg')

def checks():
    """Contrasta los datos de las figuras con identidades y diferencias finitas."""
    for v,u,target,given in [(START,U,0,G),(MEAN,CBOW_U,0,CBOW_G)]:
        for k in range(2):
            plus=v.copy();minus=v.copy();plus[k]+=1e-6;minus[k]-=1e-6
            numeric=(loss(plus,u,target)-loss(minus,u,target))/2e-6
            assert abs(numeric-given[k])<1e-7
    for i in range(4):
        for k in range(2):
            a=copy.deepcopy(CONTEXT);b=copy.deepcopy(CONTEXT);a[i][k]+=1e-6;b[i][k]-=1e-6
            am=[sum(v[j] for v in a)/4 for j in range(2)];bm=[sum(v[j] for v in b)/4 for j in range(2)]
            numeric=(loss(am,CBOW_U,0)-loss(bm,CBOW_U,0))/2e-6
            assert abs(numeric-CBOW_G[k]/4)<1e-7
    assert loss(END,U,0)<loss(START,U,0)
    assert abs(sum(PROBS)-1)<1e-12 and abs(sum(CBOW_P)-1)<1e-12
    assert abs(math.prod([.15,.2,.1,.3])-.0009)<1e-12
    assert abs(math.prod([.2,.3,.4,.5])-.012)<1e-12
    assert abs(-math.log(.012)-sum(-math.log(p) for p in [.2,.3,.4,.5]))<1e-12
    assert [j for j in range(5) if 0<abs(j-2)<=2]==[0,1,3,4]
    assert [j for j in range(5) if 0<abs(j-3)<=2]==[1,2,4]
    assert MEAN==[1.,.5] and abs(math.hypot(1.5,math.sqrt(6.75))-3)<1e-12
    return {'softmax_sums':True,'likelihood_products':True,'log_loss_identity':True,
            'window_boundaries':True,'skipgram_gradient_finite_differences':True,
            'cbow_gradient_finite_differences':True,'cbow_mean_jacobian_finite_differences':True,
            'illustrative_sgd_step_decreases_loss':True,'python_training_executed':False}

def update_page():
    """Cada figura tiene un recurso y una explicación acordes a su sección."""
    s=BeautifulSoup(PAGE.read_text(),'html.parser')
    cover=s.find(id='celda-98').find('img')
    cover['src']='../assets/figures/word2vec/cbow-intro.svg'
    cover['alt']='CBOW: los vectores de the, man, his y son se promedian para predecir loves.'
    cover['width']='1040';cover['height']='440'
    s.find(id='celda-10').find('img')['alt']='Representaciones de texto preentrenadas y aplicaciones posteriores de NLP.'
    for item in FIGURES:
        cell=s.find(id='celda-'+str(item['cell']));cell.clear()
        fig=s.new_tag('figure',id=f"figura-1-{item['number']}")
        url='../assets/figures/word2vec/'+item['file']
        link=s.new_tag('a',href=url,target='_blank',rel='noopener',attrs={'aria-label':f"Abrir figura 1.{item['number']} ampliada"})
        image=s.new_tag('img',src=url,alt=item['title']+'. '+item['caption'],loading='lazy',width='1040',height='620')
        link.append(image);fig.append(link)
        caption=s.new_tag('figcaption');caption.string=f"Fig. 1.{item['number']}. "+item['caption'];fig.append(caption);cell.append(fig)
        explanation=s.find(id='celda-'+str(item['caption_cell'])) if item['caption_cell'] else cell
        if explanation is not cell:explanation.clear()
        explanation.append(BeautifulSoup(render('##### Cómo leer la figura\n\n'+item['explanation']),'html.parser'))
        explanation['data-reviewed-source']='https://d2l.ai/chapter_natural-language-processing-pretraining/word2vec.html'
    edits={
      14:'''Los **word embeddings** asignan vectores densos a los tokens. El entrenamiento puede capturar regularidades del corpus, pero la proximidad geométrica no garantiza equivalencia de significado. Word2Vec aprende representaciones mediante tareas predictivas de contexto; su utilidad se comprueba en una evaluación apropiada.''',
      33:'''Los ejemplos de entrenamiento se extraen del texto: no requieren una etiqueta manual por cada par. El vocabulario necesita una asignación de índices; los vectores, en cambio, son parámetros aprendidos. **Skip-gram** usa el centro para predecir vecinos. **CBOW** combina los vecinos para predecir el centro. El entrenamiento ajusta puntuaciones, sin definir unas «posiciones correctas» universales.''',
      63:r'''El radio $m$ delimita las posiciones que pueden formar contexto. Una ventana mayor puede incluir asociaciones a mayor distancia; una menor se concentra en vecinos locales. El tipo de regularidad capturada depende también del corpus y del objetivo: no existe una separación garantizada entre «semántica» y «sintaxis» por elegir un radio.

En radio fijo se generan hasta $2m$ pares por centro en Skip-gram, menos junto a los bordes. Aumentar el radio suele aumentar el trabajo de entrenamiento; el coste concreto depende de la implementación. Los gradientes proceden del objetivo predictivo, no de distancias euclídeas.

El submuestreo puede descartar probabilísticamente tokens muy frecuentes antes de formar ventanas. Es una estrategia de entrenamiento cuya configuración se evalúa; no convierte todas las palabras frecuentes en ruido.''',
      66:r'''La verosimilitud de Skip-gram multiplica las probabilidades de los **pares centro–contexto observados**, bajo su factorización condicional. Ese producto no debe identificarse con una distribución autorregresiva normalizada sobre textos completos.

Multiplicar muchos factores menores que 1 puede producir subdesbordamiento numérico. El logaritmo transforma la productoria en una suma y permite expresar un objetivo aditivo por pares; no es que derivar un producto sea matemáticamente imposible.''',
      67:r'''Para el conjunto $\mathcal P$ de posiciones centro–contexto válidas, el objetivo de pérdida es

$$L=-\sum_{(t,j)\in\mathcal P}\log P(w_j\mid w_t).$$

Se minimiza el negativo de la log-verosimilitud. En la implementación se usan operaciones estables como `log_softmax` o `cross_entropy`, que calculan el equivalente sin formar primero una productoria de probabilidades.''',
      111:r'''Para las posiciones $t$ con contexto válido $\mathcal C_t$, CBOW minimiza

$$L=-\sum_t\log P(w_t\mid\mathcal C_t).$$

Aquí $t$ recorre posiciones del **corpus**, no tipos de palabra del vocabulario. Cada término usa una palabra central observada y los vecinos disponibles de esa ventana. El objetivo se aplica tanto a un ejemplo pequeño como a un corpus grande; no exige millones de ventanas.''',
      115:r'''Con $C>0$ posiciones de contexto se calcula

$$\bar v=\frac1C\sum_{r=1}^C v_{o_r},\qquad p_j=\frac{\exp(u_j^\top\bar v)}{\sum_k\exp(u_k^\top\bar v)}.$$

Los vectores $v$ pertenecen a la tabla de **entrada** y los vectores $u$ a la de **salida**. En una ventana completa de radio $m$ hay $C=2m$ vecinos; cerca de los bordes puede haber menos. Para el centro observado $c$,

$$\ell=\log p_c=u_c^\top\bar v-\log\sum_j\exp(u_j^\top\bar v),\qquad L=-\ell.$$''',
      116:r'''Primero se deriva la log-verosimilitud respecto al promedio:

$$\nabla_{\bar v}\ell=u_c-\sum_j p_j u_j.$$

Después se aplica la regla de la cadena. El promedio es una suma de vectores dividida por $C$, por lo que su Jacobiano respecto a una aparición $v_{o_r}$ es $I_d/C$, la identidad de dimensión $d$ dividida por $C$. La composición propaga $1/C$ del gradiente a cada aparición.''',
      117:r'''Para cada aparición del contexto,

$$\nabla_{v_{o_r}}\ell=\frac1C\left(u_c-\sum_jp_j u_j\right),\qquad \nabla_{v_{o_r}}L=-\nabla_{v_{o_r}}\ell.$$

La Fig. 1.24 dibuja el gradiente de la **pérdida**. Descenso de $L$ y ascenso de $\ell$ dan el mismo paso. Cuando varias apariciones comparten una fila de la tabla de embeddings, sus gradientes se suman.''',
      125:'''CBOW promedia los vectores de entrada de los vecinos y utiliza ese predictor para puntuar la palabra central. El promedio elimina el orden dentro de ese conjunto en esta variante básica.

El modelo aprende tablas de entrada y salida. En este laboratorio se inspecciona la tabla `context_embeddings`; esa elección no convierte una de las dos tablas en la única representación válida para todas las tareas. La selección se justifica con el objetivo y la evaluación posteriores.''',
      135:'''La animación de CBOW permite inspeccionar el movimiento de los vectores y la pérdida de una **ejecución didáctica**. Un coseno alto entre dos tokens no demuestra que el modelo haya aprendido una regla sintáctica ni que el contexto determine con certeza una palabra.

CBOW optimiza la probabilidad del centro a partir de un promedio de vecinos. Si el ejemplo usa un corpus pequeño y embeddings de dos dimensiones, sus agrupaciones y cosenos dependen de esa configuración y de la inicialización. Una pérdida de entrenamiento menor no certifica calidad semántica ni generalización.''',
      137:'''La animación de Skip-gram ilustra un objetivo de predicción de contexto. Compartir entornos puede favorecer representaciones parecidas, pero el resultado depende del corpus, el entrenamiento y la tabla inspeccionada.

Los cosenos que aparecen son mediciones de esa ejecución, no identidades lingüísticas ni garantías de sinonimia. Para comparar Skip-gram con CBOW hace falta controlar datos, dimensión, entrenamiento y evaluación; estas animaciones no establecen una superioridad general de ninguno.''',
    }
    for number,text in edits.items():
        cell=s.find(id='celda-'+str(number));headings=[h.extract() for h in cell.find_all(['h1','h2','h3','h4','h5','h6'])]
        cell.clear()
        for heading in headings:cell.append(heading)
        cell.append(BeautifulSoup(render(text),'html.parser'))
        cell['data-reviewed-source']='https://d2l.ai/chapter_natural-language-processing-pretraining/word2vec.html'
    # Conservar la derivación existente, corrigiendo su interpretación inicial.
    cell=s.find(id='celda-74');cell.find('p').replace_with(BeautifulSoup(render('El gradiente de la log-verosimilitud indica una dirección de ascenso. Para minimizar la pérdida negativa se resta el gradiente de esa pérdida. La derivación siguiente calcula una dirección en el espacio de parámetros; no una fuerza física entre palabras.'),'html.parser'))
    for equation in cell.find_all('math'):
        latex=equation.get('aria-label','')
        if r'\begin{align' in latex:
            for environment in ('align*','aligned'):
                latex=latex.replace(r'\begin{'+environment+'}','').replace(r'\end{'+environment+'}','')
            # MathML nativo: una fórmula por paso evita separadores de alineación visibles.
            steps=[step.replace('&','').strip() for step in latex.split(r'\\') if step.strip()]
            equation.parent.replace_with(BeautifulSoup(render('\n\n'.join('$$'+step+'$$' for step in steps)),'html.parser'))
    intro=s.find(id='celda-61').find('p')
    if intro:
        for text in intro.find_all(string=True):
            if 'entender el entender el' in text:text.replace_with(str(text).replace('entender el entender el','entender el'))
    PAGE.write_text(str(s))

def main():
    generate();result=checks();update_page()
    report={'page':str(PAGE.relative_to(ROOT/'docs')),'source_notebook':'1 - Introducción al NLP  - Parte 1 - Word2Vec.ipynb',
            'sources':['https://d2l.ai/chapter_natural-language-processing-pretraining/word2vec.html','https://arxiv.org/abs/1301.3781','https://arxiv.org/abs/1310.4546'],
            'specific_figures':len(FIGURES),'cbow_intro_replaced':True,'original_numbering_preserved':True,
            'figures':[{**x,'sha256':hashlib.sha256((OUT/x['file']).read_bytes()).hexdigest()} for x in FIGURES],
            'numeric_checks':result,'training_code_changed':False}
    (ROOT/'reports/figuras-word2vec.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'specific_figures':len(FIGURES),'numeric_checks':result},indent=2))

if __name__=='__main__':main()
