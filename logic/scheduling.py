from models.tasks import Task

def create_event_from_task(task: Task) -> dict:
    event = {
        "summary": task.name,
        "description": task.description,
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