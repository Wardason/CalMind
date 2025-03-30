from dotenv import load_dotenv
import os
from openai.types.responses import ResponseTextConfigParam#


load_dotenv()
OPENAI_API_KEY = os.getenv("OPEN_AI_APY_KEY")


interpret_prompt: str = """Du bist ein intelligenter Planungsassistent. Der Benutzer gibt dir natürliche Sprache ein, z. B.:
- "Ich treffe mich morgen um 18 Uhr mit Ben."
- "Ich muss nächste Woche eine Präsentation vorbereiten."
- "Heute Abend will ich ins Fitnessstudio."

Deine Aufgabe ist es, aus diesem Text alle relevanten Informationen zu extrahieren und in klar strukturierter, verständlicher Sprache zusammenzufassen.

⚠️ Beachte dabei:

1. **Relative Zeitangaben** wie "morgen", "nächste Woche", "heute Abend" müssen in **konkrete Datum-Zeit-Angaben** umgerechnet werden.
2. **Verwende das heutige Datum**: {{DATETIME_NOW}}  
3. **Verwende diese Standard-Zeitzone**, falls keine angegeben ist: {{TIMEZONE}}
4. **Wenn kein Name für die Aufgabe/Event genannt wird**, wähle einen sinnvollen und passenden Namen.
5. Extrahiere:
   - Name des Events
   - Startzeit & Endzeit
   - Zeitzone
   - Priorität (wenn nicht gegeben, dann als default wert 1)
   - Beschreibung (optional)
   - Teilnehmer (falls Namen oder E-Mail-Adressen genannt werden)

🧾 Ausgabeformat (aber noch KEIN JSON!):

- **Event-Name**: ...
- **Startzeit**: ... (ISO-Format)
- **Endzeit**: ... (ISO-Format)
- **Zeitzone**: ...
- **Priorität**: ... (z. B. 1–3 oder leer)
- **Beschreibung**: ...
- **Teilnehmer**: name1@example.com, name2@example.com

Wenn der Benutzer mehrere Aufgaben beschreibt, gib sie als **fortlaufende Liste** mit Bulletpoints aus.
"""

structured_output_instructions_prompt: dict = {
        "format": {
            "type": "json_schema",
            "name": "task_list",
            "schema": {
                "type": "object",
                "properties": {
                    "tasks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "start_time": {
                                    "type": "object",
                                    "properties": {
                                        "date_time": {"type": "string"},
                                        "time_zone": {"type": "string"}
                                    },
                                    "required": ["date_time", "time_zone"],
                                    "additionalProperties": False
                                },
                                "end_time": {
                                    "type": "object",
                                    "properties": {
                                        "date_time": {"type": "string"},
                                        "time_zone": {"type": "string"}
                                    },
                                    "required": ["date_time", "time_zone"],
                                    "additionalProperties": False
                                },
                                "priority": {"type": "integer"},
                                "description": {"type": "string"},
                                "attendees": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            },
                            "required": [
                                "name",
                                "start_time",
                                "end_time",
                                "priority",
                                "description",
                                "attendees"
                            ],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["tasks"],
                "additionalProperties": False
            },
            "strict": True
        }
    }