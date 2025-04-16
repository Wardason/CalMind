from collections import defaultdict
from datetime import datetime, timedelta

from core_logic.api.google_api import get_all_events_from_now_to_week, get_events_from_start_of_week
import re

CATEGORY_TAG_PREFIX = "calmind_category:"
DEFAULT_CATEGORY = "Unkategorisiert"

def extract_category_from_event(event: dict) -> str:
    description = event.get("description", "")
    match = re.search(f"{re.escape(CATEGORY_TAG_PREFIX)}(\w+)", description, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    else:
        return DEFAULT_CATEGORY

def parse_datetime_string(datetime_str: str):
    return datetime.fromisoformat(datetime_str)

def calculate_event_duration(start_dt: datetime, end_dt: datetime):
    if start_dt and end_dt:
        return end_dt - start_dt
    return timedelta(0)

def analysing_week() -> dict[str, timedelta]:
    category_durations_td = defaultdict(timedelta)
    events = get_events_from_start_of_week()

    for event in events:
        start_str = event.get('start', {}).get('dateTime')
        end_str = event.get('end', {}).get('dateTime')

        category = extract_category_from_event(event)
        start_dt = parse_datetime_string(start_str)
        end_dt = parse_datetime_string(end_str)
        duration = calculate_event_duration(start_dt, end_dt)
        if duration.total_seconds() >= 0:
            category_durations_td[category] += duration

    return dict(category_durations_td)

def format_timedelta_analysis_to_html(analysis_data: dict[str, timedelta]) -> str:
    output_lines = ["Analyse Zeit pro Kategorie:"]
    total_hours = 0.0

    for category, total_duration in sorted(analysis_data.items()):
        total_seconds = total_duration.total_seconds()

        if total_seconds > 0:
            hours = total_seconds / 3600.0
            output_lines.append(f"- {category.capitalize()}: {hours:.2f} Stunden")
            total_hours += hours
    return "<br>".join(output_lines)