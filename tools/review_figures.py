"""Figuras docentes vigentes: SVG deterministas con fórmulas y supuestos explícitos."""
from pathlib import Path
import json
from bs4 import BeautifulSoup
from editorial_figures import PANELS, panel
ROOT=Path(__file__).resolve().parents[1]
PANELS.update({
 'cbow':('Word2Vec: dirección de la predicción',[
  ('Skip-gram',['Entrada: un token central c.','Se puntúa cada token de contexto o.','p(o | c) = softmaxₒ(uₒᵀv_c)','Se generan pares centro–contexto.','La ventana excluye el propio centro.']),
  ('CBOW',['Entrada: C contextos válidos.','Promedio: v̄ = (Σᵣ vₒᵣ) / C','p(c | contextos) = softmax_c(u_cᵀv̄)','C cuenta los contextos disponibles.','Las dos tablas se aprenden con el objetivo.'])], 'Mikolov et al. (2013) · Los ejemplos de analogías no son identidades semánticas garantizadas.'),
 'glove':('GloVe: coocurrencias y ajuste logarítmico',[
  ('Estadísticas del corpus',['Xᵢⱼ cuenta contexto j alrededor de i.','Puede incluir ponderación por distancia.','Xᵢ = Σⱼ Xᵢⱼ; P(j | i) = Xᵢⱼ / Xᵢ','La ventana y el corpus deben declararse.']),
  ('Objetivo sobre Xᵢⱼ > 0',['J = Σ f(Xᵢⱼ) (wᵢᵀw̃ⱼ + bᵢ + b̃ⱼ − log Xᵢⱼ)²','Se ajustan vectores y sesgos aprendidos.','El producto depende de norma y dirección.','Los sesgos no aíslan una semántica pura.'])], 'Pennington et al. (2014) · No se evalúa log(0); se suman pares observados.'),
 'onehot':('Del índice de token al embedding aprendido',[
  ('Indicador one-hot',['Vocabulario de N tokens: 0 ≤ i < N.','eᵢ tiene un 1 en i y ceros en el resto.','eᵢᵀeⱼ = 0 si i ≠ j.','La similitud directa no distingue relaciones.']),
  ('Tabla de embeddings',['E tiene N filas y d columnas.','Consultar E[i] equivale a Eᵀeᵢ.','La transformación aprende con los datos.','No hace falta construir el one-hot completo.'])], 'La ortogonalidad del indicador no impide que una transformación posterior aprenda relaciones.'),
 'decomposable':('Atención descomponible: Attend → Compare → Aggregate',[
  ('Attend: alinear dos secuencias',['eᵢⱼ = F(aᵢ)ᵀ F(bⱼ)','βᵢ = Σⱼ softmaxⱼ(eᵢⱼ) bⱼ','αⱼ = Σᵢ softmaxᵢ(eᵢⱼ) aᵢ','Las dos direcciones normalizan ejes distintos.']),
  ('Compare y Aggregate',['vᵢ = G([aᵢ; βᵢ]); uⱼ = G([bⱼ; αⱼ])','v = Σᵢ vᵢ; u = Σⱼ uⱼ','El clasificador recibe [v; u].','G aprende características de comparación.','No contiene reglas lógicas fijas por diseño.'])], 'Parikh et al. (2016) · Los pesos ilustrativos no son mediciones de un modelo entrenado.'),
 'decode':('Del estado del decoder al siguiente token',[
  ('Distribución sobre vocabulario',['El estado se proyecta con una capa lineal.','logits = Wh + b','p = softmax(logits)','log p = log_softmax(logits)']),
  ('Regla de generación',['Greedy: escoger el máximo de p.','Muestreo: extraer un token según p.','Beam search: mantener varias hipótesis.','La generación continúa con los tokens elegidos.','La regla depende de la tarea y configuración.'])], 'Vaswani et al. (2017) · Softmax y log-softmax son operaciones distintas.'),
 'cnn-shapes':('CNN: canales, espacio y clasificación',[
  ('Conv2d con formato NCHW',['Entrada: (batch, C_in, H, W)','Pesos: (C_out, C_in / grupos, K_h, K_w)','Un filtro produce un canal de salida.','Los pesos se comparten entre posiciones.']),
  ('Salida y clasificación',['H_out = ⌊(H + 2p − d(K−1) − 1)/s⌋ + 1','La misma fórmula se aplica al ancho.','Flatten reorganiza los elementos.','Una capa lineal aprende otra transformación.','CrossEntropyLoss recibe logits, sin softmax.'])], 'PyTorch Conv2d · Los canales no tienen un significado RGB obligatorio después de la entrada.'),
 'pe-add':('Codificación posicional aditiva',[
  ('Representación de entrada',['zₚ = e_token + PE(p)','Ambos vectores tienen el mismo ancho.','PE puede ser aprendido o sinusoidal.','La suma aporta posición a la representación.']),
  ('Propiedades geométricas',['La suma puede cambiar norma y ángulo.','Ese cambio no demuestra pérdida de significado.','Las proyecciones se aprenden conjuntamente.','La capacidad de extrapolar debe evaluarse.'])], 'Vaswani et al. (2017) · Posición y contenido se combinan según el diseño de la arquitectura.'),
 'loss-gradient':('Word2Vec: pérdida y dirección del gradiente',[
  ('Objetivo de un par centro–contexto',['sⱼ = uⱼᵀv_c; pⱼ = softmaxⱼ(s)','log pₒ = sₒ − log Σⱼ exp(sⱼ)','L = −log pₒ','Minimizar L equivale a maximizar log pₒ.']),
  ('Descenso de gradiente',['∇ᵥ L = Σⱼ pⱼuⱼ − uₒ','v_c ← v_c − η∇ᵥ L','Se resta el gradiente de la pérdida.','No es una fuerza euclídea entre palabras.'])], 'La suma recorre todo el vocabulario para el objetivo softmax completo; negative sampling usa otro objetivo.'),
 'sampling':('Hard attention: una muestra categórica',[
  ('Forward discreto',['a = softmax(scores)','j ∼ Categorical(a)','s = one_hot(j)','c = Σᵢ sᵢvᵢ = vⱼ']),
  ('Entrenamiento',['El índice elegido no tiene derivada ordinaria.','REINFORCE estima el gradiente esperado.','Gumbel-softmax ofrece una relajación.','El estimador straight-through es sesgado.','Calcular todos los scores conserva ese coste.'])], 'Xu et al. (2015); Jang et al. (2017) · La categórica equivale a una multinomial con una sola muestra.'),
})
# Una figura numérica presenta únicamente sus valores vigentes.
PANELS['softmax-numeric'][1][1][1][-1]='El eje indica qué candidatos se comparan.'
REPLACEMENTS = {'07247ed3242b0361c853490c.webp': 'intra-history', '1c509a3b983ae0e05c058c27.webp': 'intra-history', 'c8960e5a81879974f2334064.webp': 'intra-history', '0c21594765b1fbb90cefe76f.webp': 'softmax-numeric', '18111cf64933f17f28938331.webp': 'softmax-numeric', '0c422e2c0c6ed5589f8c8b42.webp': 'rnn-memory', '1f18191d03b98ae967e2e524.webp': 'rnn-memory', '23e8fce21badf256cdc9d217.webp': 'rnn-memory', '6b1c20ab7450d9b4fa05c53d.webp': 'rnn-memory', '71f073c0b2b89172035a4c58.webp': 'rnn-memory', '74ad629bad4932d826f3e5c7.webp': 'rnn-memory', '7618f40f678606acd3398ff1.webp': 'rnn-memory', 'a0c2edfa965cbe2a57f9e2e4.webp': 'rnn-memory', 'aadd8ae62d2dbac19e53096e.webp': 'rnn-memory', '0c8673c4e0a7ee0e0022202e.webp': 'fourier-time', '2d8950d339520c5abdf0f311.webp': 'fourier-time', '734cc0efda07a560eb148a56.webp': 'fourier-time', 'a258275f7bf8b51bb5c6c802.webp': 'fourier-time', 'c42c72ee4902405c6cc512fe.webp': 'fourier-time', '14db6ee287a52bc03c2ab442.webp': 'additive-attention', '44f672545a89b40055df9cbf.webp': 'additive-attention', '7c2792e5d877a758d3901b62.webp': 'additive-attention', 'c01ace6a44a31ca44af7762f.webp': 'additive-attention', '1603cbf2d704ef451b724100.webp': 'decomposable', '1d3951cf60b874147a2f2def.webp': 'decomposable', '29bc9db77ea6f0b47cba236c.webp': 'decomposable', '66c6ffef351c4f75ffc061cd.webp': 'decomposable', '85828eafa81dde42d411a96a.webp': 'decomposable', 'a9b5b517a11fd01246fe1585.webp': 'decomposable', 'ba398306dcffad8b6b8e6ec6.webp': 'decomposable', 'e4527cb769459a5ee86f0fcb.webp': 'decomposable', 'e6812540457f42b68a7982b6.webp': 'decomposable', '180d66451c8358dd50260502.webp': 'cbow', '295ffb68b4e17ea2531f72dd.webp': 'cbow', '5faf656b8b094a7dd809b114.webp': 'cbow', '7366ff95b2b52bc8a3c15ad0.webp': 'cbow', '9a92453bdfb05cf887c1c84c.webp': 'cbow', 'a91ee53320495adfe4b5ee0e.webp': 'cbow', 'ebaa0c1078986393141441e2.webp': 'cbow', 'ef2fa668c71153ffd5297f2b.webp': 'cbow', 'f0a87bec0c33f9e3a5d5aa84.webp': 'cbow', '260cc9497f793d9d5cb9769b.webp': 'glove', '91f3d8f7aac860afa5dab364.webp': 'glove', 'a0af9b937bf7e45bd3807f76.webp': 'glove', 'a9f839596cc605e2c5fd42bc.webp': 'glove', '37e7533f6ee922011d15c6a0.webp': 'position-limits', '3bbc9cff9951ffe1960014c4.webp': 'position-limits', '6444fc7a9cf408561187cc5f.webp': 'position-limits', '6d00ceaac0777470edf17373.webp': 'position-limits', '7b1cd5577af2dbdc8d917154.webp': 'position-limits', '843e2165c89e2df74beef9b6.webp': 'position-limits', '8e81a28cb60325c469be510f.webp': 'position-limits', 'dd774047f6340e6d3d03e20f.webp': 'position-limits', 'ed48e2bd21fce8c4b626ecab.webp': 'position-limits', '390be00f666ee240fd268b1e.webp': 'weighted-sum', 'eab777af45ef281617840987.webp': 'weighted-sum', 'f68f7ae5ac53b98d1a569ff8.webp': 'weighted-sum', 'fc52ba129756405035d102b7.webp': 'weighted-sum', 'ff1755f920a74cb0d8c75b1c.webp': 'weighted-sum', '43e746f7abe265c76ab97a97.webp': 'subword-limits', '94d52c6d38a2901148812569.webp': 'subword-limits', 'cfa21438533a6325623f1c06.webp': 'subword-limits', '45eb68f56b429a8144246cbd.webp': 'local-window', '6a2366211a43d569fe5ad952.webp': 'local-window', 'c99eb7f200532ba182b33eff.webp': 'local-window', 'd6a350cc4935d26a99bc5312.webp': 'local-window', 'e2c97b78bb875e153ab8ce28.webp': 'local-window', '4757bc6c4c099b2324dd1bfd.webp': 'fft-exact', '53547682c5b6dcdc71b72882.webp': 'fft-exact', 'b31572804bb529479f2c1d5d.webp': 'fft-exact', 'b9d627751dd9d59d3ca7be80.webp': 'fft-exact', 'f26a1a8f4f12f46a4b511c03.webp': 'fft-exact', '4f91963e429b34afcf00cd4b.webp': 'onehot', '53f02e320bc8043da2571f21.webp': 'onehot', '6415a2bc47321dc05fb247e0.webp': 'onehot', '4fbb97591794f76b5194b3f3.webp': 'logmel-pipeline', '8c31a9fa5b0ad22384bc4710.webp': 'logmel-pipeline', 'd6ad24caf24bc30be2321d7a.webp': 'logmel-pipeline', 'd6ffd7f4c1a51d4bf6f9a8e3.webp': 'logmel-pipeline', 'ebc0148c95b152f6307406b0.webp': 'logmel-pipeline', 'edf2fdc50fdf838ca27a98a6.webp': 'logmel-pipeline', 'a24d88c5ac8a28b763304d0e.webp': 'decode', '9ecafca36b05249b2abf2cd1.webp': 'loss-gradient', 'b0d045bcaf59433a396cf69a.webp': 'loss-gradient', 'bb80ddcf7ba778bcf13a715c.webp': 'loss-gradient', 'd30856de6616d5b8a13e0fdb.webp': 'loss-gradient', 'b8a3dd5a8b8d6ad1db687ca3.webp': 'pe-add', '73f0c449de98411ee97ca68a.webp': 'sampling', '9dc0dcf70e769c0853f7ca2f.webp': 'sampling', '9642c040c2c0025330fded22.webp': 'cnn-shapes'}

REPLACEMENTS.update({'7a8dcd10ae10dc998a08a424.webp': 'attention-weights', '8f27075c85630b2a0d1b1103.webp': 'attention-weights', '94f4ea8ff5a1fd24149bbe75.webp': 'attention-weights', '95ffbfe331f3a4665d7b957f.webp': 'attention-weights', '9deaa0a3abd877c3201e1045.webp': 'attention-weights', '9fabc76ab198074e674782e5.webp': 'attention-weights', 'afe9c82fa6e0dc4fe7da8615.webp': 'attention-weights', 'c3d796306c6250f8201a6a4b.webp': 'attention-weights', 'e31c1fc247f97602d1850246.webp': 'attention-weights', 'e8ef5487cb2e7fa5b4b84082.webp': 'attention-weights', 'f14bb372fdfc17ab285b213b.webp': 'attention-weights', 'fef9da3c46986b9b3aa2025b.webp': 'attention-weights', '36d2f6c52d0c1bc5c8ac6d30.webp': 'time-frequency', 'c8534a01e3c233632aec82e6.webp': 'time-frequency', 'ebc0148c95b152f6307406b0.webp': 'mel-bank'})
SCIENTIFIC_TITLES={'attention-weights':'Ejemplo sintético de pesos de atención', 'time-frequency':'Resolución temporal y frecuencial de una señal sintética','mel-bank':'Banco Mel de doce filtros ilustrativos'}

def run():
 out=ROOT/'docs/assets/figures';out.mkdir(exist_ok=True)
 for key,args in PANELS.items():(out/(key+'.svg')).write_text(panel(*args))
 report=[]
 for p in sorted((ROOT/'docs/nlp').glob('*.html')):
  s=BeautifulSoup(p.read_text(),'html.parser')
  for im in s.find_all('img'):
   key=REPLACEMENTS.get(Path(im.get('src','')).name)
   if key:
    im['src']='../assets/figures/'+key+'.svg';im['alt']=SCIENTIFIC_TITLES[key] if key in SCIENTIFIC_TITLES else PANELS[key][0]
    im.attrs.pop('width',None);im.attrs.pop('height',None)
    report.append({'page':str(p.relative_to(ROOT)),'cell':im.find_parent('section').get('id'),'figure':key})
  p.write_text(str(s))
 (ROOT/'reports/figuras-vigentes.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 from scientific_figures import run as plots
 plots()
 print('Referencias visuales actualizadas:',len(report))
if __name__=='__main__':run()
