"""Diagramas vectoriales exactos que sustituyen ilustraciones ambiguas."""
from html import escape
from pathlib import Path
import math

def panel(title, cards, foot='Esquema didáctico · las coordenadas y ejemplos no son resultados entrenados.'):
    width=1440; height=220+max(len(lines) for _,lines in cards)*38
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img"><rect width="100%" height="100%" rx="18" fill="#111c30"/><style>text{{font-family:system-ui,sans-serif;fill:#e6e9f1}}.title{{font-size:30px;font-weight:700}}.head{{font-size:24px;fill:#d9c58f;font-weight:650}}.line{{font-size:21px}}.foot{{font-size:17px;fill:#a7b4c9}}</style><text x="45" y="60" class="title">{escape(title)}</text>']
    w=(width-90-(len(cards)-1)*24)/len(cards)
    for i,(head,lines) in enumerate(cards):
        x=45+i*(w+24)
        out.append(f'<rect x="{x}" y="94" width="{w}" height="{height-166}" rx="12" fill="#1a2942" stroke="#3d4c67"/><text class="head" x="{x+22}" y="135">{escape(head)}</text>')
        for j,line in enumerate(lines):out.append(f'<text class="line" x="{x+22}" y="{181+j*38}">{escape(line)}</text>')
    out.append(f'<text x="45" y="{height-25}" class="foot">{escape(foot)}</text></svg>')
    return ''.join(out)

FIGURES={
'cosine':panel('Similitud de coseno: geometría e interpretación',[
 ('cos θ = 1',['Vectores no nulos paralelos.','Misma dirección; pueden tener','longitudes diferentes.']),
 ('cos θ = 0',['Vectores ortogonales.','No prueba independencia','ni ausencia de relación.']),
 ('cos θ = −1',['Direcciones opuestas.','No demuestra antonimia:','el significado depende del modelo.'])], 'u·v = ‖u‖ ‖v‖ cos θ · producto punto y coseno no son equivalentes sin normalización.'),
'word2vec-glove':panel('Dos formas de usar las estadísticas de contexto',[
 ('Word2Vec',['Extrae pares de ventanas.','Predice centro o contexto.','Negative sampling evita','el softmax completo.']),
 ('GloVe',['Agrega conteos de ventanas.','Ajusta logaritmos de conteos.','Entrena pares con xᵢⱼ > 0.','No garantiza mayor velocidad.'])], 'Ambos aprenden del corpus completo; «global» no significa una ventana de todo el documento.'),
'ratios':panel('GloVe: dos centros y un contexto fijo',[
 ('Contexto k',['solid','gas','water','fashion']),
 ('P(k|ice) / P(k|steam)',['1.9e−4 / 2.2e−5 ≈ 8.64','6.6e−5 / 7.8e−4 ≈ 0.0846','3.0e−3 / 2.2e−3 ≈ 1.36','1.7e−5 / 1.8e−5 ≈ 0.944'])], 'Cifras redondeadas de Pennington et al. (2014), tabla 1. Los ratios publicados: 8.9, 0.085, 1.36 y 0.96.'),
'exp':panel('De una diferencia de puntuaciones a un cociente',[
 ('Identidad exacta',['exp(a − b) = exp(a) / exp(b)','a y b son escalares.','exp(a) es positivo;','no suma uno automáticamente.']),
 ('Motivación de GloVe',['Comparar dos centros i, j','frente al mismo contexto k.','(wᵢ − wⱼ) · w̃ₖ','modela una relación logarítmica.'])], 'El objetivo final también incorpora los sesgos de centro y contexto.'),
'weight':panel('Pares observados y ponderación en GloVe',[
 ('Dominio',['Usar solo pares x > 0.','No evaluar log(0).','0 × log(0) no es un atajo','numéricamente válido.']),
 ('Peso h(x)',['(x / xₘₐₓ)^α si 0 < x < xₘₐₓ','1 si x ≥ xₘₐₓ','Ejemplo: α = 0.75; xₘₐₓ = 100','El peso se satura, el error no.'])]),
'gradient':panel('El gradiente ajusta una puntuación; no atrae puntos',[
 ('Residual negativo',['eᵢⱼ = predicción − log xᵢⱼ < 0','Con uⱼ fijo, el paso en vᵢ','apunta en dirección +uⱼ.','Aumenta el producto punto.']),
 ('Residual positivo',['eᵢⱼ > 0','Con uⱼ fijo, el paso en vᵢ','apunta en dirección −uⱼ.','Disminuye el producto punto.'])], 'Descenso simple: Δvᵢ = −η 2 h(xᵢⱼ) eᵢⱼ uⱼ · AdaGrad reescala las coordenadas.'),
'symmetry':panel('Dos matrices de embeddings no implican igualdad',[
 ('Conteos',['Ventanas simétricas pueden','producir X = Xᵀ.','Una ventana direccional','no garantiza simetría.']),
 ('Parámetros',['Centros W y contextos W̃','se aprenden por separado.','No se exige W = W̃.','Extracción habitual: wᵢ + w̃ᵢ.'])]),
'dot':panel('Producto punto y atención',[
 ('Puntuación',['q · k = ‖q‖ ‖k‖ cos θ','Depende de normas y ángulo.','Se divide por √dₖ','en atención escalada.']),
 ('Pesos y contenido',['softmax por fila → pesos A','Cada fila suma uno.','zᵢ = Σⱼ Aᵢⱼ vⱼ','V aporta el contenido mezclado.'])]),
'qkv':panel('Self-attention: tres proyecciones aprendidas',[
 ('Comparar',['Q = X WQ','K = X WK','S = Q Kᵀ / √dₖ','Sᵢⱼ = qᵢ · kⱼ / √dₖ']),
 ('Mezclar',['V = X WV','A = softmax por fila(S)','Z = A V','Z conserva una fila por consulta.'])], 'Las proyecciones se entrenan conjuntamente. Los pesos de atención no son etiquetas lingüísticas garantizadas.'),
'equivariance':panel('Sin posiciones ni máscara de orden: equivariancia',[
 ('Entrada X',['Tokens: A, B, C','Salida: zA, zB, zC','Cada token combina valores','mediante atención.']),
 ('Entrada permutada P X',['Tokens: C, A, B','Salida: zC, zA, zB','Las filas cambian de lugar.','SA(P X) = P SA(X)'])], 'Invariancia sería conservar idéntica salida. Una máscara causal fija cambia los supuestos.'),
'sum':panel('Suma y concatenación de contenido y posición',[
 ('Suma',['e, p ∈ ℝᵈ','Entrada: e + p ∈ ℝᵈ','Mantiene el ancho del modelo.','No es invertible en general.']),
 ('Concatenación',['e ∈ ℝᵈ, p ∈ ℝᵏ','Entrada: [e;p] ∈ ℝᵈ⁺ᵏ','Aumenta el ancho; puede','seguirla una proyección.'])], 'Ninguna opción garantiza por sí sola separar la semántica o resolver la tarea.'),
'pe':panel('Posiciones sinusoidales: pares intercalados',[
 ('Dimensiones 2i y 2i+1',['ωᵢ = 10000^(−2i/d)','PE(pos, 2i) = sin(pos ωᵢ)','PE(pos, 2i+1) = cos(pos ωᵢ)','Misma frecuencia por pareja.']),
 ('Periodos',['λᵢ = 2π / ωᵢ','Con d = 6:','λ₀ ≈ 6.28; λ₁ ≈ 135.37','λ₂ ≈ 2916.40 posiciones.'])]),
'ape':panel('La suma posicional cambia la representación',[
 ('Entrada aprendida',['xₘ + pₘ combina contenido','y posición absoluta.','Puede cambiar norma y ángulo.','No demuestra daño semántico.']),
 ('Producto de atención',['qₘ = (xₘ + pₘ) WQ','kₙ = (xₙ + pₙ) WK','Aparecen términos cruzados.','Se entrenan junto con el modelo.'])], 'Una visualización de vectores sintéticos no demuestra pérdida de calidad en un Transformer entrenado.'),
'rope':panel('RoPE: posición como rotación de Q y K',[
 ('Por pareja',['Rₘ = [ cos(mθ)  −sin(mθ) ]','          [ sin(mθ)    cos(mθ) ]','q̃ₘ = Rₘ qₘ; k̃ₙ = Rₙ kₙ','Rotación: conserva la norma.']),
 ('Producto punto',['q̃ₘᵀ k̃ₙ = qₘᵀ Rₘᵀ Rₙ kₙ','Rₘᵀ Rₙ = Rₙ₋ₘ','La parte rotatoria depende','de la distancia relativa n − m.'])], 'No garantiza extrapolación ilimitada. En la formulación habitual se rotan Q y K, no los embeddings de V.'),
'base':panel('La base de RoPE controla las frecuencias',[
 ('Diseño',['θᵢ = base^(−2i/d)','Una base mayor reduce','algunas frecuencias angulares.','i = 0 mantiene θ₀ = 1.']),
 ('Alcance',['La elección depende del modelo','y de su entrenamiento.','Una base mayor por sí sola','no amplía el contexto validado.'])]),
'cross':panel('Self-attention y cross-attention',[
 ('Self-attention',['Q, K y V se proyectan','de la misma secuencia.','En un decoder causal,','se enmascara el futuro.']),
 ('Cross-attention',['Q: estados del decoder.','K y V: memoria del encoder.','Longitudes de consultas','y de memoria pueden diferir.'])]),
'dft':panel('DFT: magnitud, fase y frecuencia',[
 ('Coeficientes complejos',['X[k] = Σₙ x[n] exp(−j2πkn/N)','Magnitud: |X[k]|','Fase: atan2(Im X, Re X)','Potencia espectral: |X[k]|²']),
 ('Bins',['Δf = Fₛ / N: separación de bins','fₖ = k Fₛ/N hasta Nyquist.','Los bins altos representan','frecuencias negativas.'])], 'La resolución efectiva también depende de la duración de la ventana; añadir ceros no crea información.'),
'window':panel('Ventaneo: reducir fuga a cambio de ensanchar el pico',[
 ('Hann simétrica',['w[n] = 0.5 − 0.5 cos(2πn/(N−1))','Extremos iguales a cero.','Atenúa los lóbulos laterales.','La fuga no desaparece.']),
 ('Hamming simétrica',['w[n] = 0.54 − 0.46 cos(2πn/(N−1))','Extremos cercanos a 0.08.','Distinto compromiso espectral.','No llega a cero en los bordes.'])], 'Las variantes periódicas usadas en STFT difieren ligeramente de estas fórmulas simétricas.'),
'db':panel('Decibelios: declarar magnitud, potencia y referencia',[
 ('Magnitud A',['20 log₁₀(A / Aref)','Piso εA antes del logaritmo.','Una STFT sin normalizar','puede producir A > 1.']),
 ('Potencia P = A²',['10 log₁₀(P / Pref)','Equivalencia si Pref = Aref²','y εP = εA².','No son automáticamente dBFS.'])], 'Referencia espectral uno no equivale por sí sola a una calibración acústica o de escala completa.'),
'fft':panel('FFT Radix-2: dos mitades y una mariposa',[
 ('Separar',['N = 2ˢ muestras.','E[k]: DFT de índices pares.','O[k]: DFT de índices impares.','Wₙᵏ = exp(−j2πk/N)']),
 ('Combinar',['X[k] = E[k] + Wₙᵏ O[k]','X[k+N/2] = E[k] − Wₙᵏ O[k]','log₂ N etapas.','Coste O(N log N).'])], 'Una FFT es un algoritmo para la DFT, no una transformada distinta.'),
}

# (carpeta de recursos original, nombre) → figura exacta de reemplazo.
MAP={}
def bind(folder, names, key):
    for n in names.split(): MAP[(str(folder),n+'.png')]=key
bind(1,'a3 a4','cosine')
bind(2,'b3','word2vec-glove');bind(2,'b6 b7','ratios');bind(2,'b5.1 b6.1','exp')
bind(2,'b10 b14','weight');bind(2,'b11 b12 b13 b15','gradient');bind(2,'b16','symmetry')
bind(3,'c6 a2','dot')
bind(6,'a8 f1 f5 f6 f8','dot');bind(6,'a5 a7','qkv')
bind(11,'a1 a3','equivariance');bind(11,'a4','sum');bind(11,'a5 a6 a7','pe');bind(11,'a8','pe')
bind(12,'a1 a3','equivariance');bind(12,'a4','sum');bind(12,'a5 a6 a7 a8','pe')
bind(12,'b3 b4 b5 b8','ape');bind(12,'b6 b7','cross');bind(12,'b18','base')
bind(14,'a5 a6 a7 a8','dft');bind(14,'a9 a10','window')
bind(15,'a5 a6 a7 a8','dft');bind(15,'a9 a10 b13 b15 b16 b17 b18','window')
bind(15,'b23 b24','db');bind(16,'a1 a2 a3 b1 b5 b9','fft')

def write(directory):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    for name,svg in FIGURES.items(): (directory/(name+'.svg')).write_text(svg)
