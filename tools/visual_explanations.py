"""Diagramas y explicaciones que acompañan a las fichas, conservadas sin cambios."""
from pathlib import Path
from html import escape
import json,math,hashlib,xml.etree.ElementTree as ET
import numpy as np
from bs4 import BeautifulSoup
from editorial import render
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'docs/assets/visuals'
BG='#191d26';PANEL='#222733';FG='#e5e7eb';MUTED='#acb8cc';BLUE='#91b9e3';GOLD='#d9c58f';GREEN='#8ed2bb';PURPLE='#b7a2ed';RED='#ed9d9d'
class Diagram:
 def __init__(self,title,desc):
  self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 760" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc><defs>']
  for name,col in [('blue',BLUE),('gold',GOLD),('green',GREEN),('purple',PURPLE),('red',RED),('muted',MUTED)]:self.parts.append(f'<marker id="a-{name}" markerWidth="9" markerHeight="9" refX="8" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8" fill="{col}"/></marker>')
  self.parts.append(f'</defs><rect width="1400" height="760" rx="18" fill="{BG}"/><style>text{{font-family:DejaVu Sans,Arial,sans-serif}}path,line,polyline{{stroke-linecap:round;stroke-linejoin:round}}</style>')
  self.text(50,58,title,32,GOLD)
 def text(self,x,y,s,size=23,col=FG,anchor='start'):
  self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anchor}">{escape(str(s))}</text>')
 def rect(self,x,y,w,h,col=PANEL,stroke=MUTED,r=9):self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{col}" stroke="{stroke}" stroke-width="2"/>')
 def box(self,x,y,w,h,label,col=BLUE):
  self.rect(x,y,w,h,stroke=col);self.text(x+w/2,y+h/2+8,label,24,col,'middle')
 def line(self,x1,y1,x2,y2,col=MUTED,width=3,dashed=False):self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="{width}"'+(' stroke-dasharray="7 6"' if dashed else '')+'/>')
 def arrow(self,pts,color='blue',dashed=False):
  colors={'blue':BLUE,'gold':GOLD,'green':GREEN,'purple':PURPLE,'red':RED,'muted':MUTED}
  self.parts.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{colors[color]}" stroke-width="3.5" marker-end="url(#a-{color})"'+(' stroke-dasharray="7 6"' if dashed else '')+'/>')
 def circle(self,x,y,r,label='',col=GOLD):
  self.parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{PANEL}" stroke="{col}" stroke-width="3"/>');self.text(x,y+8,label,26,col,'middle')
 def matrix(self,x,y,a,cell=55,label='',colors=None,fmt='.2g'):
  a=np.asarray(a)
  if label:self.text(x,y-22,label,24,GOLD)
  for i in range(a.shape[0]):
   for j in range(a.shape[1]):
    val=float(a[i,j]);color=(colors[j%len(colors)] if colors else BLUE)
    self.rect(x+j*cell,y+i*cell,cell-3,cell-3,col=PANEL,stroke=color,r=2)
    self.text(x+j*cell+cell/2-2,y+i*cell+cell/2+6,format(val,fmt),20,color,'middle')
 def vector(self,x,y,values,label,col=BLUE,cell=64):self.matrix(x,y,[values],cell,label,[col])
 def foot(self,s):self.text(50,716,s,21,MUTED)
 def finish(self):return ''.join(self.parts)+'</svg>'
 def plot(self,x,y,w,h,xs,ys,domain,limits,col=BLUE,label=''):
  xmin,xmax=domain;ymin,ymax=limits
  xy=[(x+(float(a)-xmin)*w/(xmax-xmin),y+h-(float(b)-ymin)*h/(ymax-ymin)) for a,b in zip(xs,ys)]
  self.line(x,y+h,x+w,y+h);self.line(x,y,x,y+h)
  self.parts.append('<polyline points="'+' '.join(f'{a:.2f},{b:.2f}' for a,b in xy)+f'" fill="none" stroke="{col}" stroke-width="4"/>')
  if label:self.text(x,y-18,label,24,col)

def sm(x):
 x=np.asarray(x,float);e=np.exp(x-x.max(axis=-1,keepdims=True));return e/e.sum(axis=-1,keepdims=True)

# Cada ficha enlaza un concepto gráfico y una explicación del ejemplo concreto.
SPECS={}
def spec(keys,kind,title,desc,steps):
 for key in keys.split():SPECS[key]={'kind':kind,'title':title,'desc':desc,'steps':steps}

spec('fft-exact fft','fft','Una mariposa FFT: dos entradas, dos salidas','Diagrama de la combinación de DFT pares e impares para cuatro muestras.',[
 'La entrada de ejemplo es [1, 2, 3, 4]. Los índices pares forman [1, 3] y los impares [2, 4]. Sus DFT de dos puntos dan E=[4, −2] y O=[6, −2].',
 'La mariposa dibujada usa k=1 y N=4. El factor W₄¹=−i rota O[1]=−2 y produce T=2i. La misma T llega a las dos ramas: arriba se suma; abajo se resta.',
 'Se obtienen X[1]=−2+2i y X[3]=−2−2i. La otra mariposa, con k=0, produce X[0]=10 y X[2]=−2. Reutilizar estas combinaciones da el ahorro de la FFT; conservar los coeficientes complejos permite invertir la DFT.' ])
spec('weighted-sum dot','mix','Los pesos mezclan vectores completos','Tres vectores de valor contribuyen a una suma ponderada de dos coordenadas.',[
 'Cada columna representa un valor: v₀=(2,0), v₁=(0,2) y v₂=(2,2). Los pesos 0.2, 0.5 y 0.3 suman uno.',
 'Cada peso multiplica todas las coordenadas de su valor. Las contribuciones son (0.4,0), (0,1) y (0.6,0.6); al sumarlas se obtiene z=(1,1.6).',
 'Los scores se calculan antes y softmax los normaliza. La figura se centra en la mezcla posterior: un peso aislado no determina la dirección final, que también depende de los valores.' ])
spec('hard-attention sampling','sample','Elegir una posición de una distribución','Una distribución categórica se convierte en una selección one-hot y en un vector elegido.',[
 'Las barras azules representan probabilidades [0.2,0.5,0.3]. En el muestreo categórico solo se elige una posición en cada extracción; la ilustración muestra que salió la posición 1.',
 'El indicador [0,1,0] deja pasar únicamente v₁. No es la mezcla 0.2v₀+0.5v₁+0.3v₂: el contexto de esta muestra es v₁.',
 'La ruta discontinua señala que entrenar una elección discreta necesita un estimador, como REINFORCE, o una relajación. El diagrama no asigna una derivada ordinaria al índice ni supone que muestrear elimine el coste de todos los scores.' ])
spec('softmax-numeric word2vec-score','softmax','De scores a probabilidades normalizadas','Tres barras de scores se transforman en tres probabilidades positivas que suman uno.',[
 'Se usan los scores [3.2,−1.5,4.0]. Restar su máximo produce [−0.8,−5.5,0] y conserva exactamente el softmax.',
 'Las exponenciales son aproximadamente [0.4493,0.00409,1]. Se divide cada una por su suma, aproximadamente 1.4534.',
 'El resultado es [0.3092,0.0028,0.6880], salvo redondeo. Son probabilidades sobre los candidatos del eje elegido; los scores iniciales no eran probabilidades.' ])
spec('cbow','cbow','Skip-gram y CBOW: flechas de predicción','Dos grafos muestran cómo cambia la dirección entre centro y contextos.',[
 'En la mitad izquierda, la palabra central alimenta varias predicciones de contexto: esa es la dirección de Skip-gram.',
 'En la derecha, los vectores de contexto convergen en una media y el clasificador predice el centro: esa es la dirección de CBOW. El centro no se incluye entre sus propios contextos.',
 'Las flechas representan relaciones de la tarea de entrenamiento, no una creación literal de palabras a partir de otras ni una garantía de cercanía semántica.' ])
spec('glove weight ratios exp gradient symmetry word2vec-glove','glove','De ventanas de texto a una matriz de conteos','Una oración aporta pares observados, que se acumulan en una matriz centro-contexto.',[
 'La ventana selecciona vecinos del token central. Repetir el recorrido por el corpus acumula coocurrencias en filas de centros y columnas de contextos.',
 'En la matriz ilustrativa, la celda resaltada tiene Xᵢⱼ=4. Ese par aporta un término al ajuste de log Xᵢⱼ; una celda con cero no se evalúa como log(0). Los números son sintéticos.',
 'El modelo aprende tablas de centros y contextos y sus sesgos. Esta figura muestra el origen de los datos; la ficha superior especifica el aspecto concreto del objetivo, sus pesos, cocientes o gradientes.' ])
# Variantes específicas: gráficos dedicados para no confundir conceptos distintos.
SPECS['weight']['kind']='weight';SPECS['weight']['title']='El peso de GloVe crece y luego se satura';SPECS['weight']['desc']='Curva de ponderación para alpha 0.75 y xmax 100.'
SPECS['weight']['steps']=['El eje horizontal cuenta coocurrencias positivas x. Se grafica h(x)=min((x/100)^0.75,1), con parámetros elegidos para el ejemplo.','Hasta x=100 el peso aumenta; a partir de ese umbral queda en uno. Por ejemplo h(25)≈0.354 y h(100)=h(200)=1.','La saturación afecta al peso, no limita el residual ni la pérdida total. Los pares con x=0 se excluyen antes de evaluar el logaritmo.']
SPECS['ratios']['kind']='ratios';SPECS['ratios']['title']='Comparar dos centros con el mismo contexto';SPECS['ratios']['desc']='Dos series de barras y sus cocientes usan las cifras redondeadas de la ficha de GloVe.'
SPECS['ratios']['steps']=['Las dos barras de cada grupo comparan P(k|ice) y P(k|steam), manteniendo fijo el contexto k. La altura se muestra en escala logarítmica para que se vean valores pequeños.','El cociente es mayor que uno para solid, menor que uno para gas y cercano a uno en water y fashion. Esto describe proporciones de coocurrencia de ese corpus, no una regla del significado.','Los cocientes calculados aquí usan los valores ya redondeados de la ficha. Por eso pueden diferir de los cocientes publicados calculados con más precisión.']
SPECS['exp']['kind']='exp';SPECS['exp']['title']='Restar logaritmos equivale a dividir valores';SPECS['exp']['desc']='Un ejemplo escalar con a=log 8 y b=log 2 conecta diferencia y cociente.'
SPECS['exp']['steps']=['La rama superior parte de a=ln 8 y b=ln 2. Al restar, a−b=ln 4.','La exponencial devuelve exp(a−b)=4. La rama inferior obtiene lo mismo con exp(a)/exp(b)=8/2.','Es una identidad escalar exacta. No normaliza una distribución: para eso todavía haría falta dividir por una suma de exponenciales, como en softmax.']
SPECS['gradient']['kind']='gradient';SPECS['gradient']['title']='Un paso cambia el producto punto';SPECS['gradient']['desc']='Dos pasos en direcciones opuestas al cambiar el signo del residual de GloVe.'
SPECS['gradient']['steps']=['Se fija u=(1,0), así que uᵀv es la coordenada horizontal de v. El residual es predicción menos objetivo logarítmico.','Con residual negativo, descenso de gradiente desplaza v en dirección +u y aumenta su producto punto. Con residual positivo, el paso va en dirección −u y lo reduce.','Las flechas muestran una actualización con u fijo y un optimizador de descenso simple. No afirman que la distancia euclídea entre las puntas de u y v siempre disminuya; otros parámetros y optimizadores también intervienen.']
SPECS['symmetry']['kind']='symmetry';SPECS['symmetry']['title']='Conteos simétricos, parámetros distintos';SPECS['symmetry']['desc']='Una matriz de conteos simétrica no obliga a igualar las tablas aprendidas.'
SPECS['symmetry']['steps']=['La matriz de ejemplo es simétrica: su celda (i,j) coincide con (j,i). Eso puede surgir al usar ventanas simétricas.','A la derecha aparecen dos tablas separadas, W para centros y W̃ para contextos. La igualdad de conteos no impone una restricción W=W̃ al entrenamiento.','El dibujo distingue datos y parámetros. Una extracción frecuente suma los dos vectores de cada palabra, pero esa elección debe declararse y no convierte las tablas en idénticas.']
SPECS['word2vec-glove']['kind']='comparison';SPECS['word2vec-glove']['title']='Dos objetivos a partir de ventanas de contexto';SPECS['word2vec-glove']['desc']='Un corpus se bifurca hacia pares predictivos o conteos agregados.'
SPECS['word2vec-glove']['steps']=['Las dos ramas parten del mismo tipo de datos: tokens y ventanas de contexto del corpus.','Word2Vec usa pares o conjuntos de contextos en una tarea predictiva. GloVe acumula conteos y ajusta un objetivo ponderado sobre sus logaritmos.','La comparación describe objetivos, no un ranking de velocidad o calidad. El corpus, el muestreo y la implementación influyen en el resultado.']
spec('cosine','cosine','Ángulo y longitud son propiedades distintas','Tres pares de flechas muestran cosenos uno, cero y menos uno.',[
 'En el primer plano, las flechas tienen la misma dirección y longitudes distintas: su coseno es uno.',
 'En el segundo forman un ángulo recto y el coseno es cero. En el tercero apuntan en direcciones opuestas y el coseno es menos uno.',
 'Estas son relaciones geométricas entre vectores no nulos. Para leerlas como relaciones lingüísticas hace falta un modelo y una evaluación; coseno negativo no significa automáticamente antonimia.' ])
spec('onehot','onehot','Una consulta selecciona una fila del embedding','Un indicador one-hot destaca una fila de una tabla de tres tokens.',[
 'El token elegido tiene índice 1 en un vocabulario de tres entradas. Su indicador es [0,1,0].',
 'La tabla E tiene una fila por token y dos coordenadas por embedding. La selección devuelve E[1]=[0.3,0.8] en este ejemplo sintético.',
 'Multiplicar Eᵀ por el one-hot da el mismo resultado que consultar la fila directamente. La tabla se aprende; no hace falta construir el indicador completo en una implementación habitual.' ])
spec('subword-limits','subword','Fragmentos compartidos, vector compuesto','Dos palabras comparten un n-grama que apunta a un bucket de parámetros.',[
 'Se ilustran solo algunos n-gramas de «gato» y «gatos», no una segmentación exhaustiva ni una separación en morfemas. Ambas cadenas contienen el fragmento «gat».',
 'El fragmento compartido reutiliza parámetros. En fastText se aplica hashing a buckets, por lo que fragmentos distintos también pueden colisionar; no hay un vector independiente garantizado para cada fragmento.',
 'Combinar fragmentos permite construir un vector para una palabra nueva. La utilidad semántica depende de los datos y de los fragmentos aprendidos, no queda garantizada por la composición.' ])
spec('bpe-limits','bpe','BPE: reemplazar un par adyacente por una unidad','Una secuencia de caracteres muestra dos fusiones sucesivas durante la tokenización.',[
 'El ejemplo parte de las unidades [g,a,t,o]. Suponemos que el vocabulario aprendido contiene primero la fusión (g,a)→ga.',
 'La siguiente fusión ilustrada convierte (ga,t)→gat y deja [gat,o]. En entrenamiento se eligen pares mediante frecuencias; al tokenizar se aplica el orden de fusiones aprendido.',
 'Es un ejemplo de la mecánica, no una lista real de fusiones aprendidas de un corpus. Las unidades resultantes no tienen por qué coincidir con morfemas.' ])
spec('position-limits','rope','Una posición rota cada pareja de coordenadas','Cuatro flechas de igual norma muestran rotaciones sucesivas de un vector fijo.',[
 'Se mantiene fijo el contenido q=(1,0) y se cambia la posición p. La pareja se rota un ángulo pθ, con θ=π/6 en este ejemplo.',
 'Las puntas de las flechas permanecen sobre una circunferencia: la norma no cambia. La igualdad expresa isometría, no una conservación demostrada del significado.',
 'Al rotar consulta y clave, el factor de rotación de su producto punto depende de la diferencia de posiciones. Con contenido distinto, los vectores de tokens distintos no siguen necesariamente esta misma trayectoria.' ])
spec('pe ape pe-add sum','position','Posición y contenido se combinan por coordenadas','Bloques coloreados muestran suma y concatenación de dos vectores de dos componentes.',[
 'El contenido ilustrativo e=(1,−1) y la posición p=(0.5,1) tienen el mismo ancho. La suma coordenada a coordenada da (1.5,0).',
 'Concatenar conserva las dos parejas como cuatro coordenadas: [1,−1,0.5,1]. Es una operación distinta que aumenta el ancho; podría seguirla una proyección aprendida.',
 'Los valores de esta figura son sintéticos. La suma puede cambiar norma y ángulo sin que eso demuestre daño semántico; la arquitectura se entrena con su forma de incorporar la posición.' ])
SPECS['pe']['kind']='pe';SPECS['pe']['title']='Una posición, varios pares de frecuencias';SPECS['pe']['desc']='Dos parejas seno-coseno de distintas frecuencias se muestrean en una posición común.'
SPECS['pe']['steps']=['Las curvas muestran dos parejas: sin(pω) y cos(pω), con ω=1 y ω=0.2 para facilitar la lectura. Son frecuencias ilustrativas; la ficha superior da la regla 10000^(−2i/d).','La línea vertical fija p=3. En cada frecuencia se toman dos valores y se intercalan las componentes seno y coseno del mismo par.','Las parejas cambian a distintas velocidades. Ninguna componente representa un bit ni una función lingüística fija; el orden de las dimensiones debe mantenerse coherente con el modelo.']
spec('linear-map','linear','Una matriz transforma todo el plano','Un cuadrado se convierte en un rectángulo al aplicar una escala distinta por coordenada.',[
 'El cuadrado de la izquierda tiene vértices (0,0), (1,0), (1,1) y (0,1). Se aplica W=diag(2,0.5).',
 'La primera coordenada se duplica y la segunda se reduce a la mitad. El origen se conserva y el cuadrado se convierte en un rectángulo.',
 'Es un ejemplo de transformación lineal, no una rotación. Una matriz aprendida general puede mezclar coordenadas y cambiar normas y ángulos; añadir un sesgo daría una transformación afín.' ])
spec('qkv','qkv','Una entrada, tres transformaciones aprendidas','Una matriz de entrada se bifurca a consultas, claves y valores antes de comparar y mezclar.',[
 'Las tres flechas parten de X, pero atraviesan matrices de parámetros distintas: WQ, WK y WV. Producen las activaciones Q, K y V.',
 'Q y K intervienen en los scores QKᵀ/√dₖ. Softmax se aplica por fila sobre claves válidas, formando A.',
 'La salida se obtiene con AV. Una fila de salida corresponde a cada consulta. Las matrices W son parámetros; Q, K, V y A cambian con la entrada.' ])
spec('additive-attention','additive','Dos proyecciones se reúnen antes de puntuar','Dos ramas de query y key se proyectan, suman, pasan por tanh y se contraen a un score.',[
 'La consulta q y la clave k pueden tener anchos distintos. Wq y Wk las llevan al mismo ancho intermedio, para poder sumarlas.',
 'La suma, con el sesgo si se usa, pasa por tanh. El vector aprendido v convierte esa representación intermedia en un score escalar.',
 'Se repite la puntuación para las claves y softmax normaliza el conjunto. La suma de proyecciones no mide por sí sola una distancia o un ángulo entre palabras.' ])
spec('local-window','local','Atenuar posiciones lejanas y normalizar','Barras de atención global se combinan con una campana gaussiana centrada en la posición dos.',[
 'La fila superior usa scores [1,3,2,0]. El softmax global da aproximadamente [0.0871,0.6439,0.2369,0.0321].',
 'La curva marca una preferencia gaussiana centrada en 2, con σ=0.7. Al sumar su logaritmo a los scores y aplicar softmax se obtienen aproximadamente [0.0031,0.4815,0.4915,0.0240].',
 'Aquí se calculan todas las posiciones y luego se atenúan: es una variante suave global. Para ahorrar el cálculo de scores mediante atención local real hay que restringir las posiciones evaluadas; multiplicar por la gaussiana sin renormalizar tampoco asegura suma uno.' ])
spec('attention-experiment','experiment','Un mapa de atención no identifica una explicación causal','Dos matrices de pesos distintas se muestran junto al mismo resultado ilustrativo.',[
 'Las dos matrices sintéticas tienen filas normalizadas, pero una concentra pesos y la otra los reparte más. La intensidad del color representa el peso.',
 'Las dos pueden acompañar la misma etiqueta de salida en una ilustración. Esa coincidencia no establece que los modelos tengan el mismo funcionamiento interno ni demuestra mejor comprensión en el mapa más nítido.',
 'Para estudiar los mecanismos hacen falta datos, entrenamiento, máscaras y evaluaciones comparables. Este dibujo explica cómo leer un mapa, no presenta dos experimentos entrenados.' ])
spec('intra-history','history','Memoria recurrente y autoatención tienen rutas distintas','Una ruta temporal recurrente se contrasta con una matriz de atención dentro de la secuencia.',[
 'La fila superior procesa pasos en orden y conserva una dependencia entre actualizaciones. En LSTMN, la consulta a estados de memoria forma parte de ese procesamiento recurrente.',
 'La fila inferior ilustra atención entre posiciones de una misma secuencia mediante una matriz. En un Transformer puede calcularse en paralelo durante entrenamiento con la máscara adecuada.',
 'La comparación distingue arquitecturas. La self-attention no exige una LSTM, y el paralelismo del entrenamiento no elimina la dependencia autorregresiva durante generación.' ])
spec('rnn-memory','rnn','Las compuertas controlan la ruta de la celda','Dos productos se reúnen en una suma para actualizar la celda de una LSTM.',[
 'La ruta azul transporta c anterior y la multiplica por la compuerta de olvido f. La ruta violeta multiplica la propuesta g por la compuerta de entrada i.',
 'La suma produce c nuevo=f⊙c anterior+i⊙g. Después se calcula h nuevo=o⊙tanh(c nuevo). Los productos son elemento a elemento.',
 'La ruta aditiva ayuda a transportar información y gradientes, pero las compuertas y el resto de la red siguen influyendo. El dibujo no garantiza memoria ilimitada ni ausencia de gradientes que crecen o se desvanecen.' ])
spec('decomposable','decomposable','Alinear, comparar y reunir evidencia','Un grafo bipartito enlaza tokens de dos secuencias y conduce a comparaciones y un clasificador.',[
 'Attend calcula compatibilidades entre tokens de A y B. Las flechas de distinto grosor representan pesos ilustrativos de alineación suave, normalizados en la dirección correspondiente.',
 'Compare recibe cada token junto con su alineación de la otra secuencia. Una red aprendida produce características de comparación; no se asignan detectores lógicos fijos a sus neuronas.',
 'Aggregate suma las representaciones de cada lado y las entrega al clasificador. La ilustración muestra el flujo de Parikh et al.; no afirma que un peso alto pruebe implicación o contradicción.' ])
spec('decode','decode','Los logits se convierten en una elección de token','Barras de probabilidades destacan la alternativa de mayor valor antes de generar el token.',[
 'El estado del decoder atraviesa una proyección que produce logits sobre el vocabulario. Softmax los convierte en probabilidades sobre tokens.',
 'El ejemplo usa probabilidades [0.1,0.6,0.3]. La flecha dorada ilustra greedy decoding: elige el token B, que tiene el máximo.',
 'La distribución también puede usarse para muestrear, y beam search mantiene hipótesis. El dibujo de la elección greedy no convierte esa regla en la única forma de generación.' ])
spec('cnn-shapes','cnn','Un filtro produce un canal de salida','Tres mapas de entrada se combinan con un filtro de tres planos para obtener un mapa de salida.',[
 'El ejemplo tiene tres canales de entrada, espacio 5×5 y un filtro con tres planos 3×3. En cada ubicación se suman los productos sobre espacio y canales.',
 'Con stride uno, dilatación uno y sin padding, el resultado espacial es 3×3. Un filtro completo produce un canal de salida; dos filtros producirían dos canales.',
 'El diagrama omite el eje del batch. Los pesos se comparten entre posiciones; el número de canales no se obtiene sumando la altura y el ancho ni corresponde necesariamente a colores después de la entrada.' ])
spec('equivariance','equivariance','Permutar la entrada permuta las filas de salida','Dos filas de tokens pasan por el mismo bloque de self-attention y conservan su correspondencia.',[
 'La primera fila ordena A,B,C y produce zA,zB,zC. En la segunda se cambia el orden a C,A,B.',
 'Sin información posicional ni una máscara que fije el orden, la misma self-attention devuelve las filas correspondientes como zC,zA,zB. Los colores siguen al token.',
 'Esto es equivariancia: la salida se reordena con la entrada. No significa salida idéntica. La codificación posicional y una máscara causal fija cambian los supuestos de este dibujo.' ])
spec('batchnorm','bn','Normalizar por canal y aplicar escala y sesgo','Puntos de un canal atraviesan una normalización y una transformación afín.',[
 'En entrenamiento de BatchNorm2d se reúnen, por canal, valores del batch y de sus posiciones espaciales. Los cuatro puntos del ejemplo son [1,2,3,4].',
 'Con media 2.5 y varianza poblacional 1.25, la normalización ideal sin epsilon da aproximadamente [−1.342,−0.447,0.447,1.342]. La implementación añade epsilon al denominador.',
 'Después actúan gamma y beta aprendidos. Durante inferencia, el comportamiento habitual usa estadísticas móviles; la configuración puede cambiarlo. La línea de puntos no implica normalizar cada píxel por separado.' ])
spec('loss-gradient','loss','El signo de la pérdida fija la dirección del paso','Un eje muestra cómo aumenta la probabilidad observada al descender una pérdida negativa logarítmica.',[
 'La curva representa L=−ln p para 0<p≤1. Una probabilidad pequeña del contexto observado implica una pérdida grande.',
 'La flecha señala la dirección de menor pérdida, hacia probabilidades mayores. En Word2Vec el optimizador mueve parámetros y sus scores; no modifica p de forma independiente.',
 'Para el vector central, el gradiente de la pérdida es suma_j p_j u_j menos u observado. El optimizador resta ese gradiente. Maximizar log p usa el signo contrario con un paso de ascenso equivalente.' ])
spec('relu-exact','relu','ReLU conserva positivos y anula negativos','Un gráfico cartesiano y cinco puntos muestran max(0,x).',[
 'La línea dorada permanece en cero cuando x es negativo. A partir de cero sigue la diagonal y=x.',
 'Las muestras [−2,−1,0,1,2] se transforman en [0,0,0,1,2]. La operación actúa por coordenada, sin una rotación matricial.',
 'Fuera del origen, la derivada es cero en la rama negativa y uno en la positiva. En una red, su interpretación depende del entrenamiento; la curva por sí sola no codifica contradicciones lingüísticas.' ])
spec('dft fourier-time','fourier','La DFT compleja conserva magnitud y fase','Una onda pasa a un plano complejo y una flecha de inversa vuelve a las muestras.',[
 'La izquierda muestra una señal discreta sintética. La DFT completa la expresa mediante coeficientes complejos; la flecha del plano separa parte real e imaginaria.',
 'La longitud de un coeficiente es su magnitud y su ángulo es su fase. Conservar ambas permite aplicar la transformada inversa y recuperar las muestras, salvo precisión numérica.',
 'Mostrar solo magnitud es una representación derivada que descarta fase. Para localizar cambios a lo largo de una grabación se emplean ventanas y un índice temporal, como en STFT.' ])
spec('window','window','Una ventana cambia la contribución de los bordes','Curvas de Hann y Hamming se comparan sobre la misma secuencia de índices.',[
 'Las curvas son ventanas simétricas de 64 muestras. La Hann llega a cero en ambos extremos; la Hamming termina en 0.08.',
 'Cada curva multiplica la señal muestra a muestra antes de la DFT. Reducir las discontinuidades del recorte cambia el compromiso entre lóbulo principal y lóbulos laterales.',
 'No desaparece toda fuga espectral. Las versiones periódicas para análisis por frames usan otra convención en el denominador; este dibujo corresponde a las fórmulas simétricas de la ficha.' ])
spec('db','db','La escala logarítmica hace visibles relaciones pequeñas','Dos conjuntos de barras representan las mismas potencias en escala lineal y en dB relativos.',[
 'Se comparan potencias [1,0.01,0.0001]. En el panel lineal, las dos menores apenas se ven frente a la primera.',
 'Con referencia de potencia uno, sus niveles son [0,−20,−40] dB. Cada descenso de 20 dB en este ejemplo equivale a dividir la potencia por cien.',
 'Los niveles son relativos a una referencia declarada, no una calibración acústica automática ni una medida universal de sonoridad. Si se trabaja con amplitudes equivalentes, se usa 20 log10(A/Aref).' ])
spec('logmel-pipeline mel-scale','mel','De frecuencias lineales a bandas Mel','Un espectro de potencia atraviesa filtros triangulares y produce potencias por banda antes del logaritmo.',[
 'Las barras de la izquierda representan potencia por bin de frecuencia. En el centro, cada filtro triangular pondera varios bins; se suman sus contribuciones para formar una banda.',
 'La separación de filtros aumenta en Hz a frecuencias altas. La cantidad de bandas y su normalización dependen de la configuración; el dibujo muestra solo unas pocas para que se vea el mecanismo.',
 'Para obtener log-Mel se aplica un suelo positivo y después el logaritmo a las potencias de banda. Filtrar después de tomar logaritmos da, en general, otro resultado. La escala Mel es una aproximación perceptiva, no una réplica exacta del oído.' ])
spec('source-filter','source','Una fuente atraviesa un filtro del tracto vocal','Un tren de pulsos entra en un filtro con resonancias y produce una onda modificada.',[
 'La izquierda ilustra una excitación periódica simplificada de un sonido sonoro. La voz también puede tener excitaciones ruidosas, por ejemplo turbulencia.',
 'El filtro representa la respuesta del tracto vocal: refuerza o atenúa regiones del espectro. La salida conserva una organización temporal y espectral influida por ambos componentes.',
 'Es un modelo simplificado del habla, no una separación exacta en cualquier grabación. La información lingüística no reside exclusivamente en el filtro, y ASR no exige siempre aislarlo.' ])

def bars(d,x,y,values,labels=None,width=330,height=210,col=BLUE,lo=0,hi=None):
 values=np.asarray(values,float);hi=max(float(values.max()),1e-9) if hi is None else hi
 zero=y+height-(0-lo)*height/(hi-lo)
 d.line(x,zero,x+width,zero)
 step=width/len(values)
 for j,val in enumerate(values):
  yy=y+height-(val-lo)*height/(hi-lo);hh=abs(yy-zero)
  d.rect(x+j*step+step*.2,min(yy,zero),step*.6,max(2,hh),col=col,stroke=col,r=3)
  d.text(x+j*step+step/2,yy-12 if val>=0 else yy+28,f'{val:.3g}',21,col,'middle')
  if labels:d.text(x+j*step+step/2,y+height+38,labels[j],21,FG,'middle')

def draw(key):
 s=SPECS[key];kind=s['kind'];d=Diagram(s['title'],s['desc'])
 if kind=='fft':
  d.vector(60,140,[1,2,3,4],'1 · Muestras x[n]',BLUE)
  d.arrow([(185,210),(185,270)],'blue');d.vector(60,310,[1,3],'Índices pares',BLUE)
  d.vector(60,470,[2,4],'Índices impares',PURPLE)
  d.arrow([(315,172),(350,172),(350,440),(210,440),(210,500),(192,500)],'purple')
  d.arrow([(190,342),(385,342),(385,245),(445,245)],'blue');d.text(285,320,'DFT₂',23,BLUE,'middle')
  d.arrow([(190,505),(445,505)],'purple');d.text(320,480,'DFT₂',23,PURPLE,'middle')
  d.text(450,135,'2 · Mariposa con N=4, k=1',27,GOLD)
  d.box(450,210,190,70,'E[1] = −2',BLUE);d.box(450,470,190,70,'O[1] = −2',PURPLE)
  d.circle(750,505,42,'×',PURPLE);d.arrow([(640,505),(708,505)],'purple');d.text(750,590,'W₄¹ = −i',23,PURPLE,'middle')
  d.arrow([(790,505),(850,505)],'green');d.text(850,560,'T = 2i',23,GREEN)
  d.circle(1000,245,35,'+',GOLD);d.circle(1000,505,35,'−',GOLD)
  d.arrow([(640,245),(965,245)],'blue');d.arrow([(675,245),(675,395),(1000,395),(1000,470)],'blue')
  d.arrow([(875,505),(910,505),(910,320),(1000,320),(1000,280)],'green');d.arrow([(875,505),(965,505)],'green')
  d.arrow([(1035,245),(1110,245)],'gold');d.box(1120,210,230,70,'X[1]=−2+2i',GOLD)
  d.arrow([(1035,505),(1110,505)],'gold');d.box(1120,470,230,70,'X[3]=−2−2i',GOLD)
  d.text(1140,340,'Arriba: E + T',23);d.text(1140,400,'Abajo: E − T',23)
  d.foot('Las ramas azules reutilizan E; las verdes reutilizan la misma T. El signo inferior resta T a E.')
 elif kind=='mix':
  vals=[[2,0],[0,2],[2,2]];weights=[.2,.5,.3]
  for j,(v,w) in enumerate(zip(vals,weights)):
   y=170+j*160;d.vector(70,y,v,f'v{j}',[BLUE,PURPLE,GREEN][j]);d.arrow([(210,y+32),(330,y+32)],'blue')
   d.circle(380,y+32,35,'×');d.text(380,y-38,f'α{j}={w}',24,GOLD,'middle')
   d.arrow([(415,y+32),(510,y+32)],'gold');d.vector(530,y,np.array(v)*w,'Contribución',GREEN)
   d.arrow([(660,y+32),(810,y+32),(810,370),(875,370)],'green')
  d.circle(915,370,40,'Σ');d.arrow([(955,370),(1060,370)],'gold');d.vector(1080,338,[1,1.6],'z',GOLD)
  d.foot('Ejemplo de dos coordenadas: 0.2(2,0) + 0.5(0,2) + 0.3(2,2) = (1,1.6).')
 elif kind in ['softmax','sample','decode']:
  if kind=='softmax':
   d.text(70,180,'1 · Scores',28,BLUE);bars(d,70,260,[3.2,-1.5,4],['0','1','2'],280,230,lo=-2,hi=5)
   d.arrow([(390,375),(520,375)],'gold');d.box(540,300,270,140,'exp(s − max(s))',GOLD);d.text(675,490,'dividir por la suma',23,GOLD,'middle')
   d.arrow([(820,375),(940,375)],'green');bars(d,980,260,sm([3.2,-1.5,4]),['0','1','2'],330,230,GREEN,hi=1)
   d.text(980,180,'2 · Probabilidades',28,GREEN);d.foot('Los valores de probabilidad mostrados se redondean; la normalización se realiza antes del redondeo.')
  else:
   prob=[.2,.5,.3] if kind=='sample' else [.1,.6,.3];bars(d,70,230,prob,['A','B','C'],370,270,hi=1)
   d.text(70,160,'Distribución sobre 3 opciones',26,BLUE)
   d.arrow([(480,365),(590,365)],'gold');d.circle(650,365,55,'azar' if kind=='sample' else 'máx',GOLD)
   d.arrow([(705,365),(820,365)],'gold');d.vector(840,235,[0,1,0],'Selección ilustrada',GOLD)
   d.arrow([(935,325),(935,470)],'gold');d.box(820,500,380,80,'contexto = v₁' if kind=='sample' else 'siguiente token = B',GREEN)
   if kind=='sample':d.arrow([(935,600),(935,655),(650,655),(650,440)],'purple',True)
   d.foot('El sorteo mostrado es una muestra posible; no siempre sale B.' if kind=='sample' else 'Se muestra la regla greedy. Muestreo y beam search emplean otras decisiones de generación.')
 elif kind=='cbow':
  d.text(85,150,'Skip-gram',30,BLUE);d.box(70,325,170,80,'centro',BLUE)
  for j in range(3):
   y=190+j*160;d.box(420,y,190,70,f'contexto {j}',GREEN);d.arrow([(240,365),(350,365),(350,y+35),(420,y+35)],'blue')
  d.line(700,140,700,640,MUTED,2,True);d.text(780,150,'CBOW',30,PURPLE)
  for j in range(3):
   y=190+j*160;d.box(750,y,180,70,f'contexto {j}',GREEN);d.arrow([(930,y+35),(980,y+35),(980,365),(1020,365)],'green')
  d.circle(1060,365,40,'μ',GOLD);d.arrow([(1100,365),(1170,365)],'gold');d.box(1175,325,180,80,'centro',PURPLE)
  d.foot('μ es la media de los contextos válidos. Las dos mitades representan tareas predictivas diferentes.')
 elif kind=='glove':
  for j,w in enumerate(['el','gato','come','pescado']):d.box(60+j*210,160,180,65,w,GOLD if j==1 else BLUE)
  d.text(270,270,'centro',23,GOLD);d.arrow([(365,225),(650,365)],'gold')
  a=[[0,4,1],[4,0,2],[1,2,0]];d.matrix(650,390,a,75,'Conteos ilustrativos Xᵢⱼ')
  d.text(620,430,'i',24,GOLD);d.text(895,375,'j',24,GOLD)
  d.arrow([(910,500),(1030,500)],'gold');d.box(1040,460,290,90,'Xᵢⱼ > 0 → log Xᵢⱼ',GREEN)
  d.text(80,430,'Recorrer ventanas',26,BLUE);d.text(80,480,'Acumular pares',26,BLUE);d.text(80,530,'Ajustar el objetivo',26,BLUE)
  d.foot('La tabla no proviene de esta única oración: es un ejemplo de conteos acumulados de un corpus ficticio.')
 elif kind=='weight':
  xs=np.linspace(.1,200,250);ys=np.minimum((xs/100)**.75,1)
  d.plot(160,200,1050,340,xs,ys,(0,200),(0,1.15),GOLD,'h(x) = min((x/100)^0.75, 1), para x > 0')
  for x,y in [(25,(.25)**.75),(100,1),(200,1)]:
   xx=160+x*1050/200;yy=540-y*340/1.15;d.circle(xx,yy,7,'',GOLD);d.text(xx,yy-22,f'({x}, {y:.3g})',22,GOLD,'middle')
  d.text(150,580,'0',22);d.text(685,580,'100',22);d.text(1200,580,'200',22);d.text(700,635,'Coocurrencias x',26,FG,'middle');d.foot('Se satura el peso h(x); el residual y la pérdida pueden seguir creciendo.')
 elif kind=='ratios':
  p=np.array([1.9e-4,6.6e-5,3e-3,1.7e-5]);q=np.array([2.2e-5,7.8e-4,2.2e-3,1.8e-5])
  names=['solid','gas','water','fashion'];d.text(70,145,'Azul: P(k|ice)     Violeta: P(k|steam)',26,FG)
  d.line(110,510,1290,510);d.text(80,190,'10⁻²',21);d.text(80,520,'10⁻⁵',21)
  for j,(a,b,name) in enumerate(zip(p,q,names)):
   x=200+j*290
   for off,v,col in [(-35,a,BLUE),(35,b,PURPLE)]:
    h=(math.log10(v)+5)*105;d.rect(x+off,510-h,52,max(h,2),col,col,2)
   d.text(x+25,560,name,24,FG,'middle');d.text(x+25,630,f'ratio ≈ {a/b:.3g}',25,GOLD,'middle')
  d.foot('Eje vertical logarítmico. Cocientes calculados con las probabilidades redondeadas de la ficha.')
 elif kind=='exp':
  for y,labels in [(210,['a = ln 8','b = ln 2','a − b = ln 4','exp → 4']),(460,['exp(a) = 8','exp(b) = 2','8 / 2','resultado: 4'])]:
   for j,label in enumerate(labels):
    d.box(50+j*335,y,290,80,label,[BLUE,PURPLE,GREEN,GOLD][j])
    if j<3:d.arrow([(340+j*335,y+40),(380+j*335,y+40)],'gold')
  d.line(1200,300,1200,455,GOLD,3,True);d.text(1230,390,'=',32,GOLD);d.foot('Las dos rutas dan el mismo escalar. Ninguna de las dos es una normalización softmax por sí sola.')
 elif kind=='gradient':
  d.text(90,155,'u fijo = (1,0)',27,BLUE)
  for x,label,col,sign in [(80,'Residual negativo',GREEN,1),(770,'Residual positivo',RED,-1)]:
   d.text(x+60,235,label,29,col);d.arrow([(x+80,560),(x+490,560)],'muted');d.arrow([(x+80,560),(x+80,290)],'muted')
   vx=x+280;vy=370;d.arrow([(x+80,560),(vx,vy)],'blue');d.circle(vx,vy,7,'',BLUE)
   d.arrow([(vx,vy),(vx+sign*130,vy)],'green' if sign>0 else 'red');d.text(x+200,630,'uᵀv aumenta' if sign>0 else 'uᵀv disminuye',26,col)
  d.foot('Solo se ilustra el paso de v con u fijo; las flechas horizontales muestran el signo de la actualización.')
 elif kind=='symmetry':
  d.matrix(100,240,[[0,4,2],[4,0,1],[2,1,0]],85,'Datos: X = Xᵀ');d.arrow([(420,370),(570,370)],'gold')
  d.matrix(650,190,[[.2,.8],[.5,-.1],[.4,.3]],70,'Centros W');d.matrix(1020,190,[[.6,.1],[-.2,.7],[.3,.2]],70,'Contextos W̃',colors=[PURPLE])
  d.text(880,500,'W ≠ W̃ es compatible con X = Xᵀ',28,GOLD,'middle');d.foot('Los parámetros son sintéticos: la simetría de los datos no es una restricción de igualdad de las tablas.')
 elif kind=='comparison':
  d.box(540,145,320,80,'Corpus + ventanas',GOLD)
  d.arrow([(700,225),(700,300),(340,300),(340,360)],'blue');d.arrow([(700,225),(700,300),(1060,300),(1060,360)],'purple')
  d.box(140,365,400,90,'Pares predictivos',BLUE);d.box(860,365,400,90,'Conteos Xᵢⱼ',PURPLE)
  d.arrow([(340,455),(340,525)],'blue');d.arrow([(1060,455),(1060,525)],'purple')
  d.box(140,535,400,90,'Word2Vec',BLUE);d.box(860,535,400,90,'GloVe',PURPLE);d.foot('La diferencia representada es el objetivo y cómo se organizan los datos, no un ranking universal de calidad.')
 elif kind=='cosine':
  for x,label,end in [(70,'cos θ = 1',(220,0)),(510,'cos θ = 0',(0,200)),(950,'cos θ = −1',(-135,0))]:
   ox=x+170;oy=455;d.line(x+10,oy,x+360,oy,MUTED,2);d.line(ox,245,ox,590,MUTED,2)
   d.arrow([(ox,oy),(ox+140,oy)],'blue');d.arrow([(ox,oy),(ox+end[0],oy-end[1])],'purple');d.text(x+170,200,label,27,GOLD,'middle')
  d.foot('Las flechas son vectores no nulos. Se compara dirección; la longitud puede ser distinta.')
 elif kind=='onehot':
  d.vector(80,290,[0,1,0],'Token con índice 1',GOLD)
  d.arrow([(300,325),(460,325)],'gold');a=[[.2,-.1],[.3,.8],[-.4,.6]];d.matrix(500,220,a,90,'Tabla E (3×2)')
  d.rect(498,308,180,88,'none',GOLD,0);d.arrow([(710,355),(925,355)],'gold');d.vector(970,322,[.3,.8],'Embedding E[1]',GREEN)
  d.foot('Consultar la fila evita materializar el one-hot. Los valores de E son ilustrativos, no resultados entrenados.')
 elif kind=='subword':
  d.box(70,170,220,70,'gato',BLUE);d.box(70,460,220,70,'gatos',PURPLE)
  for y,name in [(130,'<ga'),(300,'gat'),(520,'tos')]:d.box(490,y,180,70,name,GREEN)
  for start,end,c in [(205,165,'blue'),(205,335,'blue'),(495,335,'purple'),(495,555,'purple')]:d.arrow([(290,start),(385,start),(385,end),(490,end)],c)
  d.arrow([(670,335),(805,335)],'green');d.box(825,270,220,130,'hash → bucket',GOLD);d.arrow([(1045,335),(1145,335)],'gold')
  d.vector(1155,302,[.4,.7],'parámetros',GOLD,58);d.foot('Solo se muestran algunos n-gramas. «gat» se comparte; el hashing también permite colisiones entre fragmentos distintos.')
 elif kind=='bpe':
  for row,(values,label) in enumerate([(['g','a','t','o'],'Unidades iniciales'),(['ga','t','o'],'Fusión 1: g + a'),(['gat','o'],'Fusión 2: ga + t')]):
   y=170+row*170;d.text(60,y+40,label,25,GOLD)
   for j,v in enumerate(values):d.box(520+j*180,y,150,75,v,BLUE if row==0 else GREEN)
   if row<2:d.arrow([(780,y+85),(780,y+150)],'gold')
  d.foot('Fusiones hipotéticas para mostrar el mecanismo; no se atribuyen a un tokenizador entrenado concreto.')
 elif kind in ['rope','linear']:
  if kind=='rope':
   cx=670;cy=420;rad=220;d.parts.append(f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="none" stroke="{MUTED}" stroke-dasharray="7 7" stroke-width="2"/>')
   d.line(cx-rad-60,cy,cx+rad+60,cy);d.line(cx,cy-rad-60,cx,cy+rad+60)
   for p,c in enumerate(['blue','green','gold','purple']):
    a=p*math.pi/6;x=cx+rad*math.cos(a);y=cy-rad*math.sin(a);d.arrow([(cx,cy),(x,y)],c);d.text(x+25,y-15,f'p={p}',25,[BLUE,GREEN,GOLD,PURPLE][p])
   d.text(80,185,'q=(1,0)',27,BLUE);d.text(80,240,'θ=π/6',27,BLUE);d.text(1040,400,'Misma norma',27,GOLD);d.foot('Se cambia la posición manteniendo fijo el contenido de esta pareja de coordenadas.')
  else:
   for x,scale,title in [(100,(1,1),'Antes'),(850,(2,.5),'Después: W=diag(2,0.5)')]:
    ox=x;oy=560;d.arrow([(ox,oy),(ox+430,oy)],'muted');d.arrow([(ox,oy),(ox,oy-350)],'muted')
    sx,sy=scale;pts=[(ox,oy),(ox+180*sx,oy),(ox+180*sx,oy-180*sy),(ox,oy-180*sy),(ox,oy)]
    d.parts.append('<polyline points="'+' '.join(f'{a},{b}' for a,b in pts)+f'" fill="none" stroke="{BLUE if x==100 else GREEN}" stroke-width="6"/>');d.text(x,170,title,26,GOLD)
   d.arrow([(560,380),(760,380)],'gold');d.foot('El origen se conserva. La escala horizontal se duplica y la vertical se reduce a la mitad.')
 elif kind=='position':
  d.vector(80,210,[1,-1],'Contenido e',BLUE);d.vector(80,450,[.5,1],'Posición p',PURPLE)
  d.circle(470,285,38,'+',GOLD);d.arrow([(210,240),(345,240),(345,285),(432,285)],'blue');d.arrow([(210,480),(345,480),(345,285),(432,285)],'purple')
  d.arrow([(508,285),(640,285)],'gold');d.vector(665,253,[1.5,0],'Suma: ancho 2',GOLD)
  d.arrow([(210,240),(270,240),(270,600),(640,600)],'blue');d.arrow([(210,480),(300,480),(300,600),(640,600)],'purple')
  d.vector(665,568,[1,-1,.5,1],'Concatenación: ancho 4',GREEN);d.foot('Cada bloque es una coordenada. Sumar y concatenar conservan anchos diferentes.')
 elif kind=='pe':
  xs=np.linspace(0,12,160)
  for i,omega in enumerate([1,.2]):
   x=120+i*660;d.plot(x,250,500,300,xs,np.sin(xs*omega),(0,12),(-1.1,1.1),BLUE,f'ω={omega}: seno (azul) y coseno (violeta)')
   d.plot(x,250,500,300,xs,np.cos(xs*omega),(0,12),(-1.1,1.1),PURPLE)
   xx=x+3*500/12;d.line(xx,230,xx,560,GOLD,3,True);d.text(xx,610,'p=3',25,GOLD,'middle')
  d.foot('Frecuencias ilustrativas para la lectura; la ficha superior especifica las frecuencias del Transformer.')
 elif kind in ['qkv','additive']:
  if kind=='qkv':
   d.matrix(60,270,[[.2,.6],[.5,.1],[.8,-.2]],60,'X')
   for j,(w,v,col) in enumerate([('WQ','Q','blue'),('WK','K','purple'),('WV','V','green')]):
    y=150+j*170;d.arrow([(200,360),(280,360),(280,y+40),(350,y+40)],col);d.box(360,y,180,80,w,{'blue':BLUE,'purple':PURPLE,'green':GREEN}[col]);d.arrow([(540,y+40),(650,y+40)],col);d.box(660,y,120,80,v,{'blue':BLUE,'purple':PURPLE,'green':GREEN}[col])
   d.arrow([(780,190),(890,190),(890,295),(940,295)],'blue');d.arrow([(780,360),(890,360),(890,295),(940,295)],'purple')
   d.box(950,255,320,85,'QKᵀ/√dₖ → softmax',GOLD);d.arrow([(1110,340),(1110,470)],'gold');d.arrow([(780,530),(1010,530)],'green');d.box(1030,480,250,100,'A × V → Z',GREEN)
  else:
   d.box(60,180,130,75,'q',BLUE);d.box(60,480,130,75,'k',PURPLE)
   for y,w,col in [(180,'Wq','blue'),(480,'Wk','purple')]:d.arrow([(190,y+38),(295,y+38)],col);d.box(310,y,150,75,w,BLUE if col=='blue' else PURPLE);d.arrow([(460,y+38),(580,y+38),(580,367),(630,367)],col)
   d.circle(670,367,40,'+',GOLD);d.text(670,460,'+ sesgo',23,GOLD,'middle');d.arrow([(710,367),(790,367)],'gold');d.box(805,320,180,95,'tanh',GREEN)
   d.arrow([(985,367),(1050,367)],'green');d.box(1065,320,120,95,'vᵀ',PURPLE);d.arrow([(1185,367),(1250,367)],'purple');d.text(1270,377,'score',25,GOLD)
  d.foot('Las formas indican el flujo de operaciones; los anchos deben ser compatibles con cada suma y producto.')
 elif kind=='local':
  scores=np.array([1,3,2,0]);global_w=sm(scores);local=sm(scores-(np.arange(4)-2)**2/(2*.7**2))
  d.text(80,145,'Softmax global',27,BLUE);bars(d,80,260,global_w,['0','1','2','3'],450,250,BLUE,hi=1)
  d.arrow([(590,380),(710,380)],'gold');d.text(665,275,'gaussiana',23,GOLD,'middle')
  xs=np.linspace(0,3,120);d.plot(780,170,450,100,xs,np.exp(-(xs-2)**2/(2*.7**2)),(0,3),(0,1.05),GOLD)
  d.text(780,145,'Centro 2; σ=0.7',25,GOLD);bars(d,780,350,local,['0','1','2','3'],450,190,GREEN,hi=1);d.text(780,620,'Pesos renormalizados',26,GREEN)
  d.foot('Ejemplo de atenuación suave global: las cuatro posiciones se calculan antes de normalizar.')
 elif kind in ['history','equivariance']:
  if kind=='history':
   d.text(60,150,'Recurrencia: dependencia entre pasos',26,BLUE)
   for j in range(4):
    d.box(80+j*310,205,200,70,f'paso {j}',BLUE)
    if j<3:d.arrow([(280+j*310,240),(385+j*310,240)],'blue')
   d.text(60,405,'Self-attention: relaciones entre posiciones',26,PURPLE)
   for j in range(4):
    d.box(70+j*170,490,140,65,f'token {j}',PURPLE)
    d.arrow([(140+j*170,555),(140+j*170,610),(850,610),(850,530),(940,530)],'purple')
   d.matrix(960,430,sm(np.eye(4)*2),62,'Pesos ilustrativos')
  else:
   for row,items in enumerate([['A','B','C'],['C','A','B']]):
    y=180+row*275
    for j,it in enumerate(items):
     col={'A':BLUE,'B':PURPLE,'C':GREEN}[it];d.box(60+j*170,y,135,65,it,col);d.box(870+j*170,y,135,65,'z'+it,col)
    d.arrow([(580,y+32),(650,y+32)],'gold');d.box(660,y-20,175,100,'SA',GOLD);d.arrow([(835,y+32),(860,y+32)],'gold')
   d.foot('Mismos parámetros, sin posiciones ni máscara causal fija: SA(PX)=P·SA(X).')
  if kind=='history':d.foot('La matriz no representa una ejecución entrenada. LSTMN conserva recurrencia; el Transformer utiliza otro diseño.')
 elif kind=='rnn':
  d.box(70,180,230,80,'c anterior',BLUE);d.arrow([(300,220),(455,220)],'blue');d.circle(500,220,40,'×',BLUE);d.text(500,145,'f',28,BLUE,'middle')
  d.box(70,470,230,80,'propuesta g',PURPLE);d.arrow([(300,510),(455,510)],'purple');d.circle(500,510,40,'×',PURPLE);d.text(500,605,'i',28,PURPLE,'middle')
  d.arrow([(540,220),(740,220),(740,365),(805,365)],'blue');d.arrow([(540,510),(740,510),(740,365),(805,365)],'purple')
  d.circle(850,365,45,'+',GOLD);d.arrow([(895,365),(1010,365)],'gold');d.box(1025,325,280,80,'c nuevo',GOLD)
  d.arrow([(1165,405),(1165,475)],'gold');d.box(1030,485,270,100,'tanh → × o → h',GREEN)
  d.foot('× representa producto elemento a elemento. La ruta de celda se actualiza con una suma controlada por compuertas.')
 elif kind=='decomposable':
  for j in range(3):d.box(60,170+j*140,150,65,f'a{j}',BLUE);d.box(500,170+j*140,150,65,f'b{j}',PURPLE)
  for i in range(3):
   for j in range(3):d.line(210,202+i*140,500,202+j*140,GREEN,5 if i==j else 1.5)
  d.text(260,135,'Attend',27,GREEN);d.arrow([(650,345),(750,345)],'gold');d.box(770,270,230,150,'Compare G',GOLD);d.arrow([(1000,345),(1080,345)],'gold')
  d.box(1090,240,230,90,'Σ por secuencia',GREEN);d.arrow([(1205,330),(1205,420)],'green');d.box(1090,435,230,90,'Clasificador',PURPLE)
  d.foot('El grosor representa pesos ilustrativos; la comparación y la decisión se aprenden de los datos.')
 elif kind=='experiment':
  a=sm(np.eye(4)*4);b=np.full((4,4),.25)
  for x,m,title in [(80,a,'Mapa concentrado'),(600,b,'Mapa repartido')]:
   d.text(x,180,title,27,GOLD)
   for i in range(4):
    for j in range(4):
     v=m[i,j];col=f'rgb({int(45+140*v)},{int(55+140*v)},{int(85+140*v)})';d.rect(x+j*74,235+i*74,68,68,col,col,2)
  d.arrow([(420,380),(470,380),(470,205),(980,205),(980,345),(1030,345)],'muted')
  d.arrow([(940,410),(1030,410)],'muted');d.box(1050,315,280,120,'misma etiqueta',GREEN)
  d.foot('Escenarios sintéticos: concentración y predicción no bastan para establecer una explicación causal.')
 elif kind=='cnn':
  for j in range(3):
   x=80+j*28;y=240-j*28;d.rect(x,y,240,240,PANEL,BLUE,2)
   for k in range(1,5):d.line(x+k*48,y,x+k*48,y+240,BLUE,1);d.line(x,y+k*48,x+240,y+k*48,BLUE,1)
  d.text(80,165,'Entrada: 3 × 5 × 5',27,BLUE);d.arrow([(420,350),(560,350)],'blue')
  for j in range(3):d.rect(580+j*20,295-j*20,110,110,PANEL,PURPLE,2)
  d.text(560,190,'Un filtro: 3 × 3 × 3',25,PURPLE);d.arrow([(750,350),(940,350)],'purple')
  d.matrix(1000,240,[[1,2,3],[4,5,6],[7,8,9]],70,'Salida: 1 × 3 × 3',fmt='.0f')
  d.text(560,560,'stride=1 · padding=0',27,GOLD);d.foot('Los números del mapa solo marcan sus nueve posiciones; no son valores de una convolución calculada.')
 elif kind=='bn':
  vals=np.array([1,2,3,4]);normalized=(vals-vals.mean())/np.sqrt(vals.var());d.text(60,170,'Un canal: 4 valores',27,BLUE)
  d.vector(60,300,vals,'x',BLUE,65);d.arrow([(350,333),(460,333)],'blue');d.box(480,260,330,140,'(x − μ) / √(var + ε)',GOLD)
  d.text(480,470,'μ=2.5; var=1.25',25,GOLD);d.arrow([(810,333),(910,333)],'gold');d.vector(930,300,np.round(normalized,3),'x̂ (ε=0 para ilustrar)',GREEN,95)
  d.arrow([(1115,410),(1115,520)],'green');d.box(940,540,330,80,'γ x̂ + β',PURPLE);d.foot('En el cálculo real se añade epsilon; BatchNorm2d agrega el batch y las posiciones espaciales por canal.')
 elif kind in ['relu','loss','window']:
  if kind=='relu':
   xs=np.linspace(-3,3,181);ys=np.maximum(xs,0);d.plot(180,180,1000,380,xs,ys,(-3,3),(-.2,3.2),GOLD,'y=max(0,x)')
   for n in [-2,-1,0,1,2]:d.circle(180+(n+3)*1000/6,560-(max(0,n)+.2)*380/3.4,7,'',GREEN)
   d.text(650,625,'Entrada x: −3 … 3',26);d.foot('Los negativos se anulan. Los positivos conservan su valor; la operación se aplica por coordenada.')
  elif kind=='loss':
   xs=np.linspace(.02,1,180);d.plot(180,180,1000,380,xs,-np.log(xs),(0,1),(0,4),BLUE,'L=−ln p');d.arrow([(570,430),(890,520)],'gold')
   d.text(970,635,'p → 1',26,GOLD);d.text(130,180,'L',28,BLUE);d.foot('La flecha indica menor pérdida al aumentar p; el entrenamiento actúa a través de parámetros y scores.')
  else:
   xs=np.arange(64);hann=.5-.5*np.cos(2*np.pi*xs/63);hamming=.54-.46*np.cos(2*np.pi*xs/63)
   d.plot(180,220,1000,330,xs,hann,(0,63),(0,1.1),BLUE,'Hann (azul) · Hamming (violeta)')
   d.plot(180,220,1000,330,xs,hamming,(0,63),(0,1.1),PURPLE);d.text(175,610,'n=0',25);d.text(1100,610,'n=63',25)
   d.foot('Ventanas simétricas de 64 muestras. Hann: extremos 0; Hamming: extremos 0.08.')
 elif kind=='fourier':
  t=np.linspace(0,1,100);d.plot(70,250,360,230,t,np.sin(4*np.pi*t),(0,1),(-1.2,1.2),BLUE,'Muestras x[n]')
  d.arrow([(460,365),(570,365)],'gold');d.text(490,300,'DFT',26,GOLD)
  cx=790;cy=430;d.line(640,cy,1020,cy);d.line(cx,180,cx,550);d.arrow([(cx,cy),(960,245)],'purple');d.text(1000,465,'Re',23);d.text(805,180,'Im',23)
  d.line(960,245,960,cy,MUTED,2,True);d.line(960,245,cx,245,MUTED,2,True);d.text(1000,260,'X[k]',27,PURPLE);d.text(1130,360,'magnitud',23);d.text(1130,410,'y fase',23)
  d.parts.append(f'<path d="M {cx+70},{cy} A70,70 0 0 0 {cx+47},{cy-52}" fill="none" stroke="{GOLD}" stroke-width="3"/>');d.text(cx+78,cy-28,'φ',25,GOLD)
  d.arrow([(1010,580),(1010,630),(250,630),(250,530)],'green');d.text(550,615,'DFT inversa',26,GREEN);d.foot('La onda y el coeficiente son dibujos esquemáticos independientes, no un par de valores medidos entre sí.')
 elif kind=='db':
  d.text(70,170,'Potencia lineal',27,BLUE);bars(d,70,260,[1,.01,.0001],['A','B','C'],480,280,BLUE,hi=1.1)
  d.arrow([(620,370),(770,370)],'gold');d.text(695,275,'10 log₁₀',25,GOLD,'middle')
  d.text(850,170,'Nivel con referencia 1',27,GREEN);bars(d,850,260,[0,-20,-40],['A','B','C'],440,280,GREEN,lo=-45,hi=5)
  d.foot('Mismas potencias: 1 → 0 dB; 0.01 → −20 dB; 0.0001 → −40 dB. No se ha fijado una calibración acústica.')
 elif kind=='mel':
  d.text(60,160,'1 · Potencia por bin',25,BLUE);vals=[.1,.8,.4,.2,.7,.3,.1,.5];bars(d,60,280,vals,None,330,230,BLUE,hi=1)
  d.arrow([(410,390),(480,390)],'gold');d.text(510,160,'2 · Filtros triangulares',25,PURPLE)
  for j,(a,b,c) in enumerate([(0,1,2),(1,2,4),(2,4,7)]):
   pts=[(520+a*45,510),(520+b*45,270),(520+c*45,510)];d.parts.append('<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{[BLUE,PURPLE,GREEN][j]}" stroke-width="4"/>')
  d.arrow([(870,390),(940,390)],'gold');d.text(970,160,'3 · Bandas → log',25,GREEN)
  d.vector(980,310,[.7,.5,.9],'Valores ilustrativos',GREEN,80);d.arrow([(1100,410),(1100,490)],'green');d.box(960,515,330,85,'suelo positivo → log',GOLD)
  d.foot('Se esquematiza la agrupación: las alturas dibujadas no pretenden ser una multiplicación numérica completa.')
 elif kind=='source':
  xs=np.linspace(0,1,160);pulse=np.zeros_like(xs)
  for at in [.1,.3,.5,.7,.9]:pulse[np.argmin(abs(xs-at))]=1
  d.plot(60,280,300,230,xs,pulse,(0,1),(-.1,1.2),BLUE,'Excitación ilustrativa')
  d.arrow([(395,395),(495,395)],'gold');d.rect(510,230,320,300,stroke=PURPLE)
  f=np.linspace(0,1,160);response=.2+np.exp(-((f-.25)/.08)**2)+.8*np.exp(-((f-.65)/.1)**2)
  d.plot(540,290,260,180,f,response,(0,1),(0,1.5),PURPLE,'Tracto vocal: filtro')
  d.arrow([(850,395),(950,395)],'gold');wave=np.sin(18*np.pi*xs)+.3*np.sin(36*np.pi*xs)
  d.plot(980,280,330,230,xs,wave,(0,1),(-1.5,1.5),GREEN,'Salida esquemática')
  d.foot('Modelo fuente–filtro simplificado. Los dibujos no son una simulación numérica de un tracto vocal concreto.')
 else:raise ValueError('Diagrama sin implementación: '+kind)
 return d.finish()

def apply():
 OUT.mkdir(exist_ok=True);manifest=[];before={};after={};used=set()
 report_path=ROOT/'reports/explicaciones-visuales.json'
 if report_path.exists():manifest=json.loads(report_path.read_text()).get('insertions',[])
 for p in sorted((ROOT/'docs/nlp').glob('*.html')):
  s=BeautifulSoup(p.read_text(),'html.parser')
  for im in list(s.select('img[src*="/figures/"]')):
   key=Path(im['src']).stem
   if key not in SPECS:continue
   original=(p.parent/im['src']).resolve();xml=original.read_text()
   if 'class="head"' not in xml:continue
   used.add(key);before[str(original.relative_to(ROOT))]=hashlib.sha256(original.read_bytes()).hexdigest()
   identity=im.find_parent('section').get('id')+'-'+key
   if im.find_parent('section').select_one('[data-visual-explanation="'+identity+'"]'):continue
   cfg=SPECS[key];wrap=s.new_tag('section',attrs={'class':'visual-explanation','data-visual-explanation':identity})
   h=s.new_tag('h4',id='imagen-'+identity);h.string='Diagrama visual · '+cfg['title'];wrap.append(h)
   figure=s.new_tag('figure');pic=s.new_tag('img',src='../assets/visuals/'+key+'.svg',alt=cfg['desc'],loading='lazy',decoding='async',width='1400',height='760');figure.append(pic)
   caption=s.new_tag('figcaption');caption.append('Ejemplo ilustrativo. ');link=s.new_tag('a',href='../assets/visuals/'+key+'.svg',target='_blank',rel='noopener');link.string='Ampliar diagrama';caption.append(link);figure.append(caption);wrap.append(figure)
   explanation=s.new_tag('h4');explanation.string='Cómo leer esta imagen';wrap.append(explanation)
   for fragment in list(BeautifulSoup(render('\n\n'.join(f'{i+1}. {step}' for i,step in enumerate(cfg['steps']))),'html.parser').contents):wrap.append(fragment)
   im.insert_after(wrap);manifest.append({'page':str(p.relative_to(ROOT)),'cell':im.find_parent('section')['id'],'topic':key,'diagram':'docs/assets/visuals/'+key+'.svg'})
  p.write_text(str(s))
 for key in sorted(used):(OUT/(key+'.svg')).write_text(draw(key))
 # El homepage conserva una sola materia y aprovecha todo el ancho disponible.
 home=ROOT/'docs/index.html';s=BeautifulSoup(home.read_text(),'html.parser')
 intro=s.select_one('.intro-grid')
 if intro:
  for item in list(intro.find_all('div',recursive=False)):
   if 'Machine Learning Avanzado' in item.get_text(' ',strip=True):item.decompose()
  intro['class']=['intro-grid','intro-nlp']
 home.write_text(str(s))
 for path,digest in before.items():
  after[path]=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
  assert digest==after[path],path
 manifest=list({(x['page'],x['cell'],x['topic']):x for x in manifest}.values())
 report_path.write_text(json.dumps({'topics':sorted(used),'insertions':manifest,'original_cards_unchanged':before==after,'original_card_sha256':before},ensure_ascii=False,indent=2))
 print(json.dumps({'topics':len(used),'insertions':len(manifest),'original_cards_unchanged':before==after}))
if __name__=='__main__':apply()
