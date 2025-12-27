# Sistema de Gestión Personal - Local Web App

Esta es una aplicación web minimalista y local para la gestión de documentos estratégicos y operativos, sin base de datos ni métricas complejas.

## Requisitos

- Python 3.x
- Flask (`pip install flask`)
- Markdown (`pip install markdown`) - Opcional, si decidimos usar renderizado en servidor, pero usaremos pre-procesamiento seguro o solo texto.

## Instalación

1.  Asegúrate de tener Python instalado.
2.  Instala las dependencias:
    ```bash
    pip install flask markdown
    ```
3.  **IMPORTANTE**: Copia el contenido real de tus documentos en los archivos dentro de la carpeta `/docs`:
    - `/docs/01_mapa_estrategico_2026.md`
    - `/docs/02_manual_operativo_diario.md`

## Ejecución

1.  Abre una terminal en la carpeta raíz del proyecto.
2.  Ejecuta el servidor:
    ```bash
    python app/server.py
    ```
3.  Abre tu navegador en `http://127.0.0.1:8000`.

## Estructura

- `docs/`: Contiene tus archivos Markdown (la fuente de verdad).
- `app/`: Código de la aplicación.
- `app/server.py`: El servidor web.
