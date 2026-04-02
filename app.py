import streamlit as st
from src.scraper import search_businesses
from src.cleaner import limpiar_datos

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
if buscar and query:
    with st.spinner("Cercando aziende..."):
        resultado = search_businesses(query)
        df = limpiar_datos(resultado)

        # --- Métricas ---
        col1, col2, col3 = st.columns(3)
        col1.metric("Totale Leads", len(df))
        col2.metric("Rating promedio", round(df["rating"].mean(), 2))
        col3.metric("Con recensioni", len(df[df["total_reseñas"] > 0]))

        # --- Tabla de resultados ---
        st.subheader(" 📋 Risultati")
        st.dataframe(df, use_container_width=True)

