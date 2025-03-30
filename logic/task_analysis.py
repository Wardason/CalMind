"""Handles the filtering for tasks form msg"""
import json
from datetime import datetime

import pytz

import utils
from models.tasks import Task
from openai import OpenAI
from utils import OPENAI_API_KEY

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

def task_from_user_input(user_input: str) -> str:
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
