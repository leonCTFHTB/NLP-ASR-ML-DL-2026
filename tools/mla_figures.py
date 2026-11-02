"""Diagramas SVG exactos y ampliables con la paleta del portafolio."""
from pathlib import Path
import math,json,re,random,textwrap
from html import escape
DEST=Path(__file__).resolve().parents[1]/'docs/assets/mla/diagramas'
DEST.mkdir(parents=True,exist_ok=True)
BG='#111318'; PANEL='#191d26'; LINE='#343b4b'; TEXT='#e5e7eb'; MUTED='#a8b0c1'; BLUE='#91b9e3'; GOLD='#d9c58f'; LAV='#b8a5ee'

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

FIGS={i:{} for i in range(1,6)}

def add(n,cell,title,kind,labels,foot):
    FIGS[n][cell]={'name':f'ml{n:02d}-celda-{cell:03d}','title':title,'kind':kind,'labels':labels.split('|'),'caption':foot}

def paragraph(d,x,y,text,width=48,size=21,color=TEXT):
    for row,line in enumerate(textwrap.wrap(text,width=width,break_long_words=False)):
        d.text(x,y+row*(size+10),line,size,color)

def curve(d,func,x,y,w,h,xmin=-3,xmax=3,ymin=-1,ymax=1,color=BLUE):
    pts=[]
    for i in range(181):
        xx=xmin+(xmax-xmin)*i/180;v=func(xx);v=max(ymin,min(ymax,v))
        pts.append(f'{x+w*i/180:.2f},{y+h-h*(v-ymin)/(ymax-ymin):.2f}')
    d.parts.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="4"/>')

def axes(d,x=95,y=490,w=480,h=275):
    d.line(x,y,x+w,y,MUTED,2,True);d.line(x,y,x,y-h,MUTED,2,True)

def scatter(d,x,y,w,h,group=0,count=30):
    rng=random.Random(42+group)
    for i in range(count):
        g=i%2;px=x+w*(.3+.38*g)+rng.gauss(0,w*.085);py=y+h*(.62-.25*g)+rng.gauss(0,h*.11)
        d.circle(round(px,1),round(py,1),5,'',[BLUE,GOLD][g])

def draw(spec,n):
    title=spec['title'];kind=spec['kind'];labs=spec['labels']
    d=Diagram(title,'ML Avanzado y DL · Clase '+str(n)+' · Esquema didáctico')
    # Los títulos largos se ajustan sin reducir los textos de los paneles.
    if len(title)>65:d.parts[1]=d.parts[1].replace('font-size="32"','font-size="28"')
    if kind=='flow':
        count=len(labs);w=(1090-45*(count-1))/count
        for i,label in enumerate(labs):
            x=55+i*(w+45);d.box(x,210,w,270,color=[BLUE,GOLD,LAV][i%3]);d.circle(x+w/2,270,26,str(i+1),[BLUE,GOLD,LAV][i%3]);paragraph(d,x+20,345,label,max(16,int(w/13)),23)
            if i<count-1:d.line(x+w+5,345,x+w+37,345,BLUE,3,True)
    elif kind in ['compare','metric','neighbors','tree']:
        for k,label in enumerate(labs[:2]):
            x=55+k*565;d.box(x,150,525,395,color=[BLUE,GOLD][k]);paragraph(d,x+25,190,label,41,22,[BLUE,GOLD][k])
            if kind=='tree':
                for xa,ya,xb,yb in [(265,290,155,360),(265,290,375,360),(155,360,105,440),(155,360,210,440),(375,360,320,440),(375,360,425,440)]:d.line(x+xa,ya,x+xb,yb,LINE,3)
                for px,py in [(265,290),(155,360),(375,360),(105,440),(210,440),(320,440),(425,440)]:d.circle(x+px,py,17,'',[BLUE,GOLD][k])
                if k==1:d.line(x+120,360,x+410,360,LAV,2,False,True)
            elif kind=='metric':
                skew=0 if 'Pitágoras en coordenadas ortonormales' in title else k
                for i in range(5):
                    dx=22*skew*(i-2);d.line(x+95+i*70+dx,300,x+95+i*70,485,LINE,2)
                    d.line(x+70,300+i*45,x+430,300+i*45+(i-2)*12*skew,LINE,2)
                d.line(x+140,450,x+365,325,[BLUE,GOLD][k],4,True)
            else:
                scatter(d,x+35,275,440,220,k)
                if kind=='neighbors':
                    d.circle(x+165,405,40+50*k,'',[BLUE,GOLD][k]);d.circle(x+165,405,8,'',LAV)
                else:d.line(x+100,490,x+420,280,[BLUE,GOLD][k],3,True)
    elif kind in ['activation','loss','tails','qcurve','learning','linearity','gradient']:
        axes(d,95,490,570,285);d.text(650,528,'x' if kind=='activation' else 'distancia / error / etapa',20,MUTED,anchor='end')
        if kind=='activation':
            funcs=[lambda x:max(0,x)/3,lambda x:1/(1+math.exp(-x)),math.tanh]
        elif kind=='linearity':funcs=[lambda x:x/3,lambda x:(x*x)/9]
        elif kind=='tails':funcs=[lambda x:math.exp(-x*x),lambda x:1/(1+x*x)]
        elif kind=='qcurve':funcs=[lambda x:1/(1+1.58*abs(x)**1.79),lambda x:1/(1+.8*abs(x)**1.2)]
        elif kind=='gradient':funcs=[lambda x:max(-1,min(1,x)),lambda x:x/3]
        elif kind=='loss':funcs=[lambda x:x*x/9,lambda x:(math.sqrt(1+x*x)-1)/3]
        else:funcs=[lambda x:.75*math.exp(-1.8*(x+3))+.08*(x+3),lambda x:.8*math.exp(-.6*(x+3))]
        for k,f in enumerate(funcs):curve(d,f,95,205,570,285,xmin=0 if kind in ['tails','qcurve'] else -3,xmax=5 if kind in ['tails','qcurve'] else 3,ymin=-1 if kind in ['activation','gradient','linearity'] else 0,ymax=1,color=[BLUE,GOLD,LAV][k])
        for k,label in enumerate(labs):paragraph(d,740,235+105*k,label,30,22,[BLUE,GOLD,LAV][k%3])
    elif kind=='svm':
        axes(d,95,510,560,330)
        for xx,color in [(265,BLUE),(395,LAV),(525,GOLD)]:d.line(xx,200,xx,485,color,3,False,xx!=395)
        for px,py in [(160,270),(210,360),(265,430),(525,270),(580,390),(600,215)]:d.circle(px,py,8,'',BLUE if px<=265 else GOLD)
        d.line(265,465,525,465,BLUE,3,True);d.text(395,560,'2 / ‖w‖',27,LAV,anchor='middle')
        for k,label in enumerate(labs):paragraph(d,750,240+105*k,label,29,23)
    elif kind=='graph':
        pts=[(170,280),(270,240),(310,360),(200,440),(780,275),(890,235),(950,380),(800,450)]
        for a,b in [(0,1),(1,2),(2,3),(3,0),(0,2),(4,5),(5,6),(6,7),(7,4)]:d.line(*pts[a],*pts[b],BLUE if a<4 else GOLD,3)
        for i,(x,y) in enumerate(pts):d.circle(x,y,11,'',BLUE if i<4 else GOLD)
        if 'unión' in title.lower() or 'asim' in title.lower():
            d.line(315,350,765,285,LAV,4,True);d.text(550,290,'0,2 + 0,8 − 0,16 = 0,84',23,LAV,anchor='middle')
        for k,label in enumerate(labs):paragraph(d,80+k*565,530,label,42,20)
    elif kind=='bits':
        for k,(x,bit) in enumerate([(95,'1'),(285,'0'),(475,'1')]):d.box(x,230,145,115);d.text(x+72,305,bit,42,[BLUE,GOLD,LAV][k],anchor='middle');d.text(x+72,395,['2² = 4','2¹ = 2','2⁰ = 1'][k],24,anchor='middle')
        d.line(640,290,720,290,BLUE,4,True);d.box(745,220,385,220,'Índice = 4 + 0 + 1 = 5');d.text(775,370,'W[5] = 45,0',32,GOLD)
        for k,label in enumerate(labs):paragraph(d,80,500+40*k,label,90,22)
    elif kind=='matrix':
        for i in range(5):
            for j in range(8):d.box(85+j*65,210+i*48,50,35,color=BLUE if (i+j)%3==0 else LINE)
        for k,label in enumerate(labs):paragraph(d,740,235+110*k,label,29,23,[BLUE,GOLD,LAV][k%3])
    elif kind=='ordered':
        for k,(cat,y,val) in enumerate([('Salta',1,'.400'),('Jujuy',0,'.400'),('Salta',0,'.700'),('Salta',1,'.467'),('Jujuy',1,'.200')]):
            x=60+k*225;d.box(x,210,200,270,cat,color=BLUE if cat=='Salta' else GOLD);d.text(x+20,310,'y = '+str(y),26);d.text(x+20,385,'TS = '+val,25,LAV);d.text(x+20,445,'posición '+str(k+1),20,MUTED)
        paragraph(d,80,545,labs[0],95,23)
    else:raise ValueError(kind)
    paragraph(d,45,600,spec['caption'],110,18,MUTED)
    d.save(spec['name'])

# Correspondencia explícita con las celdas que intentaban mostrar las figuras.
add(1,7,'Del dato a la decisión','flow','Vectores de entrada|Función aprendida|Predicción o estructura','Supervisado y no supervisado utilizan objetivos diferentes.')
add(1,9,'Una observación es un vector de atributos','matrix','Filas: observaciones|Columnas: características|No implica independencia','X tiene n filas y d columnas; cada fila representa una muestra.')
add(1,11,'Pendiente constante frente a relación no lineal','linearity','Función afín|Relación cuadrática','Curvas ilustrativas: una función afín no representa por sí sola una relación en U.')
add(1,14,'Activaciones: ReLU, sigmoide y tanh','activation','ReLU reescalada|Sigmoide|Tanh','Las activaciones introducen no linealidad; la separabilidad no está garantizada.')
add(1,16,'Dos objetivos de aprendizaje','compare','Supervisado: entrada y objetivo|No supervisado: estructura de entradas','Clasificación y regresión son tareas supervisadas diferentes.')
add(1,18,'Distancia y vecindarios de decisión','neighbors','Un vecindario pequeño|Un vecindario más amplio','El escalado y la métrica modifican quiénes son los vecinos.')
add(1,20,'PCA y agrupamiento responden preguntas distintas','compare','PCA: direcciones de varianza|k-means: cercanía a centroides','Retener varianza no equivale a identificar clases semánticas.')
add(1,24,'SVM: frontera y planos de apoyo','svm','Puntuación cero: decisión|Puntuaciones ±1: apoyo|Puntos activos: soportes','Las clases de este ejemplo son separables; el margen suave admite violaciones.')
add(1,27,'Ancho total del margen canónico','svm','Distancia a cada apoyo: 1 / ‖w‖|Ancho total: 2 / ‖w‖','Minimizar la norma amplía el margen sujeto a las restricciones.')
add(1,29,'De la formulación dual a un kernel','flow','Multiplicadores α y restricciones|Productos internos K(x, x′)|Predicción con vectores de soporte','Un kernel válido permite evitar una expansión explícita de características.')

boost=[
(7,'Gradient boosting: correcciones sucesivas','flow','Modelo inicial F₀|Aprendiz sobre −∇L|Fₜ = Fₜ₋₁ + ηfₜ','El ensamble es aditivo y se construye por etapas.'),
(10,'De un aprendiz base a un ensamble','tree','Modelo de capacidad limitada|Combinación de varios modelos','Un aprendiz débil tiene un significado formal dependiente de la tarea.'),
(12,'Analogía de las correcciones de golf','flow','Predicción actual|Diferencia hasta el objetivo|Corrección amortiguada','La analogía no garantiza llegar exactamente al objetivo.'),
(13,'Cada etapa usa el ensamble anterior','flow','Evaluar Fₜ₋₁|Aproximar una dirección de mejora|Añadir un nuevo árbol','Los árboles anteriores permanecen fijos en el esquema por etapas.'),
(15,'Bagging y boosting','compare','Bagging: ajustes independientes|Boosting: ajustes secuenciales','Random Forest combina bootstrap y aleatorización de atributos.'),
(17,'Tres componentes del boosting','flow','Aprendiz base|Función de pérdida|Modelo aditivo','La dirección de mejora viene de la pérdida elegida.'),
(19,'Un árbol predice correcciones numéricas','tree','Cortes en características|Valores numéricos en hojas','También en clasificación los árboles aportan correcciones a las puntuaciones.'),
(21,'La pérdida define los gradientes','loss','Pérdida cuadrática|Pseudo-Huber suave','Curvas ilustrativas reescaladas; la robustez depende de la pérdida.'),
(23,'El modelo inicial también cuenta','flow','F₀(x)|ηf₁(x) + … + ηfₜ(x)|Fₜ(x)','El término inicial no se debe omitir de la suma del ensamble.'),
(25,'Parámetros y espacio de funciones','compare','Una red ajusta sus parámetros|Boosting agrega funciones base','Los dos procedimientos optimizan representaciones distintas.'),
(29,'El pseudo-residuo es el gradiente negativo','flow','Pérdida L(y, F)|Derivada respecto de F|r = −∂L / ∂F','Con media pérdida cuadrática, r = y − F.'),
(33,'Una iteración completa','flow','Calcular gradiente negativo|Ajustar el aprendiz|Elegir paso y actualizar','El tamaño de paso y el ajuste condicionan la mejora.'),
(35,'Entrenamiento y validación pueden divergir','learning','Validación ilustrativa|Entrenamiento ilustrativo','Reducir error de entrenamiento no garantiza mejorar fuera de muestra.'),
(38,'Shrinkage regula cada corrección','flow','Nuevo árbol hₜ|Paso ηγₜ|Contribución al ensamble','Tasa y cantidad de árboles deben seleccionarse conjuntamente.'),
(40,'Muestreo de filas y columnas','matrix','Filas seleccionadas por etapa|Columnas candidatas|Aleatoriedad como regularización','La estrategia y la proporción dependen de la biblioteca y configuración.'),
(42,'Parada temprana sin consultar el test','learning','Métrica de validación|Pérdida de entrenamiento','Se elige la mejor etapa con validación; el test se reserva para el final.'),
(44,'Árbol, bosque y boosting','flow','Árbol: un modelo|Bosque: promedio de modelos|Boosting: suma por etapas','No hay un método universalmente superior en todos los problemas.'),
(45,'Regularización del ensamble','flow','Limitar cada árbol|Amortiguar y muestrear|Seleccionar con validación','Complejidad, tasa y número de etapas interactúan.')]
for c,t,k,l,f in boost:add(2,c,t,k,l,f)

cat=[
(7,'CatBoost: categorías y boosting','flow','Datos heterogéneos|Estadísticas de categorías|Ensamble de árboles','El tipo de boosting y la política de crecimiento son configurables.'),
(9,'Dos fuentes de dependencia del objetivo','compare','Target encoding con objetivo propio|Gradientes sobre predicciones in-sample','El artículo de CatBoost analiza mecanismos concretos de prediction shift.'),
(14,'Mecanismos que se complementan','flow','Estadísticas ordenadas|Boosting ordenado|Árboles simétricos','Son componentes diferentes; no equivalen a ausencia total de sobreajuste.'),
(16,'Una permutación define el historial disponible','ordered','Cada fila usa solo objetivos de posiciones anteriores.','El orden artificial no debe confundirse con tiempo físico.'),
(18,'Estadística suavizada por categoría','flow','Suma de objetivos previos + a·p|Conteo previo + a|Cociente: estadística ordenada','El prior del ejemplo se fija independientemente del objetivo propio.'),
(24,'Traza de cinco observaciones','ordered','Prior fijo p = 0,40; peso a = 1.','La media de los cinco objetivos es 0,60; no es el prior elegido.'),
(27,'Una categoría puede recibir distintas estadísticas','compare','Media única de toda la categoría|Media de prefijos con suavizado','Excluir el objetivo propio es la protección relevante frente a esa fuga.'),
(29,'Gradientes calculados con modelos de prefijo','flow','Modelo entrenado sobre prefijo|Predicción de la fila siguiente|Gradiente sin usar su objetivo al ajustar ese prefijo','La implementación comparte trabajo entre modelos y permutaciones.'),
(31,'Una condición por nivel','tree','Árbol con cortes por rama|Árbol simétrico: corte compartido','Un árbol simétrico de profundidad d almacena 2ᵈ posiciones de hoja.'),
(35,'Cortes numéricos y regiones','compare','Cortes locales por rama|Predicados globales compartidos','Las regiones no son necesariamente regulares ni todas las hojas alcanzables.'),
(36,'Índice de hoja mediante bits','bits','Evaluar las condiciones cuesta O(d).|Consultar W[index] cuesta O(1).','La inferencia de T árboles cuesta aproximadamente O(Td) por muestra.')]
for c,t,k,l,f in cat:add(3,c,t,k,l,f)

tsne=[
(6,'Representar datos y explorar vecindades','flow','Características de entrada|PCA o afinidades locales|Mapa para investigar','Una proyección no prueba por sí sola clases o grupos.'),
(9,'Una capa afín: entradas y salidas','matrix','X: n × d|W: d × h|O: n × h','nn.Linear almacena W con forma h × d y utiliza su transpuesta.'),
(11,'Transformaciones afines','metric','Base cartesiana|Escala y cizalla','Una transformación afín también puede reflejar o colapsar dimensiones.'),
(13,'La limitación de la pendiente constante','linearity','Salida afín|Relación cuadrática','La monotonía de cada puntuación no equivale a monotonía de un mapa completo.'),
(15,'Separación lineal y no lineal','compare','Un único hiperplano|Representaciones transformadas','No toda transformación vuelve separables todos los datos.'),
(16,'No linealidad entre capas','flow','Transformación afín|Activación elemento a elemento|Siguiente transformación','Apilar solo aplicaciones afines produce otra aplicación afín.'),
(19,'ReLU: rectificación por coordenada','activation','ReLU reescalada|Sigmoide de referencia|Tanh de referencia','ReLU puede colapsar regiones; el plegado es una analogía.'),
(21,'Sigmoide y tanh: compresión suave','activation','ReLU reescalada|Sigmoide: (0,1)|Tanh: (−1,1)','La simetría de tanh no garantiza media nula en cualquier distribución.'),
(23,'Representación y decisión','flow','Entrada original|Capas con no linealidad|Puntuación de salida','La capacidad de representar no garantiza el resultado del entrenamiento.'),
(27,'Elevar la dimensión con características nuevas','flow','x ∈ ℝ|Φ(x) = (x, x²)|Separación en el nuevo espacio','Cover motiva la expansión bajo condiciones; no promete generalización.'),
(29,'La dimensionalidad también tiene un costo estadístico','matrix','Más características|Muestreo más disperso|Métrica y regularización importan','La maldición de la dimensionalidad no equivale solo a uso de memoria.'),
(31,'Producto interno sin formar la expansión','flow','Par x, x′|Evaluar K(x, x′)|Producto en el espacio de Φ','La matriz de Gram de un kernel válido es semidefinida positiva.'),
(33,'El kernel evita un cálculo explícito','flow','Datos originales|K(x, x′) = ⟨Φ(x), Φ(x′)⟩|Algoritmo basado en productos','El costo aún depende de muestras, kernel y vectores de soporte.'),
(36,'PCA: máxima varianza lineal','compare','Datos en el espacio de entrada|Proyección sobre componentes','Una proyección lineal puede superponer regiones de una variedad curva.'),
(37,'Diferentes objetivos de proyección','compare','PCA retiene varianza|t-SNE ajusta afinidades','Ninguno garantiza conservar toda la topología.'),
(39,'t-SNE: dos distribuciones sobre pares','flow','Afinidades P de entrada|Afinidades Q del mapa|Minimizar KL(P ‖ Q)','La optimización se realiza sobre las coordenadas del embedding.'),
(42,'Afinidad dirigida por cada observación','neighbors','Vecindario de escala menor|Vecindario de escala mayor','El ancho σᵢ se adapta por fila; σᵢ² es la varianza.'),
(43,'Normalizar los pesos gaussianos','flow','Distancias al cuadrado|exp(−d² / 2σᵢ²)|Normalización por fila','La probabilidad del propio punto se fija en cero.'),
(45,'Perplejidad como restricción de entropía','neighbors','Distribución más concentrada|Distribución más difusa','Perplejidad no es el número exacto de enlaces de peso no nulo.'),
(48,'Una escala entrópica de vecindad','flow','Pᵢ: probabilidades por fila|H(Pᵢ) = −Σp log₂p|Perp(Pᵢ) = 2ᴴ','Una distribución uniforme sobre k elementos tiene perplejidad k.'),
(51,'Escalas diferentes, entropías comparables','neighbors','Región densa: escala menor|Región dispersa: escala mayor','La búsqueda de ancho de banda aproxima una entropía objetivo.'),
(53,'Simetrización de las afinidades','flow','p(j|i) y p(i|j)|Sumar y dividir por 2n|P simétrica y normalizada','La simetría no asigna el mismo peso a todos los pares.'),
(55,'La densidad visual puede engañar','compare','Densidad en la entrada|Densidad en la proyección','Las áreas y densidades de islas no son estimaciones fieles de las originales.'),
(57,'El reto de alojar muchas relaciones en 2D','compare','Muchas direcciones de entrada|Dos coordenadas de salida','Reducir dimensión fuerza compromisos entre relaciones de distancia.'),
(59,'El volumen relativo de una capa exterior','flow','Radio r|Radio 2r|Vᴰ(2r) / Vᴰ(r) = 2ᴰ','El volumen a radio fijo no tiene por qué crecer con la dimensión.'),
(61,'Colas gaussianas y de Student','tails','exp(−d²)|1 / (1+d²)','Núcleos sin normalizar; la cola de Student decae más lentamente.'),
(63,'Colas pesadas para aliviar el hacinamiento','tails','Núcleo gaussiano|Núcleo de Student','Permiten representar afinidades moderadas con separaciones mayores.'),
(65,'Qué compara la divergencia KL','flow','P: afinidades de entrada|Q: afinidades normalizadas del mapa|Σ pᵢⱼ log(pᵢⱼ / qᵢⱼ)','Cambiar la perplejidad modifica el objetivo P.'),
(69,'Descenso: atracción y repulsión','graph','Atracción ponderada por P|Repulsión inducida por Q','t-SNE sí tiene repulsión entre puntos en la formulación exacta.'),
(71,'Leer la proyección con evidencia adicional','compare','Mapa de entrada desconocido|Mapa bidimensional observado','Distancias entre islas y relaciones de inclusión no están garantizadas.'),
(72,'Varios parámetros, varias escalas','neighbors','Énfasis muy local|Vecindad efectiva más amplia','La perplejidad 30 es un punto de partida, no un óptimo universal.'),
(73,'Pipeline del laboratorio de dígitos','flow','Digits: 1797 × 64|PCA y cinco ajustes de t-SNE|Comparar mapas y registrar costos','Las etiquetas se reservan para colorear los resultados.')]
for c,t,k,l,f in tsne:add(4,c,t,k,l,f)
add(4,101,'Clases para interpretar, no para ajustar el mapa','flow','t-SNE recibe atributos|Las etiquetas colorean los puntos|Validar vecindades en la entrada','La disposición de una clase no garantiza una interpretación morfológica única.')

umap=[
(6,'UMAP construye y aproxima un grafo','flow','Vecinos en la entrada|Grafo con pertenencias difusas|Embedding de baja dimensión','Conservar el grafo aproximadamente no garantiza toda la geometría.'),
(8,'Distintos criterios para reducir dimensión','compare','PCA: varianza de proyecciones|UMAP y t-SNE: vecindades','La elección depende del objetivo y de la validación.'),
(9,'De la tabla al espacio de características','matrix','Cada fila es una muestra|La métrica define cercanía|La estructura no se deduce del orden de filas','El preprocesamiento puede cambiar por completo el grafo de vecinos.'),
(11,'Tres hipótesis que motivan UMAP','flow','Uniformidad bajo una métrica|Métrica aproximadamente local|Conectividad local','Los datos reales no vienen con una garantía de cumplir estos supuestos.'),
(14,'Uniformidad respecto de una métrica','neighbors','Densidad de las coordenadas|Escala adaptativa de vecindad','Uniformidad métrica no exige densidad uniforme en el espacio observado.'),
(15,'Una escala local por punto','flow','Distancias de vecinos|Calibrar ρᵢ y σᵢ|Pesos dirigidos en el grafo','Los pesos difusos no están normalizados como probabilidades por fila.'),
(17,'Una misma regla puede cambiar la vecindad','neighbors','Distancias y escalas originales|Reescalado local de vecindades','El ajuste local no recupera un tensor métrico completo.'),
(18,'El tensor métrico define productos internos','metric','g = identidad|g simétrica definida positiva','La forma cuadrática da longitudes infinitesimales positivas.'),
(20,'Pitágoras en coordenadas ortonormales','metric','Ejes ortogonales, igual unidad|Desplazamiento dx, dy','ds² = dx² + dy² en coordenadas cartesianas ortonormales.'),
(22,'Escala y ángulo de una base','metric','Base con igual escala|Base escalada u oblicua','Un término mixto expresa el producto interno de las direcciones.'),
(24,'De la matriz al elemento de longitud','flow','Desplazamiento d x|Matriz métrica g(x)|ds² = d xᵀ g(x) d x','Una matriz variable no implica necesariamente curvatura intrínseca.'),
(26,'Una medición local no es una distancia global','metric','Métrica en un punto|Longitud integrada a lo largo de un camino','La distancia geodésica minimiza longitudes de caminos.'),
(27,'Escalas de una aproximación geométrica','neighbors','Vecindario pequeño|Región global','La aproximación local debe justificarse a la escala usada.'),
(29,'Reescalar no equivale a reconstruir una variedad','flow','Distancias de entrada|Escala σᵢ y desplazamiento ρᵢ|Afinidades locales','UMAP admite distintas métricas de entrada; no solo distancia euclídea.'),
(31,'La métrica aproximadamente constante es local','metric','Parche pequeño|Variación entre parches','Un plano tangente aproxima la geometría a pequeña escala.'),
(34,'Cómo decae el peso dirigido','flow','d(xᵢ,xⱼ)|max(0, d − ρᵢ) / σᵢ|wᵢ→ⱼ = exp(−valor)','La resta de ρᵢ y la escala σᵢ cumplen papeles diferentes.'),
(36,'Analogía del mapa local','compare','Aproximar una parcela|Considerar una superficie extensa','Una aproximación local no justifica usarla a cualquier distancia.'),
(41,'Enlace local fuerte, grafo posiblemente desconectado','graph','Componente A conectada localmente|Componente B conectada localmente','Un enlace al vecino próximo no une necesariamente todas las componentes.'),
(44,'Cuerdas al vecino más cercano','graph','Un grupo de montañistas|Otro grupo de montañistas','Puede no haber puntos aislados y seguir habiendo grupos desconectados.'),
(47,'Las afinidades pueden ser asimétricas','neighbors','El punto i usa su escala|El punto j usa otra escala','Una relación de vecindad dirigida no tiene por qué ser recíproca.'),
(49,'Comparar pesos exige comparar definiciones','compare','t-SNE: probabilidades normalizadas|UMAP: pertenencias difusas','El promedio de t-SNE no prueba por sí mismo que se rompan puentes.'),
(51,'Unión difusa de dos sentidos','graph','Dos pesos dirigidos|Un peso simétrico','wᵢⱼ = u + v − uv; con 0,2 y 0,8 el resultado es 0,84.'),
(53,'Qué preserva la unión difusa','graph','Si un sentido pesa 1|La unión también pesa 1','Preservar una arista del grafo no garantiza una geometría global exacta.'),
(54,'Del vecindario al embedding','flow','Calibrar vecindades|Simetrizar el grafo|Optimizar coordenadas','La construcción del grafo y la optimización son etapas diferentes.'),
(56,'Comparar pertenencias de entrada y salida','compare','Grafo ponderado de entrada|Relaciones entre coordenadas de salida','La baja dimensión obliga a compromisos entre aristas y no aristas.'),
(58,'Una curva de afinidad en baja dimensión','qcurve','Curva q con parámetros ilustrativos|Otra elección de a y b','q = 1 / (1 + a·d²ᵇ); no se normaliza sobre todos los pares.'),
(60,'La curva objetivo de min_dist y spread','flow','Elegir min_dist y spread|Ajustar parámetros a, b|Curva suave q(d)','min_dist es una preferencia de empaquetamiento, no una restricción rígida.'),
(61,'La forma del decaimiento','qcurve','Afinidad suave ilustrativa|Otra forma de decaimiento','Las curvas ilustran parámetros; no son densidades normalizadas.'),
(63,'El parámetro a en la curva de afinidad','qcurve','Primera curva de referencia|Segunda configuración','El parámetro a modifica la escala del decaimiento en conjunto con b.'),
(64,'El exponente b modifica la forma','qcurve','Primera forma de referencia|Segunda configuración','a y b se ajustan conjuntamente; no son controles independientes exactos.'),
(66,'Empaquetamiento y visualización','neighbors','Vecindades compactas permitidas|Mayor dispersión preferida','La densidad del mapa no estima necesariamente la densidad original.'),
(68,'Entropía cruzada de pertenencias','flow','Aristas: término de atracción|No aristas: término de repulsión|Optimización con muestreo','El entrenamiento práctico no evalúa todos los pares en cada actualización.'),
(70,'La atracción depende del peso del enlace','graph','Pares con peso alto|Compromisos entre relaciones','El embedding no reproduce perfectamente todas las vecindades.'),
(72,'Repulsión mediante ejemplos negativos','graph','Aristas observadas|Pares negativos muestreados','La fuerza depende de distancia y parámetros; no es constante.'),
(73,'Usar UMAP como parte de un análisis','flow','Elegir representación y métrica|Explorar parámetros y semillas|Validar fuera del mapa','UMAP y t-SNE no garantizan distancias globales calibradas.')]
for c,t,k,l,f in umap:add(5,c,t,k,l,f)

if __name__=='__main__':
    for n,figs in FIGS.items():
        for spec in figs.values():draw(spec,n)
    print({n:len(f) for n,f in FIGS.items()})
