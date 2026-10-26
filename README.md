# Portafolio docente · NLP y reconocimiento del habla

**Jacobo León Juárez · 2026**

Libro web con 29 páginas de clases sobre embeddings, CNN, atención, Transformers, posiciones, audio y diarización.

- [Leer el libro](https://leonctfhtb.github.io/NLP-ASR-ML-DL-2026/)
- [Bibliografía y criterios](https://leonctfhtb.github.io/NLP-ASR-ML-DL-2026/revision.html)
- [LinkedIn](https://www.linkedin.com/in/lic-jacobo-leon-juarez/)
- [Portafolio de Notion](https://app.notion.com/p/leon-ctf/Portafolio-4034120b17c880048026ec0abf21f685)

Las páginas y sus recursos se mantienen en `docs/`, que GitHub Pages publica desde `main`. El sitio incluye búsqueda local, navegación por clases, código desplegable y fórmulas MathML sin CDN. Para consultar sin conexión se necesita el repositorio completo.

## Mantenimiento y comprobaciones

Los HTML de `docs/nlp/` constituyen la edición vigente. Las explicaciones enlazan artículos y documentación oficial. Las figuras vectoriales se generan con `tools/review_figures.py` y `tools/scientific_figures.py`; las gráficas sintéticas declaran sus datos y supuestos.

Después de editar el contenido:

```bash
python -m pip install -r tools/requirements.txt
python tools/current_edition.py
python tools/postprocess.py
python tools/clean_resources.py
python tools/validate.py
```

Las pruebas pequeñas de los ejemplos requieren PyTorch y no descargan datos ni entrenan modelos:

```bash
python -m pip install torch
python tools/check_examples.py
```

`reports/cobertura.json` enumera las 29 páginas y su bibliografía. `reports/revision-integral.json`, `reports/figuras-vigentes.json` y `reports/codigo-vigente.json` identifican el contenido actualizado. `reports/validacion.json` y `reports/pruebas-ejemplos.json` contienen los resultados de las comprobaciones. Las modificaciones se explican en los commits.

## Licencias y cita

Material docente propio: **CC BY 4.0**. Código propio: **Apache 2.0**. Las adaptaciones de D2L mantienen CC BY-SA 4.0 y su código MIT modificada; los demás materiales de terceros conservan sus autores y condiciones. Véanse `LICENCIAS.md`, `THIRD_PARTY.md`, `CITATION.bib` y `CITATION.cff`.
