"""Функции для работы с выдачей оборудования."""
from datetime import date


def is_equipment_available(
    equipment: dict[int, dict],
    equipment_id: int,
) -> bool:
    """Проверить, доступно ли оборудование для выдачи."""
    if equipment_id not in equipment:
        return False
    return equipment[equipment_id]["is_available"]


def issue_equipment(
    issuances: list[dict],
    equipment: dict[int, dict],
    equipment_id: int,
    employee: str,
) -> dict:
    """Выдать оборудование сотруднику."""
    if not is_equipment_available(equipment, equipment_id):
        raise ValueError("Оборудование недоступно для выдачи")
    issuance_id = max(
        (item["id"] for item in issuances), default=0
    ) + 1
    issuance = {
        "id": issuance_id,
        "equipment_id": equipment_id,
        "employee": employee,
        "date": str(date.today()),
    }
    issuances.append(issuance)
    equipment[equipment_id]["is_available"] = False
    return issuance


def return_equipment(
    issuances: list[dict],
    equipment: dict[int, dict],
    issuance_id: int,
) -> None:
    """Вернуть оборудование (отмена выдачи)."""
    for item in issuances:
        if item["id"] == issuance_id:
            equipment[item["equipment_id"]]["is_available"] = True
            issuances.remove(item)
            return
    raise ValueError("Выдача с таким id не найдена")


def get_issuance_status(is_available: bool) -> str:
    """Вернуть текстовый статус (функция из ПР1)."""
    if is_available:
        return "Оборудование доступно для выдачи"
    return "Оборудование уже выдано"