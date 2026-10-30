# Bibliografía y criterios del material

El libro reúne 30 páginas de clases sobre embeddings, redes convolucionales, atención, Transformers, posiciones, audio, diarización y Whisper. Las explicaciones distinguen definiciones matemáticas, elecciones de implementación y ejemplos ilustrativos.

## Fuentes

Las referencias principales son artículos de sus autores, documentación oficial y el texto de Dive into Deep Learning. Cada tema incluye su bibliografía y las explicaciones revisadas enlazan su fuente.

- [Mikolov et al. · Word2Vec](https://arxiv.org/abs/1310.4546)
- [D2L · Word embedding](https://d2l.ai/chapter_natural-language-processing-pretraining/word2vec.html)
- [Pennington et al. · GloVe](https://aclanthology.org/D14-1162/)
- [Duchi et al. · AdaGrad](https://jmlr.org/papers/v12/duchi11a.html)
- [Bojanowski et al. · Subword information](https://aclanthology.org/Q17-1010/)
- [fastText · Implementación oficial](https://github.com/facebookresearch/fastText/tree/main/src)
- [Joulin et al. · Clasificación de texto](https://aclanthology.org/E17-2068/)
- [PyTorch · EmbeddingBag](https://docs.pytorch.org/docs/stable/generated/torch.nn.EmbeddingBag.html)
- [Loshchilov y Hutter · AdamW](https://arxiv.org/abs/1711.05101)
- [PyTorch · CrossEntropyLoss](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)
- [D2L · Convoluciones](https://d2l.ai/chapter_convolutional-neural-networks/conv-layer.html)
- [PyTorch · Conv2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html)
- [D2L · Padding y stride](https://d2l.ai/chapter_convolutional-neural-networks/padding-and-strides.html)
- [D2L · Pooling](https://d2l.ai/chapter_convolutional-neural-networks/pooling.html)
- [PyTorch · BatchNorm2d](https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html)
- [Simonyan y Zisserman · VGG](https://arxiv.org/abs/1409.1556)
- [Vaswani et al. · Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [Bahdanau et al. · Alineación aprendida](https://arxiv.org/abs/1409.0473)
- [Luong et al. · Atención global y local](https://aclanthology.org/D15-1166/)
- [Xu et al. · Show, Attend and Tell](https://proceedings.mlr.press/v37/xuc15.html)
- [PyTorch · Gumbel-softmax](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.gumbel_softmax.html)
- [Hochreiter y Schmidhuber · LSTM](https://www.bioinf.jku.at/publications/older/2604.pdf)
- [Parikh et al. · Decomposable attention](https://aclanthology.org/D16-1244/)
- [Cheng et al. · LSTMN](https://aclanthology.org/D16-1053/)
- [Graves et al. · Neural Turing Machines](https://arxiv.org/abs/1410.5401)
- [Su et al. · RoFormer](https://arxiv.org/abs/2104.09864)
- [Matplotlib · Animation.to_jshtml](https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.Animation.html#matplotlib.animation.Animation.to_jshtml)
- [D2L · SSD](https://d2l.ai/chapter_computer-vision/ssd.html)
- [Girshick et al. · R-CNN](https://arxiv.org/abs/1311.2524)
- [Girshick · Fast R-CNN](https://arxiv.org/abs/1504.08083)
- [Ren et al. · Faster R-CNN](https://arxiv.org/abs/1506.01497)
- [He et al. · Mask R-CNN](https://arxiv.org/abs/1703.06870)
- [Redmon y Farhadi · YOLO9000](https://arxiv.org/abs/1612.08242)
- [Redmon y Farhadi · YOLOv3](https://arxiv.org/abs/1804.02767)
- [Lin et al. · Focal Loss](https://arxiv.org/abs/1708.02002)
- [Torchvision · Transformaciones](https://docs.pytorch.org/vision/stable/transforms.html)
- [Torchvision · batched_nms](https://docs.pytorch.org/vision/stable/generated/torchvision.ops.batched_nms.html)
- [SciPy · Fourier transforms](https://docs.scipy.org/doc/scipy/tutorial/fft.html)
- [SciPy · ShortTimeFFT](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.ShortTimeFFT.html)
- [SciPy · Reconstrucción STFT y NOLA](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.check_NOLA.html)
- [librosa · Banco Mel](https://librosa.org/doc/0.10.2/generated/librosa.filters.mel.html)
- [librosa · MFCC](https://librosa.org/doc/0.10.2/generated/librosa.feature.mfcc.html)
- [librosa · CQT inversa](https://librosa.org/doc/0.10.2/generated/librosa.icqt.html)
- [librosa · Preénfasis](https://librosa.org/doc/0.10.2/generated/librosa.effects.preemphasis.html)
- [Radford et al. · Whisper](https://proceedings.mlr.press/v202/radford23a.html)
- [MIT OpenCourseWare · Fourier y principio de incertidumbre](https://ocw.mit.edu/courses/18-103-fourier-analysis-fall-2013/)
- [Wan et al. · GE2E](https://arxiv.org/abs/1710.10467)
- [GE2E · Publicación y actualizaciones de los autores](https://google.github.io/speaker-id/publications/GE2E/)
- [Wang et al. · Speaker diarization](https://arxiv.org/abs/1710.10468)
- [Mansfield et al. · Links](https://arxiv.org/abs/1801.10123)

## Convenciones y ejemplos

Las fórmulas declaran ejes, dimensiones, índices y supuestos cuando afectan el resultado. Las analogías acompañan al cálculo y no sustituyen una definición. Las gráficas sintéticas indican sus parámetros; no se presentan como resultados de un entrenamiento. Las cifras publicadas se interpretan dentro del experimento que las produjo.

Los ejemplos de atención incluyen máscaras y el tratamiento explícito de secuencias sin claves válidas. La variante gaussiana didáctica calcula scores globales y no representa una implementación dispersa. La autoatención bilineal del laboratorio es una adaptación y no una reproducción de la recurrencia LSTMN.

## Comprobaciones

Se comprueban enlaces y recursos internos, fórmulas MathML y sintaxis del código. Las pruebas pequeñas ejecutan atención, padding, IoU y NMS, y verifican identidades de Word2Vec, RoPE, Links y FFT. No se han repetido los entrenamientos completos, las descargas de datasets ni los benchmarks de GPU; estas comprobaciones no certifican el rendimiento de los modelos.

Las animaciones se inspeccionan mediante fotogramas representativos. Los códigos, recursos y referencias vigentes forman parte del repositorio. Las modificaciones se documentan en sus commits.

## Autoría y licencias

Las aportaciones propias y los materiales de terceros conservan sus condiciones de uso y atribución. Las adaptaciones de D2L mantienen su licencia específica. Consultá [cómo citar y las licencias](citar.html).

## Incorporación de las clases 20–23 · Whisper

El notebook adjunto se incorporó como una página adicional con 244 celdas, nueve imágenes referenciadas de los ZIP, una gráfica de salida y una muestra de audio guardada. Se conservaron el orden, las explicaciones, el código y las salidas estáticas. Las rutas personales de Google Drive se muestran como `/content/images` y `/content/audio`, los colores se adaptan al tema y se omiten los widgets de progreso exclusivos de Colab. La importación no ejecutó entrenamiento ni volvió a comprobar sus resultados experimentales. El registro de importación conserva el SHA-256 del archivo fuente. La revisión bibliográfica descrita anteriormente corresponde a las 29 páginas previas.
