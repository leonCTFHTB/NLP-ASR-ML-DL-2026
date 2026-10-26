"""Esquemas vectoriales precisos; conservan las imágenes originales en assets."""
from pathlib import Path
from html import escape
import json,textwrap
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
# Dos tarjetas amplias mantienen el texto legible en escritorio y ampliación.
PANELS={
'word2vec-score':('Softmax: puntuación, exponencial y normalización',[
 ('1 · Puntuar y exponenciar',['sᵢ = uᵢᵀv_c','sᵢ combina norma y dirección.','El numerador es exp(sₒ), siempre positivo.','Aumentar el ángulo no es la única manera','de cambiar un producto punto.']),
 ('2 · Comparar con los candidatos',['Z_c = Σᵢ exp(sᵢ)','p(o | c) = exp(sₒ) / Z_c','Las probabilidades suman 1.','El gradiente ajusta puntuaciones;','no es una fuerza de distancia euclídea.'])], 'Mikolov et al. (2013) · El objetivo con negative sampling es distinto del softmax completo.'),
'position-limits':('RoPE: lo que conserva y lo que no garantiza',[
 ('Identidad geométrica',['q̃ₘ = Rₘqₘ; k̃ₙ = Rₙkₙ','Rₘ es una rotación ortogonal por parejas.','‖Rₘqₘ‖ = ‖qₘ‖','q̃ₘᵀk̃ₙ = qₘᵀRₙ₋ₘkₙ']),
 ('Interpretación y límites',['La rotación depende de la posición.','La norma no equivale al significado.','Q y K pueden contener contexto previo.','No garantiza decaimiento monótono,','ni extrapolación ilimitada de contexto.'])], 'Su et al., RoFormer · No se atribuyen detalles no publicados a modelos comerciales.'),
'linear-map':('Una matriz aprendida es una transformación lineal',[
 ('Sin sesgo: y = Wx',['Puede cambiar dimensión, normas y ángulos.','Conserva el origen: W0 = 0.','No añade una traslación.','No es necesariamente una rotación','ni una proyección ortogonal.']),
 ('Con sesgo: y = Wx + b',['El sesgo añade una traslación.','La transformación es afín.','En atención se aprenden matrices','para construir consultas, claves y valores.','Sus propiedades dependen de los pesos.'])], 'El término «proyección» se usa de forma amplia en redes neuronales; no impone ortogonalidad.'),
'hard-attention':('Atención discreta: selección y aprendizaje',[
 ('Elegir una posición',['a = softmax(scores)','j se muestrea de una distribución categórica.','El contexto toma el valor vⱼ.','La elección discreta no permite','la derivada ordinaria del índice.']),
 ('Optimizar el objetivo esperado',['Los parámetros de la distribución','pueden entrenarse con estimadores','como REINFORCE o con relajaciones.','Una muestra no implica por sí sola','un ahorro en todo el cálculo de scores.'])], 'Xu et al. (2015) · No debe confundirse falta de derivada del muestreo con imposibilidad de aprender.'),
'rnn-memory':('RNN y LSTM: activaciones, memoria y gradientes',[
 ('RNN con tanh',['hₜ = tanh(Wₕhₜ₋₁ + Wₓxₜ + b)','La salida de tanh está acotada.','El gradiente atraviesa productos','de matrices y derivadas: puede','desvanecerse o explotar.']),
 ('LSTM con compuertas',['cₜ = fₜ ⊙ cₜ₋₁ + iₜ ⊙ gₜ','hₜ = oₜ ⊙ tanh(cₜ)','La ruta aditiva facilita la retención.','Las compuertas controlan qué pasa.','No garantiza memoria ilimitada.'])], 'La cota de una activación no es una cota del gradiente de toda la red.'),
'fft-exact':('FFT Radix-2: reutilización sin perder información',[
 ('Mariposa para N = 2ˢ',['T = W_Nᵏ O[k]','X[k] = E[k] + T','X[k + N/2] = E[k] − T','Se reutiliza una multiplicación compleja.']),
 ('Coste e implementación',['log₂ N etapas, con trabajo O(N) por etapa.','Coste total O(N log N), no exponencial.','Puede implementarse in-place.','La memoria auxiliar depende del código.','No toda FFT requiere invertir bits explícitamente.'])], 'SciPy: FFT · La DFT compleja completa admite una transformada inversa.'),
'subword-limits':('fastText: composición de subpalabras y sus límites',[
 ('Construir el vector',['Una palabra aporta n-gramas de caracteres.','Sus vectores se combinan.','Fragmentos compartidos reutilizan parámetros.','Esto permite representar palabras nuevas','sin una entrada propia de palabra completa.']),
 ('Interpretar el resultado',['Los fragmentos no son necesariamente morfemas.','La composición no garantiza significado correcto.','Importan el corpus, los fragmentos y el modelo.','El laboratorio filtra subpalabras conocidas.','fastText original usa hashing en buckets.'])], 'Bojanowski et al. (2017) · Un ejemplo OOV no demuestra inmunidad a errores o generalización perfecta.'),
'bpe-limits':('BPE: compresión de secuencias y tokenización',[
 ('Aprender fusiones',['Se parte de unidades pequeñas.','Se cuentan pares adyacentes.','Se fusionan pares frecuentes.','Se repite según el vocabulario objetivo.']),
 ('Qué no se presupone',['Las unidades no tienen que ser morfemas.','Una palabra puede ser uno o varios tokens.','La tokenización depende del vocabulario.','No aprende una segmentación lingüística','óptima para todas las tareas e idiomas.'])], 'Sennrich et al. (2016), Neural Machine Translation of Rare Words with Subword Units.'),
'attention-experiment':('Mapas de atención: observar un experimento',[
 ('Una ejecución didáctica',['El mapa depende de los parámetros','aprendidos, las entradas y el entrenamiento.','La nitidez muestra concentración de pesos.','No demuestra por sí sola mejor comprensión.']),
 ('Comparar mecanismos',['Dot, general y aditiva no tienen','una jerarquía universal de concentración.','Un mapa uniforme también puede ser útil.','Se necesitan evaluación y varias ejecuciones','para comparar rendimiento y generalización.'])], 'Los mapas y pérdidas guardados son ejemplos; no son garantías inherentes a una arquitectura.'),
'local-window':('Atención local: centro, vecindad y gaussiana',[
 ('Centro aprendido',['pₜ = S · sigmoid(vₚᵀ tanh(Wₚhₜ))','Se evalúan posiciones alrededor de pₜ.','g(i) = exp(−(i − pₜ)² / (2σ²))','La gaussiana es suave respecto de pₜ.']),
 ('Detalles que deben declararse',['Recortar índices es una operación discreta.','El producto align(i) · g(i) puede no sumar 1.','Renormalizar es una decisión adicional.','Puntuar toda la secuencia antes de atenuarla','no obtiene el ahorro de una ventana real.'])], 'Luong et al. (2015), atención local predictiva · La selección y la ponderación son operaciones distintas.'),
'weighted-sum':('Atención: mezcla ponderada de contenido',[
 ('Puntuar y normalizar',['Aᵢⱼ = softmaxⱼ(score(qᵢ, kⱼ))','Cada fila suma 1 sin dropout posterior.','Los scores no son distancias euclídeas','ni cosenos en todos los mecanismos.']),
 ('Combinar valores',['zᵢ = Σⱼ Aᵢⱼ vⱼ','Cada peso multiplica un vector completo.','La contribución depende también de su norma.','Un peso alto no determina en exclusiva','la dirección de la mezcla final.'])], 'Vaswani et al. (2017) · Las etiquetas lingüísticas de los pesos son interpretaciones, no supervisión garantizada.'),
'additive-attention':('Atención aditiva: compatibilidad aprendida',[
 ('Calcular una puntuación',['rᵢⱼ = tanh(W_q qᵢ + W_k kⱼ + b)','eᵢⱼ = vᵀ rᵢⱼ','Las entradas pueden tener distinto ancho.','Los parámetros se entrenan con el modelo.']),
 ('Normalizar y mezclar',['Aᵢⱼ = softmaxⱼ(eᵢⱼ)','zᵢ = Σⱼ Aᵢⱼ vⱼ','No se mide directamente un ángulo','ni una distancia entre los tokens.','Afinidad significa aquí puntuación aprendida.'])], 'Bahdanau, Cho y Bengio (2015) · La analogía geométrica no sustituye esta ecuación.'),
'relu-exact':('ReLU: una no linealidad elemento a elemento',[
 ('Operación',['ReLU(x) = max(0, x)','Valores negativos pasan a 0.','Valores positivos se conservan.','No rota los vectores como una matriz.']),
 ('En una red aprendida',['La derivada es 0 en la rama negativa','y 1 en la positiva, fuera del origen.','El significado depende del entrenamiento.','No crea por sí sola valles de contradicción','ni una medida universal de equivalencia.'])], 'Una visualización de un paisaje semántico es una metáfora; no describe la operación literal de ReLU.'),
'fourier-time':('DFT global y análisis por ventanas',[
 ('DFT compleja completa',['X[k] conserva magnitud y fase.','La transformada inversa recupera las muestras.','La DFT no destruye el orden temporal.','Mostrar solo |X[k]| descarta la fase.']),
 ('STFT y espectrograma',['La STFT analiza fragmentos ventaneados.','Permite localizar componentes en el tiempo.','El espectrograma suele mostrar |STFT|².','Tamaño de ventana y salto determinan','el muestreo y el compromiso de resolución.'])], 'SciPy: transformadas discretas de Fourier · Distinguir la transformada de su visualización de magnitud.'),
'logmel-pipeline':('Log-Mel: orden del procesamiento',[
 ('1 · Obtener potencia por trama',['Audio → ventaneo → STFT compleja','Magnitud: A = |X|','Potencia: P = A²','Las muestras y las frecuencias tienen','convenciones de escala explícitas.']),
 ('2 · Agrupar y comprimir',['Banco Mel: M = H · P','Aplicar un piso positivo a M.','Después: log(M) o conversión a dB.','Filtrar después de tomar logaritmos','produce en general otro resultado.'])], 'El número de bandas, la referencia y la normalización dependen del pipeline; no todos usan 80 bandas.'),
'intra-history':('Intra-atención: distinguir arquitecturas',[
 ('Cheng et al. (2016): LSTMN',['Procesa la secuencia incrementalmente.','Usa memoria y atención durante recurrencia.','Consulta estados anteriores almacenados.','Conserva dependencias recurrentes.']),
 ('Transformer: self-attention',['Q, K y V provienen de la misma secuencia.','Puede calcular posiciones en paralelo','durante entrenamiento, con la máscara adecuada.','La inferencia autorregresiva aún genera','tokens con dependencia de los anteriores.'])], 'Cheng, Dong y Lapata (2016); Vaswani et al. (2017) · Intra-atención no es sinónimo de paralelismo completo.'),
}

PANELS.update({
'softmax-numeric':('Softmax: un ejemplo numérico verificable',[
 ('Puntuaciones y exponenciales',['scores = [3.2, −1.5, 4.0]','Restar el máximo conserva el softmax.','scores − 4 = [−0.8, −5.5, 0]','exp(scores − 4) ≈ [0.4493, 0.00409, 1]']),
 ('Normalización',['La suma es aproximadamente 1.4534.','Probabilidades ≈ [0.3092, 0.0028, 0.6880]','La suma es 1, salvo redondeo.','No son [0.15, 0.05, 0.80].'])], 'El eje del softmax determina qué conjunto de puntuaciones se normaliza.'),
'source-filter':('Modelo fuente–filtro: una aproximación del habla',[
 ('Fuente de excitación',['La vibración de las cuerdas vocales','participa en sonidos sonoros.','La turbulencia aporta excitación ruidosa.','La excitación y su evolución también','pueden aportar información lingüística.']),
 ('Filtro y representación',['El tracto vocal modifica el espectro.','Las resonancias ayudan a describir vocales.','No toda la información fonética está','exclusivamente en los formantes.','Los modelos pueden usar espectros o audio.'])], 'Es un modelo simplificado: el objetivo de ASR no es aislar siempre y únicamente el filtro.'),
'mel-scale':('Mel: una escala perceptual aproximada',[
 ('Frecuencias y bandas',['En la convención HTK:','mel(f) = 2595 log₁₀(1 + f / 700)','Es una transformación de coordenadas.','Hay otras convenciones, como Slaney.']),
 ('Interpretación',['El banco agrupa potencia con filtros.','Las bandas no modelan exactamente el oído.','No establece un umbral universal','para distinguir dos frecuencias.','La percepción depende del sonido y la tarea.'])], 'La escala Mel no convierte por sí sola una amplitud espectral en sonoridad percibida.')
})

def panel(title,cards,foot):
    """Genera dos tarjetas con ajuste de línea y altura calculada."""
    wrapped=[(head,[part for line in lines for part in textwrap.wrap(line,49)]) for head,lines in cards]
    rows=max(len(lines) for _,lines in wrapped);height=250+rows*37
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(" ".join(head+": "+" ".join(lines) for head,lines in cards))}</desc><rect width="1440" height="{height}" rx="14" fill="#191d26"/><style>text{{font-family:system-ui,sans-serif;fill:#e5e7eb}}.title{{font-size:29px;font-weight:700}}.head{{font-size:24px;fill:#d9c58f;font-weight:650}}.line{{font-size:22px}}.foot{{font-size:17px;fill:#a8b0c1}}</style><text x="38" y="55" class="title">{escape(title)}</text>']
    for i,(head,lines) in enumerate(wrapped):
        x=38+i*694
        out.append(f'<rect x="{x}" y="88" width="670" height="{height-180}" rx="9" fill="#222733" stroke="#3b4354"/><text x="{x+22}" y="129" class="head">{escape(head)}</text>')
        for j,line in enumerate(lines):out.append(f'<text x="{x+22}" y="{174+j*37}" class="line">{escape(line)}</text>')
    for j,line in enumerate(textwrap.wrap(foot,143)):out.append(f'<text x="38" y="{height-42+j*23}" class="foot">{escape(line)}</text>')
    return ''.join(out)+'</svg>'

def apply_figures():
    """Sustituye referencias a diagramas ambiguos sin alterar los originales."""
    out=ROOT/'docs/assets/figures';out.mkdir(exist_ok=True)
    for key,args in PANELS.items():(out/(key+'.svg')).write_text(panel(*args))
    patches=json.loads((ROOT/'reports/figure-patches.json').read_text())
    mapping={Path(x['original']).name:x for x in patches};history=[]
    for path in (ROOT/'docs/nlp').glob('*.html'):
        soup=BeautifulSoup(path.read_text(),'html.parser');changed=False
        for im in soup.find_all('img'):
            patch=mapping.get(Path(im.get('src','')).name)
            if not patch:continue
            old=im['src'];key=Path(patch['replacement']).stem
            im['data-original-src']=old;im['src']='../assets/figures/'+key+'.svg'
            im['alt']=PANELS[key][0] if key in PANELS else 'Suma posicional: cambios geométricos sin garantía de pérdida semántica'
            note=soup.new_tag('p',attrs={'class':'note figure-revision'});note.append('Esquema corregido: '+im['alt']+'. ')
            a=soup.new_tag('a',href=old);a.string='Ver ilustración recibida';note.append(a);im.insert_after(note)
            history.append({'page':str(path.relative_to(ROOT)),'original':old,'replacement':im['src'],'reason':patch['reason']});changed=True
        if changed:path.write_text(str(soup))
    # Reconstruir el registro completo también en ejecuciones incrementales.
    history=[]
    for path in (ROOT/'docs/nlp').glob('*.html'):
        soup=BeautifulSoup(path.read_text(),'html.parser')
        for im in soup.select('img[data-original-src]'):
            patch=mapping.get(Path(im['data-original-src']).name)
            if patch:
                history.append({'page':str(path.relative_to(ROOT)),'original':im['data-original-src'],'replacement':im['src'],'reason':patch['reason']})
    report=ROOT/'reports/auditoria-figuras.json'
    report.write_text(json.dumps(history,ensure_ascii=False,indent=2))
    print('Figuras de sustitución:',len(PANELS),'referencias corregidas:',len(history))
if __name__=='__main__':apply_figures()
