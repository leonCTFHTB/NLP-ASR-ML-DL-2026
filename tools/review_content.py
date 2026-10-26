"""Edición canónica del material docente; solo contiene explicaciones vigentes.

Aplica explicaciones verificadas a las celdas y a sus copias equivalentes.
No almacena versiones anteriores: el historial está en Git.
"""
from pathlib import Path
import json, re, hashlib
from bs4 import BeautifulSoup
from editorial import render

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
PATCHES = []
SOURCES = {
 'word2vec': ('Mikolov et al. · Word2Vec', 'https://arxiv.org/abs/1310.4546'),
 'w2v-math': ('D2L · Word embedding', 'https://d2l.ai/chapter_natural-language-processing-pretraining/word2vec.html'),
 'glove': ('Pennington et al. · GloVe', 'https://aclanthology.org/D14-1162/'),
 'adagrad': ('Duchi et al. · AdaGrad', 'https://jmlr.org/papers/v12/duchi11a.html'),
 'fasttext': ('Bojanowski et al. · Subword information', 'https://aclanthology.org/Q17-1010/'),
 'ft-code': ('fastText · Implementación oficial', 'https://github.com/facebookresearch/fastText/tree/main/src'),
 'ft-class': ('Joulin et al. · Clasificación de texto', 'https://aclanthology.org/E17-2068/'),
 'embbag': ('PyTorch · EmbeddingBag', 'https://docs.pytorch.org/docs/stable/generated/torch.nn.EmbeddingBag.html'),
 'adamw': ('Loshchilov y Hutter · AdamW', 'https://arxiv.org/abs/1711.05101'),
 'ce': ('PyTorch · CrossEntropyLoss', 'https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html'),
 'attention': ('Vaswani et al. · Attention Is All You Need', 'https://arxiv.org/abs/1706.03762'),
 'bahdanau': ('Bahdanau et al. · Alineación aprendida', 'https://arxiv.org/abs/1409.0473'),
 'luong': ('Luong et al. · Atención global y local', 'https://aclanthology.org/D15-1166/'),
 'hard': ('Xu et al. · Show, Attend and Tell', 'https://proceedings.mlr.press/v37/xuc15.html'),
 'lstm': ('Hochreiter y Schmidhuber · LSTM', 'https://www.bioinf.jku.at/publications/older/2604.pdf'),
 'rope': ('Su et al. · RoFormer', 'https://arxiv.org/abs/2104.09864'),
 'conv': ('D2L · Convoluciones', 'https://d2l.ai/chapter_convolutional-neural-networks/conv-layer.html'),
 'bn': ('PyTorch · BatchNorm2d', 'https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html'),
 'pool': ('D2L · Pooling', 'https://d2l.ai/chapter_convolutional-neural-networks/pooling.html'),
 'fft': ('SciPy · Fourier transforms', 'https://docs.scipy.org/doc/scipy/tutorial/fft.html'),
 'stft': ('SciPy · ShortTimeFFT', 'https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.ShortTimeFFT.html'),
 'mel': ('librosa · Banco Mel', 'https://librosa.org/doc/latest/generated/librosa.filters.mel.html'),
 'mfcc': ('librosa · MFCC', 'https://librosa.org/doc/latest/generated/librosa.feature.mfcc.html'),
 'whisper': ('Radford et al. · Whisper', 'https://proceedings.mlr.press/v202/radford23a.html'),
}

def add(prefix, cell, text, source, title=None):
    PATCHES.append(dict(prefix=prefix, cell=f'celda-{cell}', text=text, source=source, title=title))

W='clase-02-'
add(W, 16, r'''Sea $N$ el tamaño del vocabulario y $i\in\{0,\ldots,N-1\}$ el índice de una palabra. Su vector one-hot $e_i\in\mathbb R^N$ tiene componentes $(e_i)_j=\delta_{ij}$, con el mismo rango de índices para $j$.

El vector identifica el token; las relaciones entre palabras pueden aprenderse después mediante una matriz de embeddings: $v_i=E^\top e_i$. No hace falta materializar el vector one-hot para consultar la fila correspondiente de $E$.''','w2v-math')
add(W,20,r'''Dos vectores one-hot de palabras distintas son ortogonales: $e_i^\top e_j=0$ y su distancia euclídea es $\sqrt2$. Por eso la similitud directa entre esos indicadores no distingue relaciones lingüísticas. Esto no impide que una red que los recibe aprenda representaciones útiles: una tabla de embeddings realiza precisamente esa transformación.''','w2v-math')
add(W,23,'''La ortogonalidad pertenece a la codificación one-hot. No afirma que las palabras sean lingüísticamente independientes ni limita lo que puede aprender una transformación posterior.''','w2v-math')
add(W,24,r'''Para vectores no nulos, la similitud coseno es $\cos\theta=x^\top y/(\|x\|\|y\|)$. Compara direcciones y es invariante al escalado positivo de cada vector. Su interpretación semántica depende de los embeddings y de la tarea; no mide directamente el significado.''','w2v-math')
add(W,30,'''Word2Vec aprende dos tablas de vectores mediante una tarea predictiva de contexto. Skip-gram predice contextos a partir del centro; CBOW predice el centro a partir de una combinación de sus contextos. Las representaciones pueden capturar regularidades distribucionales y algunas analogías, pero no garantizan sinonimia, razonamiento algebraico exacto ni superioridad para cualquier tarea.''','word2vec')
add(W,62,r'''Para cada posición $t$, el contexto contiene posiciones válidas $j$ con $0<|j-t|\le m$ y $1\le j\le T$. Skip-gram maximiza el producto de $P(w_j\mid w_t)$ sobre esos pares. Es una independencia condicional asumida por el modelo, no una propiedad del lenguaje. Una ventana dinámica puede reducir aleatoriamente el radio en cada ejemplo; el laboratorio de radio fijo es una variante válida.''','w2v-math')
add(W,70,r'''Para un par centro–contexto, definimos $s_j=u_j^\top v_c$ y $Z_c=\sum_j e^{s_j}$. La log-verosimilitud que se maximiza es
$$\ell=\log P(w_o\mid w_c)=s_o-\log Z_c.$$
La pérdida que se minimiza tiene el signo opuesto:
$$L=-\ell=\log Z_c-s_o.$$
Esta diferencia de signo determina la dirección de la actualización.''','w2v-math')
add(W,71,r'''Minimizar $L=-\log P(w_o\mid w_c)$ aumenta la probabilidad relativa del contexto observado. Sus dos términos comparten parámetros: no se optimizan de forma independiente. El producto punto depende de normas y ángulos.''','ce')
add(W,77,r'''Para ascenso de log-verosimilitud se usa $\nabla_{v_c}\ell=u_o-\sum_j p_j u_j$. Para descenso de la pérdida se usa $\nabla_{v_c}L=\sum_j p_j u_j-u_o$. Ambos dan el mismo paso $v_c\leftarrow v_c-\eta\nabla L$. La suma incluye también el contexto verdadero. Son direcciones de actualización, no fuerzas que garanticen acercar o alejar las puntas de los vectores.''','w2v-math')
add(W,85,r'''El bucle calcula logits y aplica `CrossEntropyLoss`, que combina log-softmax y pérdida negativa. Por eso `loss.backward()` calcula $\nabla L$, con signo opuesto al gradiente de $\log P$. El optimizador resta ese gradiente. Guardar coordenadas permite visualizar el entrenamiento; la trayectoria depende de la inicialización, los datos y el optimizador.''','ce')
add(W,87,'''La animación muestra los embeddings y la pérdida de una ejecución didáctica. Se pueden comparar trayectorias y cosenos, pero un corpus tan pequeño no demuestra que las categorías deban agruparse ni que la pérdida disminuya en todos los pasos.''','word2vec')
add(W,89,'''El coseno compara direcciones: 1 indica dirección idéntica, 0 ortogonalidad y −1 direcciones opuestas. Ninguno de esos valores demuestra por sí solo sinonimia, ausencia de relación o antonimia. El objetivo de entrenamiento usa productos punto y, por tanto, también depende de las normas. Los colores de la animación muestran valores calculados, no resultados semánticos garantizados.''','word2vec')
add(W,91,r'''Negative sampling utiliza una pérdida logística para distinguir pares observados de pares muestreados:
$$L=-\log\sigma(u_o^\top v_c)-\sum_{k=1}^K\log\sigma(-u_{n_k}^\top v_c).$$
Es otro objetivo, no un cálculo exacto del softmax completo. Un negativo es una muestra de ruido; no demuestra que dos palabras carezcan de relación. Si el ejemplo amplía el vocabulario con CESS pero entrena pares de una frase de juguete, no equivale a entrenar sobre todo CESS. El tiempo y el beneficio de GPU deben medirse.''','word2vec')
add(W,99,'''CBOW asigna una distribución de probabilidad a la palabra central a partir de las palabras del contexto. El contexto puede ser ambiguo: el modelo no presupone que exista una única palabra deducible con certeza.''','w2v-math')
add(W,105,r'''Si el contexto válido tiene $C$ posiciones, su representación promediada es
$$\bar v=\frac1C\sum_{i=1}^C v_{o_i}.$$
En una ventana completa de radio $m$, $C=2m$; junto a los extremos de una secuencia puede ser menor. Es una suma de vectores, no una tupla dividida por un escalar.''','w2v-math')
add(W,108,r'''La puntuación de cada candidato es $s_j=u_j^\top\bar v$ y la probabilidad es $p_j=e^{s_j}/\sum_k e^{s_k}$. El numerador contiene la exponencial. La puntuación combina normas y ángulo: elegir el mayor producto punto no equivale a elegir el vector más paralelo.''','w2v-math')
add(W,110,'''Fig. 1.22. CBOW puntúa candidatos mediante productos punto con el promedio del contexto y normaliza sus exponenciales.''','w2v-math')
add(W,112,r'''Para una ventana, $L=\log\sum_j e^{u_j^\top\bar v}-u_c^\top\bar v$. El descenso favorece la puntuación del centro observado respecto de los otros candidatos. No garantiza una distancia euclídea menor ni elimina todas las relaciones con palabras que no fueron elegidas.''','w2v-math')
add(W,120,r'''Con $C$ posiciones en el contexto, el gradiente de la log-verosimilitud respecto de una aparición $v_{o_i}$ es
$$\frac{\partial\ell}{\partial v_{o_i}}=\frac1C\left(u_c-\sum_j p_j u_j\right).$$
El gradiente de la pérdida negativa cambia de signo. Si una palabra aparece varias veces, su fila compartida recibe la suma de las contribuciones de sus apariciones. Las direcciones ajustan puntuaciones; no son fuerzas físicas entre palabras.''','w2v-math')

G='clase-03-'
add(G,46,r'''Definimos el residual $e_{ij}=u_j^\top v_i+b_i+c_j-\log x_{ij}$ para $x_{ij}>0$. El entrenamiento reduce la suma ponderada de sus cuadrados. Con los demás parámetros fijos, el gradiente de un par respecto de $v_i$ es $2h(x_{ij})e_{ij}u_j$. Su signo indica si el producto punto debe subir o bajar; no describe un resorte entre posiciones.''','glove',title='2.2.7. Optimización de los residuales')
add(G,57,'''Fig. 2.13. La función de ponderación modula el aporte de cada par observado; su saturación no acota por sí sola el gradiente completo.''','glove')
add(G,58,'''AdaGrad adapta cada coordenada según sus gradientes acumulados. Puede ser útil con actualizaciones de frecuencia desigual. SGD con tasa constante no produce necesariamente oscilaciones ni impide aprender palabras raras: el comportamiento depende también de la tasa, el muestreo y los datos.''','adagrad')
add(G,59,r'''Por coordenada, $G_t=G_{t-1}+g_t^2$ y una convención es $\theta_{t+1}=\theta_t-\eta g_t/(\sqrt{G_t}+\epsilon)$. Cuanto mayor sea el acumulado, menor será el factor efectivo de paso. La frecuencia no determina por sí sola $G_t$: también importan las magnitudes de los gradientes. El valor exacto de $\epsilon$ y su ubicación dependen de la implementación.''','adagrad')
add(G,62,r'''La función de pérdida se evalúa únicamente sobre pares con conteo positivo:
$$J=\sum_{(i,j):x_{ij}>0}h(x_{ij})\left(u_j^\top v_i+b_i+c_j-\log x_{ij}\right)^2.$$
Es una suma de errores cuadrados ponderados; una implementación puede dividirla por el número de pares. Los sesgos son escalares entrenables y los dos vectores tienen dimensión $d$. No se evalúa $\log0$.''','glove')
add(G,77,'''El ejemplo construye conteos ponderados sobre ventanas del corpus. Un vecino a distancia 1 aporta 1 y uno a distancia 2 aporta 1/2. Estos pesos expresan una decisión de conteo, no una medida directa de fuerza semántica. La matriz global puede almacenarse de forma dispersa; no necesita ser una matriz densa del vocabulario completo.''','glove')
add(G,79,'''La tabla y el mapa de calor muestran coocurrencias de este corpus y esta ventana. Un cero significa que no se observó ese par bajo ese procedimiento; no prueba ausencia de relación. La curva de ponderación satura en uno, pero el gradiente depende además del residual y de los vectores.''','glove')
add(G,84,'''El bucle usa pares con conteo positivo y actualiza vectores y sesgos con AdaGrad. La combinación final $e_i=v_i+u_i$ es una elección habitual de representación. No obliga a que ambas tablas sean iguales ni elimina la variabilidad de la inicialización.''','glove')
add(G,86,'''La animación representa una ejecución y su pérdida. Las trayectorias no son una ley de atracción entre palabras, y la pérdida no tiene que disminuir en cada paso. La calidad de los embeddings se evalúa con tareas y datos separados, además de inspeccionar el gráfico.''','glove')

F='clase-04-'
add(F,9,'''fastText comparte vectores entre n-gramas de caracteres y mantiene una entrada propia para cada palabra conocida. Así puede combinar fragmentos para representar una palabra nueva. El modelo de embeddings sigue siendo estático: una misma palabra recibe la misma representación fuera de un mecanismo contextual adicional.''','fasttext')
add(F,11,'''Fig. 3.1. La representación combina la entrada de la palabra conocida y sus n-gramas; una palabra nueva se compone con sus subpalabras.''','fasttext')
add(F,14,'''El modelo subléxico de Bojanowski et al. amplía Skip-gram: su puntuación suma contribuciones de n-gramas de caracteres de la palabra central y un vector de salida de palabra completa para el contexto. La implementación oficial combina entradas mediante un promedio; la formulación de puntuación del artículo se presenta como suma. El laboratorio usa `EmbeddingBag(mode="sum")` y debe interpretarse con esa convención.''','ft-code')
add(F,18,'''La palabra conocida tiene una entrada propia, separada de los buckets de n-gramas. La notación delimitada ayuda a visualizarla, pero el laboratorio que reúne cadenas en un conjunto explícito es una simplificación de la estructura de datos de fastText oficial.''','ft-code')
add(F,27,r'''Se puede definir un modelo softmax con puntuación $s(w,c)=u_c^\top\sum_{g\in G_w}z_g$. Sin embargo, el entrenamiento del artículo usa negative sampling: sus sigmoides distinguen pares de datos y ruido y no son una distribución normalizada de palabras de contexto. Las representaciones de salida corresponden a palabras completas.''','fasttext')
add(F,31,'''El gradiente aumenta puntuaciones de pares observados y reduce las de pares de ruido muestreados. Esto cambia normas y direcciones de los vectores compartidos. No garantiza acercamiento euclídeo, paralelismo ni que todos los negativos sean semánticamente incoherentes.''','fasttext',title='3.3.3. Interpretación de las actualizaciones')
add(F,33,'''fastText también ofrece clasificación supervisada con una arquitectura ligera. El artículo de Joulin et al. compara precisión y tiempo en datasets concretos. Esos resultados no garantizan un coste o una precisión superior para cualquier problema.''','ft-class')
add(F,37,'''Un promedio de palabras conserva la presencia de «no», pero pierde su posición y alcance. Añadir n-gramas de palabras permite distinguir algunos patrones locales. No garantiza resolver la negación ni igualar a una RNN o CNN en cualquier corpus.''','ft-class')
add(F,55,'''Los delimitadores distinguen fragmentos iniciales, internos y finales. No identifican de forma automática morfemas ni eliminan ambigüedad semántica. En la implementación con hashing, distintas cadenas pueden además caer en el mismo bucket.''','ft-code')
add(F,56,'''Para `<gato>` y longitudes 3–5, hay 4 trigramas (`<ga`, `gat`, `ato`, `to>`), 3 tetragramas (`<gat`, `gato`, `ato>`) y 2 pentagramas (`<gato`, `gato>`). El laboratorio añade `<gato>` como entrada completa: 10 cadenas distintas en este caso. Las cadenas deben escaparse como texto para que el navegador no las interprete como etiquetas HTML.''','fasttext')
add(F,57,r'''Una cadena delimitada de longitud $L=K+2$ genera $\max(0,L-n+1)$ apariciones de longitud $n$. Para longitudes 3–5 y $K\ge3$, el total de apariciones más la entrada completa es $3K-2$. El número de cadenas **distintas** puede ser menor por repeticiones; un conjunto también puede fusionar la entrada completa con una subcadena idéntica.''','fasttext')
add(F,59,'''El tamaño real de `subword2idx` se obtiene ejecutando `len(subword2idx)` sobre el corpus y el extractor exactos. No se puede inferir con conteos aproximados por longitud. El laboratorio asigna índices explícitos a las cadenas; fastText oficial usa buckets para los n-gramas y admite colisiones.''','ft-code')
add(F,63,'''Cada muestra contiene subpalabras de longitud variable, un contexto positivo y K negativos muestreados. La función `collate_fn` concatena los índices y registra dónde empieza cada bolsa. La exclusión de negativos depende del código: no hay que suponer que todos queden fuera de la ventana entera. Con longitudes 3–5 y entrada completa, «sol» produce 7 cadenas y «rapidamente», de 11 letras, produce 31 apariciones antes de deduplicar.''','fasttext')
add(F,69,r'''El laboratorio usa $P_n(w)\propto f(w)^{0.75}$, como la elección habitual de Word2Vec SGNS. No es una constante universal de fastText: la implementación oficial de su muestreo negativo utiliza la raíz cuadrada de los conteos. Hay que declarar qué distribución implementa cada ejemplo.''','ft-code')
add(F,80,'''Con `include_last_offset=False`, los offsets [0,3,7] dividen los índices planos en los intervalos [0,3), [3,7) y [7,fin). `EmbeddingBag(mode="sum")` suma las filas de cada bolsa. Evita materializar el tensor completo de embeddings intermedios; el número de kernels y el ahorro concreto dependen del backend y de las formas.''','embbag')
add(F,88,'''`EmbeddingBag(mode="sum")` busca y suma las filas de cada bolsa sin construir todos los embeddings intermedios. Esto puede ahorrar memoria frente a un tensor rellenado, pero no existe un porcentaje fijo de ahorro. `nn.Embedding` también admite índices planos; por sí sola no exige padding ni una salida 3D.''','embbag')
add(F,90,r'''Una inicialización pequeña limita la escala inicial de las puntuaciones. Para la pérdida logística combinada, $d[-\log\sigma(s)]/ds=\sigma(s)-1$: una predicción positiva muy equivocada puede mantener un gradiente grande aunque la derivada de la sigmoide aislada sea pequeña. No se debe concluir que la pérdida se congela solo porque $|s|$ sea grande.''','ce')
add(F,97,r'''`u_neg` tiene forma [B,K,D] y `v_center.unsqueeze(2)`, [B,D,1]. `torch.bmm` produce [B,K,1]. Se elimina **solo** el último eje con `.squeeze(-1)`, manteniendo [B,K] incluso si B o K valen 1. La suma de `logsigmoid(-neg_scores)` sobre K da una contribución [B].''','embbag')
add(F,107,'''La dimensión, la cantidad de épocas y la tasa de aprendizaje son hiperparámetros del laboratorio. No existe un intervalo universal de tasas por familia de modelos: la escala de la pérdida, la reducción, el optimizador y el batch también influyen. Las filas de embeddings pueden recibir gradiente cero en un lote, pero momentum y weight decay pueden seguir modificándolas según la configuración.''','adamw')
add(F,108,r'''AdamW mantiene estimaciones del primer y segundo **momento** del gradiente. El segundo momento no es su varianza. Aplica el decaimiento de pesos de forma separada de la actualización adaptativa; en general esto no equivale a añadir una penalización L2 al objetivo de Adam. Su tasa efectiva depende del historial de gradientes, no únicamente de la frecuencia de la subpalabra.''','adamw')
add(F,127,'''El experimento consulta palabras conocidas y nuevas, y calcula los cosenos obtenidos. Compartir fragmentos puede influir en la representación, pero no permite anticipar intervalos como 0.70–0.95 sin ejecutar y evaluar el modelo. «Perro» puede aparecer en contextos relacionados con «jugar»: pertenecer a otra categoría gramatical o temática no obliga a que su coseno sea negativo. Los IDs concretos de subpalabras deben consultarse en `subword2idx`.''','fasttext')

SOURCES.update({
 'conv2d':('PyTorch · Conv2d','https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html'),
 'padding':('D2L · Padding y stride','https://d2l.ai/chapter_convolutional-neural-networks/padding-and-strides.html'),
 'vgg':('Simonyan y Zisserman · VGG','https://arxiv.org/abs/1409.1556'),
 'gumbel':('PyTorch · Gumbel-softmax','https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.gumbel_softmax.html'),
 'parikh':('Parikh et al. · Decomposable attention','https://aclanthology.org/D16-1244/'),
 'cheng':('Cheng et al. · LSTMN','https://aclanthology.org/D16-1053/'),
})
C='clase-05-1-1-'
add(C,5,'''Una CNN combina filtros locales cuyos pesos se comparten entre posiciones. El entrenamiento puede producir detectores útiles de patrones, pero no garantiza que un filtro concreto detecte una rueda en cualquier imagen. Padding, stride y kernel determinan las dimensiones; el pooling resume regiones y puede perder información. Las características y la generalización se evalúan con datos separados.''','conv')
add(C,20,r'''Una imagen puede tener cualquier resolución y número de canales. Para una entrada de $1024\times1024\times3$, aplanar produce 3.145.728 valores. Una capa densa con H salidas usa $3.145.728H+H$ parámetros con sesgo. Una convolución comparte pesos entre posiciones: su cantidad depende de canales, grupos y kernel, no directamente de la resolución de entrada.''','conv2d')
add(C,38,r'''La entrada de este ejemplo tiene $224\times224$ posiciones y **3 canales**. Con `groups=1`, un filtro de $3\times3$ abarca los tres canales: 27 pesos y, si se usa, un sesgo. Produce un canal de salida. Las dimensiones espaciales finales dependen además del stride y del padding.''','conv2d')
add(C,43,r'''Con 3 canales de entrada, 2 filtros de $3\times3$, `groups=1` y sesgo, hay $2\cdot3\cdot3\cdot3+2=56$ parámetros. La salida tiene 2 canales. Los grupos y las convoluciones depthwise modifican la conectividad; estos conteos corresponden a una convolución densa entre canales.''','conv2d')
add(C,55,'''Max pooling no tiene pesos entrenables. Con stride mayor que uno puede reducir activaciones y cómputo posterior, pero no altera el número de pesos de una convolución posterior de canales y kernel fijos. Sí puede reducir los de una capa densa sobre el mapa aplanado. Descarta detalle y no garantiza conservar lo importante para la tarea.''','pool')
add(C,60,'''La convolución aprende filtros. El pooling se aplica por separado a los mapas resultantes y resume cada ventana mediante una operación fija, como máximo o promedio. No aprende detectores de ojos, plumas o bordes.''','pool')
add(C,69,'''Las capas densas producen puntuaciones o logits. En clasificación de una sola etiqueta, softmax puede convertirlos en probabilidades. Con una entrada de 224×224 y la configuración VGG-16 usual, el extractor termina en 512×7×7; una entrada distinta puede producir otra forma.''','vgg')
add(C,77,r'''En `BatchNorm2d`, los estadísticos de cada canal se calculan sobre lote y posiciones espaciales. Convolución → BatchNorm → ReLU es un orden habitual, no obligatorio. Un sesgo de convolución puede omitirse si inmediatamente después se aplica BatchNorm con desplazamiento aprendido. La normalización de una capa densa usa otros ejes; no se debe trasladar sin más su notación a imágenes.''','bn')

V='clase-05-1-2-'
add(V,7,'''Cada canal de salida tiene pesos entrenables que combinan regiones locales de los canales de entrada. Los patrones resultantes dependen del entrenamiento; no hay una correspondencia obligatoria «un filtro, un concepto». En PyTorch `Conv2d` aplica correlación cruzada, sin invertir espacialmente el kernel.''','conv2d')
add(V,9,'''El padding agrega valores en los bordes. Puede elegirse para conservar la resolución con ciertas combinaciones de kernel, stride y dilatación; no conserva el tamaño automáticamente ni tiene que ser siempre cero o simétrico.''','padding')
add(V,10,'''Max pooling selecciona máximos por ventana. Con stride 2 suele reducir la resolución; con stride 1 y padding adecuado puede mantenerla. La operación descarta información y no garantiza conservar todas las características relevantes.''','pool')
add(V,11,'''El shape describe el tamaño de cada eje. `torch.nn.Conv2d` recibe normalmente [N,C,H,W]: lote, canales, altura y ancho. [N,H,W,C] es otra convención; requiere reordenar ejes para usar esta interfaz.''','conv2d')
add(V,12,'''Convolución: combina regiones locales con pesos compartidos. Padding: agrega bordes. Stride: determina la separación entre aplicaciones. Pooling: resume ventanas sin pesos entrenables. Shape: identifica los ejes y tamaños. Ninguna de estas operaciones garantiza por sí sola conservar significado o mejorar la precisión.''','conv2d')
add(V,31,r'''Con 3 canales de entrada y `groups=1`, un filtro de 3×3 tiene 27 pesos y un sesgo opcional. Una capa con 32 filtros tiene 32 canales de salida; **32 no es la resolución espacial**. Para una entrada [N,3,32,32], 32 filtros de 5×5, stride 1 y padding 0 producen [N,32,28,28], con $32(3\cdot5\cdot5+1)=2432$ parámetros si hay sesgo.''','conv2d')
add(V,32,r'''Con padding p por lado, dilatación d, kernel k y stride s, el tamaño de salida en un eje es
$$n_{out}=\left\lfloor\frac{n+2p-d(k-1)-1}{s}\right\rfloor+1.$$
Ejemplos: (n,k,p,s,d)=(5,3,0,2,1) da 2; (5,3,2,2,1) da 4; (64,3,0,1,1) da 62. Dos convoluciones 3×3 sin padding llevan 64→62→60; un max pooling 2×2 con stride 2 lleva 60→30. Una entrada de 32 canales necesita filtros de 32 canales cuando `groups=1`.''','conv2d')
add(V,38,r'''Dos filtros 3×3 sobre 3 canales, con `groups=1`, usan $2\cdot3\cdot3\cdot3=54$ pesos y 2 sesgos: 56 parámetros en total. Producen dos canales de salida.''','conv2d')
add(V,43,r'''ReLU aplica $\max(0,x)$ a cada elemento y aporta no linealidad. Una composición de transformaciones afines sin operaciones no lineales sigue siendo afín. Max pooling también es no lineal; por eso no basta con quitar ReLU para afirmar que cualquier CNN completa se reduce a una única convolución.''','conv')
add(V,48,'''La reducción espacial mediante pooling produce menos activaciones. Puede aumentar la tolerancia local a desplazamientos, pero descarta detalle y puede perjudicar tareas que requieren localización precisa.''','pool')
add(V,62,'''Flatten reorganiza ejes; no añade una capa densa ni parámetros. Para [N,2,5,5], `flatten(start_dim=1)` produce [N,50]. Una capa lineal posterior genera logits. Softmax puede aplicarse sobre cualquier eje elegido, no exige entradas unidimensionales y no requiere Flatten por sí misma.''','ce')
add(V,66,'''Un kernel pequeño combina vecindades menores por capa; apilar capas amplía el campo receptivo. La información y el rendimiento que se obtienen no dependen solo del tamaño del kernel.''','conv2d')
add(V,68,'''Un kernel mayor abarca una región mayor por aplicación y suele tener más parámetros con los mismos canales. No extrae necesariamente menos información ni entrena peor. La reducción espacial depende también del padding, stride y dilatación.''','conv2d')
add(V,70,'''El padding controla el tratamiento de los bordes y la forma de salida. Agregar ceros no reconstruye información externa ni garantiza una mejora de precisión. Con kernel impar, dilatación 1 y stride 1, p=(k−1)/2 por lado conserva el tamaño.''','padding')
add(V,72,'''El stride es la separación entre aplicaciones del kernel. Aumentarlo suele reducir posiciones de salida y cómputo; también puede descartar detalle y producir aliasing. Un stride pequeño no garantiza aprender más características útiles.''','padding')
add(V,81,r'''Para un canal c, M=NHW, la media es $\mu_c=M^{-1}\sum_{n,h,w}A_{nchw}$ y la **varianza** es $v_c=M^{-1}\sum_{n,h,w}(A_{nchw}-\mu_c)^2$. Se normaliza con $\hat A=(A-\mu_c)/\sqrt{v_c+\epsilon}$ y se aplica $Y=\gamma_c\hat A+\beta_c$. No se vuelve a elevar la varianza al cuadrado. Por epsilon, la varianza normalizada no es exactamente uno. PyTorch usa estimador sesgado en el forward y no sesgado para actualizar la varianza acumulada.''','bn')
add(V,100,'''FC2 transforma 512 características en 10 **logits**. El código entrenado con `CrossEntropyLoss` devuelve esos logits sin softmax. Para mostrar probabilidades en inferencia se puede aplicar `softmax(logits, dim=1)`; no se añade antes de esa pérdida.''','ce')
add(V,102,'''Convoluciones 3×3, stride 1 y padding 1 conservan H y W. Los tres bloques producen [N,32,16,16], [N,64,8,8] y [N,64,4,4]. Flatten conserva el batch y produce [N,1024]; las capas lineales llevan 1024→512→10 logits. Es una CNN reducida inspirada en bloques VGG, no la VGG-16 original de 13 convoluciones y 3 capas densas.''','vgg')
add(V,85,'''El laboratorio usa seis convoluciones y dos capas densas. Se inspira en bloques de VGG, pero no reproduce VGG-16. Sus formas y el número de clases corresponden a la configuración didáctica de entrada 32×32.''','vgg',title='24.4. Implementación de una CNN reducida inspirada en VGG')
D='clase-05-1-cnn-'
add(D,35,'''Para ampliar una entrada 3×3 a 5×5 se agrega **una fila o columna por lado** (padding=1 en PyTorch), no un padding de 3×3. Con un kernel 2×2, stride 1 y dilatación 1, la salida es 4×4.''','padding')
add(D,38,r'''En la notación que usa padding **total**, se agregan $p_h$ filas y $p_w$ columnas. Con stride 1 y dilatación 1, la salida es $(n_h-k_h+p_h+1)\times(n_w-k_w+p_w+1)$. Para conservar tamaño, $p_h=k_h-1$ y $p_w=k_w-1$. Si el total es impar, se reparte como piso y techo entre ambos lados; no se usa el mismo entero en los dos. `Conv2d(padding=p)` expresa p **por lado**.''','padding')
add(D,59,'''Una convolución 1×1 con stride 1, padding 0 y groups=1 aplica la misma transformación afín de canales en cada posición. Con Ci entradas y Co salidas usa Ci·Co pesos y Co sesgos opcionales. Los pesos se **comparten** entre posiciones; no hay pesos distintos para cada píxel. No mezcla vecinos espaciales en esa capa.''','conv2d')

R='clase-06-6-mecanismos-de-atencion-parte-1-'
add(R,12,'''Un resumen de dimensión fija puede dificultar el manejo de secuencias largas. No existe un umbral universal de palabras a partir del cual se pierda la información. La retención depende de parámetros, entrenamiento y datos; las dependencias recurrentes también pueden dificultar la optimización.''','lstm')
add(R,20,'''Una RNN reutiliza los mismos parámetros en todos los pasos. El número de parámetros no crece con la longitud; el trabajo y las activaciones de entrenamiento sí dependen de ella. Compartir pesos favorece aplicar la misma regla temporal, pero no garantiza generalizar a longitudes nuevas.''','lstm')
add(R,28,'''El estado oculto es una representación aprendida de dimensión fija que depende del prefijo procesado. Puede conservar información útil, pero no contiene necesariamente toda la historia ni tiene coordenadas con una interpretación lingüística prefijada. Un ejemplo de significado es una intuición, no una lectura exacta del vector.''','lstm')
add(R,37,'''En una recurrencia lineal, algunas dinámicas pueden crecer si se multiplican repetidamente por una transformación expansiva. `tanh` acota las activaciones, pero no garantiza controlar el gradiente de toda la red. Este depende de productos de matrices y derivadas.''','lstm')
add(R,50,r'''Para «amigo», los bigramas delimitados incluyen `<a`, `am`, `mi`, `ig`, `go`, `o>`; los trigramas incluyen `<am`, `ami`, `mig`, `igo`, `go>`. Son fragmentos de caracteres, no morfemas garantizados. `get_word_vector` de fastText oficial **promedia** las entradas correspondientes a la palabra conocida y sus subpalabras; una palabra OOV usa sus subpalabras.''','ft-code')
add(R,56,'''Una palabra nueva se representa combinando los buckets de sus fragmentos. Es posible calcular el vector aunque no exista una fila de palabra completa, pero no se garantiza que sea lingüísticamente coherente. Los fragmentos pueden compartir buckets por hashing.''','ft-code')

A='clase-06-6-mecanismos-de-atencion-parte-2-'
add(A,14,'''Una representación final fija puede dificultar la traducción de secuencias largas. No implica que las primeras palabras se sobrescriban por completo ni que exista un límite rígido de 30 o 40 tokens. Las LSTM pueden conservar información a largo plazo, con límites que dependen del entrenamiento.''','bahdanau')
add(A,31,'''Luong et al. compararon funciones dot, general y concat y variantes globales y locales. Las formas multiplicativas permiten cálculos matriciales eficientes, pero no hay una superioridad universal de coste o calidad frente a la atención aditiva.''','luong')
add(A,32,'''La atención aditiva proyecta consulta y claves, combina los resultados con tanh y produce una puntuación escalar. Las proyecciones de claves pueden precalcularse y las operaciones se pueden vectorizar en GPU. El tiempo debe medirse para las dimensiones y el backend concretos.''','bahdanau')
add(A,47,'''La puntuación bilineal puede calcularse mediante productos matriciales. Ese patrón es eficiente en muchos aceleradores, pero «más rápido» requiere una comparación medida: tamaño de secuencia, dimensión intermedia y precálculo de claves cambian el coste.''','luong')
add(A,49,'''Si consulta y clave tienen igual dimensión, el producto punto directo no necesita parámetros adicionales de alineación. Las representaciones que lo alimentan sí pueden tener parámetros entrenables. Esto no garantiza convergencia más rápida ni una mejora exponencial.''','luong')
add(A,54,'''La atención local predictiva de Luong evalúa una vecindad alrededor de un centro continuo. Para un centro entero y radio D, el intervalo inclusivo contiene hasta **2D+1 posiciones**, y menos junto a los extremos. El tratamiento de un centro no entero requiere declarar cómo se eligen los índices.''','luong')
add(A,82,'''Las proyecciones de consulta y claves llevan sus dimensiones a un ancho común; la capa final produce un escalar. `bias=False` es una elección del laboratorio. Un sesgo común sumado después de producir todos los scores se cancela en softmax, pero un sesgo **dentro de tanh** no es en general redundante.''','bahdanau')
for cell in [112,113,115,117,119,122]:
 add(A,cell,'''Los mapas y probabilidades guardados describen una ejecución pequeña. Su forma no demuestra que un mecanismo sea intrínsecamente agudo, uniforme o mejor. No se puede atribuir una predicción a un mínimo local, a una palabra o a la escala de los scores sin mediciones y pruebas adicionales. Para comparar se requieren varias semillas y evaluación fuera de entrenamiento.''','attention')
soft_grad=r'''Escribimos $c=\sum_i\alpha_i v_i$ y $\alpha=\operatorname{softmax}(e)$. Tratando los scores y valores como variables independientes, $\partial c/\partial v_i=\alpha_i I$ y $\partial c/\partial e_i=\alpha_i(v_i-c)$. Si una entrada también genera claves o scores, su **derivada total** contiene esas rutas adicionales. La diferenciabilidad no garantiza estabilidad ni convergencia.'''
add(A,128,soft_grad,'attention')
H='clase-08-'
add(H,33,soft_grad,'attention')
hard_def=r'''En atención discreta, $s\sim\operatorname{Categorical}(\alpha)$ y $c=v_s$. Si se representa la elección como one-hot, corresponde a una multinomial con **un ensayo**. Seleccionar un índice corta la ruta ordinaria del gradiente hacia sus probabilidades; la esperanza del objetivo puede entrenarse con estimadores como REINFORCE o con relajaciones.'''
add(A,133,hard_def,'hard');add(H,38,hard_def,'hard')
reinforce=r'''Xu et al. optimizan una cota variacional de la log-verosimilitud con muestreo de localizaciones y un estimador de tipo REINFORCE. No debe atribuirse a ese experimento una recompensa BLEU o +1 inventada. Para una recompensa independiente de los parámetros, $\nabla_\theta\mathbb E[R(s)]=\mathbb E[R(s)\nabla_\theta\log\pi_\theta(s)]$. Si R también depende de parámetros, se añade su derivada directa. Una baseline independiente de la acción puede reducir varianza.'''
add(A,138,reinforce,'hard');add(A,140,reinforce,'hard');add(H,43,reinforce,'hard')
add(H,62,'''El ejemplo calcula scores para todas las posiciones y aplica una gaussiana suave, de modo que conserva coste global. Para pesos normalizados y estabilidad numérica se puede sumar el logaritmo de la gaussiana a los logits y aplicar un único softmax en posiciones válidas. Añadir epsilon a un denominador arbitrario hace que la suma no sea exactamente uno. Una secuencia vacía requiere tratamiento explícito.''','luong')
add(H,67,'''La proyección bilineal genera los scores. Con `gumbel_softmax(..., hard=True)`, el forward es one-hot y la temperatura cambia la relajación usada para el backward; **no vuelve uniforme el one-hot del forward**. El estimador straight-through es sesgado y no es la derivada exacta de una elección discreta.''','gumbel')
add(H,71,'''Durante entrenamiento, Gumbel-softmax con `hard=True` devuelve una selección discreta y usa el gradiente de una relajación para actualizar parámetros. En evaluación el código elige argmax sin ruido. Es una adaptación didáctica distinta del entrenamiento REINFORCE de Xu et al.; no deben presentarse como el mismo algoritmo.''','gumbel')
T='clase-05-4-1-'
add(T,46,r'''Cada cabeza tiene matrices aprendidas $W_i^Q,W_i^K,W_i^V$. Q, K y V son **activaciones calculadas**, no pesos. El Transformer base del artículo usa 8 cabezas y $d_k=d_v=64$; son elecciones de esa configuración, no constantes de todos los Transformers.''','attention')
add(T,48,'''Las matrices W son parámetros compartidos entre posiciones. Al multiplicar las entradas por ellas se obtienen Q, K y V, que cambian con la entrada. Distintas cabezas pueden aprender patrones diferentes, pero no están obligadas a especializarse en funciones lingüísticas separadas.''','attention')
add(T,68,'''La primera capa recibe embeddings con información posicional. Las siguientes reciben representaciones contextuales del mismo ancho. El largo del batch puede variar mediante padding y máscaras dentro del contexto admitido; no tiene que ser la oración más larga de todo el entrenamiento. El decoder también tiene embeddings de sus tokens de entrada.''','attention')
add(T,75,'''La atención sin información de posición es equivariante a permutaciones de sus entradas. La codificación posicional introduce orden; puede ser aditiva, relativa o rotatoria según la arquitectura. No garantiza crear distancias semánticas significativas ni que toda representación absoluta permita una extrapolación fiable.''','attention')
add(T,83,'''Sumar directamente el índice de posición puede introducir una escala que crece con la longitud. Es una decisión de diseño que requiere controlar escalas; no significa que los pesos de toda red deban estar alrededor de cero ni que usar índices grandes provoque necesariamente gradientes explosivos.''','attention')
add(T,87,'''Dividir el índice por la longitud representa una posición relativa: el mismo índice cambia de valor si cambia el largo. Eso puede ser útil para ciertas tareas, pero no identifica una posición absoluta de forma independiente de la secuencia. No demuestra que sea imposible trabajar con longitudes variables.''','attention')
add(T,94,r'''La codificación sinusoidal del Transformer es una elección explícita de funciones, no una interpolación obligatoria de bits:
$$PE(p,2i)=\sin(p/10000^{2i/d}),\qquad PE(p,2i+1)=\cos(p/10000^{2i/d}).$$
Los pares recorren distintas frecuencias angulares. Una dimensión no representa un bit ni una cantidad fija de significado.''','attention')
add(T,96,'''Cada posición tiene un vector de componentes sinusoidales. El orden de dimensiones depende de la convención gráfica. En la fórmula usual las frecuencias disminuyen al aumentar el índice de pareja; no se duplican sensibilidades como en un contador binario.''','attention')
add(T,97,'''En la fórmula original la frecuencia angular de la primera pareja es 1 radián por posición y la pareja i usa 10000^(−2i/d). No se usa la sucesión π/2, π/4, π/8. Agrupar o intercalar senos y cosenos es una permutación de dimensiones si se mantiene la misma convención en todo el cálculo.''','attention')
add(T,111,'''La self-attention causal permite atender a la posición actual y a posiciones anteriores; bloquea las futuras antes del softmax. La cross-attention usa consultas del decoder y claves/valores del encoder. Durante entrenamiento, teacher forcing y la máscara permiten calcular muchas posiciones a la vez; durante generación autorregresiva se incorporan tokens sucesivamente.''','attention')
add(T,114,'''La proyección de salida produce un logit por token del vocabulario. Softmax los convierte en una distribución sobre ese eje. Greedy decoding elige el máximo; también se pueden usar muestreo o beam search. El vocabulario suele contener subpalabras, no necesariamente palabras completas.''','attention')

SOURCES.update({
 'nola':('SciPy · Reconstrucción STFT y NOLA','https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.check_NOLA.html'),
 'preemphasis':('librosa · Preénfasis','https://librosa.org/doc/0.10.2/generated/librosa.effects.preemphasis.html'),
 'cqt':('librosa · CQT inversa','https://librosa.org/doc/0.10.2/generated/librosa.icqt.html'),
 'ge2e':('Wan et al. · GE2E','https://arxiv.org/abs/1710.10467'),
 'diarization':('Wang et al. · Speaker diarization','https://arxiv.org/abs/1710.10468'),
 'links':('Mansfield et al. · Links','https://arxiv.org/abs/1801.10123'),
 'yolo3':('Redmon y Farhadi · YOLOv3','https://arxiv.org/abs/1804.02767'),
 'yolo2':('Redmon y Farhadi · YOLO9000','https://arxiv.org/abs/1612.08242'),
 'focal':('Lin et al. · Focal Loss','https://arxiv.org/abs/1708.02002'),
 'maskrcnn':('He et al. · Mask R-CNN','https://arxiv.org/abs/1703.06870'),
 'ssd':('D2L · SSD','https://d2l.ai/chapter_computer-vision/ssd.html'),
 'nms':('Torchvision · batched_nms','https://docs.pytorch.org/vision/stable/generated/torchvision.ops.batched_nms.html'),
 'augment':('Torchvision · Transformaciones','https://docs.pytorch.org/vision/stable/transforms.html'),
 'uncertainty':('MIT OpenCourseWare · Fourier y principio de incertidumbre','https://ocw.mit.edu/courses/18-103-fourier-analysis-fall-2013/'),
})
SOURCES['cheng']=('Cheng et al. · LSTMN','https://aclanthology.org/D16-1053/')
SOURCES['mel']=('librosa · Banco Mel','https://librosa.org/doc/0.10.2/generated/librosa.filters.mel.html')
SOURCES['mfcc']=('librosa · MFCC','https://librosa.org/doc/0.10.2/generated/librosa.feature.mfcc.html')

R='clase-13-'
for c,title in [(48,'RoPE en la atención'),(54,'Posición y representación'),(55,'Geometría de la codificación aditiva'),(80,'Relaciones entre posiciones'),(88,'Construcción rotatoria'),(94,'Rotaciones y norma'),(117,'Propiedades geométricas'),(141,'Norma y gradientes')]:
    add(R,c,'RoPE aplica una rotación por parejas de coordenadas a consultas y claves. Conserva la norma de cada vector rotado y hace que el factor de rotación en su producto escalar dependa del desplazamiento relativo. Estas propiedades geométricas no garantizan preservar un significado, mejorar la tarea ni estabilizar toda la red.','rope',title)
add(R,68,'Con codificación aditiva, la primera capa puede calcular Q y K a partir de embeddings más posición. Las capas siguientes reciben representaciones contextuales, no de nuevo el embedding original. RoPE rota las proyecciones Q y K en las capas de atención que lo incorporan.','rope')
add(R,96,r'''Identificamos una pareja real $(a,b)$ con $z=a+ib$. La rotación es $z\mapsto ze^{ip\theta}$. El producto escalar real de dos parejas corresponde a $\operatorname{Re}(z_q\overline{z_k})$. Declarar esta convención evita cambiar el signo del desplazamiento por error.''','rope')
add(R,102,r'''Con vectores columna, $(R_mq)^\top R_nk=q^\top R_{n-m}k$. El factor rotatorio depende de $n-m$; los vectores q y k pueden contener información contextual y posicional procedente de otras capas. La identidad no elimina toda dependencia absoluta de un modelo completo.''','rope')
add(R,104,'Las parejas complejas son una forma compacta de escribir el cálculo. Se implementa también con productos y sumas reales; no es cierto que las GPU solo puedan operar con números reales. El coste depende de la implementación.','rope')
for c in [119,135,142]:
    add(R,c,'La hélice es una visualización de una pareja de coordenadas de contenido fijo mientras cambia la posición. Tokens distintos tienen vectores de contenido distintos y no tienen por qué seguir una misma hélice. Las frecuencias múltiples codifican posición, pero no garantizan extrapolar a cualquier longitud ni asignan funciones lingüísticas fijas a las dimensiones.','rope')
add('clase-12-',51,'Este ejemplo describe GPT-2: suma embeddings de token y posición aprendida antes de sus bloques. No todos los modelos llamados GPT usan ese esquema; la codificación depende de la arquitectura concreta.','attention')

P='clase-09-6-mecanismos-'
add(P,11,'Las RNN tienen una dependencia recurrente entre pasos. Las CNN pueden procesar posiciones en paralelo dentro de una capa; su campo receptivo crece al apilar capas. La atención conecta posiciones mediante scores aprendidos. Son diseños distintos, sin una superioridad universal.','attention')
add(P,27,'Ejemplo hipotético: la premisa «Un perro marrón corre en el césped» contiene siete tokens si se separa por espacios. La hipótesis y la premisa se alinean mediante softmax por fila; los pesos deben sumar uno sobre posiciones válidas. Un número ilustrativo no es una medición del modelo.','parikh')
for c in [37,38,39]:
    add(P,c,'La etapa Compare aplica una red aprendida a la concatenación de cada token y su alineación suave. ReLU introduce una no linealidad; no tiene detectores lógicos predefinidos ni demuestra contradicción por sí sola. Aggregate suma las representaciones de comparación y un clasificador aprende la decisión a partir de ejemplos etiquetados.','parikh')
add(P,44,'Cheng et al. (2016) desarrollaron LSTMN, con memoria de estados y atención dentro de la secuencia. Es una contribución temprana a la atención interna, distinta de la self-attention sin recurrencia del Transformer. No debe atribuirse a un único artículo la invención de toda forma de autoatención.','cheng')
add(P,47,'Una LSTM mantiene estado oculto h y estado de celda c. Sus compuertas controlan actualizaciones y pueden favorecer dependencias largas; no existe una cantidad fija de palabras que siempre recuerde ni una garantía de gradientes estables en cualquier entrenamiento.','lstm')
add(P,50,'El ejemplo es una simplificación didáctica de atención sobre estados pasados, no una reproducción exacta de LSTMN. En Cheng et al. las lecturas ponderadas de memorias ocultas y de celda intervienen en la actualización recurrente; hay que consultar las ecuaciones del artículo para reproducir esa arquitectura.','cheng')
for c in [95,98,102]:
    add(P,c,'El mapa muestra pesos del ejemplo, no una prueba de que el modelo haya aprendido una regla lingüística. Para interpretarlo hay que conocer los datos, las máscaras, el modo de evaluación y el entrenamiento. La atención por sí sola no identifica causas de la predicción.','attention')
add(P,101,'En evaluación, el softmax suma uno por consulta sobre claves válidas. El dropout puede alterar las sumas durante entrenamiento. Los pesos tampoco miden una proporción literal de información: importan los valores, sus normas y las transformaciones posteriores.','attention')

A0='clase-05-2-'
add(A0,6,'La atención calcula compatibilidades entre consultas y claves, normaliza scores y combina valores. Un score no es necesariamente un coeficiente estadístico de correlación.','attention')
add(A0,13,'Las compuertas de una LSTM regulan su memoria recurrente. La atención selecciona o pondera representaciones mediante una consulta. Pueden combinarse, pero son mecanismos distintos y no una reproducción literal de la atención humana.','lstm')
add(A0,58,'En Bahdanau la alineación usa el estado previo del decoder y los estados del encoder. En la formulación global de Luong se usan el estado actual del decoder y los estados del encoder. Se consultan estados de diferentes posiciones, no solo el primero y el último.','luong')
add(A0,62,'La atención local de Luong et al. (2015) restringe la combinación a una ventana alrededor de una posición central. Puede usar una predicción diferenciable del centro; no se atribuye este esquema local a Bahdanau.','luong')
add(A0,64,'Soft attention combina valores con pesos continuos. Hard attention elige posiciones discretas. Local attention limita la región atendida y puede seguir siendo suave dentro de ella: local y hard no son sinónimos.','luong')

B='clase-14-14-'
add(B,48,'Muchos sistemas dividen el audio en ventanas de decenas de milisegundos, con solapamiento. La longitud y el salto son parámetros del frontend; no todos los sistemas ASR usan la misma ventana ni todos requieren un espectrograma explícito.','stft')
add(B,50,'La STFT devuelve coeficientes complejos por tiempo y frecuencia. Su magnitud y su potencia son representaciones derivadas; un espectrograma de potencia usa el módulo al cuadrado. Algunos modelos trabajan con características espectrales y otros aprenden representaciones desde la onda.','stft')
F='clase-15-'
complexity='La DFT directa requiere orden N² operaciones y los algoritmos FFT habituales orden N log N. Un cociente de operaciones no equivale a un factor de aceleración medido: influyen el tamaño, la factorización, la memoria, el hardware y la biblioteca. Radix-2 exige N potencia de dos; una biblioteca FFT puede usar otros algoritmos.'
for c in [34,43,47,49,51,66,70]:add(F,c,complexity,'fft')
add(F,41,r'''El salto H fija una tasa nominal de $f_s/H$ frames por segundo. Sin padding, una señal de L muestras y una ventana de W muestras produce $1+\lfloor(L-W)/H\rfloor$ frames si L≥W. A 16 kHz, W=400 y H=160 dan 98 frames para un segundo sin padding, con tasa nominal de 100 Hz.''','stft')
invertible='La DFT compleja completa es invertible dentro de la precisión numérica. Sus coeficientes contienen la información de las muestras; no destruye el tiempo. Un espectro de magnitud global pierde fase y no indica directamente cuándo ocurrió un evento. La STFT introduce un índice de ventana para representar evolución temporal.'
for c in [69,95]:add(F,c,invertible,'fft')
add(F,90,'Una FFT radix-2 para N=2^s tiene s etapas y N salidas X[0], …, X[N−1]. Cada mariposa combina dos entradas mediante un factor de giro. La ordenación depende de la variante del algoritmo.','fft')
add(F,98,r'''Con ventana de W muestras, salto H y N≥W puntos de FFT:
$$X[m,k]=\sum_{n=0}^{W-1}x[mH+n]w[n]e^{-2\pi i kn/N}.$$
Esta expresión usa ventanas sin centrar; otras convenciones añaden padding. Para señales reales, rFFT devuelve $\lfloor N/2\rfloor+1$ bins. El zero-padding refina la rejilla espectral, sin aumentar la resolución física impuesta por W y la ventana.''','stft')
add(F,104,'La ventana suaviza los bordes del segmento y modifica el compromiso entre anchura del lóbulo principal y lóbulos laterales. Su elección depende del análisis y de la reconstrucción; no hay una ventana única obligatoria para todos los vocoders o modelos.','stft')
add(F,108,'Las frecuencias de un ejemplo sintético pertenecen a ese ejemplo. El enventanado multiplica la señal en tiempo y convoluciona su espectro con el de la ventana. La fuga espectral de una observación finita no significa que la FFT añada ruido físico a la señal.','fft')
add(F,116,r'''Para inversión mediante overlap-add normalizado se necesita cubrir las muestras y que $\sum_m w^2[n-mH]\ne0$ en la región reconstruida (NOLA, usando la misma ventana de análisis y síntesis). El denominador se utiliza para normalizar. Una suma constante es una condición más restrictiva; no es necesaria para toda implementación de ISTFT.''','nola')
add(F,120,'La STFT compleja conserva fase. Usar magnitud, potencia o log-Mel es una elección del frontend y pierde información respecto a ella. Cada arquitectura define qué características recibe; no todas las redes de voz consumen directamente la misma matriz.','stft')
unc=r'''Para una señal de energía finita y varianzas finitas, usando frecuencia en Hz y la convención Fourier $e^{-2\pi ift}$, las desviaciones estándar normalizadas por la energía satisfacen $\sigma_t\sigma_f\ge1/(4\pi)$. No son el salto temporal H/f_s y el espaciado de bins f_s/N: aumentar N mediante ceros no vence este límite.'''
add(F,124,unc,'uncertainty')
add(F,143,'Los formantes son resonancias del tracto vocal. Un espectrograma puede hacer visibles bandas relacionadas con ellas, pero el logaritmo por sí solo no garantiza identificarlas ni clasificar fonemas.','stft')
add(F,145,'La potencia espectral puede definirse como |X|²; una densidad espectral requiere además una normalización con unidades apropiadas. El orden de logaritmo y agregación importa: log(sum P) no es sum(log P). El frontend debe especificar su convención.','stft')
for c in [165,167,169]:
    add(F,c,'El logaritmo comprime el rango dinámico. Para potencia se usa 10 log10(P/P_ref); para amplitud comparable, 20 log10(A/A_ref). Hay que declarar referencia, suelo numérico y posible recorte. Añadir epsilon y limitar con max(P,epsilon) son operaciones distintas. Los dB no son una medida universal de sonoridad percibida.','mel')
for c in [175,177,183]:
    add(F,c,'La escala Mel aproxima relaciones perceptivas de altura tonal. Un banco Mel agrupa bins mediante filtros, normalmente triangulares, más separados en Hz a frecuencias altas. No reproduce exactamente la cóclea ni sus bandas críticas. La implementación puede elegir la fórmula HTK o la convención Slaney y normalizar por área.','mel')
add(F,184,r'''Para frecuencias de bin $f_k=kf_s/N$ y bordes $a_m<b_m<c_m$ en Hz, un filtro triangular de pico uno es
$$H_m(f)=\max(0,\min((f-a_m)/(b_m-a_m),(c_m-f)/(c_m-b_m))).$$
Se evalúa como H_m(f_k). La normalización por área cambia su altura; no se debe mezclar un índice de bin con una frecuencia en Hz.''','mel')
add(F,186,r'''El espectrograma Mel de potencia es $S[m,r]=\sum_k H_r(f_k)|X[m,k]|^2$. El log-Mel aplica después un logaritmo con suelo positivo o conversión a dB. «Mel» y «log-Mel» no son el mismo paso.''','mel')
add(F,194,'Los valores pequeños de una matriz pueden verse como ceros por la precisión de impresión. Eso no demuestra que sean exactamente cero; hay que inspeccionar los valores numéricos y el rango de los filtros.','mel')
add(F,198,'La cantidad de bandas Mel es un parámetro del modelo y debe coincidir con su frontend. Whisper original usa 80; existen variantes posteriores con otras configuraciones. No se debe imponer 80 a todos los modelos de voz.','whisper')
add('clase-16-',16,'En una FFT radix-2 DIT iterativa habitual se permutan índices por inversión de bits. Para N=4: 00→00, 01→10, 10→01, 11→11; la entrada queda [x0,x2,x1,x3]. Otras variantes cambian dónde se hace la permutación. No es un paso universal obligatorio previo a toda FFT.','fft')

S='clase-14-attentioncnn-'
add(S,12,'Una representación derivada de la onda no crea información que la onda no contenga. Espectrogramas y otras características introducen una organización y sesgos útiles para ciertos modelos. Normalizar o rellenar una señal no equivale a eliminar ruido; la elección debe validarse en la tarea.','stft')
add(S,19,'La conversión analógica-digital implica muestreo y cuantización. Los MFCC suelen calcularse mediante potencia espectral, filtros Mel, logaritmo y DCT-II. No son la transformada inversa directa del logaritmo de la FFT de la onda.','mfcc')
add(S,21,r'''Un preénfasis de primer orden habitual es $y[n]=x[n]-\alpha x[n-1]$, con $0\le\alpha<1$. Su respuesta es $H(e^{i\omega})=1-\alpha e^{-i\omega}$ y $|H|^2=1+\alpha^2-2\alpha\cos\omega$. Realza las frecuencias altas respecto de las bajas. No corrige clipping y no es obligatorio en todos los frontends.''','preemphasis')
add(S,23,'Se aproxima la voz como localmente estacionaria durante ventanas cortas; no es una propiedad exacta de cualquier fragmento. Por ejemplo, ventanas de 25 ms con salto de 10 ms se solapan un 60 %. Son parámetros configurables.','stft')
add(S,25,r'''Una ventana rectangular vale uno dentro del frame. La Hann simétrica de longitud W es $w[n]=0.5-0.5\cos(2\pi n/(W-1))$, para 0≤n<W. La versión periódica cambia el denominador a W. La Hamming simétrica usa $0.54-0.46\cos(2\pi n/(W-1))$. No se intercambian sus signos ni denominadores sin cambiar la ventana.''','stft')
add(S,27,'El tamaño de FFT determina la rejilla de bins. La longitud y forma de la ventana determinan la capacidad de separar componentes cercanas. Usar más ceros no aporta nuevas observaciones. El cuadrado de la magnitud necesita una normalización adicional si se quiere expresar una densidad de potencia.','fft')
add(S,29,'Los filtros Mel se aplican a frecuencias físicas de los bins. Pueden normalizarse a pico uno o por área, con resultados distintos. La escala comprime el eje de Hz a frecuencias altas; no significa que el oído tenga mayor discriminación absoluta en Hz allí.','mel')
add(S,33,r'''Sea $L_m=\log(\max(S_m,\epsilon))$ la energía log-Mel de M bandas. Los MFCC se obtienen con DCT-II:
$$c_r=\gamma_r\sum_{m=0}^{M-1}L_m\cos\left(\frac{\pi r(m+1/2)}M\right).$$
La normalización depende de la implementación. Retener 13 o 20 coeficientes es una elección, no una ley. DCT no garantiza independencia estadística. El cepstrum real clásico, en cambio, usa la inversa de Fourier de log|X|: es una construcción relacionada, pero distinta.''','mfcc')
add(S,36,r'''La función característica de una variable aleatoria es $\varphi(t)=\mathbb E[e^{itX}]$ y siempre existe. Su desarrollo en momentos, cuando está justificado, comienza en n=0 y requiere condiciones de convergencia; no toda distribución admite esa serie. No es un paso necesario para calcular chroma.''','uncertainty')
add(S,37,'Una representación tiempo-frecuencia no es siempre una densidad de probabilidad. El espectrograma es no negativo; la distribución de Wigner puede tener valores negativos y términos de interferencia.','stft')
add(S,38,r'''Para $E=\int |x(t)|^2dt>0$, la densidad temporal normalizada es $|x(t)|^2/E$. Su media y varianza se calculan con esa normalización. Tener varianza finita no implica que la mayoría de la energía esté necesariamente dentro de dos desviaciones estándar con un porcentaje gaussiano fijo.''','uncertainty')
add(S,39,'La transformada de Fourier depende de una convención declarada de signo y normalización. Sus variables son tiempo y frecuencia; la propagación y dispersión físicas dependen del medio y no se deducen universalmente de una transformada.','fft')
add(S,40,'Wigner tiene marginales de energía temporal y espectral con una convención coherente. Eso no la convierte en una probabilidad conjunta positiva. Un espectrograma suaviza la energía mediante una ventana y sus marginales no son sin más las mismas expresiones sin suavizado.','stft')
add(S,41,unc,'uncertainty')
for c in [44,45]:add(S,c,r'''Una altura logarítmica puede definirse como $p=\log_2(f/f_{ref})$ para f>0. Usar un cociente hace adimensional el logaritmo. La parte entera identifica la octava relativa y la parte fraccionaria la clase de altura; al discretizar en doce clases se agrupan frecuencias separadas por octavas.''','cqt')
add(S,47,'Chroma agrupa energía de distintas octavas en clases de altura. Pierde información de registro y puede ser útil para armonía. Ninguna distribución de Wigner evita el principio de incertidumbre; la concentración aparente puede incluir valores negativos e interferencias.','cqt')
add(S,49,r'''La CQT usa centros geométricos $f_k=f_{min}2^{k/B}$ y ventanas de longitud aproximada $N_k=\lceil Qf_s/f_k\rceil$, con $Q\approx(2^{1/B}-1)^{-1}$. A frecuencias bajas usa ventanas más largas. Hay variantes invertibles y rutinas de inversión aproximada, como librosa.icqt. Conservar coeficientes complejos es distinto de conservar solo magnitud; no se debe afirmar que toda CQT sea imposible de invertir.''','cqt')
add(S,50,r'''Con frecuencia f en Hz, una convención de Wigner es $W_x(t,f)=\int x(t+\tau/2)\overline{x(t-\tau/2)}e^{-2\pi if\tau}d\tau$. Puede tomar valores negativos; se usa como representación de energía con interferencias, no como una probabilidad conjunta ordinaria.''','uncertainty','Distribución de Wigner')
add(S,51,'Las representaciones anteriores deben elegirse según la tarea y la información que se desea conservar.','stft','Elección de representación')

D='clase-14-1-2-'
add(D,10,'La diarización estima quién habla y cuándo mediante segmentos y etiquetas de hablante, normalmente anónimas. ASR transcribe qué se dice. Se pueden combinar, pero no son la misma tarea.','diarization')
add(D,11,'La detección de actividad vocal localiza regiones con habla. Un encoder produce embeddings y un algoritmo de clustering agrupa segmentos por hablante. Agrupar no revela por sí solo la identidad real de una persona. El solapamiento de hablantes necesita tratamiento específico.','diarization')
add(D,14,r'''GE2E entrena con N hablantes y M≥2 segmentos por hablante. Los embeddings se normalizan en norma L2. Para comparar un segmento con su propio hablante, el centroide excluye ese segmento: $c_j^{(-i)}=\frac1{M-1}\sum_{m\ne i}e_{jm}$. Los centroides de otros hablantes usan sus M segmentos. Se aplica similitud coseno con escala positiva y sesgo aprendidos, seguida del objetivo de entrenamiento.''','ge2e','Entrenamiento GE2E')
add(D,24,'Los datos y resultados citados corresponden a experimentos publicados en 2018. No describen necesariamente los sistemas desplegados hoy ni permiten prometer el mismo rendimiento con otros datos.','diarization')
add(D,36,r'''En un modelo angular alrededor de un centro unitario, una densidad proporcional a $\exp[-\theta^2/(2\sigma^2)]$ debe normalizarse respecto de la medida de superficie. En dimensión N, el área de la esfera unidad es $2\pi^{N/2}/\Gamma(N/2)$ y el elemento angular contiene $\sin^{N-2}\theta$. La densidad marginal angular no es una gaussiana ordinaria ni tiene necesariamente su máximo en cero.''','links')
add(D,37,'Normalizar la suma de vectores da la dirección de la media extrínseca, si la suma no es cero. No es en general la media de Fréchet para distancias geodésicas sobre la esfera. La concentración angular usada por Links es una aproximación de modelado.','links')
add(D,39,r'''Con 0<T_c<1, el umbral aproximado de Links para un nuevo vector y un subcluster de k miembros es
$$s(k)=\frac{T_c^2}{\sqrt{1/k+(1-1/k)T_c^2}}.$$
Así s(1)=T_c² y el límite al crecer k es T_c. El numerador es T_c². Es un umbral del modelo y sus supuestos, no una identidad universal para cualquier distribución de embeddings.''','links')
add(D,42,'En la comparación entre subclusters, k_J cuenta los vectores del subcluster J. Se crea una conexión cuando la similitud satisface el umbral de conexión; no se invierte esa condición. Las componentes conectadas del grafo definen los clusters.','links')
add(D,45,'Las etiquetas de cluster son arbitrarias: intercambiar sus números no cambia el agrupamiento. Para evaluar diarización se alinean hablantes y se usa una métrica como DER, declarando collar y tratamiento del solapamiento. Una exactitud de IDs sin alinear no es una evaluación válida.','diarization')
add(D,46,'El método de codo es una heurística sobre una curva de dispersión; no equivale a maximizar siempre el valor absoluto de su primera derivada. La cantidad de hablantes y la calidad del clustering deben evaluarse con un protocolo explícito.','diarization')
add(D,47,'En clustering espectral se construye una afinidad, se aplica el refinamiento definido y se examinan autovalores ordenados para estimar la cantidad de clusters. El criterio de eigengap requiere limitar el rango y tratar denominadores nulos. Una normalización por filas puede romper la simetría: no se debe usar un solver exclusivo de matrices simétricas sin comprobarla. El umbral no conoce las etiquetas reales.','diarization')

V='clase-05-3-2-'
add(V,14,'R-CNN original obtiene propuestas de región con selective search y procesa cada región con una CNN. Los anchors aparecen en el RPN de Faster R-CNN; no son sinónimo de las propuestas originales.','maskrcnn')
add(V,43,'El RPN de Faster R-CNN clasifica anchors y predice ajustes de cajas. En su etiquetado original, es positivo el anchor con mayor IoU para una caja real o con IoU superior a 0.7; por debajo de 0.3 es negativo si no fue asignado positivo. Los demás se ignoran. El artículo propuso entrenamiento alternado; las implementaciones conjuntas posteriores son otra elección.','maskrcnn')
add(V,63,r'''YOLOv1 divide la imagen en S×S celdas. Predice B cajas por celda y C probabilidades de clase compartidas por sus cajas. La pérdida suma regresión de centro y raíz de tamaño de la caja responsable, error de confianza con distintos pesos para objeto/fondo y error de clase en celdas con objeto. Los índices de celda recorren 0,…,S²−1 y los de caja 0,…,B−1. Es un objetivo diferente del utilizado por YOLOv3; no se deben intercambiar sus parametrizaciones.''','yolo2')
add(V,68,'Recall se traduce como exhaustividad o sensibilidad: TP/(TP+FN). No es «memoria». Las mejoras y cifras de YOLOv2 pertenecen a los datasets y protocolos del artículo.','yolo2')
add(V,71,'La capa passthrough de YOLOv2 reorganiza bloques espaciales 2×2 en canales y concatena esas características con un mapa de menor resolución. No es la suma identidad de un bloque residual ResNet.','yolo2')
add(V,72,'YOLO9000 combina detección y clasificación mediante WordTree, una jerarquía de categorías con probabilidades condicionales entre nodos hermanos. El modelo del artículo cubre 9418 categorías; no debe confundirse con las 1000 clases de ImageNet usadas en otros experimentos.','yolo2')
add(V,79,r'''Para una decisión binaria de clase, $p_t=p$ si y=1 y $p_t=1-p$ si y=0. Focal loss es $-\alpha_t(1-p_t)^\gamma\log p_t$. En RetinaNet se usa clasificación sigmoide por clase y anchor; no es únicamente una pérdida de objectness.''','focal')
add(V,82,r'''En la variante balanceada, $\alpha_t=\alpha$ para positivos y $1-\alpha$ para negativos. El factor $(1-p_t)^\gamma$ reduce el peso de ejemplos bien clasificados. Los valores γ=2 y α=0.25 son una configuración estudiada, no un óptimo universal.''','focal')
add(V,85,'RetinaNet utiliza una pirámide de mapas de características FPN calculados por la red. Es diferente de ejecutar el modelo sobre una pirámide de imágenes redimensionadas.','focal')
add(V,89,'Las comparaciones del artículo son resultados de sus experimentos y configuraciones. El ranking entre arquitecturas puede cambiar con el dataset, la métrica, la resolución y el presupuesto de cómputo.','focal')
add(V,90,'RetinaNet coloca nueve anchors por posición espacial: tres escalas por tres razones de aspecto. Los niveles P3–P7 tienen strides 8–128 y áreas base de 32²–512² píxeles. No son solo nueve cajas en todo un nivel.','focal')
add(V,93,'Los autores de YOLOv3 informaron que focal loss no mejoró su configuración probada. Ese resultado no demuestra una causa universal ni que el objetivo sea inútil para otros detectores.','yolo3')
Y='clase-05-3-3-'
add(Y,4,'YOLOv3 es un detector convolucional con predicciones a varias escalas. Admite resoluciones compatibles con sus strides, pero cambiar la entrada cambia los mapas y el coste. Una red convolucional no es automáticamente invariante a escala; las imágenes de un batch deben tener dimensiones compatibles.','yolo3')
add(Y,5,'Cada posición del mapa tiene un campo receptivo en la imagen; no equivale al tamaño de la celda de la rejilla. Los anchors son formas de referencia, no detectores preasignados a clases. Con tres anchors y C clases, la salida tiene 3(5+C) canales por posición.','yolo3')
add(Y,9,'YOLOv3 usa nueve tamaños de anchor repartidos entre tres escalas, tres por escala. Las formas se obtienen mediante clustering de cajas de entrenamiento usando distancia basada en IoU; no son nueve anchors en total para toda la imagen.','yolo3')
add(Y,11,'La sigmoide produce un desplazamiento entre cero y uno dentro de la celda. Por ejemplo, si el índice horizontal es 6 y σ(t_x)=0.7, el centro horizontal es 6.7 en unidades de celda.','yolo3')
add(Y,15,r'''En píxeles de la imagen, $b_x=(\sigma(t_x)+c_x)s_x$, $b_y=(\sigma(t_y)+c_y)s_y$, $b_w=a_we^{t_w}$ y $b_h=a_he^{t_h}$, con anchors a en píxeles y strides s. Para coordenadas normalizadas se divide después por ancho/alto de imagen. Si el código expresa anchors en celdas, debe convertirlos de forma coherente al aplicar el stride.''','yolo3')
add(Y,16,'Objectness es una predicción aprendida de presencia de objeto para una caja. El entrenamiento asigna positivos y puede ignorar ciertas predicciones solapadas. No obliga a que todas las celdas vecinas de un objeto tengan confianza uno.','yolo3')
add(Y,17,'YOLOv3 usa salidas sigmoidales independientes para clases, sin softmax entre ellas. La arquitectura permite etiquetas no mutuamente excluyentes; el postprocesado del laboratorio selecciona la clase de mayor score para cada caja.','yolo3')
add(Y,22,'Para entrada 416×416, las rejillas 52×52, 26×26 y 13×13 con tres anchors cada una producen 3(52²+26²+13²)=10 647 cajas por imagen, antes del filtrado.','yolo3')
add(Y,32,'La ruta de fusión aumenta la resolución con interpolación de vecino más cercano y concatena mapas de una capa anterior. Hay que mantener esa elección al cargar pesos de la arquitectura Darknet descrita.','yolo3')
add(Y,64,'En el archivo de pesos YOLOv3 usado aquí, el encabezado inicial leído como cinco int32 ocupa 20 bytes (160 bits). El formato Darknet depende de la versión y puede almacenar seen como entero de 64 bits. No se deben confundir 160 bits con 160 bytes.','yolo3')
add(Y,70,'El tensor de predicciones tiene forma (batch, 10 647, 85) para entrada 416 y COCO: 4 coordenadas, 1 objectness y 80 scores de clase. El primer eje cuenta imágenes, no cajas.','yolo3')
add(Y,73,'La implementación didáctica aplica NMS con bucles. También existen operaciones optimizadas y agrupadas, como torchvision.ops.batched_nms; los bucles Python no son una limitación intrínseca del algoritmo.','nms')
add(Y,75,'bbox_iou compara una caja con un conjunto de cajas y devuelve sus intersecciones sobre uniones. Las coordenadas y la convención de bordes deben ser coherentes; para cajas continuas no se añade un píxel a ancho y alto.','nms')
add(Y,81,'Las filas conservadas son detecciones predichas, no «detecciones verdaderas» verificadas con ground truth. El postprocesado debe definir una salida vacía estable cuando no quedan cajas.','nms')
add(Y,90,'El tensor se organiza por ejes (batch, canales, alto, ancho). PyTorch no impone que esos canales sean RGB; este modelo se entrenó con ese orden, por lo que una imagen BGR de OpenCV debe convertirse a RGB antes de inferencia.','yolo3')
add(Y,102,'El ejemplo procesa vídeo frame a frame. Es una elección de implementación; también se pueden agrupar frames en batches, con compromisos de memoria y latencia.','yolo3')
I='clase-05-3-1-'
add(I,17,'En torchvision la transformación de reflexión horizontal aleatoria se llama RandomHorizontalFlip. Una reflexión puede ser una aumentación válida si conserva la etiqueta de la tarea.','augment')
add(I,24,'ColorJitter modifica aleatoriamente brillo, contraste, saturación o tono según su configuración. Las aumentaciones deben respetar el significado de las etiquetas.','augment')
add(I,30,'ToTensor convierte una imagen a un tensor por imagen; el DataLoader forma después el batch. Para imágenes uint8 habituales convierte 0–255 a 0–1. No normaliza automáticamente cualquier entrada flotante ni aplica la estandarización por media y desviación.','augment')
add(I,71,'El experimento siguiente inicializa una red y la entrena con los datos del ejemplo. Solo se considera preentrenamiento si se cargan pesos aprendidos previamente; inicializar una arquitectura conocida no basta.','augment','Entrenamiento del ejemplo')
add(I,125,'NMS selecciona una caja con score alto y suprime otras con IoU superior al umbral. No promedia ni fusiona sus coordenadas. Hay que especificar si se aplica por clase o de forma independiente de la clase.','nms')
add(I,126,'En la convención habitual se conservan cajas con IoU menor o igual al umbral respecto de las seleccionadas. La variante batched_nms separa grupos por identificador; otras implementaciones pueden usar una supresión independiente de la clase.','nms')
add(I,134,'Las coordenadas normalizadas se expresan respecto del ancho y alto. Las cajas generadas o decodificadas pueden salirse de [0,1] hasta que se recorten explícitamente.','ssd')
add(I,139,'Mapas de mayor resolución ofrecen más posiciones espaciales para anchors y ayudan a localizar objetos pequeños. Eso no demuestra que los objetos pequeños sean más frecuentes en un dataset.','ssd')
add(I,141,'Los centros de una rejilla normalizada quedan dentro de la imagen. Los bordes de sus anchors pueden quedar fuera por el tamaño y la relación de aspecto. Recortarlos es una operación adicional.','ssd')
Z='clase-05-3-vision-'
add(Z,18,'El dataset sintético de bananas usado por D2L permite demostrar detección con un conjunto pequeño. Existen otros datasets de distintos tamaños; no se debe afirmar que no hay ningún dataset pequeño de detección.','ssd')
add(Z,34,'Para a anchors por posición y q clases de objeto más fondo, la cabeza produce a(q+1) canales y hwa anchors. Los índices son 0≤i<a y 0≤j≤q; el canal i(q+1)+j representa la clase j del anchor i.','ssd')
add(Z,48,'Tres reducciones espaciales por un factor de dos convierten una entrada 256×256 en mapas 32×32: 256/2³=32.','ssd')
add(Z,54,'La configuración del ejemplo usa escalas pequeñas 0.2, 0.37, 0.54, 0.71 y 0.88. Las escalas complementarias se calculan con medias geométricas de escalas adyacentes; por ejemplo √(0.2·0.37)≈0.272 para el primer bloque. Deben corresponder a los valores utilizados en el código.','ssd')
add(Z,67,'La exactitud por anchor y el error absoluto de offsets son diagnósticos del entrenamiento. Una exactitud alta puede estar dominada por el fondo y no equivale a buen rendimiento de detección. La evaluación final requiere métricas de cajas y clases, como AP bajo un protocolo de IoU definido.','ssd')
U='clase-05-4-transformers-'
add(U,98,'Los embeddings densos son representaciones aprendidas. Bag of words cuenta ocurrencias en un documento y no es lo mismo que un one-hot por token. Word2Vec aprende regularidades de contexto; no garantiza que toda pareja cercana en texto termine cercana en el espacio ni que resuelva comprensión semántica por sí sola.','word2vec')
add(U,112,'El encoder y el decoder tienen embeddings en su entrada. Las capas siguientes reciben representaciones contextuales. El batch puede usar padding y máscaras con longitud variable dentro del contexto soportado; no tiene que fijarse a la oración más larga del corpus completo.','attention')
add(U,118,'La codificación posicional aporta información de orden a la atención. Puede ser aprendida o fija, aditiva o aplicada mediante otros mecanismos. No garantiza crear distancias semánticas significativas entre vectores.','attention')
add(U,122,'Las frecuencias de los pares sinusoidales disminuyen con el índice de dimensión. Son valores continuos evaluados en posiciones enteras, no un contador binario. La eficiencia en memoria depende de la representación y precisión elegidas, no se deduce simplemente de que sean números flotantes.','attention')
add(U,123,r'''Para una frecuencia ω y un desplazamiento δ, el par (sin(iω),cos(iω)) se transforma en (sin((i+δ)ω),cos((i+δ)ω)) mediante una matriz 2×2 independiente de i:
$$\begin{pmatrix}\cos(\delta\omega)&\sin(\delta\omega)\\-\sin(\delta\omega)&\cos(\delta\omega)\end{pmatrix}.$$
Esta identidad facilita representar desplazamientos; no garantiza que cualquier modelo aprenda a usarlos ni extrapole bien.''','attention')
add(U,134,'La capa lineal produce logits sobre el vocabulario de salida y softmax los convierte en probabilidades por token. Greedy decoding escoge el máximo; muestreo y beam search son alternativas. El vocabulario puede contener subpalabras. Softmax no produce log-probabilidades: para ello se usa log-softmax.','attention')

SOURCES['ntm']=('Graves et al. · Neural Turing Machines','https://arxiv.org/abs/1410.5401')
SOURCES['faster']=('Ren et al. · Faster R-CNN','https://arxiv.org/abs/1506.01497')
for patch in PATCHES:
    if patch['prefix']==V and patch['cell'] in ['celda-14','celda-43']:patch['source']='faster'
add(D,20,r'''La similitud correcta es $S_{ji,k}=w\cos(e_{ji},c_k)+b$ para k≠j y $S_{ji,j}=w\cos(e_{ji},c_j^{(-i)})+b$, con w>0. El sesgo queda **fuera** del coseno. El objetivo softmax es $L_{ji}=-S_{ji,j}+\log\sum_k e^{S_{ji,k}}$; la etiqueta objetivo es one-hot, pero las probabilidades no se vuelven exactamente cero o uno con logits finitos. La alternativa contrastiva penaliza el positivo y el negativo con mayor similitud. GE2E suma las pérdidas de los segmentos del batch.''','ge2e')
add(D,21,'GE2E reutiliza un batch con varios hablantes para comparar cada segmento con centroides positivos y negativos. Esto aporta muchas comparaciones en una actualización. No significa que su gradiente o el paso del optimizador sean idénticos a ejecutar una cantidad fija de pasos TE2E.','ge2e')
add(U,6,'La atención neuronal calcula compatibilidades, normaliza puntuaciones y combina vectores de valor. Los pesos no son necesariamente correlaciones estadísticas ni constituyen una medición de la atención humana.','attention')
add(U,7,r'''Un encoder recurrente produce estados $h_t\in\mathbb R^d$. Un seq2seq puede resumirlos en un contexto fijo c y factorizar $p(y\mid x)=\prod_{t=1}^{T_y}p(y_t\mid y_{<t},c)$. Comprimir la entrada en un único vector puede dificultar el uso de secuencias largas, sin hacerlas matemáticamente imposibles. La atención ofrece acceso a una secuencia de estados.''','bahdanau')
add(U,13,r'''En Bahdanau, $e_{ij}=a(s_{i-1},h_j)$, $\alpha_{ij}=e^{e_{ij}}/\sum_k e^{e_{ik}}$ y $c_i=\sum_j\alpha_{ij}h_j$. El decoder usa ese contexto para actualizar su estado y predecir el token. La información se distribuye entre estados de la fuente; esto no demuestra una reducción del coste computacional total, pues se calculan alineaciones por paso.''','bahdanau')
add(U,27,r'''Con índices 0,…,N−1, el desplazamiento circular es $\tilde w_t(i)=\sum_{j=0}^{N-1}w_t^g(j)s_t((i-j)\bmod N)$. Después se realza con $w_t(i)=\tilde w_t(i)^{\gamma_t}/\sum_{j=0}^{N-1}\tilde w_t(j)^{\gamma_t}$, para γ_t≥1. La suma debe ser no nula y la distribución inicial estar normalizada.''','ntm')
add(U,33,r'''LSTMN almacena estados ocultos h_i y celdas c_i. Para t>1 puntúa estados pasados con $a_i^t=v^\top\tanh(W_hh_i+W_xx_t+W_{\tilde h}\tilde h_{t-1})$ y normaliza sobre i<t. Las lecturas son $\tilde h_t=\sum_{i<t}s_i^t h_i$ y $\tilde c_t=\sum_{i<t}s_i^t c_i$. Las compuertas usan la lectura oculta y la entrada actual; la actualización de celda combina $f_t\odot\tilde c_t+i_t\odot\hat c_t$. El primer paso requiere la inicialización definida por el modelo.''','cheng')
add(U,34,'Deep Attention Fusion combina una lectura de la memoria fuente con la memoria recurrente objetivo mediante una compuerta adicional. La atención entre fuente y objetivo es inter-atención; la consulta sobre el historial de la propia secuencia es intra-atención. Sus parámetros y ecuaciones deben seguir la arquitectura LSTMN del artículo.','cheng')
add(U,37,'NMT significa traducción automática neuronal; NTM significa Neural Turing Machine. El modelo de traducción encoder–decoder con atención global de Luong es NMT y no requiere memoria externa NTM. Factoriza la probabilidad de salida en condicionales autoregresivos.','luong')
add(U,38,r'''En Luong se puntúan el estado actual h_t del decoder y los estados fuente $\bar h_s$. Las variantes son dot: $h_t^\top\bar h_s$; general: $h_t^\top W_a\bar h_s$; concat: $v_a^\top\tanh(W_a[h_t;\bar h_s])$. Dot requiere anchos iguales; las proyecciones permiten otros anchos. Se normaliza sobre posiciones fuente válidas. La variante location usa un vector de logits dependiente de h_t y tiene las restricciones de longitud indicadas en el artículo.''','luong')
add(U,40,'En cada paso del decoder se construye un contexto a partir de los estados del encoder. Los estados recurrentes se actualizan durante toda la secuencia, no solo al principio de una capa. La bidireccionalidad del encoder es una elección de arquitectura.','luong')
add(U,42,r'''La atención local usa posiciones alrededor de un centro p_t, con hasta 2D+1 índices enteros para radio D entero. En local-m el centro es t; en local-p es $S\sigma(v_p^\top\tanh(W_ph_t))$. Luong atenúa la alineación con $\exp[-(s-p_t)^2/(2\sigma^2)]$, con σ=D/2. El producto no suma necesariamente uno. Si se renormaliza, se obtiene una variante; calcular primero scores globales tampoco ahorra el coste de puntuarlos.''','luong')
add(U,45,'La atención discreta de Xu muestrea una posición; la suave combina anotaciones con pesos continuos. Muestrear después de calcular todos los scores no evita ese cálculo. El muestreo requiere un estimador de gradiente o una relajación; seleccionar una sola posición no garantiza un ahorro global ni mejor rendimiento.','hard')
add(U,46,'En captioning, una CNN codifica la imagen en L vectores de dimensión D asociados a regiones con campos receptivos. El decoder produce una secuencia de tokens del vocabulario. El encoder visual no genera por sí solo la descripción y se usan características convolucionales espaciales, no necesariamente la capa con menor tamaño.','hard')
add(U,49,r'''La atención suave usa $z_t=\sum_i\alpha_{ti}a_i$, la esperanza de la selección bajo una distribución categórica. Sin embargo, pasar esa esperanza por una red no lineal no equivale en general a promediar sus salidas. Las aproximaciones de Taylor y de media geométrica normalizada del artículo son aproximaciones, no identidades de esperanzas para cualquier LSTM.''','hard')
add(U,59,'Cada cabeza calcula activaciones Q, K y V a partir de matrices aprendidas. En el Transformer base se eligieron 8 cabezas de ancho 64 para un modelo de ancho 512. Es una configuración concreta, no un coste constante independiente de longitud ni una dimensión obligatoria.','attention')
add(U,62,r'''Para una consulta q_i y una clave k_j, el producto punto es $q_i^\top k_j=\sum_{r=1}^{d_k}q_{ir}k_{jr}$. El índice j recorre tokens y r recorre coordenadas; no deben confundirse con d_k, que es el ancho de la clave.''','attention')
add(U,65,r'''Se dividen los productos punto por $\sqrt{d_k}$. Si sus componentes tienen varianza uno y cumplen las hipótesis de independencia apropiadas, el producto tiene varianza d_k; el escalado controla esa magnitud y ayuda a evitar saturación del softmax. No garantiza por sí solo estabilidad de todos los gradientes.''','attention')

add(V,25,r'''Fast R-CNN calcula un mapa convolucional de la imagen y aplica RoI pooling a n propuestas. Cada región se transforma a un tensor C×H_R×W_R; el batch de regiones tiene forma n×C×H_R×W_R. La cabeza produce probabilidades para K clases de objeto más fondo y ajustes de caja. La regresión original es específica por clase (4K valores para las clases de objeto); una cabeza de cuatro valores independiente de clase es una variante, no la misma parametrización.''','faster')
add(V,36,r'''Para una región con etiqueta u, la pérdida multitarea de Fast R-CNN es $L=-\log p_u+\lambda\,\mathbf1[u\ge1]\sum_{r\in\{x,y,w,h\}}\operatorname{smooth}_{L1}(t_r^u-v_r)$. Aquí v es el **objetivo de regresión codificado relativo a la propuesta**, no las coordenadas brutas de la caja real. La rama de caja se omite para fondo. En la definición original, smooth_L1(z)=0.5z² si |z|<1 y |z|−0.5 en otro caso; λ controla su peso.''','faster')
add(V,48,'Mask R-CNN añade una rama de máscaras a Faster R-CNN y utiliza RoIAlign para extraer características alineadas por región. La interpolación bilineal permite evaluar posiciones fraccionarias sin la cuantización de límites de RoI pooling. Las cabezas predicen clase, ajustes de caja y una máscara por región.','maskrcnn')
add(V,49,'RoIAlign evita redondear los límites y las coordenadas de muestreo de cada región. Usa interpolación bilineal de los mapas de características y agrega muestras dentro de cada bin de salida. Es especialmente relevante para preservar alineación espacial en segmentación.','maskrcnn','RoIAlign')
add(V,52,'RoIAlign evita la cuantización de coordenadas usada por RoI pooling; no se trata de hashing. La escala espacial convierte coordenadas de imagen a coordenadas del mapa y la interpolación bilineal evalúa los puntos fraccionarios. Los detalles de alineación deben coincidir con la implementación usada.','maskrcnn')

add('clase-05-1-cnn-',7,r'''Para una imagen X y una representación H con estructura espacial, una capa densa puede escribirse como
$$H_{ij}=U_{ij}+\sum_{k,l}W_{ijkl}X_{kl}.$$
Cada salida tiene sus propios pesos. Si se exige localidad y se comparten pesos entre posiciones, se obtiene una operación de correlación cruzada:
$$H_{ij}=b+\sum_{a,b'}K_{ab'}X_{i+a,j+b'}.$$
La elección de bordes, stride y dilatación completa su definición. La compartición favorece equivariancia a traslaciones compatibles con la rejilla y los bordes; no garantiza invariancia de toda la red.''','conv')
add('clase-05-1-cnn-',17,r'''Con entrada $X=\begin{pmatrix}0&1&2\\3&4&5\\6&7&8\end{pmatrix}$ y kernel $K=\begin{pmatrix}0&1\\2&3\end{pmatrix}$, stride uno y sin padding, la correlación cruzada produce $\begin{pmatrix}19&25\\37&43\end{pmatrix}$. Por ejemplo, la primera salida es 0·0+1·1+3·2+4·3=19. Se multiplica y suma cada ventana; no se invierte el kernel como en la convolución matemática.''','conv')
add(V,18,r'''Para una propuesta con centro y tamaño $(p_x,p_y,p_w,p_h)$, un regresor predice offsets d. La caja ajustada se decodifica con $\hat g_x=p_x+p_wd_x$, $\hat g_y=p_y+p_hd_y$, $\hat g_w=p_we^{d_w}$ y $\hat g_h=p_he^{d_h}$. Anchos y altos de la propuesta deben ser positivos. Los offsets provienen de características de la región, aunque se escriban de forma abreviada como d(p).''','faster')
add(V,21,r'''Para una caja real g y una propuesta p con tamaños positivos, los objetivos son $t_x=(g_x-p_x)/p_w$, $t_y=(g_y-p_y)/p_h$, $t_w=\log(g_w/p_w)$ y $t_h=\log(g_h/p_h)$. Son valores reales sin un intervalo fijo de salida. R-CNN original usa regresores ajustados con pérdida cuadrática regularizada; Fast R-CNN integra una cabeza de regresión con smooth L1. No son el mismo entrenamiento.''','faster')

add(S,16,'FFT designa una familia de algoritmos para calcular la DFT. Cooley–Tukey descompone un tamaño compuesto N=N₁N₂ y combina subtransformadas con factores de giro. La variante radix-2 requiere N potencia de dos. El algoritmo de factores primos utiliza una factorización con factores coprimos; no cualquier partición satisface ese requisito. El orden N log N expresa complejidad asintótica, no un tiempo medido.','fft')
SOURCES['animation']=('Matplotlib · Animation.to_jshtml','https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.Animation.html#matplotlib.animation.Animation.to_jshtml')
add(R,139,'El ejemplo usa FuncAnimation y to_jshtml() para incrustar fotogramas y un reproductor JavaScript con controles. Esa salida no es un archivo de vídeo HTML5 y no requiere codificar con FFmpeg. to_html5_video() es otro método y sí depende de un codificador de vídeo configurado.','animation','Animación con controles JavaScript')

def apply():
    soups={p:BeautifulSoup(p.read_text(),'html.parser') for p in sorted(DOCS.rglob('*.html'))}
    def signature(cell):
        clone=BeautifulSoup(str(cell),'html.parser')
        for n in clone.select('.editorial-source,.figure-revision'):n.decompose()
        for n in clone.find_all(True):
            for a in list(n.attrs):
                if a=='id' or a.startswith('data-'):del n[a]
        return str(clone)
    index={}
    for p,s in soups.items():
        for c in s.select('section.cell[id]'):
            index.setdefault(signature(c),[]).append((p,c))
    report_path=ROOT/'reports/revision-integral.json'
    report=json.loads(report_path.read_text()) if report_path.exists() else []
    for patch in PATCHES:
        matched=[(p,s.find(id=patch['cell'])) for p,s in soups.items() if p.name.startswith(patch['prefix'])]
        matched=[(p,c) for p,c in matched if c is not None]
        if not matched:raise ValueError(f"Celda inexistente: {patch['prefix']}:{patch['cell']}")
        targets={id(c):(p,c) for p,c in matched}
        for p,c in matched:
            for pp,cc in index.get(signature(c),[]):targets[id(cc)]=(pp,cc)
        for p,c in targets.values():
            headings=[h.extract() for h in c.find_all(re.compile('^h[1-6]$'),recursive=False)]
            c.clear()
            for i,h in enumerate(headings):
                if i:
                    if h.get('id'):c.append(soups[p].new_tag('span',id=h['id']))
                    continue
                if patch['title']:
                    h.clear();h.string=patch['title']
                c.append(h)
            text=re.sub(r'\\\\(?=[A-Za-z])',r'\\',patch['text'])
            fragment=BeautifulSoup(render(text),'html.parser')
            for n in list(fragment.contents):c.append(n)
            c['data-reviewed-source']=SOURCES[patch['source']][1]
            note=soups[p].new_tag('p',attrs={'class':'note source-reference'})
            link=soups[p].new_tag('a',href=SOURCES[patch['source']][1]);link.string=SOURCES[patch['source']][0]
            note.append('Referencia: ');note.append(link);c.append(note)
            report.append({'page':str(p.relative_to(ROOT)),'cell':c['id'],'source':SOURCES[patch['source']][1]})
    for p,s in soups.items():p.write_text(str(s))
    report=list({(v['page'],v['cell']):v for v in report}.values())
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print('Celdas actualizadas:',len(report))

if __name__=='__main__':
    apply()
