import re
import requests
from bs4 import BeautifulSoup
import urllib.parse

class JobScraperService:
    def __init__(self):
        # We use a generic search as an example
        self.base_url = "https://www.jobs.lu/job-search"

    def search_jobs(self, keyword="comptable", limit=3):
        """
        Scrape jobs.lu for a specific keyword.
        Note: Website structures change, this is a basic example.
        """
        try:
            # Format the URL properly based on jobs.lu structure (might require adjustments based on actual site structure)
            search_url = f"{self.base_url}?k={urllib.parse.quote(keyword)}"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.get(search_url, headers=headers)

            if response.status_code != 200:
                return f"Erreur lors de la recherche sur jobs.lu (Status: {response.status_code})"

            soup = BeautifulSoup(response.content, 'html.parser')

            jobs = []
            # Find job cards. This selector might need to be adjusted based on Jobs.lu's actual DOM.
            # Assuming a generic article or div wrapper with 'job-item' class as fallback
            job_cards = soup.find_all('article', class_=re.compile(r'job', re.I))
            if not job_cards:
                job_cards = soup.find_all('div', class_=re.compile(r'job(-| )?card', re.I))

            for card in job_cards:
                title_elem = card.find(['h2', 'h3'])
                if not title_elem:
                    continue

                title = title_elem.text.strip()

                link_elem = title_elem.find('a') if title_elem.name != 'a' else title_elem
                if not link_elem and title_elem.parent.name == 'a':
                    link_elem = title_elem.parent

                link = link_elem['href'] if link_elem and link_elem.has_attr('href') else "#"
                if link.startswith('/'):
                    link = f"https://www.jobs.lu{link}"

                company_elem = card.find(class_=re.compile(r'company|employer', re.I))
                company = company_elem.text.strip() if company_elem else "Entreprise inconnue"

                jobs.append({"title": title, "company": company, "link": link})
                if len(jobs) >= limit:
                    break

            if not jobs:
                # Fallback to general message since actual scraping requires a headless browser often
                return f"Aucune offre trouvée directement, mais vous pouvez chercher '{keyword}' ici: {search_url}"


            if not jobs:
                return f"Aucune offre trouvée pour '{keyword}'."

            result = f"🔍 Voici quelques offres pour '{keyword}' au Luxembourg :\n\n"
            for i, job in enumerate(jobs[:limit]):
                result += f"{i+1}. {job['title']} chez {job['company']}\n🔗 Lien: {job['link']}\n\n"

            result += "Si une offre vous intéresse, envoyez-moi sa description et je vous rédigerai une lettre de motivation !"
            return result

        except Exception as e:
            return f"Erreur lors de la recherche d'emploi: {e}"

job_service = JobScraperService()
