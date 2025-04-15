from core_logic.api.google_api import add_event_to_calendar, delete_event_from_calendar, colliding_events
from core_logic.logic.task_analysis import interpret_user_input, structured_output_from_user_input, tasks_from_structured_output
from core_logic.models.tasks import Task


def reschedule_assistant():
    pass

def reschedule_manual(reschedule_tasks: list[Task]):
    for reschedule_task in reschedule_tasks:
        new_date: str = input("✏️  Manual mode: Please enter a new date and time for " + reschedule_task.name + ": ")
        input_message: str = ("Task: name: " + reschedule_task.name + "\nDate: " + new_date)
        for task in user_input_to_tasks(input_message):
            task_collision_validation(task)

def handle_reschedule_choice(tasks: list[Task]):
    print(f"📆 Rescheduling for: " + ", ".join(task.name for task in tasks))
    print("⏳ Please choose: enter a new time or let the assistant find one.")
    choice: str = ""
    while choice not in ["manual", "assistant"]:
        choice = input("👉 Type 'manual' or 'assistant': ").strip().lower()
        if choice == 'manual':
            reschedule_manual(tasks)
        elif choice == 'assistant':
            reschedule_assistant()
        else:
            print("❌ Please enter a valid choice (manual or assistant).")

def resolve_scheduling_conflict(new_task: Task, collied_tasks: list[Task]):
    scheduling_conflict_messages(collied_tasks, new_task)
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

def scheduling_conflict_messages(collied_tasks, new_task):
    print("⚠️Error: Event collision conflict detected")
    print(f"1️⃣ Existing events: " + ", ".join(task.name for task in collied_tasks))
    print(f"2️⃣ New task: {new_task.name}")

def task_collision_validation(input_task: Task):
    info_message: str = ""
    if len(colliding_events(input_task)) > 0:
        resolve_scheduling_conflict(input_task, colliding_events(input_task))
    else:
        info_message = add_event_to_calendar(input_task)

    return info_message

def user_input_to_tasks(input_message: str) -> list[Task]:
    interpret_input: str = interpret_user_input(input_message)
    structured_output: dict = structured_output_from_user_input(interpret_input)
    return tasks_from_structured_output(structured_output)