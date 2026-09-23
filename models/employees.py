"""Класс Employee и функции работы с сотрудниками."""
from typing import List, Optional


class Employee:
    """Сотрудник, которому может быть выдано оборудование."""

    def __init__(
        self,
        employee_id: int,
        name: str,
        email: str,
    ) -> None:
        """Создать объект сотрудника."""
        self.id = employee_id
        self.name = name
        self.email = email

    def __str__(self) -> str:
        """Строковое представление сотрудника."""
        return f"[{self.id}] {self.name} <{self.email}>"

    @classmethod
    def from_data(cls, data: dict) -> "Employee":
        """Создать объект Employee из словаря JSON."""
        return cls(
            employee_id=data["id"],
            name=data["name"],
            email=data["email"],
        )


def add_employee(
    employees: List[Employee],
    name: str,
    email: str,
) -> Employee:
    """Создать сотрудника и добавить его в коллекцию."""
    new_id = max(
        (emp.id for emp in employees), default=0
    ) + 1
    employee = Employee(new_id, name, email)
    employees.append(employee)
    return employee


def find_employee(
    employees: List[Employee],
    query: str,
) -> List[Employee]:
    """Найти сотрудников по имени или email."""
    query_lower = query.lower()
    result = []
    for emp in employees:
        if (
            query_lower in emp.name.lower()
            or query_lower in emp.email.lower()
        ):
            result.append(emp)
    return result


def find_employee_by_id(
    employees: List[Employee],
    employee_id: int,
) -> Optional[Employee]:
    """Найти сотрудника по идентификатору."""
    for emp in employees:
        if emp.id == employee_id:
            return emp
    return None


def show_employees(employees: List[Employee]) -> None:
    """Вывести список сотрудников."""
    if not employees:
        print("Список сотрудников пуст.")
        return
    for employee in employees:
        print(employee)
