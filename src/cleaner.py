import pandas as pd

def limpiar_datos(empresas):
    df = pd.DataFrame(empresas)

    #Eliminar duplicados
    df = df.drop_duplicates(subset=["nombre"])

    # Rellenar Valores vacíos
    df["rating"] = df["rating"].fillna(0)
    df["total_reseñas"] = df["total_reseñas"].fillna(0)

    # Convertir tipos
    df["rating"] = df["rating"].astype(float)
    df["total_reseñas"] = df["total_reseñas"].astype(int)

    #Ordenar por rating descendente
    df = df.sort_values("rating", ascending=False).reset_index(drop=True)

    return df

