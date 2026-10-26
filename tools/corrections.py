"""Correcciones editoriales verificables; no ejecuta entrenamientos."""
import re

W2V = '1 - Introducción al NLP  - Parte 1 - Word2Vec'
GLOVE = '1 - Introducción al NLP  - Parte 2 - GloVe'
PE = '11 - Positional Encoding (PE) y GPT - Parte 1'
ROPE = '13 - Introducción a GPT - RoPE - Parte 2'
ASR1 = '14 - Inotroducción a ASR - Parte 1'
ASR2 = '15 - Introducción a ASR - Parte 2'
REPLACEMENTS = {
W2V: {
26: r'''#### **1.2.2.2. El espectro de la similitud de coseno**

Para vectores no nulos, el coseno pertenece a $[-1,1]$:

* **$1$:** misma dirección, aunque las longitudes pueden ser distintas.
* **$0$:** direcciones ortogonales.
* **$-1$:** direcciones opuestas.

Estas son propiedades geométricas. En embeddings, la interpretación depende del modelo y del corpus: **un coseno negativo no demuestra antonimia y un coseno cero no demuestra ausencia de relación lingüística**. Los antónimos pueden aparecer cerca porque comparten contextos. La similitud tampoco garantiza sinonimia.''',
},
GLOVE: {
12: r'''### **2.1.1. Objetivo predictivo y estadísticas globales**

Word2Vec aprende de pares centro–contexto extraídos de ventanas locales a lo largo del corpus: esto también acumula información estadística global, aunque no construya explícitamente una matriz de conteos. El softmax completo cuesta $O(|V|d)$ por predicción. **Negative sampling y hierarchical softmax evitan recorrer todo el vocabulario**; por tanto, el softmax completo no describe todas las implementaciones de Word2Vec.

GloVe elige otro objetivo: ajustar productos punto a logaritmos de coocurrencias agregadas. Su eficiencia depende del corpus, la dispersión y la implementación; no es una superioridad universal sobre Word2Vec.''',
14: '_Fig. 2.2. Word2Vec y GloVe organizan de manera diferente las estadísticas de contexto; ambos aprovechan el corpus completo._',
15: r'''## **2.2. El surgimiento de GloVe y la matriz de coocurrencia**

GloVe precomputa conteos globales a partir de ventanas de contexto. La metáfora de «encender la luz» se refiere a **agregar los pares antes del entrenamiento**, no a que cada ventana abarque todo el documento.''',
16: r'''### **2.2.1. La estructura de la matriz $X$**

$x_{ij}$ agrega las apariciones del contexto $j$ junto al centro $i$. Según la construcción, pueden usarse pesos inversos a la distancia, de modo que los valores no tienen por qué ser enteros.

$$x_i=\sum_j x_{ij},\qquad P(j\mid i)=x_{ij}/x_i.$$

Esta es una distribución **empírica de coocurrencias de la ventana elegida**. No es la probabilidad verdadera de todo el lenguaje ni la frecuencia aislada de la palabra $i$. GloVe ajusta logaritmos de conteos; no entrena para copiar directamente un softmax de estas probabilidades.''',
19: r'''### **2.2.2. La eficiencia computacional**

Una matriz de $100000\times100000$ tiene $10^{10}$ posiciones, pero se almacena de forma dispersa. El objetivo se evalúa **solo para pares con $x_{ij}>0$**. Es necesario excluir esos ceros antes del logaritmo: en aritmética numérica $0\cdot\log(0)$ no es una operación válida.

La ponderación $h(x)$ reduce el peso relativo de conteos pequeños y se satura para conteos grandes. Esto no elimina el coste de construir la matriz ni garantiza más velocidad que negative sampling.''',
23: r'''Para comparar **dos palabras centrales**, «ice» y «steam», mantenemos fijo el contexto $k$ y calculamos $P(k\mid\mathrm{ice})/P(k\mid\mathrm{steam})$.

En la tabla del artículo original los cocientes aproximados son **8.9 para solid, 0.085 para gas, 1.36 para water y 0.96 para fashion**. Se calculan con probabilidades redondeadas y por eso no son igualdades exactas. Un cociente cercano a uno indica probabilidades parecidas; no elimina por sí solo todo el ruido.''',
24: r'''### **2.2.4. Interpretación geométrica: aproximación de ratios**

Para dos centros $i,j$ y un contexto fijo $k$, la motivación de GloVe es representar:

$$F(w_i-w_j,\widetilde w_k)\approx P(k\mid i)/P(k\mid j).$$

Mantener los índices consistentes es esencial: **comparar ice contra steam para solid es distinto de comparar solid contra gas para ice**.''',
26: r'''La exponencial transforma una diferencia escalar en un cociente:

$$\exp(a-b)=\exp(a)/\exp(b).$$

Esto motiva $\exp((w_i-w_j)^\top\widetilde w_k)$ como relación entre centros frente a un contexto. El objetivo final incorpora sesgos y ajusta $w_i^\top\widetilde w_k+b_i+\widetilde b_k$ a $\log x_{ik}$. **Una exponencial aislada no es una probabilidad normalizada ni una aproximación lineal.**''',
28: '_Fig. 2.5. Identidad exponencial y diferencia entre una puntuación positiva y una probabilidad normalizada._',
29: r'''El producto punto satisface $u^\top v=\|u\|\|v\|\cos\theta$: combina **normas y dirección**. Solo el coseno normalizado elimina la dependencia de la longitud. Restar productos punto produce una diferencia de puntuaciones; no una resta de vectores.''',
30: r'''#### **2.2.4.1. Analogía**

Imaginemos dos fichas, ice y steam, evaluadas frente a la misma etiqueta solid. Cada ficha obtiene una puntuación aprendida. Restar esas puntuaciones y exponenciar la diferencia produce un número positivo que puede modelar una razón. Es una analogía de **puntuaciones**, no de atracción magnética ni de fuerzas físicas.''',
34: r'''Tomemos las probabilidades redondeadas de la tabla original:

* **solid:** $1.9\times10^{-4}/(2.2\times10^{-5})\approx8.64$; el artículo informa 8.9 con sus cifras originales.
* **gas:** $6.6\times10^{-5}/(7.8\times10^{-4})\approx0.0846$.
* **water:** $3.0\times10^{-3}/(2.2\times10^{-3})\approx1.36$.
* **fashion:** $1.7\times10^{-5}/(1.8\times10^{-5})\approx0.944$; el artículo informa 0.96.

**Siempre cambia el centro ice/steam y se mantiene fijo el contexto.** El cociente water/fashion dentro de ice sería otro cálculo y no explica la cancelación comparativa anterior.''',
38: r'''La ecuación ajusta tres elementos:

* **Producto punto:** depende de la dirección y de las normas de los vectores.
* **Sesgos:** parámetros escalares aprendidos para centro y contexto.
* **Objetivo:** $\log x_{ij}$ del par observado.

Los sesgos ayudan a modelar efectos de frecuencia, pero no garantizan una geometría puramente direccional.''',
39: r'''### **2.2.6. Función de pérdida: mínimos cuadrados ponderados**

$$J=\sum_{i,j:x_{ij}>0}h(x_{ij})(u_j^\top v_i+b_i+c_j-\log x_{ij})^2.$$

Es una suma de errores cuadrados ponderados. Puede dividirse por una constante para obtener una media. GloVe usa este objetivo log-bilineal; Word2Vec con negative sampling usa otro objetivo eficiente, sin softmax completo.''',
42: r'''La función habitual es $h(x)=(x/x_{\max})^\alpha$ si $0<x<x_{\max}$, y $h(x)=1$ si $x\ge x_{\max}$. Valores usuales del artículo son $\alpha=0.75$ y $x_{\max}=100$.

**Los pares cero se excluyen antes de evaluar el logaritmo.** La saturación en uno limita la ponderación, pero el gradiente también depende del residual y de los vectores; no queda acotado automáticamente.''',
44: '_Fig. 2.9. Pares positivos y función de ponderación; los ceros se excluyen antes de calcular el logaritmo._',
48: r'''1. **Predicción por debajo del objetivo:** si $e_{ij}=u_j^\top v_i+b_i+c_j-\log x_{ij}<0$, un paso de descenso simple mueve $v_i$ en la dirección $+u_j$ y eleva su producto punto con $u_j$ fijo. No implica necesariamente reducir la distancia euclidiana entre sus puntas.''',
50: '_Fig. 2.11. Dirección del paso de gradiente; se ajusta una puntuación escalar._',
51: r'''2. **Predicción por encima del objetivo:** si $e_{ij}>0$, el descenso mueve $v_i$ en la dirección $-u_j$ para reducir el producto punto, con $u_j$ fijo. AdaGrad reescala cada coordenada, y también se actualizan contextos y sesgos.''',
53: '_Fig. 2.12. Residual positivo: disminuye la puntuación prevista, sin una fuerza física de repulsión._',
54: r'''3. **Residual cero:** ese par aporta gradiente cero, aunque otros pares todavía pueden modificar los mismos parámetros.

4. **Ponderación:** $h(x_{ij})$ escala el error de los pares observados. Su saturación no limita por sí sola todo el gradiente. Los pares cero se omiten explícitamente.''',
69: r'''#### **2.2.7.4. Interpretación geométrica**

$$\nabla_{v_i}J=2\sum_{j:x_{ij}>0}h(x_{ij})e_{ij}u_j.$$

Cada contribución combina el peso $h(x_{ij})$, el residual escalar $e_{ij}$ y el vector $u_j$. El paso se toma en la dirección **opuesta** al gradiente. No es una ley de atracción entre puntos; con AdaGrad, cada coordenada se reescala por su historial de gradientes.''',
70: r'''### **2.2.8. Simetría y representación dual**

Con una ventana simétrica y pesos simétricos puede cumplirse $x_{ij}=x_{ji}$. Una ventana direccional no tiene esa garantía. GloVe mantiene dos matrices de parámetros: centros $W$ y contextos $\widetilde W$.''',
72: r'''Aunque los conteos sean simétricos, **no se impone $W=\widetilde W$**: existen distintas soluciones de la factorización. Una representación final habitual es $e_i=w_i+\widetilde w_i$. Es una elección de extracción, no un colapso obligatorio ni una garantía de eliminar el sobreajuste. También pueden usarse variantes de combinación de embeddings en otros modelos.''',
},
PE: {}, ROPE: {},
ASR2: {
38: r'''Para este ejemplo elegimos audio a **16 kHz**, ventanas de **400 muestras (25 ms)** y saltos de **160 muestras (10 ms)**. La FFT se completa a **512 puntos** para ilustrar Radix-2. **Whisper usa una FFT de 400 puntos y Hann**; Wav2Vec2 puede extraer características directamente de la forma de onda. Estos parámetros no son universales para todo ASR.''',
57: r'''Esta celda permite escuchar el original y dos construcciones didácticas. La reconstrucción por ventanas depende de cómo se solapan y normalizan los bloques; una pulsación audible puede ser un artefacto de esa reconstrucción. **El modelo no recibe un audio «pulsado»: recibe las características o muestras que define su arquitectura.**''',
64: r'''**A. Memoria de una DFT matricial explícita**

Con $N=960000$, almacenar una matriz densa $N\times N$ en complex64 requiere $N^2\times8=7372800000000$ bytes: aproximadamente **7.37 TB decimales o 6.71 TiB**. Este coste pertenece a esa implementación matricial; una DFT directa calculada con bucles no necesita almacenar la matriz completa. La FFT evita el coste temporal cuadrático.''',
74: r'''Una implementación **iterativa Radix-2 DIT** puede reordenar previamente la entrada por inversión de bits y producir salida en orden natural. Una versión recursiva separa pares e impares mediante las llamadas y no requiere el mismo paso explícito. La ubicación del reordenamiento depende de la variante.''',
135: r'''1. **Este laboratorio usa `power=1.0`:** devuelve la magnitud $|X|=\sqrt{X_r^2+X_i^2}$. Por eso la conversión usa `multiplier=20.0`. La variante posterior con `power=2.0` devuelve $|X|^2$ y usa factor 10.''',
137: r'''3. **`amin=1e-5`:** reemplaza magnitudes menores que ese piso antes del logaritmo. Con referencia uno, el mínimo es $20\log_{10}(10^{-5})=-100$ dB. **Es una decisión numérica**; no describe por sí sola el umbral de audición, el ruido del micrófono ni la calidad de 16 bits.''',
138: r'''4. **`db_multiplier=0.0`:** corresponde a $\log_{10}(\mathrm{ref})=0$, es decir, referencia uno. Una magnitud espectral igual a uno da 0 dB. **Una STFT sin normalizar puede superar uno aunque las muestras de audio estén en $[-1,1]$**. Esta escala no se convierte automáticamente en dBFS ni en dB SPL.''',
153: r'''3. **`amin=1e-10` en potencia:** el piso es $10\log_{10}(10^{-10})=-100$ dB respecto a referencia uno. Coincide con el piso de magnitud $10^{-5}$. Es un límite numérico; no garantiza conservar toda información útil de cualquier grabación.''',
154: r'''4. **Referencia de los dB:** `db_multiplier=0.0` usa referencia espectral uno. Potencias mayores que uno producen dB positivos. La normalización de las muestras temporales no normaliza automáticamente la STFT; para hablar de dBFS o de presión sonora hace falta definir la calibración correspondiente.''',
161: r'''> El logaritmo comprime la escala de magnitud o potencia. Sin pisos, para $A>0$ y $P=A^2$:

$$10\log_{10}(P/P_{\rm ref})=20\log_{10}(A/A_{\rm ref}),\qquad P_{\rm ref}=A_{\rm ref}^2.$$

Con pisos, la equivalencia exacta requiere $\epsilon_P=\epsilon_A^2$. **Sumar el mismo $\epsilon$ a $A$ y a $A^2$ no conserva la igualdad.**''',
170: r'''> El rango de los dB depende de la referencia y de la normalización espectral. Con piso de potencia $10^{-10}$ y referencia uno, el mínimo es $-100$ dB; el máximo puede superar 0 dB. El logaritmo transforma un producto fuente–filtro en suma; su separación requiere supuestos y procesamiento adicional, por ejemplo cepstral.''',
},
}

for name in [PE, ROPE]:
 REPLACEMENTS[name].update({
 6: '## <font color="#de9f68">**11.1. Equivariancia a la permutación en self-attention**</font>',
 11: r'''Sin posiciones ni máscara dependiente del orden, la atención por filas verifica $\mathrm{SA}(PX)=P\mathrm{SA}(X)$. Al permutar los tokens se permutan las filas de salida: **es equivariancia, no invariancia**. Una agregación simétrica posterior puede producir invariancia. La propiedad no se aplica sin cambios a una máscara causal fija.''',
 13: r'''> **Self-attention sin información posicional y sin máscara de orden es equivariante a permutaciones.** Los vectores por token cambian de lugar con la entrada. Incorporar posiciones permite distinguir órdenes; una máscara causal también introduce estructura de orden.''',
 15: r'''### **11.2.1. ¿Por qué sumar $E_{tok}+PE$?**

La suma mantiene $d_{model}$ constante y permite usar las mismas dimensiones en las capas posteriores. Concatenar también es posible, pero cambia el ancho salvo que se añada una proyección. **La suma no es invertible en general y no garantiza separar perfectamente contenido y posición.** Los parámetros se aprenden con esa representación conjunta; no se presupone ortogonalidad entre ambos componentes.''',
 18: r'''### **11.3.1. Las ecuaciones sinusoidales**

$$PE_{pos,2i}=\sin(pos/10000^{2i/d}),\quad PE_{pos,2i+1}=\cos(pos/10000^{2i/d}).$$

$pos$ es el índice del token e $i$ el índice del par seno–coseno. La base 10000 controla el rango de frecuencias: $\lambda_i=2\pi\,10000^{2i/d}$, **no una longitud máxima exactamente igual a 10000**. Seno y coseno están intercalados por dimensiones en esta convención.''',
 20: r'''#### **11.3.1.1. Propiedad de desplazamiento lineal**

Cada par seno–coseno admite una transformación lineal para un desplazamiento fijo $k$:

$$\begin{bmatrix}\sin((pos+k)\omega_i)\\\cos((pos+k)\omega_i)\end{bmatrix}=\begin{bmatrix}\cos(k\omega_i)&\sin(k\omega_i)\\-\sin(k\omega_i)&\cos(k\omega_i)\end{bmatrix}\begin{bmatrix}\sin(pos\omega_i)\\\cos(pos\omega_i)\end{bmatrix}.$$

Esto facilita representar desplazamientos, pero **no obliga al producto punto de consultas y claves aprendidas a depender solo de la distancia relativa**. RoPE impone esa estructura de manera explícita en sus rotaciones.''',
 38: r'''**Lectura de las ondas:** cada pareja comparte frecuencia, con seno en la dimensión par y coseno en la impar. La pareja 0 tiene periodo $2\pi\approx6.28$ posiciones; entre posiciones 0 y 6 recorre casi un ciclo. El ejemplo manual anterior usa $d=6$; el laboratorio siguiente usa **$d=32$**, por lo que sus divisores son distintos.

Con $d=32$, las dimensiones 0–5 usan divisores **1, 1.7783 y 3.1623**, y periodos **6.28, 11.17 y 19.87**. Para $pos=4$, sus seis primeras componentes son aproximadamente **[-0.7568, -0.6536, 0.7783, -0.6276, 0.9536, 0.3011]**. La fila completa tiene 32 valores. Esto distingue posiciones; no garantiza por sí solo resolver toda ambigüedad sintáctica. Las sinusoidales no son odómetros globalmente monótonos.''',
 40: r'''##### **Celda 3: visión por filas**

Cada fila es un vector PE de **32 componentes**, una por dimensión del embedding del laboratorio. Los seis primeros valores pueden compararse con las ondas seleccionadas; no deben confundirse con todo el vector ni con el ejemplo manual de $d=6$.''',
 49: r'''* El tokenizador convierte texto en una secuencia de IDs; **$V$ es el tamaño del vocabulario, no la longitud de la secuencia**.
* GPT-2 emplea BPE a nivel de bytes con 50257 tokens. Las codificaciones de tiktoken dependen del modelo; `cl100k_base` incluye tokens especiales y no es un vocabulario de exactamente 100000 IDs. No debe atribuirse una única codificación a todas las versiones de GPT.''',
 })

REPLACEMENTS[ROPE].update({
 60: r'''##### **2. Qué muestra la suma posicional**

Sumar $x+p$ puede cambiar norma y dirección. Esto es una propiedad geométrica, **no una demostración de pérdida de identidad ni de colapso semántico**: el modelo se entrena con esa entrada. Un ángulo ilustrativo de 40° no demuestra deterioro general de los sinónimos.

RoPE rota pares de coordenadas de **Q y K** y conserva sus normas. La identidad $R_m^TR_n=R_{n-m}$ hace que la parte rotatoria del producto punto dependa del desplazamiento relativo. No garantiza por sí sola extrapolación ilimitada ni mejor rendimiento en cualquier tarea.''',
 64: r'''###### **Panel izquierdo: vectores sintéticos de referencia**

Los puntos del ejemplo son una construcción geométrica, no embeddings entrenados ni una medición de sinonimia. Sirven para comparar el efecto de sumar posiciones con una referencia fija.''',
 65: r'''###### **Panel derecho: efecto geométrico de sumar posiciones**

La suma desplaza cada punto de forma diferente y puede cambiar su norma. El dibujo es ilustrativo: **no prueba corrupción del lenguaje ni una pérdida de calidad de un Transformer entrenado**.''',
 66: '#### **13.1.2.2. Términos cruzados en la autoatención con posiciones aditivas**',
 82: r'''> Los términos cruzados mezclan contenido y posición absoluta. Pueden ser aprendidos y útiles; no son necesariamente «parásitos». RoPE adopta otra parametrización que hace explícita la dependencia relativa en el producto de Q y K rotadas.''',
})

COMMON = [
 ('Apuntan en direcciones opuestas (Antónimos).', 'Apuntan en direcciones opuestas; esto no demuestra antonimia.'),
 ('su nombre proviene del concepto matemático de transformación', 'fue presentada por Vaswani et al. (2017)'),
 ('la pura alineación direccional', 'la combinación de normas y alineación direccional'),
 ('pura alineación direccional', 'combinación de normas y alineación direccional'),
 ('complejidad cuadrática $O(N)$', 'coste lineal $O(N)$ por consulta; $O(N^2)$ para N consultas'),
 ('6.71\\text{ TB}', '6.71\\text{ TiB}'),
 ('6.71\\text{ Terabytes}', '6.71\\text{ TiB}'),
 ('arctan\\left(\\frac{\\text{Im}\\{X[k]\\}}{\\text{Re}\\{X[k]\\}}\\right)', 'operatorname{atan2}(\\text{Im}\\{X[k]\\},\\text{Re}\\{X[k]\\})'),
 ('amortigua los extremos gradualmente hacia cero, evitando discontinuidades artificiales', 'atenúa los extremos y reduce lóbulos laterales; Hann llega a cero en su versión simétrica, mientras Hamming conserva un pedestal cercano a 0.08. El ventaneo reduce la fuga, no la elimina'),
 ('incapaz de generar texto fluido de manera natural', 'no diseñado para generación autoregresiva token a token'),
 ('eliminando cualquier ambigüedad sintáctica', 'aportando una señal que permite distinguir posiciones'),
 ('guarantee', 'guarantee'),
]

def correct(stem, index, text, cell_type):
    original = text
    if cell_type == 'markdown':
        text = REPLACEMENTS.get(stem, {}).get(index, text)
        for old,new in COMMON:
            text = text.replace(old,new)
        text = re.sub(r'(?m)^(#{1,6})(?!#)(?=\S)', r'\1 ', text)
        if 'la mitad izquierda son generados' in text:
            text = '*Este gráfico usa una visualización que agrupa senos y cosenos por separado. La formulación intercalada asigna seno a dimensiones pares y coseno a impares; ambas disposiciones se relacionan por una permutación fija de columnas.*'
        if 'se entrenarán a dos redes neuronales' in text:
            text = r'''En self-attention se aprenden tres proyecciones: $Q=XW_Q$, $K=XW_K$ y $V=XW_V$. No son necesariamente tres redes independientes: son transformaciones entrenadas conjuntamente.

$$A=\operatorname{softmax}_{\rm fila}(QK^\top/\sqrt{d_k}),\qquad Z=AV.$$

La puntuación $q_i^\top k_j$ depende de normas y direcciones. Tras softmax, cada fila contiene pesos no negativos que suman uno. La salida $z_i=\sum_j A_{ij}v_j$ combina valores de posiciones permitidas por la máscara. **V no es por sí solo la traducción ni la predicción final.**'''
        if 'Vector clave' in text and 'cuatro patas' in text:
            text = '> **Analogía Q/K/V:** Q expresa qué busca una posición; K permite comparar posiciones; V aporta el contenido que se mezcla. Son vectores aprendidos: no hay una coordenada obligatoria para «cuatro patas» ni una traducción ya contenida en V.'
        if 'cuya similitud coseno natural es mayor' in text:
            text = 'Los pesos de esta ejecución son un resultado concreto del modelo y sus parámetros. Que una posición reciba más atención no demuestra una preferencia universal por tokens cercanos: depende de las representaciones, la función de puntuación y el entrenamiento. El producto punto no es un coseno normalizado salvo que se normalicen los vectores.'
        if stem=='1 - CNN - Teoría Completa':
            text=text.replace('Invariancia de Traducción','Equivariancia a la traslación').replace('La **invariancia de traducción** implica','La **equivariancia a la traslación** implica').replace('características ahora son invariantes a la traducción','características son equivariantes a traslaciones compatibles con la discretización, salvo efectos de borde')
    elif stem in (PE,ROPE):
        text=text.replace('El Vector de 6 Dimensiones que Recibe Cada Palabra','El vector de 32 dimensiones de cada token').replace('Columnas 0 a 5','Columnas 0 a 31')
        if 'VISUALIZADOR GEOMÉTRICO AVANZADO' in text:
            text=text.replace('CORRUPCIÓN APE','EFECTO GEOMÉTRICO DE APE').replace('CORRUPTO','DESPLAZADO').replace('Corrupción','Efecto geométrico').replace('Corrupcion','Efecto geométrico')
    # Rutas de ejecución portables; nunca publica nombres de instituciones.
    text=re.sub(r'([rR]?[\"\'])/content/(?:drive/)?MyDrive/[^\n\"\']*([\"\'])', r'\1./datos\2', text)
    text=text.replace('UPATECO','institución')
    return text, text!=original
