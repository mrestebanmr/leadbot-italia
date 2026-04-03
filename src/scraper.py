import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
BASE_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

def search_businesses(query, language="it"):
    # Verificar que la API Key existe
    if not API_KEY:
        raise ValueError("API key non trovata. Controlla il file .env")
    
    params = {
        "query": query,
        "language": language,
        "key": API_KEY
    }

    # Hacer la llamada HTTP
    response = requests.get(BASE_URL, params=params)

    # Verificar que la respuesta fue exitosa
    if response.status_code != 200:
        raise ConnectionError(f"Errore di conessione: {response.status_code}")
    
    data = response.json()

    # Verificar que Google no devolvió el error
    if data["status"] not in ["OK", "ZERO_RESULTS"]:
        raise ValueError(f"Erorre API Google: {data['status']}")
    
    if data["status"] == "ZERO_RESULTS":  #Si no hay resultados, devolver lista vacía
        return []

    empresas = []

    for empresa in data["results"]:
        empresas.append({
            "Nome": empresa.get("name", "N/A"),
            "Indirizzo": empresa.get("formatted_address", "N/A"),
            "Rating": empresa.get("rating", "N/A"),
            "Recensioni_totali": empresa.get("user_ratings_total", "N/A")
        })

    return empresas
