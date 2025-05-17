import json
import os

TOGGLE_FILE_PATH = "user_data.json"

def load_toggle_states() -> list[str]:
    if not os.path.exists(TOGGLE_FILE_PATH):
        return []

    try:
        with open(TOGGLE_FILE_PATH, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            return data.get("toggle_selection", [])
    except json.JSONDecodeError:
        return []

def save_toggle_states(toggle_selection: list[str]):
    with open(TOGGLE_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump({"toggle_selection": toggle_selection}, f, ensure_ascii=False, indent=4)
