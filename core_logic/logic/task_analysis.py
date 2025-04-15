import json
from datetime import datetime
import pytz

from core_logic.api.openai_api import gpt_generate_response_request, gpt_structured_response_request
from core_logic.logic.utils import structured_output_instructions_prompt, interpret_prompt
from core_logic.models.tasks import Task, TimeInfo

def interpret_user_input(user_input: str) -> str:
    tz = pytz.timezone("Europe/Berlin")
    now = datetime.now(tz).isoformat()

    prompt: str = interpret_prompt.replace("{{DATETIME_NOW}}", now).replace("{{TIMEZONE}}", tz.zone)
    response = gpt_generate_response_request(prompt, user_input)
    return response.output_text

def structured_output_from_user_input(user_input: str) -> dict:
    response = gpt_structured_response_request(structured_output_instructions_prompt, user_input)
    tasks = json.loads(response.output_text)
    return tasks

def tasks_from_structured_output(data: dict) -> list[Task]:
        task_list = []
        for task_dict in data["tasks"]:
            start = task_dict["start_time"]
            end = task_dict["end_time"]

            task = Task(
                name=task_dict["name"],
                start_time=TimeInfo(
                    date_time=datetime.fromisoformat(start["date_time"]),
                    time_zone=start["time_zone"]
                ),
                end_time=TimeInfo(
                    date_time=datetime.fromisoformat(end["date_time"]),
                    time_zone=end["time_zone"]
                ),
                duration=task_dict["duration"],
                priority=task_dict["priority"],
                description=task_dict["description"],
                attendees=task_dict["attendees"]
            )
            task_list.append(task)
        return task_list
