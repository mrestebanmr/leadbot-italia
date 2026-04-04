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

def exportar_google_sheets(df, sheet_id):
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

    # Limpia el contenido anterior
    worksheet.clear()
    
    datos = [df.columns.tolist()] + df.values.tolist()
    worksheet.update(datos)

    # Devuelve el enlace público
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}"

