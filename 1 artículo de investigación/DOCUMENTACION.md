# Documentación de `1 artículo de investigación`

## Propósito

Conservar el documento original correspondiente al primer trabajo de
investigación del curso.

## Archivos

### `PRIMER_TRABAJO_DE_INVESTIGACION_U-1.docx`

Documento Word de aproximadamente 174 kB. El contenido está compuesto
principalmente por tres imágenes incrustadas, por lo que no se puede buscar ni
extraer el texto con fiabilidad. Debe abrirse visualmente en Microsoft Word,
LibreOffice Writer o Google Docs.

## Cómo revisarlo

1. Abrir el DOCX y comprobar las tres páginas o imágenes.
2. Identificar título, formato y requisitos de presentación.
3. Usar `05_avances/articulo_investigacion_borrador.md` como versión editable
   del contenido técnico del proyecto.

### `articulo_gemelo_digital.tex` y `articulo_gemelo_digital.pdf`

Artículo paralelo titulado "Implementación de un Gemelo Digital para la
Optimización Energética y Diagnóstico Operativo de una Bomba Centrífuga
Industrial". El PDF tiene 4 páginas y desarrolla arquitectura física, IoT,
modelo virtual, seguimiento del punto de mejor eficiencia y diagnóstico de
cavitación. No corresponde al cálculo del ventilador Sirocco.

### `scopus_scraper.py`

Extractor de metadatos desde la API de Scopus. Usa `requests` y `pandas`, pagina
resultados, combina consultas y exporta un CSV. Requiere la variable de entorno
`SCOPUS_API_KEY`; nunca debe guardarse una clave directamente en el repositorio.

### `scopus_digital_twin_results.csv`

Contiene 49 registros y 11 columnas de metadatos sobre gemelos digitales,
bombas y temas relacionados. Debe revisarse manualmente porque una búsqueda
automática puede incluir resultados que no correspondan exactamente al tema.

### `README_SCOPUS.md`

Guía de instalación, configuración segura, estructura de consulta, ejecución y
campos del CSV.

## Separación temática

Esta línea de gemelos digitales para bombas se conserva como trabajo de
investigación independiente. No usar sus resultados como validación del
ventilador Sirocco ni mezclar sus referencias con la memoria del diseño sin una
justificación explícita.

## Limitación

El DOCX es material de entrada y el artículo de gemelo digital corresponde a
otra turbomáquina. Ninguno contiene los cálculos reproducibles vigentes del
ventilador; estos se encuentran en `06_calculos/` y `08_software/`.
