from dotenv import load_dotenv
import os

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
- **Dauer der Aufgabe**: ...
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
                                "duration": {"type": "integer"},
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
                                "duration",
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

smart_assistant_prompt  = """
Du bist ein intelligenter Planungsassistent. Ich werde dir gleich:
- eine Liste an Aufgaben übergeben,
- die bereits belegten Zeitfenster meines Kalenders (im ISO-Format),
- sowie meine persönlichen Planungsregeln.

Bitte plane jede Aufgabe sinnvoll in meinem Kalender ein. Niemals darf die übergebne Aufgabe einen schon 
gebuchten Zeitslot überschneiden, dann suche lieber nach einem neuen freien Slot auch wenn dieser in weiter 
Zukunft liegt.
---

📋 **Aufgaben:**  
🗓️ **Belegte Zeitfenster (nicht verfügbar):**  
📌 **Planungsregeln:**  
---

🎯 **Deine Aufgabe für jede Task:**
1. **Dauer abschätzen**, falls keine genannt ist.
2. **Kategorie zuordnen**: entweder `work`, `social` oder `health`.
3. **Einen passenden freien Termin finden**, der:
   - sich **nicht mit belegten Slots überschneidet**
   - **meine Planungsregeln** berücksichtigt
4. **Antwort im folgenden Format zurückgeben (eine Zeile pro Aufgabe):**
<Emoji> <Category>: <Task text> on <YYYY-MM-DD>THH:MM for <Dauer in Minuten> minutes.
"""

user_rules = """
    Bitte keine Arbeitstermine vor 8 Uhr morgens und nach 18 Uhr abends.
    Ich mache zwischen 12 und 13 Uhr Mittagspause – dort keine Aufgaben einplanen.
    Sonntags möchte ich komplett frei haben.
    Zwischen zwei Aufgaben sollte mindestens 30 Minuten Pause sein.
    Wenn möglich, plane Fokus-Aufgaben am liebsten vormittags zwischen 9 und 12 Uhr oder nachmittags zwischen 14 und 16 Uhr.
    Ich möchte nicht mehr als 5 Aufgaben pro Tag einplanen.
    Vermeide es, Aufgaben direkt hintereinander zu legen – etwas Abstand ist mir wichtig.
    Ich fange ungern vor 8:30 Uhr mit konzentrierten Aufgaben an.
    Spätestens um 17:30 Uhr möchte ich mit allem durch sein.
    """