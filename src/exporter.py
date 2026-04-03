import pandas as pd
from datetime import datetime

def exportar_csv(df):
    # Genera nombre de archivo con fecha y ora actual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"lead_{timestamp}.csv"

    # Guarda el Dataframe como CSV sin el índice de Pandas
    df.to_csv(f"data/processed/{nombre_archivo}", index=False)

    return nombre_archivo

