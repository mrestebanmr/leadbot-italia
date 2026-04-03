import os
from dotenv import load_dotenv
import streamlit as st
from src.scraper import search_businesses
from src.cleaner import limpiar_datos
from src.exporter import exportar_csv, exportar_google_sheets

load_dotenv()
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# --- Configuración de la página ---
st.set_page_config(
    page_title = "LeadBot Italia",
    page_icon = "🤖",
    layout = "wide"
)

# --- Título y descripión ---
st.title(" 🤖 LeadBot Italia")
st.markdown("Trova aziende B2B in Italia in un modo autentico")

# --- Pánel de búsqueda ---
st.sidebar.header(" 🔍 Ricerca")
query = st.sidebar.text_input("Settore + Cittá", placeholder="agenzie marketing Milano")
buscar = st.sidebar.button("Cercare Leads")

# --- Lógica Principal ---
# Inicializar session_state si no existe
if "df" not in st.session_state:
    st.session_state.df = None

if buscar and query:
    with st.spinner("Ricerca in corso..."):
        resultado = search_businesses(query)
        st.session_state.df = limpiar_datos(resultado)

# Mostrar resultados si existen en memoria
if st.session_state.df is not None:
    df = st.session_state.df


    # --- Métricas ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Totale Leads", len(df))
    col2.metric("Rating promedio", round(df["Rating"].mean(), 2))
    col3.metric("Con recensioni", len(df[df["Recensioni_totali"] > 0]))

    # --- Tabla de resultados ---
    st.subheader(" 📋 Risultati")
    st.dataframe(df, use_container_width=True)

    # --- Exportación ---
    st.subheader("📥 Esporta i risultati")

    if st.button("💾 Scarica CSV"):
        nombre = exportar_csv(df)
        st.success(f"File salvato: data/processed/{nombre}")

    if st.button("📊 Esporta su Google Sheets"):
        with st.spinner("Caricando su Google Sheets..."):
            enlace = exportar_google_sheets(df, SHEET_ID)
        st.success("Foglio creato con succeso!")
        st.markdown(f"[Apri il foglio Google Sheets]({enlace})")
