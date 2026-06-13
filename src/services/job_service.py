import urllib.parse
import requests
from bs4 import BeautifulSoup
from src.services.gemini_service import gemini

class JobScraperService:
    def __init__(self):
        pass

    def search_jobs(self, keyword="comptable", limit=3):
        try:
            # We use a Google Search query specifically targeted at Luxembourg job sites
            query = f"{keyword} emploi luxembourg site:moovijob.com OR site:jobs.lu"

            # Since we can't reliably scrape without getting 403 blocks from Cloudflare on jobs.lu,
            # we prompt Gemini to act as a parser/formatter if we could pass it HTML,
            # but since Gemini can't browse the web directly in this simple API setup,
            # we will just provide direct Google search links to the user.

            google_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
            moovijob_url = f"https://www.moovijob.com/offres-emploi/jobs?q={urllib.parse.quote(keyword)}&l=luxembourg"

            result = f"🔍 La recherche automatique directe sur Jobs.lu a été bloquée par leur sécurité anti-robot.\n\n"
            result += f"Cependant, voici les liens directs pour chercher '{keyword}' au Luxembourg :\n"
            result += f"1. 🔗 Moovijob : {moovijob_url}\n"
            result += f"2. 🔗 Google Emplois : {google_url}\n\n"

            result += "🤖 **Comment utiliser l'IA Gemini :**\n"
            result += "Cliquez sur un de ces liens, trouvez une offre qui vous plaît, copiez la description du poste et collez-la moi ici en disant 'Rédige ma lettre de motivation pour ce poste : [Collez l'offre]'."

            return result

        except Exception as e:
            return f"Erreur lors de la recherche d'emploi: {e}"

job_service = JobScraperService()
