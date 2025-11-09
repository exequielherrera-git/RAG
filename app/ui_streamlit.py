import sys, os

# --- Ajustar path raíz ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
    
import streamlit as st
from rag.pipelines import build_index, answer_query

# --- Configuración general ---
st.set_page_config(page_title="RAG | Tickets Soporte Tecno", layout="wide")

# --- Cargar estilos externos ---
css_path = os.path.join(ROOT_DIR, "assets", "styles", "main.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.warning("⚠️ Archivo de estilos no encontrado en assets/styles/main.css")

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.markdown(
    """
    <div class="sidebar-header">
        <h3>RAG | Tickets Soporte Tecno</h3>
        <hr>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("Opciones")
menu = st.sidebar.radio(
    "Selecciona una acción:",
    ["Consultar", "Actualizar índice", "Subir nuevos tickets"]
)

# =====================================================
# 1️⃣ SUBIR NUEVOS TICKETS
# =====================================================
if menu == "Subir nuevos tickets":
    st.subheader("📤 Subir archivos JSON de tickets")
    uploaded_files = st.file_uploader(
        "Seleccioná uno o varios archivos JSON",
        type=["json"],
        accept_multiple_files=True
    )

    if uploaded_files:
        os.makedirs("data/raw", exist_ok=True)
        for file in uploaded_files:
            save_path = os.path.join("data/raw", file.name)
            with open(save_path, "wb") as f:
                f.write(file.read())
        st.success(f"✅ {len(uploaded_files)} archivos subidos correctamente a data/raw/")

# =====================================================
# 2️⃣ ACTUALIZAR ÍNDICE
# =====================================================
elif menu == "Actualizar índice":
    st.subheader("⚙️ Reconstruir índice FAISS")
    if st.button("🔄 Ejecutar Ingesta + Indexado", use_container_width=True):
        with st.spinner("Procesando archivos y actualizando índice..."):
            build_index()
        st.success("✅ Índice actualizado correctamente.")

# =====================================================
# 3️⃣ CONSULTAR
# =====================================================
elif menu == "Consultar":
    st.markdown("<h2 class='main-title'>Hola, ¿en qué puedo ayudarte?</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    with col2:
        # --- Input y botón en una misma fila ---
        col_input, col_button = st.columns([9, 1])
        with col_input:
            query = st.text_input(
                label="",
                placeholder="Escribí tu pregunta aquí...",
                label_visibility="collapsed",
                key="query_box"
            )

        submitted = False
        with col_button:
            if st.button(" -> ", key="send_btn"):
                submitted = True

        # --- Si se presionó el botón ---
        if submitted:
            if not query.strip():
                st.warning("Por favor, ingresá una pregunta.")
            else:
                # Crear un marcador temporal para el spinner
                progress_placeholder = st.empty()

                # Mostrar animación mientras busca
                progress_placeholder.markdown(
                    "<div class='casino-progress'><span class='casino-icon'></span><span>Buscando información y generando respuesta...</span></div>",
                    unsafe_allow_html=True
                )

                # Ejecutar consulta
                answer = answer_query(query)

                # Eliminar spinner al terminar
                progress_placeholder.empty()

                # Mostrar respuesta debajo del textbox
                st.markdown("<p class='answer-title'>Respuesta:</p>", unsafe_allow_html=True)
                st.markdown(f"<div class='answer-text'>{answer}</div>", unsafe_allow_html=True)