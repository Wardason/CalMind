import os.path
from datetime import timezone, datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from core_logic.models.tasks import Task, TimeInfo

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

def colliding_events(task) -> list[Task]:
    colliding_tasks: list[Task] = []
    start = task.start_time.date_time
    end = task.end_time.date_time

    end, start = formatting_timezone(end, start)

    collision_events_results = service.events().list(
        calendarId="primary",
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    collision_events = collision_events_results.get("items", [])
    for event in collision_events:
        new_task = Task(
            name=event["summary"],
            calendar_event_id=event["id"],
            start_time=TimeInfo(event["start"]["dateTime"], event["start"]["timeZone"]),
            end_time=TimeInfo(event["end"]["dateTime"], event["end"]["timeZone"]))
        colliding_tasks.append(new_task)
    return colliding_tasks

def formatting_timezone(end, start):
    if start.tzinfo is None:
        start = start.replace(tzinfo=timezone.utc)
    if end.tzinfo is None:
        end = end.replace(tzinfo=timezone.utc)
    return end, start

def add_event_to_calendar(task: Task):
  event_body = create_event_from_task(task)
  event = service.events().insert(calendarId="primary", body=event_body).execute()
  task.calendar_event_id = event.get("id")
  dt_object = task.start_time.date_time
  formatted_time = dt_object.strftime("%H:%M Uhr am %d.%m")
  return f"✅ {task.name} erstellt, für {formatted_time}\n"

def delete_event_from_calendar(task: Task):
    service.events().delete(calendarId='primary', eventId=task.calendar_event_id).execute()

def get_all_events_from_current_week():
    now = datetime.now(tz=timezone.utc)
    one_week_later = now + timedelta(days=7)
    event_results = service.events().list(
        calendarId="primary",
        timeMin=now.isoformat(),
        timeMax=one_week_later.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()
    return event_results.get("items", [])

def create_event_from_task(task: Task) -> dict:
    event = {
        "summary": task.name,
        "description": task.tag,
        "start": {
            "dateTime": task.start_time.date_time.isoformat(),
            "timeZone": task.start_time.time_zone,
        },
        "end": {
            "dateTime": task.end_time.date_time.isoformat(),
            "timeZone": task.end_time.time_zone,
        },
        #"attendees": [{"email": email} for email in task.attendees],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup", "minutes": 10}
            ],
        }
    }
    return event