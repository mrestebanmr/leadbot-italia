# 🤖 LeadBot Italia

> Trova, analizza ed esporta lead B2B italiani in pochi secondi.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)
![Google Maps API](https://img.shields.io/badge/Google%20Maps-API-green)

---

## 🎯 Cos'è LeadBot Italia?

LeadBot Italia è uno strumento di generazione automatica di lead B2B
per il mercato italiano. Inserisci un settore e una città — LeadBot
trova le aziende, le analizza e le esporta in CSV o Google Sheets.

**Ideale per:**

- Agenzie di marketing che cercano nuovi clienti
- Consulenti B2B che fanno prospecting
- Team commerciali che vogliono automatizzare la ricerca

---

## ⚡ Funzionalità

- 🔍 Ricerca aziende per settore e città in tutta Italia
- 📊 Analisi automatica: rating, recensioni, distribuzione
- 🎯 Filtri interattivi per rating minimo e recensioni
- 💾 Esportazione CSV con timestamp automatico
- 📋 Esportazione diretta su Google Sheets
- 🌙 Interfaccia dark mode professionale

---

## 🛠️ Stack Tecnico

| Tecnologia        | Utilizzo                      |
| ----------------- | ----------------------------- |
| Python 3.13       | Linguaggio principale         |
| Streamlit         | Interfaccia web               |
| Pandas            | Pulizia e analisi dati        |
| Google Maps API   | Estrazione dati aziendali     |
| Google Sheets API | Esportazione cloud            |
| gspread           | Integrazione Google Sheets    |
| python-dotenv     | Gestione variabili d'ambiente |

---


## 🏗️ Architettura

```
leadbot-italia/
│
├── app.py                  # Entry point — Streamlit UI
├── config/
│   └── settings.py         # Configurazione globale
├── src/
│   ├── scraper.py          # Estrazione dati (Google Maps API)
│   ├── cleaner.py          # Pulizia dati con Pandas
│   └── exporter.py         # Export CSV e Google Sheets
├── data/
│   └── processed/          # Dati esportati
├── notebooks/
│   └── exploracion.ipynb   # Esplorazione e test
└── requirements.txt
```


## 🚀 Installazione

---
## 🚀 Installazione

**1. Clona il repository**
```bash
git clone https://github.com/mrestebanmr/leadbot-italia.git
cd leadbot-italia
```

**2. Crea e attiva l'ambiente virtuale**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Installa le dipendenze**
```bash
pip install -r requirements.txt
```

**4. Configura le variabili d'ambiente**
```bash
cp .env.example .env
```
Inserisci la tua API key di Google Maps e l'ID del foglio Google Sheets nel file `.env`.

**5. Avvia l'applicazione**
```bash
streamlit run app.py
```
---
## 🔐 Variabili d'ambiente

Crea un file `.env` nella root del progetto:


## 👨‍💻 Autore

---
**Esteban Muriel**  
Python Developer & Data Science Student  
📧 [estebanmuriel16@outlook.es]  
🔗 [LinkedIn] https://www.linkedin.com/in/esteban-muriel-648b552ba/
🐙 [GitHub](https://github.com/mrestebanmr)
---
## 📄 Licenza

MIT License — libero di usare, modificare e distribuire.
