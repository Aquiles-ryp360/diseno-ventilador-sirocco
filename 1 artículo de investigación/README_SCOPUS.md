# Guía de Uso: Extractor de Artículos Científicos de Scopus

Este directorio contiene un script en Python (`scopus_scraper.py`) diseñado para realizar búsquedas avanzadas en la base de datos científica de **Scopus (Elsevier)**, extraer metadatos de artículos de acceso abierto (Open Access) y estructurarlos en un archivo CSV para su revisión o uso bibliográfico.

---

## 📋 Requisitos Previos

Antes de ejecutar el extractor, asegúrate de tener instalado Python y las siguientes librerías:

```bash
pip install requests pandas
```

---

## 🔑 Configuración de la API Key de Scopus

La API de Scopus requiere una clave de autenticación para permitir solicitudes.

1.  Regístrate o inicia sesión en el portal de desarrolladores de Elsevier: [Elsevier Developer Portal](https://dev.elsevier.com/).
2.  Haz clic en **"Create API Key"**.
3.  Ingresa un nombre para tu clave (ej. *ScopusResearch*) y la URL de tu sitio (puedes usar `http://localhost`).
4.  Configura la clave como variable de entorno; no la escribas en el código:

    Linux o macOS:

    ```bash
    export SCOPUS_API_KEY="TU_CLAVE"
    ```

    Windows PowerShell:

    ```powershell
    $env:SCOPUS_API_KEY="TU_CLAVE"
    ```

> Si una clave se publicó previamente en GitHub, debe revocarse en Elsevier
> Developer Portal y reemplazarse por una nueva.

> ⚠️ **Nota de Red / Acceso Institucional:** La API de Scopus suele limitar el acceso completo a los metadatos y resúmenes a menos que la consulta provenga de una dirección IP autorizada institucionalmente (ej. red de tu universidad o conexión a través de VPN institucional).

---

## ⚙️ Adaptación del Script a Otros Temas

El script está actualmente optimizado para el tema **"Gemelos Digitales (Digital Twin) en bombas centrífugas"**. Si deseas utilizarlo para otros proyectos de investigación, sigue estos pasos:

### 1. Modificar las Consultas (Queries)
Abre el script `scopus_scraper.py` y busca la sección `queries = [...]` al final del archivo. Reemplaza los textos de búsqueda por los términos de tu nuevo tema.

**Ejemplo para el tema anterior de "Primeros Auxilios en Accidentes de Trabajo":**
```python
queries = [
    'TITLE-ABS-KEY("first aid response" AND "workplace accidents") AND SUBJAREA(medi) AND DOCTYPE(ar) AND OPENACCESS(1)',
    'TITLE-ABS-KEY("emergency response" AND "workplace safety") AND SUBJAREA(medi) AND DOCTYPE(ar) AND OPENACCESS(1)'
]
```

### 🔍 Consejos para construir la consulta de Scopus:
*   `TITLE-ABS-KEY("término A" AND "término B")`: Busca los términos en el Título, Resumen (Abstract) o Palabras Clave.
*   `AND DOCTYPE(ar)`: Restringe los resultados únicamente a artículos científicos (*Articles*), filtrando revisiones o capítulos de libros.
*   `AND OPENACCESS(1)`: Garantiza que los artículos devueltos sean de acceso abierto, permitiéndote descargar el archivo completo sin costo.
*   `AND SUBJAREA(engr)`: Opcional. Restringe la búsqueda al área temática de Ingeniería (*Engineering*).

---

## 🚀 Ejecución del Script

Abre la terminal en esta carpeta y ejecuta:

```bash
python scopus_scraper.py
```

### Comportamiento del Script:
*   Realiza las peticiones de manera iterativa por cada consulta de la lista.
*   Controla los límites de velocidad de la API (`Rate Limits`) pausando automáticamente la ejecución cuando es necesario.
*   Combina los resultados de todas las consultas, elimina los duplicados implícitos y los limita a los **120 artículos más relevantes**.
*   Genera un archivo llamado `scopus_digital_twin_results.csv` en este mismo directorio.

---

## 📊 Estructura del Archivo de Salida (`.csv`)

El archivo de salida estructurado contiene las siguientes columnas útiles para tu estado del arte o memoria de investigación:

| Columna | Descripción |
| :--- | :--- |
| **Title** | Título oficial del artículo científico. |
| **Author(s)** | Autor principal o lista de autores. |
| **Year** | Año de publicación del artículo. |
| **Objective/Purpose** | Resumen (Abstract) del artículo que detalla el objetivo. |
| **Methodology** | Metodología empleada (por defecto "N/A", adaptable mediante procesamiento de texto). |
| **Results** | Resultados obtenidos en la investigación. |
| **DOI** | Identificador de Objeto Digital para citación directa. |
| **Link** | Enlace web directo provisto por la API. |
| **ScopusID** | Identificador interno de Scopus. |
| **Direct Link** | Enlace de redirección directo a la ficha del artículo en el portal de Scopus. |
