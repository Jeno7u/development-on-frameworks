"""Тесты функций выдачи оборудования."""
import pytest
from equipment import add_equipment
from issuance import (
    is_equipment_available,
    issue_equipment,
    return_equipment,
)


def test_is_equipment_available():
    equipment = {}
    eq_id = add_equipment(
        equipment, "Ноутбук HP", 10245, "Рабочее"
    )
    assert is_equipment_available(equipment, eq_id)


def test_issue_equipment_marks_unavailable():
    equipment = {}
    issuances = []
    eq_id = add_equipment(
        equipment, "Ноутбук HP", 10245, "Рабочее"
    )
    issue_equipment(issuances, equipment, eq_id, "Иванов И.И.")
    assert not is_equipment_available(equipment, eq_id)
    assert len(issuances) == 1


def test_double_issue_forbidden():
    equipment = {}
    issuances = []
    eq_id = add_equipment(
        equipment, "Ноутбук HP", 10245, "Рабочее"
    )
    issue_equipment(issuances, equipment, eq_id, "Иванов И.И.")
    with pytest.raises(ValueError):
        issue_equipment(
            issuances, equipment, eq_id, "Петров П.П."
        )


def test_return_equipment():
    equipment = {}
    issuances = []
    eq_id = add_equipment(
        equipment, "Ноутбук HP", 10245, "Рабочее"
    )
    item = issue_equipment(
        issuances, equipment, eq_id, "Иванов И.И."
    )
    return_equipment(issuances, equipment, item["id"])
    assert is_equipment_available(equipment, eq_id)
    assert len(issuances) == 0