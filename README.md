# Assistant Personnel (Telegram Bot)

Ce projet est un assistant personnel intelligent fonctionnant via Telegram. Il est conçu pour vous aider dans vos tâches quotidiennes, gérer vos fichiers locaux, votre comptabilité et vos recherches d'emploi au Luxembourg.

Il utilise l'IA de Google (Gemini) pour comprendre vos demandes et générer du texte (ex: lettres de motivation).

## Fonctionnalités principales

- 🤖 **Intelligence Artificielle (Gemini)** : Discutez naturellement avec l'assistant, il comprendra vos intentions.
- 📅 **Agenda** (`/agenda`) : Consultez vos prochains événements et formations stockés localement.
- 📁 **Gestionnaire de fichiers** (`/fichiers`) : Trie automatiquement le contenu d'un dossier (ex: Téléchargements) vers des dossiers organisés (Images, PDF, Comptabilité, etc.).
- 💶 **Comptabilité** (`/compta`) : Gère vos dépenses et factures via un fichier local.
- 💼 **Recherche d'emploi** (`/emplois [mot-clé]`) : Cherche des offres sur les sites luxembourgeois. L'IA peut ensuite rédiger votre lettre de motivation si vous lui fournissez la description du poste.

## Prérequis

1. Python 3.9 ou supérieur.
2. Un bot Telegram (créé via BotFather).
3. Une clé API Google Gemini.
4. L'ID de votre utilisateur Telegram (`ALLOWED_USER_ID`) pour restreindre l'accès au bot.

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
4. Remplissez les informations dans le fichier `.env` avec vos propres clés API, l'ID utilisateur et chemins de dossiers.

## Lancement

Exécutez la commande suivante pour démarrer l'assistant :

```bash
python -m src.bot.main
```

## Utilisation

Sur Telegram, envoyez un message à votre bot ou utilisez les commandes :
- `/start` - Afficher le message de bienvenue
- `/agenda` - Voir les événements à venir
- `/fichiers` - Ranger le dossier source
- `/compta` - Voir vos opérations comptables
- `/emplois comptable` - Chercher des offres de comptable
