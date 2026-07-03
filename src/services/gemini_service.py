import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key or self.api_key == "votre_cle_gemini_ici":
            print("Warning: GEMINI_API_KEY is not properly set in .env")
        else:
            genai.configure(api_key=self.api_key)
            # Use gemini-pro for text tasks
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def generate_response(self, prompt: str) -> str:
        """
        Generate a simple text response to a prompt asynchronously.
        """
        if not self.api_key or self.api_key == "votre_cle_gemini_ici":
            return "Désolé, l'API Gemini n'est pas configurée. Veuillez ajouter votre clé dans le fichier .env."

        try:
            # Use generate_content_async to avoid blocking the asyncio event loop
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"Une erreur s'est produite lors de la communication avec l'IA: {str(e)}"

    async def generate_cover_letter(self, job_description: str, user_cv_summary: str) -> str:
        """
        Generate a tailored cover letter for a job description based on the user's CV asynchronously.
        """
        prompt = f"""
        Tu es un assistant de recherche d'emploi expert.
        Rédige une lettre de motivation professionnelle en français pour le poste décrit ci-dessous,
        en mettant en valeur les compétences du candidat (résumé du CV).

        Offre d'emploi :
        {job_description}

        Résumé du candidat :
        {user_cv_summary}
        """
        return await self.generate_response(prompt)

    async def analyze_intent(self, user_message: str) -> str:
        """
        Analyze user message to determine what module they want to interact with asynchronously.
        """
        prompt = f"""
        Analyse ce message de l'utilisateur : "{user_message}"

        Dans quelle catégorie tombe ce message ? Réponds uniquement par un de ces mots:
        - AGENDA (s'il parle de rendez-vous, rappels, temps)
        - FICHIERS (s'il veut ranger, trier, trouver un document)
        - COMPTA (s'il parle d'argent, dépenses, factures, Odoo)
        - EMPLOI (s'il cherche un travail, CV, lettre de motivation)
        - CHAT (pour toute autre conversation)
        """
        response = await self.generate_response(prompt)
        return response.strip().upper()

# Singleton instance
gemini = GeminiService()
