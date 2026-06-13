import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class CalendarService:
    def __init__(self):
        self.creds = None
        self.creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "config/credentials.json")
        self.token_path = "config/token.json"

    def authenticate(self):
        """Authenticates the user with Google Calendar API."""
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception:
                    pass

            if not self.creds or not self.creds.valid:
                if not os.path.exists(self.creds_path):
                    return False, f"Le fichier {self.creds_path} est introuvable. Veuillez le télécharger depuis Google Cloud Console."
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(self.creds_path, SCOPES)
                    # For a bot running on a server, you might need console flow or out of band
                    # For local usage, run_local_server is fine
                    self.creds = flow.run_local_server(port=0)
                except Exception as e:
                    return False, f"Erreur d'authentification: {e}"

            # Save the credentials for the next run
            with open(self.token_path, 'w') as token:
                token.write(self.creds.to_json())

        return True, "Authentification réussie"

    def get_upcoming_events(self, max_results=5):
        """Prints the start and name of the next max_results events on the user's calendar."""
        success, msg = self.authenticate()
        if not success:
            return msg

        try:
            service = build('calendar', 'v3', credentials=self.creds)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = service.events().list(
                calendarId='primary', timeMin=now,
                maxResults=max_results, singleEvents=True,
                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                return "Vous n'avez aucun événement à venir."

            result = "Vos prochains événements :\n"
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                # Format the date nicely (very simplified here)
                result += f"📅 {start[:10]} {start[11:16]} - {event['summary']}\n"

            return result

        except Exception as e:
            return f"Une erreur s'est produite avec l'agenda: {e}"

    def add_event(self, summary, start_time, end_time=None, description=""):
        """Add a simple event to the calendar."""
        success, msg = self.authenticate()
        if not success:
            return msg

        try:
            service = build('calendar', 'v3', credentials=self.creds)

            # If no end time, assume it lasts 1 hour
            if not end_time:
                start_dt = datetime.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                end_time = (start_dt + datetime.timedelta(hours=1)).isoformat().replace('+00:00', 'Z')

            event = {
                'summary': summary,
                'description': description,
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'Europe/Luxembourg',
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'Europe/Luxembourg',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 30},
                    ],
                },
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            return f"Événement créé : {event.get('htmlLink')}"

        except Exception as e:
            return f"Erreur lors de la création de l'événement: {e}"

calendar = CalendarService()
