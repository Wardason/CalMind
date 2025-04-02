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


def handle_reschedule_choice(tasks: list[Task]):
    for task in tasks:
        print("ima reseduling the " + task.name)


def resolve_scheduling_conflict(new_task: Task, collied_tasks: list[Task]):
    print("⚠️Error: Event collision conflict detected")
    print(f"1️⃣ Existing events: " + ", ".join(task.name for task in collied_tasks))
    print(f"2️⃣ New task: {new_task.name}")
    user_decision: str = ""

    while user_decision not in ["1", "2"]:
        user_decision = input("Which of these should be scheduled at the current time? (1️⃣ or 2️⃣): ")
        if user_decision == "1":
            handle_reschedule_choice([new_task])
        elif user_decision == "2":
            handle_reschedule_choice(collied_tasks)
        else:
            print("❌ Please enter a valid choice (1 or 2).")