import os
import json
from datetime import datetime

class CalendarService:
    def __init__(self):
        self.data_file = "data/agenda.json"
        # Ensure data dir exists
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)

        # Create file if not exists
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump({"events": []}, f)

    def get_upcoming_events(self, max_results=5):
        """Get events from local JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            events = data.get("events", [])

            if not events:
                return "Vous n'avez aucun événement à venir dans votre agenda local."

            result = "Vos prochains événements :\n"
            for event in events[-max_results:]:
                result += f"📅 {event['date']} - {event['title']}\n"

            return result

        except Exception as e:
            return f"Une erreur s'est produite avec l'agenda: {e}"

    def add_event(self, title, date_str):
        """Add an event to local JSON file"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            data["events"].append({
                "title": title,
                "date": date_str,
                "added_on": datetime.now().isoformat()
            })

            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            return f"Événement créé avec succès : {title} le {date_str}"

        except Exception as e:
            return f"Erreur lors de la création de l'événement: {e}"

calendar = CalendarService()
