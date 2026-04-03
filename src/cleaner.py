import pandas as pd

def limpiar_datos(empresas):
    df = pd.DataFrame(empresas)

    # Eliminar duplicados
    df = df.drop_duplicates(subset=["Nome"])

    # Convierte a númerico - cualquier valor no convertible se vuelve NaN
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce").fillna(0)
    df["Recensioni_totali"] = pd.to_numeric(df["Recensioni_totali"], errors="coerce").fillna(0)

    # Convertir tipos
    df["Rating"] = df["Rating"].astype(float)
    df["Recensioni_totali"] = df["Recensioni_totali"].astype(int)

    # Ordenar por rating descendente
    df = df.sort_values("Rating", ascending=False).reset_index(drop=True)

    return df


