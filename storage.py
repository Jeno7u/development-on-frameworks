"""Сохранение и загрузка данных проекта (JSON <-> объекты)."""
import json
import os
from typing import List

from models import Equipment, Employee, Issuance

DATA_DIR = "data"
EQUIPMENT_FILE = os.path.join(DATA_DIR, "equipment.json")
EMPLOYEES_FILE = os.path.join(DATA_DIR, "employees.json")
ISSUANCES_FILE = os.path.join(DATA_DIR, "issuances.json")


def _ensure_data_dir() -> None:
    """Создать каталог data/, если он отсутствует."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def _read_json(path: str):
    """Прочитать JSON-файл, вернуть None при ошибке."""
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def load_equipment() -> List[Equipment]:
    """Загрузить оборудование из JSON в объекты Equipment.

    Поддерживает оба формата: список (ПР3) и словарь (ПР2).
    """
    raw = _read_json(EQUIPMENT_FILE)
    if raw is None:
        return []

    if isinstance(raw, dict):
        items = list(raw.values())
    elif isinstance(raw, list):
        items = raw
    else:
        return []

    result: List[Equipment] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            result.append(Equipment.from_data(item))
        except (KeyError, TypeError):
            continue
    return result


def save_equipment(equipment_list: List[Equipment]) -> None:
    """Сохранить объекты Equipment в JSON."""
    _ensure_data_dir()
    data = [
        {
            "id": eq.id,
            "name": eq.name,
            "inventory_number": eq.inventory_number,
            "status": eq.status,
            "is_available": eq.is_available,
        }
        for eq in equipment_list
    ]
    with open(EQUIPMENT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_employees() -> List[Employee]:
    """Загрузить сотрудников из JSON в объекты Employee."""
    raw = _read_json(EMPLOYEES_FILE)
    if raw is None:
        return []

    if isinstance(raw, dict):
        items = list(raw.values())
    elif isinstance(raw, list):
        items = raw
    else:
        return []

    result: List[Employee] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            result.append(Employee.from_data(item))
        except (KeyError, TypeError):
            continue
    return result


def save_employees(employees: List[Employee]) -> None:
    """Сохранить объекты Employee в JSON."""
    _ensure_data_dir()
    data = [
        {
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
        }
        for emp in employees
    ]
    with open(EMPLOYEES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_issuances(
    equipment_list: List[Equipment],
    employees: List[Employee],
) -> List[Issuance]:
    """Загрузить выдачи из JSON, восстановив связи объектов.

    Поддерживает форматы ПР2 (employee, date) и ПР3
    (employee_id, issue_date).
    """
    raw = _read_json(ISSUANCES_FILE)
    if raw is None:
        return []

    if isinstance(raw, dict):
        items = list(raw.values())
    elif isinstance(raw, list):
        items = raw
    else:
        return []

    result: List[Issuance] = []
    for item in items:
        if not isinstance(item, dict):
            continue

        # Нормализация полей ПР2 -> ПР3
        if "employee_id" not in item and "employee" in item:
            # В ПР2 "employee" — это ФИО, ищем по имени
            employee_name = item.get("employee")
            matched = None
            for emp in employees:
                if emp.name == employee_name:
                    matched = emp
                    break
            if matched is None:
                continue
            item["employee_id"] = matched.id

        if "issue_date" not in item and "date" in item:
            item["issue_date"] = item["date"]

        issuance = Issuance.from_data(
            item, equipment_list, employees
        )
        if issuance is not None:
            result.append(issuance)
    return result


def save_issuances(issuances: List[Issuance]) -> None:
    """Сохранить объекты Issuance в JSON (только id связей)."""
    _ensure_data_dir()
    data = [
        {
            "id": item.id,
            "equipment_id": item.equipment.id,
            "employee_id": item.employee.id,
            "issue_date": item.issue_date,
            "is_returned": item.is_returned,
        }
        for item in issuances
    ]
    with open(ISSUANCES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
