# Portafolio docente · NLP y reconocimiento del habla

**Jacobo León Juárez · 2026**

Libro web con 30 páginas de clases sobre embeddings, CNN, atención, Transformers, posiciones, audio, diarización y Whisper.

- [Leer el libro](https://leonctfhtb.github.io/NLP-ASR-ML-DL-2026/)
- [Bibliografía y criterios](https://leonctfhtb.github.io/NLP-ASR-ML-DL-2026/revision.html)
- [LinkedIn](https://www.linkedin.com/in/lic-jacobo-leon-juarez/)
- [Portafolio de Notion](https://app.notion.com/p/leon-ctf/Portafolio-4034120b17c880048026ec0abf21f685)

Las páginas y sus recursos se mantienen en `docs/`, que GitHub Pages publica desde `main`. El sitio incluye búsqueda local, navegación por clases, código desplegable y fórmulas MathML sin CDN. Para consultar sin conexión se necesita el repositorio completo.

## Mantenimiento y comprobaciones

Los HTML de `docs/nlp/` constituyen la edición vigente. Las explicaciones enlazan artículos y documentación oficial. Las figuras vectoriales se generan con `tools/review_figures.py` y `tools/scientific_figures.py`; las gráficas sintéticas declaran sus datos y supuestos.

El número de clase del catálogo coincide con el prefijo `clase-NN` del archivo HTML. `tools/postprocess.py` sincroniza ese número en la portada, las barras laterales, los títulos, la navegación y la búsqueda. Los apartados internos conservan la numeración temática del material. Solo se muestran entradas con contenido publicado.

Después de editar el contenido:

```bash
python -m pip install -r tools/requirements.txt
python tools/postprocess.py
python tools/clean_resources.py
python tools/validate.py
```

Las pruebas pequeñas de los ejemplos requieren PyTorch y no descargan datos ni entrenan modelos:

```bash
python -m pip install torch
python tools/check_examples.py
```

Los 24 diagramas numerados de Word2Vec se mantienen con `python tools/word2vec_figures.py`, seguido del posprocesado y la validación habituales. El generador comprueba las probabilidades, la pérdida y los gradientes de sus ejemplos, y registra la correspondencia con las imágenes del notebook en `reports/figuras-word2vec.json`.

`tools/current_edition.py` regenera la revisión editorial original; no debe usarse como paso general de importación porque sustituye bibliografías y su informe.

`reports/cobertura.json` enumera las 29 páginas y su bibliografía. `reports/revision-integral.json`, `reports/figuras-vigentes.json` y `reports/codigo-vigente.json` identifican el contenido actualizado. `reports/validacion.json` y `reports/pruebas-ejemplos.json` contienen los resultados de las comprobaciones. Las modificaciones se explican en los commits.

## Importar el notebook de Whisper

La página de la clase 17 conserva las 244 celdas y las salidas estáticas del notebook recibido. No se ejecutó su código. Las imágenes referenciadas se toman de los ZIP de las clases 18 y 21; las imágenes de los otros ZIP no se insertan si no están referenciadas. Las rutas personales de Drive se sustituyen por `/content/images` y `/content/audio` en el código mostrado.

```bash
python tools/import_whisper.py /ruta/notebook.ipynb /ruta/directorio-de-zips
python tools/postprocess.py
python tools/validate.py
```

`reports/importacion-whisper.json` registra la procedencia, el hash del notebook y el alcance de la conversión. Las comprobaciones de importación verifican texto, código, imágenes y audio; no equivalen a ejecutar el entrenamiento. La revisión bibliográfica documentada de las 29 páginas anteriores se conserva.

## Licencias y cita

Material docente propio: **CC BY 4.0**. Código propio: **Apache 2.0**. Las adaptaciones de D2L mantienen CC BY-SA 4.0 y su código MIT modificada; los demás materiales de terceros conservan sus autores y condiciones. Véanse `LICENCIAS.md`, `THIRD_PARTY.md`, `CITATION.bib` y `CITATION.cff`.
