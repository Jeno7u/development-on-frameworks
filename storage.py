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


def load_equipment() -> List[Equipment]:
    """Загрузить оборудование из JSON в объекты Equipment."""
    if not os.path.exists(EQUIPMENT_FILE):
        return []
    try:
        with open(EQUIPMENT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Equipment.from_data(item) for item in data]
    except (json.JSONDecodeError, OSError, KeyError):
        return []


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
    if not os.path.exists(EMPLOYEES_FILE):
        return []
    try:
        with open(EMPLOYEES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Employee.from_data(item) for item in data]
    except (json.JSONDecodeError, OSError, KeyError):
        return []


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
    """Загрузить выдачи из JSON, восстановив связи объектов."""
    if not os.path.exists(ISSUANCES_FILE):
        return []
    try:
        with open(ISSUANCES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []

    result: List[Issuance] = []
    for item in data:
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