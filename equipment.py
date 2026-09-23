"""Функции для работы с оборудованием."""


def add_equipment(
    equipment: dict[int, dict],
    name: str,
    inventory_number: int,
    status: str,
) -> int:
    """Добавить оборудование в словарь equipment.

    Возвращает идентификатор добавленного оборудования.
    """
    equipment_id = max(equipment.keys(), default=0) + 1
    equipment[equipment_id] = {
        "name": name,
        "inventory_number": inventory_number,
        "status": status,
        "is_available": True,
    }
    return equipment_id


def find_equipment(
    equipment: dict[int, dict],
    query: str,
) -> list[int]:
    """Найти оборудование по подстроке названия."""
    query_lower = query.lower()
    result = []
    for eq_id, eq_data in equipment.items():
        if query_lower in eq_data["name"].lower():
            result.append(eq_id)
    return result


def filter_equipment_by_status(
    equipment: dict[int, dict],
    status: str,
) -> list[int]:
    """Отобрать оборудование по состоянию."""
    result = []
    for eq_id, eq_data in equipment.items():
        if eq_data["status"].lower() == status.lower():
            result.append(eq_id)
    return result


def sort_equipment(
    equipment: dict[int, dict],
) -> list[int]:
    """Отсортировать оборудование по названию (lambda)."""
    return sorted(
        equipment.keys(),
        key=lambda eq_id: equipment[eq_id]["name"],
    )


def get_equipment_info(
    equipment: dict[int, dict],
    equipment_id: int,
) -> str:
    """Сформировать карточку оборудования (функция из ПР1)."""
    eq = equipment[equipment_id]
    return (
        f"Оборудование: {eq['name']} | "
        f"Инв. №: {eq['inventory_number']} | "
        f"Состояние: {eq['status']}"
    )