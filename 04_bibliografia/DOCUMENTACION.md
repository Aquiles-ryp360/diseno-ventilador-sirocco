# Documentación de `04_bibliografia`

## Propósito

Reunir las fuentes que sustentan el método de diseño y el trabajo futuro de
validación. La bibliografía se concentra en ventiladores centrífugos
multialabe, interacción rodete-voluta-lengua, CFD y optimización geométrica.

## Archivos

### `bibliografia_inicial.csv`

Base estructurada de artículos. Cada fila incluye tipo, título, autores, año,
DOI, fuente, resumen metodológico y aplicación al proyecto. Actualmente
contiene referencias de 2020 a 2026.

Campos principales:

- `doi`: identificador estable para localizar la publicación.
- `resumen_metodologia_resultados`: qué hizo el artículo y qué reportó.
- `aplicacion_al_proyecto`: por qué la fuente es relevante para el Sirocco.

### `estado_del_arte_preliminar.md`

Resume cinco líneas de investigación:

1. Interacción entre rodete, voluta y lengua.
2. CFD para validar diseños unidimensionales.
3. Optimización de ángulos, número de álabes y curvatura.
4. Métodos DOE, Taguchi y ANOVA.
5. Modelos a escala y prototipado.

## Cómo usar las referencias

- Las leyes de semejanza deben apoyarse en documentación técnica AMCA.
- La holgura de la lengua y el análisis de fluctuaciones deben justificarse con
  estudios específicos de ventiladores de álabes hacia adelante.
- La metodología CFD puede tomar referencias de OpenFOAM o ANSYS-CFX, pero las
  condiciones de frontera deben adaptarse al modelo de este proyecto.
- No copiar resultados de eficiencia de otros ventiladores como si fueran
  resultados propios.

## Criterio de citación

Toda afirmación externa debe incluir autor, año y DOI o URL. Los valores
calculados del proyecto deben citar el script o la memoria que los genera, no
un artículo externo.

## Pendientes

- Descargar y archivar las versiones permitidas de las fuentes principales.
- Completar lectura crítica y extraer geometrías comparables.
- Añadir normas de ensayo, seguridad, balanceo y selección de rodamientos.
