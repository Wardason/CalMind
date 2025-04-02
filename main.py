from logic.scheduling import resolve_scheduling_conflict
from logic.task_analysis import interpret_user_input, structured_output_from_user_input, tasks_from_structured_output
from api.google_api import add_event_to_calendar, colliding_events

userMsg: str = input("Enter your task: ")
interpret_user_input: str = interpret_user_input(userMsg)
structured_output: dict = structured_output_from_user_input(interpret_user_input)
tasks = tasks_from_structured_output(structured_output)
for task in tasks:
    if len(colliding_events(task)) > 0:
        resolve_scheduling_conflict(task, colliding_events(task))
    else:
        add_event_to_calendar(task)
