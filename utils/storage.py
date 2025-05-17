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

FILE = "toggle_states.json"  # файл, куда сохраняем состояния

def load_toggle_state(name: str) -> list[str]:
    """
    Загружает из файла состояния для группы toggle с именем `name`.
    Если файла нет или что-то пошло не так — возвращает пустой список.
    """
    if not os.path.exists(FILE):
        return []
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get(f"toggle_{name}", [])
    except json.JSONDecodeError:
        return []

def save_toggle_state(name: str, data: list[str]):
    """
    Сохраняет в файл состояния `data` для группы toggle с именем `name`.
    Если файл существует — обновляет данные, не трогая остальное.
    """
    all_data = {}
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                all_data = json.load(f)
        except json.JSONDecodeError:
            all_data = {}

    all_data[f"toggle_{name}"] = data

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)