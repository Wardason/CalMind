import json
from datetime import datetime
import pytz
from logic import utils
from models.tasks import Task, TimeInfo
from openai import OpenAI
from logic.utils import OPENAI_API_KEY

def interpret_user_input(user_input: str) -> str:
    tz = pytz.timezone("Europe/Berlin")
    now = datetime.now(tz).isoformat()
    prompt: str = utils.interpret_prompt.replace("{{DATETIME_NOW}}", now).replace("{{TIMEZONE}}", tz.zone)

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(
        model="gpt-4o",
        instructions=prompt,
        input=user_input,
    )
    return response.output_text

def structured_output_from_user_input(user_input: str) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": user_input}
    ],
        text=utils.structured_output_instructions_prompt
)
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
                priority=task_dict["priority"],
                description=task_dict["description"],
                attendees=task_dict["attendees"]
            )
            task_list.append(task)
        return task_list