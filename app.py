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

# --- Estilos CSS personalizados ---
st.markdown("""
    <style>
    /* Fuente general */
    html, body, [class*="css"] {
        font-family: 'Courier New', monospace;
    }

    /* Título principal */
    h1 {
        color: #00D4AA;
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: 2px;
    }

    /* Subtítulos */
    h2, h3 {
        color: #00D4AA;
        letter-spacing: 1px;
    }

    /* Tarjetas de métricas */
    [data-testid="metric-container"] {
        background-color: #1A1F2E;
        border: 1px solid #00D4AA;
        border-radius: 10px;
        padding: 15px;
    }

    /* Botones */
    .stButton > button {
        background-color: #00D4AA;
        color: #0E1117;
        font-weight: 700;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        letter-spacing: 1px;
        transition: 0.3s;
    }

    /* Efecto hover en botones */
    .stButton > button:hover {
        background-color: #00F5C4;
        transform: translateY(-2px);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1A1F2E;
        border-right: 1px solid #00D4AA33;
    }
    </style>
""", unsafe_allow_html=True)

# --- Título y descripión ---
st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1>🤖 LeadBot Italia</h1>
        <p style='color: #00D4AA; font-size: 1.1rem; letter-spacing: 2px;'>
            TROVA · ANALIZZA · ESPORTA
        </p>
        <p style='color: #888; font-size: 0.9rem;'>
            Lead B2B italiani in pochi secondi
        </p>
    </div>
    <hr style='border-color: #00D4AA33; margin-bottom: 30px;'>
""", unsafe_allow_html=True)

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
