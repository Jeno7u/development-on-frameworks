"""Сохранение и загрузка данных проекта."""
import json
import os

DATA_DIR = "data"
EQUIPMENT_FILE = os.path.join(DATA_DIR, "equipment.json")
ISSUANCES_FILE = os.path.join(DATA_DIR, "issuances.json")


def _ensure_data_dir() -> None:
    """Создать каталог data/, если он отсутствует."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def load_equipment() -> dict[int, dict]:
    """Загрузить оборудование из JSON-файла."""
    if not os.path.exists(EQUIPMENT_FILE):
        return {}
    try:
        with open(EQUIPMENT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {int(k): v for k, v in data.items()}
    except (json.JSONDecodeError, OSError):
        return {}


def save_equipment(equipment: dict[int, dict]) -> None:
    """Сохранить оборудование в JSON-файл."""
    _ensure_data_dir()
    data = {str(k): v for k, v in equipment.items()}
    with open(EQUIPMENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_issuances() -> list[dict]:
    """Загрузить выдачи из JSON-файла."""
    if not os.path.exists(ISSUANCES_FILE):
        return []
    try:
        with open(ISSUANCES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_issuances(issuances: list[dict]) -> None:
    """Сохранить выдачи в JSON-файл."""
    _ensure_data_dir()
    with open(ISSUANCES_FILE, "w", encoding="utf-8") as f:
        json.dump(issuances, f, ensure_ascii=False, indent=2)