from core_logic.api.google_api import get_all_events_from_now_to_week
from core_logic.api.openai_api import gpt_generate_response_request
from core_logic.logic.settings import get_user_rules
from core_logic.logic.utils import smart_assistant_prompt, user_rules


def extract_event_times(events: list[dict]) -> list[tuple[str, str]]:
    slots = []
    for event in events:
        start = event.get("start", {}).get("dateTime")
        end = event.get("end", {}).get("dateTime")
        if start and end:
            slots.append((start, end))
    return slots


def find_available_time_slot(user_task: str):
    print(get_user_rules())
    already_used_event_slots = extract_event_times(get_all_events_from_now_to_week())
    #TODO: function which interprets the get_user_rules to full sentences
    prompt = f"{smart_assistant_prompt}; aufgaben: {user_task}; belegte zeitfenster: {already_used_event_slots}; user rules: {get_user_rules()}"
    response = gpt_generate_response_request(prompt, user_task)
    return response.output_text