# Revisión técnica y diseño

Edición del 26 de octubre de 2026 · Material docente de Jacobo León Juárez.

## Qué se revisó

Se inventariaron los 32 HTML recibidos, sus enlaces internos y recursos locales. La revisión conceptual se centró en definiciones, ecuaciones, supuestos y coherencia de ejemplos en embeddings, CNN, atención, posiciones y procesamiento del audio. Se inspeccionaron hojas de contacto de las 354 imágenes de mapa de bits, incluidos fotogramas representativos de GIF, y se sustituyeron diagramas con afirmaciones ambiguas o incorrectas. Las animaciones no se verificaron fotograma a fotograma.

La revisión es crítica y trazable; **no constituye una certificación de exactitud de cada afirmación, cifra o figura**. Los ejemplos ejecutables y las salidas históricas se conservan; no se volvieron a entrenar redes ni se reprodujeron las métricas. Las figuras de resultados experimentales no prueban superioridad universal de un modelo.

## Correcciones principales

| Tema | Criterio aplicado |
|---|---|
| Word2Vec | El softmax normaliza exponenciales de productos punto. Producto punto y coseno no son equivalentes sin normalización. |
| GloVe | Los sesgos no garantizan una geometría puramente direccional. |
| fastText | Las subpalabras permiten composición para OOV; no garantizan significado correcto ni segmentación morfológica exacta. |
| Reproducibilidad | Fijar semillas controla azar, pero no garantiza resultados idénticos entre dispositivos o versiones. |
| CNN | Distinguir equivarianza e invariancia; precisar qué parámetros reduce el pooling. |
| BatchNorm | Distinguir ejes, estadísticas de entrenamiento y evaluación, configuración y evidencia sobre optimización. |
| Atención | Separar self-attention, cross-attention y LSTMN; precisar complejidad, máscaras, mezcla de valores y ventana local. |
| Posiciones y RoPE | Conservar norma no equivale a conservar significado; los términos cruzados de posiciones aditivas pueden ser útiles. |
| Dimensiones | Diferenciar ancho del modelo y ancho por cabeza: 4096/32 = 128 en el ejemplo de Llama 3 8B. |
| FFT y ASR | La DFT compleja es invertible; la magnitud sola descarta fase. Separación de bins y resolución efectiva son distintas. |
| Detección | Precisar el orden de NMS y la comparación en el umbral del código heredado. |

Cada cambio textual nuevo se registra con página, celda, motivo, fuente y antes/después en `reports/auditoria-editorial.json`. Las sustituciones visuales nuevas están en `reports/auditoria-figuras.json`. El registro `reports/correcciones.json` ya venía en el material recibido y se conserva como antecedente, sin atribuir sus cambios a esta revisión.

## Criterios de diseño

Fondo grafito `#111318`, paneles `#191D26`, texto `#E5E7EB`, lavanda `#B8A5EE`, azul contextual `#91B9E3` y ámbar de énfasis `#D9C58F`. Se usa una pila de tipografías de sistema; el código utiliza tipografía monoespaciada. Los seis niveles de título se distinguen por tamaño, peso y espaciado, además del color.

Se eliminaron los colores inline de las etiquetas `font` en favor de tres roles CSS compartidos. Los diagramas vectoriales propios usan la misma paleta. Las ilustraciones ajenas y las gráficas de datos conservan sus píxeles y escalas originales dentro del marco visual común: invertir o recolorear una escala científica puede alterar su interpretación. Las imágenes recibidas sustituidas siguen disponibles mediante un enlace junto al nuevo esquema.

El diseño incluye navegación lateral, estado de página actual, búsqueda local, código desplegable, copia de código, foco de teclado y una variante de impresión clara. La búsqueda se reconstruye a partir del texto corregido. El MP4 fragmentado se carga solo al solicitarlo.

## Fuentes primarias de contraste

- Mikolov et al. (2013), [Distributed Representations of Words and Phrases](https://arxiv.org/abs/1310.4546).
- Pennington et al. (2014), [GloVe](https://aclanthology.org/D14-1162/).
- Bojanowski et al. (2017), [Enriching Word Vectors with Subword Information](https://arxiv.org/abs/1607.04606).
- Sennrich et al. (2016), [Subword Units](https://aclanthology.org/P16-1162/).
- Bahdanau et al. (2015), [Learning to Align and Translate](https://arxiv.org/abs/1409.0473).
- Luong et al. (2015), [Effective Approaches to Attention](https://aclanthology.org/D15-1166/).
- Xu et al. (2015), [Show, Attend and Tell](https://arxiv.org/abs/1502.03044).
- Cheng et al. (2016), [Long Short-Term Memory-Networks](https://arxiv.org/abs/1601.06733).
- Parikh et al. (2016), [Decomposable Attention](https://aclanthology.org/D16-1244/).
- Vaswani et al. (2017), [Attention Is All You Need](https://arxiv.org/abs/1706.03762).
- Su et al., [RoFormer](https://arxiv.org/abs/2104.09864).
- Santurkar et al. (2018), [How Does Batch Normalization Help Optimization?](https://arxiv.org/abs/1805.11604).
- Baevski et al. (2020), [wav2vec 2.0](https://arxiv.org/abs/2006.11477).
- Wang et al., [Speaker Diarization with LSTM](https://arxiv.org/abs/1710.10468).
- [PyTorch: reproducibilidad](https://docs.pytorch.org/docs/stable/notes/randomness.html), [BatchNorm2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html), [cosine_similarity](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.cosine_similarity.html) y [LSTM](https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html).
- [TorchVision: NMS](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.nms.html).
- [SciPy: FFT](https://docs.scipy.org/doc/scipy/tutorial/fft.html).
- [D2L: convoluciones para imágenes](https://d2l.ai/chapter_convolutional-neural-networks/conv-layer.html).
- [Meta: implementación de Llama 3](https://github.com/meta-llama/llama3/blob/main/llama/model.py).

## Licencias y alcance

Se mantienen los archivos de licencia y cita recibidos, incluida la excepción de D2L. La revisión no cambia las condiciones de materiales de terceros. Consultá [cómo citar y las licencias](citar.html).

El catálogo recibido tiene 29 notebooks de las clases 2–16. La clase 1 sigue pendiente; las clases 17–19 no estaban incluidas en este paquete. Las descargas de una página HTML individual requieren también los assets del repositorio para verse sin conexión.
