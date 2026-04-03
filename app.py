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
query = st.sidebar.text_input("Settore + Città", placeholder="Agenzie Marketing Milano")
buscar = st.sidebar.button("Cercare Leads")

# --- Filtros ---
st.sidebar.header("🎯 Filtri")
min_rating = st.sidebar.slider("Rating minimo", 0.0, 5.0, 0.0, 0.5)
min_recensioni = st.sidebar.number_input("Recensioni minime:", min_value=0, value=0, step=10)

# --- Lógica Principal ---
# Inicializar session_state si no existe
if "df" not in st.session_state:
    st.session_state.df = None

if buscar and not query:     #Aviso si el usuario no escribió nada
    st.sidebar.warning("⚠️ Inserisci un settore e una città")

if buscar and query:
    try:
        with st.spinner("Ricerca in corso..."):
            resultado = search_businesses(query)
        
            if not resultado:
                st.info("🔍 Nessuna azienda trovata. Prova con un'altra ricerca.")
            else:
                st.session_state.df = limpiar_datos(resultado)

    except ValueError as e:
        st.error(f"⚠️ Errore: {e}")
    except ConnectionError:
        st.error("🔌 Problema di conessione. Controlla la tua rete e riprova")
    except Exception as e:
        st.error(f"❌ Erorre inaspettato: {e}")

# Mostrar resultados si existen en memoria
if st.session_state.df is not None:
    df = st.session_state.df

    # Aplicar filtros al DataFrame
    df = df[df["Rating"] >= min_rating]
    df = df[df["Recensioni_totali"] >= min_recensioni]

    # Aviso si los filtros eliminaron todos los resultados
    if df.empty:
        st.warning("⚠️ Nessuna azienda corrisponde ai filtri selezionati.")
        st.stop()


    # --- Métricas ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Totale Leads", len(df))
    col2.metric("Rating promedio", round(df["Rating"].mean(), 2))
    col3.metric("Con recensioni", len(df[df["Recensioni_totali"] > 0]))

    # --- Tabla de resultados ---
    st.subheader(" 📋 Risultati")
    st.dataframe(df, width="stretch")

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
