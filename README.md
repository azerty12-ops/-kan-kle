# Assistant Personnel (Telegram Bot)

Ce projet est un assistant personnel intelligent fonctionnant via Telegram. Il est conçu pour vous aider dans vos tâches quotidiennes, gérer vos fichiers locaux, votre comptabilité (via Odoo) et vos recherches d'emploi au Luxembourg.

Il utilise l'IA de Google (Gemini) pour comprendre vos demandes et générer du texte (ex: lettres de motivation).

## Fonctionnalités principales

- 🤖 **Intelligence Artificielle (Gemini)** : Discutez naturellement avec l'assistant, il comprendra vos intentions.
- 📅 **Agenda Google** (`/agenda`) : Consultez vos prochains événements et formations.
- 📁 **Gestionnaire de fichiers** (`/fichiers`) : Trie automatiquement le contenu d'un dossier (ex: Téléchargements) vers des dossiers organisés (Images, PDF, Comptabilité, etc.).
- 💶 **Comptabilité Odoo** (`/compta`) : Se connecte à votre base Odoo pour récupérer vos dernières factures.
- 💼 **Recherche d'emploi** (`/emplois [mot-clé]`) : Cherche des offres sur les sites luxembourgeois. L'IA peut ensuite rédiger votre lettre de motivation si vous lui fournissez la description du poste.

## Prérequis

1. Python 3.9 ou supérieur.
2. Un bot Telegram (créé via BotFather).
3. Une clé API Google Gemini.
4. Une base de données Odoo (URL, DB, Email, Mot de passe).
5. Des identifiants Google Calendar API (`credentials.json`).

## Installation

1. Clonez ce dépôt.
2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Copiez le fichier `.env.example` et renommez-le en `.env`.
   ```bash
   cp .env.example .env
   ```
4. Remplissez les informations dans le fichier `.env` avec vos propres clés API et chemins de dossiers.
5. Placez votre fichier `credentials.json` (téléchargé depuis Google Cloud Console pour l'API Calendar) dans le dossier `config/`.

## Lancement

Exécutez la commande suivante pour démarrer l'assistant :

```bash
python -m src.bot.main
```

Lors du premier lancement, une fenêtre de navigateur s'ouvrira pour vous demander l'autorisation d'accéder à votre Google Agenda.

## Utilisation

Sur Telegram, envoyez un message à votre bot ou utilisez les commandes :
- `/start` - Afficher le message de bienvenue
- `/agenda` - Voir les événements à venir
- `/fichiers` - Ranger le dossier source
- `/compta` - Voir les factures Odoo
- `/emplois comptable` - Chercher des offres de comptable
