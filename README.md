# Portafolio docente · NLP y reconocimiento del habla

**Jacobo León Juárez** · 2026

Libro web con 29 notebooks correspondientes a las clases 2–16 y sus recursos complementarios. La carpeta de la clase 1 se recibió vacía y aparece como pendiente. Las clases 17–19 quedan fuera de esta edición.

- [Sitio previsto en GitHub Pages](https://leonctfhtb.github.io/NLP-ASR-ML-DL-2026/)
- [LinkedIn](https://www.linkedin.com/in/lic-jacobo-leon-juarez/)
- [Portafolio de Notion](https://app.notion.com/p/leon-ctf/Portafolio-4034120b17c880048026ec0abf21f685)

El sitio ofrece índice por clases, búsqueda dentro del material, navegación anterior/siguiente, código desplegable y fórmulas MathML que no requieren una conexión externa. Los HTML y sus recursos están en `docs/`; pueden abrirse localmente tras descargar y descomprimir el repositorio. Algunas visualizaciones heredadas que dependen de JavaScript externo o de un kernel pueden requerir su entorno original; las salidas estáticas y los audios guardados se conservan.

## Activación inicial de GitHub Pages

En [Settings → Pages](https://github.com/leonCTFHTB/NLP-ASR-ML-DL-2026/settings/pages), seleccionar **Deploy from a branch**, rama **main**, carpeta **/docs**, y guardar. GitHub publica después los cambios de esa carpeta. El enlace previsto no implica que esta configuración ya esté activada.

## Alcance editorial

Se retiraron las celdas iniciales de montaje de Drive y rutas institucionales. Se mantuvo el contenido restante salvo correcciones técnicas registradas en `reports/correcciones.json` y sustituciones de figuras ambiguas. La organización y numeración interna original se conserva, aunque algunos notebooks se repiten como complementos en varias clases.

No se ejecutaron entrenamientos ni se certifican métricas de rendimiento: las salidas de los notebooks son las guardadas por su autor. Se recalcularon únicamente los gráficos deterministas de codificación posicional para que coincidan con las 32 dimensiones del laboratorio. La validación estructural se registra en `reports/validacion.json`.

## Reproducir la conversión

Instalar las dependencias de `tools/requirements.txt` y extraer los ZIP originales en una carpeta `extracted/`, preservando su estructura. El conversor recibe esa carpeta y una caché opcional de imágenes externas:

```bash
python tools/positional_plots.py
python tools/build.py --inputs /ruta/extracted --external /ruta/external
python tools/finalize.py
python tools/theme.py
python tools/editorial.py
python tools/editorial_figures.py
python tools/postprocess.py
python tools/validate.py
```

Los ZIP originales no se publican. Los HTML renderizados, recursos y herramientas de conversión están versionados para conservar una copia recuperable.

## Licencia y cita

Material docente **propio**: CC BY 4.0. Código **propio**: Apache 2.0. Las adaptaciones de D2L conservan CC BY-SA 4.0 y su código la licencia MIT modificada de D2L; otros materiales ajenos conservan sus condiciones. Véanse `LICENCIAS.md` y `THIRD_PARTY.md`.

Si reutilizás o adaptás las aportaciones propias, conservá la atribución. Para trabajos académicos se solicita citar con el registro de `CITATION.bib`; también se incluye `CITATION.cff`.

## Edición para GitHub Pages · 26 de octubre de 2026

Tema grafito con tres roles de color, eliminación de etiquetas `font`, títulos recuperados, búsqueda sincronizada con las correcciones y reparación de la carga del video fragmentado. Se conservan las licencias y las imágenes originales de las figuras sustituidas.

La revisión y sus límites están explicados en [reports/REVISION.md](reports/REVISION.md) y en `docs/revision.html`. Los cambios nuevos están separados de los registros recibidos: `reports/auditoria-editorial.json` y `reports/auditoria-figuras.json`. La revisión no certifica cada afirmación ni reproduce entrenamientos. Las escalas científicas y las imágenes de terceros conservan sus colores originales.

Para previsualizar también la búsqueda, los scripts y el video fragmentado, servir la carpeta con HTTP:

```bash
python -m http.server 8000 --directory docs
```

Abrir `http://localhost:8000/`. Descargar un HTML individual requiere también sus assets para verlo sin conexión.
