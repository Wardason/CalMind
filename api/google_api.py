import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from logic.scheduling import create_event_from_task
from models.tasks import Task

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def calendar_authorization():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "secrets/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

creds = calendar_authorization()
service = build("calendar", "v3", credentials=creds)

def check_if_event_collision(task: Task) -> bool:
    collision_events = service.events().list(
        calendarId="primary",
        timeMin=task.start_time.date_time.isoformat(),
        timeMax=task.end_time.date_time.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    return len(collision_events["items"]) > 0

def add_event_to_calendar(task: Task):
  event_body = create_event_from_task(task)
  event = service.events().insert(calendarId="primary", body=event_body).execute()
  print("✅ Event erstellt:", event.get("htmlLink"))


