"""Тесты класса Issuance и функций работы с выдачами."""
import pytest

from models import Equipment, Employee, Issuance
from models.issuances import (
    create_issuance,
    is_equipment_available,
    return_issuance,
    find_issuance_by_id,
)


def _make_equipment() -> Equipment:
    return Equipment(1, "Ноутбук HP", 10245, "Рабочее")


def _make_employee() -> Employee:
    return Employee(1, "Иванов Иван", "ivan@example.com")


def test_issuance_creation():
    eq = _make_equipment()
    emp = _make_employee()
    issuance = Issuance(1, eq, emp, "2026-09-15")
    assert issuance.id == 1
    assert issuance.equipment is eq
    assert issuance.employee is emp
    assert issuance.issue_date == "2026-09-15"
    assert issuance.is_returned is False


def test_issuance_str():
    eq = _make_equipment()
    emp = _make_employee()
    issuance = Issuance(1, eq, emp, "2026-09-15")
    text = str(issuance)
    assert "Ноутбук HP" in text
    assert "Иванов Иван" in text
    assert "активно" in text


def test_create_issuance_marks_unavailable():
    eq = _make_equipment()
    emp = _make_employee()
    issuances = []
    issuance = create_issuance(
        issuances, eq, emp, "2026-09-15"
    )
    assert issuance is not None
    assert not is_equipment_available(eq)
    assert len(issuances) == 1


def test_double_issuance_forbidden():
    eq = _make_equipment()
    emp = _make_employee()
    issuances = []
    create_issuance(issuances, eq, emp, "2026-09-15")
    second = create_issuance(issuances, eq, emp, "2026-09-16")
    assert second is None
    assert len(issuances) == 1


def test_return_equipment():
    eq = _make_equipment()
    emp = _make_employee()
    issuances = []
    issuance = create_issuance(issuances, eq, emp, "2026-09-15")
    assert issuance is not None
    assert return_issuance(issuances, issuance.id)
    assert is_equipment_available(eq)
    assert issuance.is_returned is True


def test_double_return_forbidden():
    eq = _make_equipment()
    emp = _make_employee()
    issuances = []
    issuance = create_issuance(issuances, eq, emp, "2026-09-15")
    assert issuance is not None
    return_issuance(issuances, issuance.id)
    with pytest.raises(ValueError):
        issuance.return_equipment()


def test_issuance_from_data():
    eq = _make_equipment()
    emp = _make_employee()
    equipment_list = [eq]
    employees = [emp]
    data = {
        "id": 1,
        "equipment_id": 1,
        "employee_id": 1,
        "issue_date": "2026-09-15",
        "is_returned": False,
    }
    issuance = Issuance.from_data(data, equipment_list, employees)
    assert issuance is not None
    assert issuance.equipment is eq
    assert issuance.employee is emp


def test_issuance_from_data_missing_links():
    data = {
        "id": 1,
        "equipment_id": 99,
        "employee_id": 99,
        "issue_date": "2026-09-15",
        "is_returned": False,
    }
    issuance = Issuance.from_data(data, [], [])
    assert issuance is None


def test_find_issuance_by_id():
    eq = _make_equipment()
    emp = _make_employee()
    issuances = []
    issuance = create_issuance(issuances, eq, emp, "2026-09-15")
    assert issuance is not None
    assert find_issuance_by_id(issuances, issuance.id) is issuance
    assert find_issuance_by_id(issuances, 999) is None