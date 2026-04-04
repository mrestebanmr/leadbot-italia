import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

def exportar_csv(df):
    # Genera nombre de archivo con fecha y ora actual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"lead_{timestamp}.csv"

    # Guarda el Dataframe como CSV sin el índice de Pandas
    df.to_csv(f"data/processed/{nombre_archivo}", index=False)

    return nombre_archivo

def exportar_google_sheets(df, sheet_id, query):
    # Permisos necesarios para leer y escribir Sheets y Drive
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # Carga las credenciales desde el archivo JSON
    credenciales = Credentials.from_service_account_file(
        "config/google_credentials.json",
        scopes = scopes
    )

    # Conecta con Google Sheets
    cliente = gspread.authorize(credenciales)

    # Abre la hoja existente por ID
    hoja = cliente.open_by_key(sheet_id)
    worksheet = hoja.get_worksheet(0)

    # Añade columnas de metadata a los datos
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    df = df.copy()
    df.insert(0, "Data ricerca", timestamp)
    df.insert(1, "Query", query)

    # Verifica si la hoja ya tiene encabezados
    contenuto_attuale = worksheet.get_all_values()

    if not contenuto_attuale:
        worksheet.append_row(df.columns.tolist())

    datos = df.astype(str).values.tolist() # Convierte todo a String para evitar conflictos con Sheets
    # Escribe fila por fila para evitar problemas de estructura.
    for fila in datos:
        # Aplana cualquier valor anidado a string simple
        fila_limpia = [str(v) if not isinstance(v, (str, int, float)) else v for v in fila]
        worksheet.append_row(fila_limpia)
    
    # Devuelve el enlace público
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}"

