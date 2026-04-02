import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
BASE_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

def search_businesses(query, language="it"):
    params = {
        "query": query,
        "language": language,
        "key": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    empresas = []

    for empresa in data["results"]:
        empresas.append({
            "nombre": empresa.get("name", "N/A"),
            "direccion": empresa.get("formatted_address", "N/A"),
            "rating": empresa.get("rating", "N/A"),
            "total_reseñas": empresa.get("user_ratings_total", "N/A")
        })

    return empresas
