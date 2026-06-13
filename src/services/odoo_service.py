import os
import csv
from datetime import datetime
from collections import deque

class ComptaService:
    def __init__(self):
        self.data_file = "data/compta.csv"
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

        # Initialize CSV if it doesn't exist
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Date", "Motif", "Montant"])

    def get_recent_invoices(self, limit=5):
        """Get recent expenses/invoices from local CSV"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None) # Skip header
                # Use deque to only keep the last 'limit' rows in memory, making memory usage O(limit) instead of O(N)
                rows = list(deque(reader, maxlen=limit))

            if not rows:
                return "Aucune dépense enregistrée dans votre fichier comptable local."

            result = "Vos dernières opérations :\n"
            for row in rows:
                if len(row) >= 3:
                    result += f"💶 {row[0]} - {row[1]} : {row[2]}\n"

            return result
        except Exception as e:
            return f"Erreur lors de la lecture des comptes: {e}"

    def add_expense(self, motif, montant):
        """Add an expense to the local CSV"""
        try:
            with open(self.data_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), motif, montant])
            return f"Dépense enregistrée : {motif} pour {montant}"
        except Exception as e:
            return f"Erreur lors de l'enregistrement de la dépense: {e}"

# We keep the variable name 'odoo' so we don't break main.py, but it's now a local service
odoo = ComptaService()
