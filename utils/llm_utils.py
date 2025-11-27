import json
from constants import JSON_FILE

with open(JSON_FILE, "r") as f:
    LLM_DATA = json.load(f)

# gets daily guidance from pre-built json store
def get_daily_guidance(day: str) -> dict:
    """Fetch daily LLM guidance for a given cycle day."""
    return LLM_DATA[day]