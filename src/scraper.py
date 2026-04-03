import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
BASE_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

def search_businesses(query, language="it", max_paginas=3):
    # Verificar que la API Key existe
    if not API_KEY:
        raise ValueError("API key non trovata. Controlla il file .env")
    
    params = {
        "query": query,
        "language": language,
        "key": API_KEY
    }

    empresas = []

    # Iteramos hasta max_paginas veces
    for pagina in range(max_paginas):
        response = requests.get(BASE_URL, params=params) # Llamada HTTP

        if response.status_code != 200:
            raise ConnectionError(f"Errore di conessione: {response.status_code}")  # Verificar que la respuesta fue exitosa
        data = response.json()

    # Verificar que Google no devolvió el error
        if data["status"] not in ["OK", "ZERO_RESULTS"]:
            raise ValueError(f"Erorre API Google: {data['status']}")
    
        if data["status"] == "ZERO_RESULTS":  #Si no hay resultados en 1ma página, salir
            break

        for empresa in data["results"]: # Extraer empresas de esta página
            empresas.append({
                "Nome": empresa.get("name", "N/A"),
                "Indirizzo": empresa.get("formatted_address", "N/A"),
                "Rating": empresa.get("rating", "N/A"),
                "Recensioni_totali": empresa.get("user_ratings_total", "N/A")
        })
    
        if "next_page_token" not in data: # Si no hay más páginas, salir del blucle
            break

        next_token = data["next_page_token"]
        time.sleep(5) # Google requiere una pausa antes de usar el token.

        params = {
            "pagetoken": next_token,
            "key": API_KEY
        }
        return empresas