from openai import OpenAI

from logic.utils import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def gpt_generate_response_request(prompt, user_input):
    response = client.responses.create(
        model="gpt-4o",
        instructions=prompt,
        input=user_input,
    )
    return response

def gpt_structured_response_request(prompt, user_input):
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": "Extract the event information."},
            {"role": "user", "content": user_input}
        ],
        text=prompt
    )
    return response