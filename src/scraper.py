import os
from dotenv import load_dotenv
from outscraper import ApiClient

load_dotenv()

OUTSCRAPER_API_KEY = os.getenv("OUTSCRAPER_API_KEY")

def search_businesses(query, language="it", max_leads=20):
    # Verificar que la API Key existe
    if not OUTSCRAPER_API_KEY:
        raise ValueError("Outscraper API Key non trovata. Controlla il file .env")
    
    # Inicializar cliente Outscraper
    cliente = ApiClient(api_key=OUTSCRAPER_API_KEY)

    # Hacer la búsqueda - limit controla cuantos resultados devuelve
    resultados = cliente.google_maps_search(
        query,
        limit = max_leads,
        language = language,
        region = "IT"
    )

    # Outscraper devuelve la lista de listas 
    empresas = []
    for grupo in resultados:
        for empresa in grupo:
            empresas.append({
                "Nome": empresa.get("name", "N/A"),
                "Indirizzo": empresa.get("address", "N/A"),
                "Telefono": empresa.get("phone", "N/A"),
                "Sito Web": empresa.get("website", "N/A"),
                "Rating": empresa.get("rating", 0),
                "Recensioni_totali": empresa.get("reviews", 0)
            })

    return empresas
