"""Класс Issuance и функции работы с выдачами."""
from typing import List, Optional

from .equipment import Equipment, find_equipment_by_id
from .employees import Employee, find_employee_by_id


class Issuance:
    """Выдача оборудования сотруднику."""

    def __init__(
        self,
        issuance_id: int,
        equipment: Equipment,
        employee: Employee,
        issue_date: str,
        is_returned: bool = False,
    ) -> None:
        """Создать объект выдачи."""
        self.id = issuance_id
        self.equipment = equipment
        self.employee = employee
        self.issue_date = issue_date
        self.is_returned = is_returned

    def return_equipment(self) -> None:
        """Вернуть оборудование (изменить состояние выдачи)."""
        if self.is_returned:
            raise ValueError("Выдача уже закрыта")
        self.is_returned = True
        self.equipment.is_available = True

    def __str__(self) -> str:
        """Строковое представление выдачи."""
        state = "возвращено" if self.is_returned else "активно"
        return (
            f"[{self.id}] {self.equipment.name} -> "
            f"{self.employee.name} ({self.issue_date}, {state})"
        )

    @classmethod
    def from_data(
        cls,
        data: dict,
        equipment_list: List[Equipment],
        employees: List[Employee],
    ) -> Optional["Issuance"]:
        """Создать объект Issuance из словаря JSON.

        Возвращает None, если оборудование или сотрудник
        не найдены в соответствующих коллекциях.
        """
        equipment = find_equipment_by_id(
            equipment_list, data["equipment_id"]
        )
        employee = find_employee_by_id(
            employees, data["employee_id"]
        )
        if equipment is None or employee is None:
            return None
        return cls(
            issuance_id=data["id"],
            equipment=equipment,
            employee=employee,
            issue_date=data["issue_date"],
            is_returned=data.get("is_returned", False),
        )


def is_equipment_available(
    equipment: Equipment,
) -> bool:
    """Проверить, доступно ли оборудование для выдачи."""
    return equipment.is_available_for_issue()


def create_issuance(
    issuances: List[Issuance],
    equipment: Equipment,
    employee: Employee,
    issue_date: str,
) -> Optional[Issuance]:
    """Создать выдачу оборудования сотруднику.

    Возвращает объект Issuance при успехе или None,
    если оборудование недоступно.
    """
    if not is_equipment_available(equipment):
        return None
    new_id = max(
        (item.id for item in issuances), default=0
    ) + 1
    issuance = Issuance(
        issuance_id=new_id,
        equipment=equipment,
        employee=employee,
        issue_date=issue_date,
    )
    issuances.append(issuance)
    equipment.is_available = False
    return issuance


def find_issuance_by_id(
    issuances: List[Issuance],
    issuance_id: int,
) -> Optional[Issuance]:
    """Найти выдачу по идентификатору."""
    for item in issuances:
        if item.id == issuance_id:
            return item
    return None


def return_issuance(
    issuances: List[Issuance],
    issuance_id: int,
) -> bool:
    """Вернуть оборудование по идентификатору выдачи.

    Возвращает True при успехе, False если выдача не найдена.
    """
    issuance = find_issuance_by_id(issuances, issuance_id)
    if issuance is None:
        return False
    issuance.return_equipment()
    return True


def get_issuance_status(is_available: bool) -> str:
    """Вернуть текстовый статус (функция из ПР1)."""
    if is_available:
        return "Оборудование доступно для выдачи"
    return "Оборудование уже выдано"


def show_issuances(issuances: List[Issuance]) -> None:
    """Вывести список выдач."""
    if not issuances:
        print("Выдач пока нет.")
        return
    for item in issuances:
        print(item)