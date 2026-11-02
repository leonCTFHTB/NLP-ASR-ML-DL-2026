"""Diagramas vectoriales de PyTorch con ejemplos exactos."""
from pathlib import Path
from html import escape
import math

DEST=Path(__file__).resolve().parents[1]/'docs/assets/pytorch'
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

D=Diagram

def cells(d,x,y,values,cols=6,w=74,h=58,colors=None):
    for i,v in enumerate(values):
        xx=x+i%cols*w;yy=y+i//cols*h
        d.box(xx,yy,w-6,h-6,color=(colors[i] if colors else BLUE));d.text(xx+(w-6)/2,yy+h*.61,v,24,TEXT,500,'middle')

def matrix(d,x,y,rows,w=84,h=60):
    cells(d,x,y,[v for r in rows for v in r],len(rows[0]),w,h)

def make():
    d=D('PyTorch · Del tensor a sus operaciones','Guía de lectura: representación, memoria y cálculo.')
    matrix(d,80,235,[[0,1,2],[3,4,5]],90,80)
    for x,title,lines in [(470,'Metadatos',['shape = (2, 3)','stride = (3, 1)','dtype = int64']),(850,'Operaciones',['Vistas y copias','Broadcasting','Álgebra lineal'])]:
        d.box(x,180,300,310,title)
        for j,t in enumerate(lines):d.text(x+25,285+j*65,t,25)
    d.line(365,325,455,325,BLUE,3,True);d.line(775,325,835,325,BLUE,3,True)
    d.foot('Los ejemplos se acotan a tensores densos con layout torch.strided, salvo indicación contraria.');d.save('t01-portada')

    d=D('1.1 · Una estructura lógica sobre un almacenamiento','Ejemplo: dos tensores pueden compartir los mismos datos y tener distintas formas.')
    d.box(55,165,510,195,'Tensor A');d.text(85,250,'shape (2, 3) · stride (3, 1)',27,BLUE)
    d.box(635,165,510,195,'Tensor B');d.text(665,250,'shape (3, 2) · stride (2, 1)',27,LAV)
    cells(d,375,440,[10,20,30,40,50,60],6)
    d.line(300,360,460,430,BLUE,3,True);d.line(890,360,740,430,BLUE,3,True)
    d.text(600,560,'Un almacenamiento compartido · seis valores',27,GOLD,500,'middle')
    d.foot('La forma pertenece a cada tensor. Compartir almacenamiento no implica tener los mismos metadatos.');d.save('t02-storage')

    d=D('2 · Leer, transformar y calcular','Tres preguntas para cada operación: ¿qué forma?, ¿qué strides?, ¿comparte datos?')
    for x,t,a,b in [(60,'Leer','shape / stride / offset','Localizar un elemento'),(450,'Transformar','view / reshape / transpose','Vista o copia según el caso'),(840,'Calcular','suma / producto matricial','Resultado con valores nuevos')]:
        d.box(x,195,300,290,t);d.text(x+20,310,a,20,BLUE);d.text(x+20,405,b,20)
    d.line(365,340,440,340,BLUE,3,True);d.line(755,340,830,340,BLUE,3,True)
    d.foot('Las operaciones fuera de sitio del ejemplo generan un resultado; las vistas reutilizan sus datos.');d.save('t03-operaciones')

    d=D('2.1.1 · Capas de un tensor denso','El descriptor, el almacenamiento y el bloque de datos cumplen funciones distintas.')
    for x,y,w,t,sub in [(70,180,450,'at::Tensor / TensorBase','Handle C++ con propiedad compartida'),(70,365,450,'c10::TensorImpl','Forma, strides, offset y estado'),(690,180,450,'c10::StorageImpl','Datos, capacidad y asignador'),(690,365,450,'Bloque de datos','CPU, CUDA u otro backend')]:
        d.box(x,y,w,140,t);d.text(x+20,y+100,sub,21)
    d.line(295,325,295,355,BLUE,3,True);d.line(525,430,680,250,BLUE,3,True);d.line(915,325,915,355,BLUE,3,True)
    d.foot('El objeto Python es otra envoltura. Los punteros representan direcciones virtuales del proceso.');d.save('t04-capas')

    d=D('2.1.2 · Del índice lógico al elemento','Tensor t = [[10, 20, 30], [40, 50, 60]] · float32 · offset inicial 0.')
    matrix(d,70,180,[[10,20,30],[40,50,60]],110,80)
    d.box(510,170,625,235,'Buscar t[1, 2]');d.text(540,265,'offset = 0 + 1 × 3 + 2 × 1 = 5',29,BLUE)
    d.text(540,335,'desplazamiento en bytes = 5 × 4 = 20',25,GOLD)
    cells(d,130,465,[10,20,30,40,50,60],6,140,65)
    d.line(830,410,900,455,BLUE,4,True)
    d.foot('Los strides y storage_offset se expresan en elementos. El tamaño de elemento convierte a bytes.');d.save('t05-offset')

    d=D('2.1.3 · Bytes de seis valores float32','Ejemplo little-endian: el byte menos significativo se almacena primero.')
    vals=[('10,0','00 00 20 41'),('20,0','00 00 A0 41'),('30,0','00 00 F0 41'),('40,0','00 00 20 42'),('50,0','00 00 48 42'),('60,0','00 00 70 42')]
    for i,(v,b) in enumerate(vals):
        x=65+i%3*390;y=170+i//3*195;d.box(x,y,340,150,v);d.text(x+25,y+100,b,30,BLUE)
    d.foot('Cada bloque tiene 4 bytes. El ejemplo completo contiene 6 × 4 = 24 bytes de datos.');d.save('t06-bytes')

    d=D('2.1.3 · Decodificar 10,0 con IEEE 754','0x41200000 = 01000001001000000000000000000000₂.')
    for x,w,title,t,col in [(60,150,'Signo','0',BLUE),(245,300,'Exponente','10000010₂ = 130',GOLD),(580,555,'Fracción','01000000000000000000000₂',LAV)]:
        d.box(x,200,w,170,title,col);d.text(x+w/2,310,t,24,col,600,'middle')
    d.text(600,455,'(−1)⁰ × (1 + 1/4) × 2¹³⁰⁻¹²⁷ = 1,25 × 8 = 10',32,TEXT,500,'middle')
    d.foot('La fórmula corresponde a valores normales; ceros, subnormales, infinitos y NaN requieren otros casos.');d.save('t07-ieee')

    d=D('2.1.3 · De los bytes a la matriz','Los mismos seis valores se interpretan mediante shape y stride.')
    cells(d,90,190,['10','20','30','40','50','60'],6,165,75)
    d.text(600,310,'offset = fila × 3 + columna',29,GOLD,500,'middle')
    matrix(d,365,370,[[10,20,30],[40,50,60]],150,80)
    d.line(370,275,450,355,BLUE,3,True);d.line(820,275,700,355,BLUE,3,True)
    d.foot('Storage no almacena una forma matricial: es el descriptor el que define el recorrido lógico.');d.save('t08-mapeo')

    d=D('2.2 · Elegir cómo inicializar','Crear una forma no siempre significa definir sus valores.')
    for x,y,title,v in [(65,165,'empty(2, 3)',['?','?','?','?','?','?']),(660,165,'zeros(2, 3)',[0,0,0,0,0,0]),(65,365,'ones(2, 3)',[1,1,1,1,1,1]),(660,365,'rand(2, 3)',['0,2','0,7','0,1','0,5','0,9','0,4'])]:
        d.box(x,y,470,170,title);cells(d,x+35,y+65,v,6,65,70)
    d.foot('Los «?» indican valores sin especificar; los números de rand son ilustrativos, no una corrida.');d.save('t09-inicializar')

    d=D('2.4.1 · La forma conserva la cantidad de elementos','Doce elementos pueden organizarse como 3 × 4 o 2 × 6.')
    matrix(d,65,195,[[0,1,2,3],[4,5,6,7],[8,9,10,11]],90,80)
    matrix(d,650,235,[[0,1,2,3,4,5],[6,7,8,9,10,11]],80,80)
    d.line(440,335,630,335,BLUE,4,True);d.text(600,525,'3 × 4 = 2 × 6 = 12',34,GOLD,500,'middle')
    d.foot('La conservación de numel es necesaria; compartir datos exige además compatibilidad de strides.');d.save('t10-forma')

    d=D('2.4.1 · view y reshape: comprobar los strides','El criterio no se reduce a preguntar si is_contiguous() es True.')
    d.box(65,160,500,355,'view(nueva_forma)');d.text(90,255,'Solo devuelve una vista.',27,BLUE)
    d.text(90,315,'La forma y los strides deben',24);d.text(90,355,'permitir el recorrido solicitado.',24)
    d.text(90,440,'Incompatible → RuntimeError',25,GOLD)
    d.box(635,160,500,355,'reshape(nueva_forma)');d.text(660,255,'Vista si es compatible.',27,BLUE)
    d.text(660,315,'Copia cuando la vista',24);d.text(660,355,'no puede representar la forma.',24)
    d.text(660,440,'No asumir vista ni copia.',25,GOLD)
    d.foot('Contraejemplo: arange(12).reshape(3,4)[:,::2] no es contiguo y admite view(6), stride (2,).');d.save('t11-view')

    d=D('2.4.2 · Añadir y quitar un eje unitario','unsqueeze(0) y squeeze(0) comparten el almacenamiento del ejemplo.')
    for x,t,s,st in [(60,'Original','(3, 4)','(4, 1)'),(450,'unsqueeze(0)','(1, 3, 4)','(12, 4, 1)'),(840,'squeeze(0)','(3, 4)','(4, 1)')]:
        d.box(x,185,300,290,t);d.text(x+25,300,'shape '+s,25,BLUE);d.text(x+25,375,'stride '+st,23)
    d.line(365,330,440,330,BLUE,3,True);d.line(755,330,830,330,BLUE,3,True)
    d.foot('squeeze() sin dim elimina todos los ejes de tamaño 1, incluido el lote cuando batch_size = 1.');d.save('t12-squeeze')

    d=D('2.5.1 · Broadcasting y stride cero','B: shape (1, 3) · expand(4, 3): stride (0, 1).')
    cells(d,80,245,[10,20,30],3,105,80);d.text(80,385,'12 bytes de datos en B',25,GOLD)
    matrix(d,720,170,[[10,20,30]]*4,105,80)
    for i in range(4):d.line(400,280,700,210+i*80,BLUE,2,True)
    d.text(75,490,'Cada fila lee los offsets 0, 1, 2.',25)
    d.foot('expand no duplica los datos; A + B sí produce un resultado. Evitar escrituras en una vista solapada.');d.save('t13-broadcast')

    d=D('2.6.1 · Multiplicación matricial','Cada salida es un producto punto entre una fila y una columna.')
    matrix(d,65,185,[[1,2,3],[4,5,6]],90,75);matrix(d,480,145,[[1,0],[0,1],[1,1]],90,75);matrix(d,900,185,[[4,5],[10,11]],90,75)
    d.text(385,280,'×',42,GOLD);d.text(800,280,'=',42,GOLD)
    d.text(200,440,'A: (2, 3)',28,BLUE);d.text(500,440,'B: (3, 2)',28,BLUE);d.text(900,440,'C: (2, 2)',28,BLUE)
    d.text(600,530,'C₀₀ = 1 × 1 + 2 × 0 + 3 × 1 = 4',30,GOLD,500,'middle')
    d.foot('La dimensión de contracción K coincide. Para bmm también debe coincidir el tamaño del lote.');d.save('t14-matmul')

    d=D('2.6.1 · Elegir la operación de álgebra lineal','Los rangos y las reglas de lote determinan la operación apropiada.')
    xs=[70,365,830];headers=['Operación','Entrada → salida','Broadcasting de lote']
    for x,t in zip(xs,headers):d.text(x,180,t,25,GOLD,600)
    rows=[('dot','(K,), (K,) → escalar','No'),('mm','(M,K), (K,N) → (M,N)','No'),('bmm','(B,M,K), (B,K,N)','No'),('matmul / @','Vectores o matrices','Sí, en ejes de lote')]
    for i,row in enumerate(rows):
        for x,t in zip(xs,row):d.text(x,260+75*i,t,23,BLUE if i==3 else TEXT)
        d.line(65,285+75*i,1140,285+75*i)
    d.foot('matmul no acepta operandos escalares 0D; los casos de vectores siguen sus reglas específicas.');d.save('t15-tabla')

    d=D('c10 / ATen · La estructura detrás del tensor','Del handle C++ al descriptor y al almacenamiento.')
    for x,y,title,sub in [(70,175,'at::Tensor','Interfaz y propiedad compartida'),(660,175,'TensorImpl','Metadatos y estado'),(70,375,'StorageImpl','Bloque, capacidad y asignador'),(660,375,'DataPtr','Datos, contexto y liberación')]:
        d.box(x,y,470,150,title);d.text(x+20,y+105,sub,23)
    d.line(545,250,650,250,BLUE,3,True);d.line(890,330,305,365,BLUE,3,True);d.line(545,450,650,450,BLUE,3,True)
    d.foot('Esquema conceptual para tensores densos strided; no es un plano ABI con tamaños universales.');d.save('c01-portada')

    d=D('2.1 · Copiar un handle no copia sus datos','at::Tensor b = a comparte la misma implementación de a.')
    d.box(65,185,310,135,'Handle a');d.box(65,380,310,135,'Handle b')
    d.box(690,255,440,205,'TensorImpl compartido');d.text(720,370,'Una implementación',28,BLUE)
    d.line(385,250,680,310,BLUE,3,True);d.line(385,445,680,405,BLUE,3,True)
    d.foot('El handle puede estar en la pila, en el heap o dentro de otro objeto. clone() copia los datos.');d.save('c02-handle')

    d=D('2.2 · Una vista tiene metadatos propios','Transposición de una matriz 2 × 3: los datos siguen en el mismo orden.')
    matrix(d,70,175,[[0,1,2],[3,4,5]],100,75);matrix(d,790,145,[[0,3],[1,4],[2,5]],100,75)
    d.text(75,395,'shape (2, 3) · stride (3, 1)',24,BLUE);d.text(715,420,'shape (3, 2) · stride (1, 3)',24,LAV)
    cells(d,320,485,[0,1,2,3,4,5],6,95,65)
    d.line(300,410,430,475,BLUE,3,True);d.line(900,435,770,475,BLUE,3,True)
    d.foot('La vista comparte StorageImpl, mientras sus sizes y strides describen otro recorrido.');d.save('c03-metadatos')

    d=D('2.2.1 · Optimización de metadatos pequeños','SizesAndStrides dispone de almacenamiento inline para pocos ejes.')
    d.box(65,175,500,325,'Pocos ejes');cells(d,100,265,['N','C','H','W'],4,95,70);d.text(95,425,'Metadatos en el propio objeto',24,BLUE)
    d.box(635,175,500,325,'Más ejes que la capacidad inline');d.text(665,280,'Puntero a un arreglo adicional',25,BLUE)
    d.line(885,325,885,380,BLUE,3,True);cells(d,675,395,['s₀','s₁','…','sₙ'],4,100,70)
    d.foot('El umbral es interno y depende de la revisión. No determina dónde se asignan los datos del tensor.');d.save('c04-inline')

    d=D('2.2.2 · El dispatcher selecciona una implementación','Las claves del tensor se combinan con estado local y prioridades del despacho.')
    for x,y,t,s in [(55,170,'Tensores','backend · layout · claves'),(55,380,'Estado local','modos incluidos / excluidos'),(455,270,'Dispatcher','conjunto efectivo y prioridad'),(850,270,'Kernel registrado','CPU / CUDA / Autograd / …')]:
        d.box(x,y,300,155,t);d.text(x+18,y+105,s,19,BLUE)
    d.line(360,245,445,310,BLUE,3,True);d.line(360,455,445,380,BLUE,3,True);d.line(760,345,840,345,BLUE,3,True)
    d.foot('El despacho no se reduce a un AND/OR ni permite prometer una latencia universal en nanosegundos.');d.save('c05-dispatch')

    d=D('2.3 · DataPtr y propiedad del bloque','El puntero visible y el contexto que se libera pueden ser diferentes.')
    d.box(60,165,480,360,'DataPtr');d.text(90,260,'data → comienzo de los datos',25,BLUE)
    d.text(90,330,'context → objeto de propiedad',25,LAV);d.text(90,400,'deleter(context)',28,GOLD);d.text(90,470,'device → tipo e índice',25)
    d.box(760,165,380,160,'Bloque de datos');cells(d,790,240,['0','1','2','…'],4,77,60)
    d.box(760,370,380,155,'Estado del asignador');d.text(785,470,'Control de vida útil',24)
    d.line(550,245,750,245,BLUE,3,True);d.line(550,395,750,440,BLUE,3,True)
    d.foot('El deleter recibe el contexto. sizeof y offsets dependen del compilador, la STL y la revisión.');d.save('c06-dataptr')

    d=D('2.3.1 · Vistas compartidas y copia explícita','No hay copy-on-write automático para las vistas ordinarias de este ejemplo.')
    d.box(65,160,490,345,'a y v = a.view(2, 3)');cells(d,95,245,[0,1,2,3,4,5],6,70,65)
    d.text(95,375,'v[0, 0] = 99',28,GOLD);d.text(95,440,'a[0] también pasa a valer 99.',25,BLUE)
    d.box(645,160,490,345,'c = a.clone()');cells(d,675,245,[99,1,2,3,4,5],6,70,65)
    d.text(675,375,'c[0] = −1',28,GOLD);d.text(675,440,'Los datos de a no cambian.',25,BLUE)
    d.foot('Autograd puede prohibir ciertas escrituras in-place; esa restricción no es copy-on-write.');d.save('c07-alias')

    d=D('2.4 · Medir el layout de la compilación','Un diagrama conceptual no reemplaza al ABI real del binario analizado.')
    for x,t,a,b in [(60,'Revisión','torch.__version__','Código y cabeceras'),(450,'Herramientas','Compilador · ABI · STL','Arquitectura y opciones'),(840,'Medición','sizeof / alignof','Símbolos y depurador')]:
        d.box(x,185,300,300,t);d.text(x+20,305,a,22,BLUE);d.text(x+20,405,b,21)
    d.line(365,335,440,335,BLUE,3,True);d.line(755,335,830,335,BLUE,3,True)
    d.foot('Un offset observado en MSVC x86-64 no se traslada automáticamente a Linux, ARM u otra versión.');d.save('c08-abi')

if __name__=='__main__':make()
