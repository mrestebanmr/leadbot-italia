import pandas as pd

def limpiar_datos(empresas):
    df = pd.DataFrame(empresas)

    # Eliminar duplicados
    df = df.drop_duplicates(subset=["Nome"])

    # Rellenar valores vacíos
    df["Rating"] = df["Rating"].fillna(0)
    df["Recensioni_totali"] = df["Recensioni_totali"].fillna(0)

    # Convertir tipos
    df["Rating"] = df["Rating"].astype(float)
    df["Recensioni_totali"] = df["Recensioni_totali"].astype(int)

    # Ordenar por rating descendente
    df = df.sort_values("Rating", ascending=False).reset_index(drop=True)

    return df


