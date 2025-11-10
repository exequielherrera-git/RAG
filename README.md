# RAG — Asistente de Tickets (Soporte Técnico)

Este README explica cómo iniciar la app a partir de estos archivos.

## Instalación

1) Descargar todos los archivos localmente, en una carpeta (ej. RAG)

2) Situarse en la carpeta creada, en donde deberían estar todos los archivos y hacer lo siguiente:

```bash
# Crear y activar un entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1

# Instalar dependencias (puede fallar con faiss en macOS; ver nota arriba)
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3) Ejecutar la UI Streamlit: Abre el entorno web local creado

```bash
streamlit run app/ui_streamlit.py
# Por defecto abre en http://localhost:8501
```

** Aclaraciones:

- La primera vez, en el menú de la izquierda, ejecutar "Actualizar índice" así Ejecuta la ingesta y el indexado.

- A partir de este momento, ya se podrían hacer las consultas al RAG