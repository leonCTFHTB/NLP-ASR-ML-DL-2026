# Portafolio docente · NLP y reconocimiento del habla

**Jacobo León Juárez** · 2026

Libro web con 29 notebooks correspondientes a las clases 2–16 y sus recursos complementarios.

- [Sitio previsto en GitHub Pages](https://leonctfhtb.github.io/NLP-ASR-ML-DL-2026/)
- [LinkedIn](https://www.linkedin.com/in/lic-jacobo-leon-juarez/)
- [Portafolio de Notion](https://app.notion.com/p/leon-ctf/Portafolio-4034120b17c880048026ec0abf21f685)

El sitio ofrece índice por clases, búsqueda dentro del material, navegación anterior/siguiente, código desplegable y fórmulas MathML que no requieren una conexión externa. Los HTML y sus recursos están en `docs/`; pueden abrirse localmente tras descargar y descomprimir el repositorio. Algunas visualizaciones heredadas que dependen de JavaScript externo o de un kernel pueden requerir su entorno original; las salidas estáticas y los audios guardados se conservan.

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

## Licencia y cita

Material docente **propio**: CC BY 4.0. Código **propio**: Apache 2.0. Las adaptaciones de D2L conservan CC BY-SA 4.0 y su código la licencia MIT modificada de D2L; otros materiales ajenos conservan sus condiciones. Véanse `LICENCIAS.md` y `THIRD_PARTY.md`.

Si reutilizás o adaptás las aportaciones propias, conservá la atribución. Para trabajos académicos se solicita citar con el registro de `CITATION.bib`; también se incluye `CITATION.cff`.

## Edición para GitHub Pages · 26 de octubre de 2026

La revisión y sus límites están explicados en [reports/REVISION.md](reports/REVISION.md) y en `docs/revision.html`. Los cambios nuevos están separados de los registros recibidos: `reports/auditoria-editorial.json` y `reports/auditoria-figuras.json`. La revisión no certifica cada afirmación ni reproduce entrenamientos. Las escalas científicas y las imágenes de terceros conservan sus colores originales.
