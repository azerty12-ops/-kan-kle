import xmlrpc.client
import os
from dotenv import load_dotenv

load_dotenv()

class OdooService:
    def __init__(self):
        self.url = os.getenv("ODOO_URL")
        self.db = os.getenv("ODOO_DB")
        self.username = os.getenv("ODOO_USERNAME")
        self.password = os.getenv("ODOO_PASSWORD")
        self.uid = None
        self.models = None

    def connect(self):
        """Connect to Odoo XML-RPC API"""
        if not all([self.url, self.db, self.username, self.password]) or self.url == "https://votre-domaine.odoo.com":
            return False, "Les identifiants Odoo ne sont pas configurés dans .env"

        try:
            common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
            self.uid = common.authenticate(self.db, self.username, self.password, {})

            if self.uid:
                self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')
                return True, "Connexion à Odoo réussie"
            else:
                return False, "Échec de l'authentification Odoo"
        except Exception as e:
            return False, f"Erreur de connexion à Odoo: {e}"

    def get_recent_invoices(self, limit=5):
        """Get recent invoices from Odoo"""
        success, msg = self.connect()
        if not success:
            return msg

        try:
            # Assuming 'account.move' is the invoice model in Odoo
            invoice_ids = self.models.execute_kw(self.db, self.uid, self.password,
                'account.move', 'search',
                [[['move_type', '=', 'out_invoice']]],
                {'limit': limit, 'order': 'invoice_date desc'})

            if not invoice_ids:
                return "Aucune facture récente trouvée."

            invoices = self.models.execute_kw(self.db, self.uid, self.password,
                'account.move', 'read',
                [invoice_ids],
                {'fields': ['name', 'partner_id', 'amount_total', 'state', 'invoice_date']})

            result = "Vos dernières factures Odoo :\n"
            for inv in invoices:
                partner = inv.get('partner_id', [0, "Inconnu"])[1]
                result += f"📄 {inv.get('name')} - {partner} : {inv.get('amount_total')}€ ({inv.get('state')})\n"

            return result

        except Exception as e:
            return f"Erreur lors de la récupération des factures: {e}"

odoo = OdooService()
