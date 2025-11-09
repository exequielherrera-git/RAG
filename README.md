# RAG — Asistente de Tickets (Soporte Técnico)

Este README explica cómo iniciar la app a partir de estos archivos.

## Instalación

1) Descargar todos los archivos localmente, en una carpeta (ej. RAG)

2) Situarse en la carpeta creada, en donde deberían estar todos los archivos y hacer lo siguiente:

```bash
# Crear y activar un entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias (puede fallar con faiss en macOS; ver nota arriba)
pip install --upgrade pip
pip install -r requirements.txt
```

3) Ejecutar la ingesta y procesamiento inicial

```bash
python -m rag.pipelines
```

1) Ejecutar la UI Streamlit -> A partir de aqui ya se puede hacer todo de forma Web

```bash
streamlit run app/ui_streamlit.py
# Por defecto abre en http://localhost:8501
```