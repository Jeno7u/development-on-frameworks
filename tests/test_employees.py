"""Тесты класса Employee и функций работы с сотрудниками."""
from models import Employee
from models.employees import (
    add_employee,
    find_employee,
    find_employee_by_id,
)


def test_employee_creation():
    emp = Employee(1, "Иванов Иван", "ivan@example.com")
    assert emp.id == 1
    assert emp.name == "Иванов Иван"
    assert emp.email == "ivan@example.com"


def test_employee_str():
    emp = Employee(1, "Иванов Иван", "ivan@example.com")
    assert "Иванов Иван" in str(emp)
    assert "ivan@example.com" in str(emp)


def test_employee_from_data():
    data = {
        "id": 1,
        "name": "Иванов Иван",
        "email": "ivan@example.com",
    }
    emp = Employee.from_data(data)
    assert emp.id == 1
    assert emp.name == "Иванов Иван"


def test_add_employee():
    employees = []
    emp = add_employee(employees, "Иванов Иван", "ivan@example.com")
    assert isinstance(emp, Employee)
    assert emp.id == 1
    assert len(employees) == 1


def test_find_employee_by_name():
    employees = []
    add_employee(employees, "Иванов Иван", "ivan@example.com")
    add_employee(employees, "Петров Петр", "petr@example.com")
    found = find_employee(employees, "иванов")
    assert len(found) == 1
    assert found[0].name == "Иванов Иван"


def test_find_employee_by_id():
    employees = []
    add_employee(employees, "Иванов Иван", "ivan@example.com")
    emp = find_employee_by_id(employees, 1)
    assert emp is not None
    assert emp.name == "Иванов Иван"
    assert find_employee_by_id(employees, 999) is None
