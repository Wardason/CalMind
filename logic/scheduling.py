from api.google_api import add_event_to_calendar, delete_event_from_calendar
from models.tasks import Task

def handle_reschedule_choice(tasks: list[Task]):
    print(f"Rescheduling for: " + ", ".join(task.name for task in tasks))
    print("⏳ Please choose: enter a new time or let the assistant find one.")
    choice = input("👉 Type 'manual' or 'assistant': ").strip().lower()

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
            add_event_to_calendar(new_task)
            for task in collied_tasks:
                delete_event_from_calendar(task)
            handle_reschedule_choice(collied_tasks)
        else:
            print("❌ Please enter a valid choice (1 or 2).")