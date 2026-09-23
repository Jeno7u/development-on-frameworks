"""Класс Equipment и функции работы с оборудованием."""
from typing import List, Optional


class Equipment:
    """Оборудование, учитываемое в системе."""

    def __init__(
        self,
        equipment_id: int,
        name: str,
        inventory_number: int,
        status: str,
        is_available: bool = True,
    ) -> None:
        """Создать объект оборудования."""
        self.id = equipment_id
        self.name = name
        self.inventory_number = inventory_number
        self.status = status
        self.is_available = is_available

    def is_available_for_issue(self) -> bool:
        """Проверить, доступно ли оборудование для выдачи."""
        return self.is_available

    def __str__(self) -> str:
        """Строковое представление оборудования."""
        availability = (
            "доступно" if self.is_available else "выдано"
        )
        return (
            f"[{self.id}] {self.name} "
            f"(инв. № {self.inventory_number}, "
            f"состояние: {self.status}, {availability})"
        )

    @classmethod
    def from_data(cls, data: dict) -> "Equipment":
        """Создать объект Equipment из словаря JSON."""
        return cls(
            equipment_id=data["id"],
            name=data["name"],
            inventory_number=data["inventory_number"],
            status=data["status"],
            is_available=data.get("is_available", True),
        )

    @staticmethod
    def validate_inventory_number(value: int) -> bool:
        """Проверить корректность инвентарного номера."""
        return isinstance(value, int) and value > 0


def add_equipment(
    equipment_list: List[Equipment],
    name: str,
    inventory_number: int,
    status: str,
) -> Equipment:
    """Создать оборудование и добавить его в коллекцию."""
    if not Equipment.validate_inventory_number(inventory_number):
        raise ValueError("Некорректный инвентарный номер")
    new_id = max(
        (eq.id for eq in equipment_list), default=0
    ) + 1
    equipment = Equipment(
        equipment_id=new_id,
        name=name,
        inventory_number=inventory_number,
        status=status,
    )
    equipment_list.append(equipment)
    return equipment


def find_equipment(
    equipment_list: List[Equipment],
    query: str,
) -> List[Equipment]:
    """Найти оборудование по подстроке названия."""
    query_lower = query.lower()
    return [
        eq
        for eq in equipment_list
        if query_lower in eq.name.lower()
    ]


def find_equipment_by_id(
    equipment_list: List[Equipment],
    equipment_id: int,
) -> Optional[Equipment]:
    """Найти оборудование по идентификатору."""
    for eq in equipment_list:
        if eq.id == equipment_id:
            return eq
    return None


def filter_equipment_by_status(
    equipment_list: List[Equipment],
    status: str,
) -> List[Equipment]:
    """Отобрать оборудование по состоянию."""
    status_lower = status.lower()
    return [
        eq
        for eq in equipment_list
        if eq.status.lower() == status_lower
    ]


def sort_equipment(
    equipment_list: List[Equipment],
) -> List[Equipment]:
    """Отсортировать оборудование по названию (lambda)."""
    return sorted(equipment_list, key=lambda eq: eq.name)


def show_equipment(equipment_list: List[Equipment]) -> None:
    """Вывести список оборудования."""
    if not equipment_list:
        print("Список оборудования пуст.")
        return
    for equipment in sort_equipment(equipment_list):
        print(equipment)