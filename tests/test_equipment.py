"""Тесты функций работы с оборудованием."""
from equipment import (
    add_equipment,
    find_equipment,
    filter_equipment_by_status,
    get_equipment_info,
)


def test_add_equipment():
    equipment = {}
    eq_id = add_equipment(
        equipment, "Ноутбук HP", 10245, "Рабочее"
    )
    assert eq_id == 1
    assert len(equipment) == 1


def test_find_equipment():
    equipment = {}
    add_equipment(equipment, "Ноутбук HP", 10245, "Рабочее")
    add_equipment(equipment, "Монитор Dell", 10246, "Рабочее")
    found = find_equipment(equipment, "ноутбук")
    assert len(found) == 1


def test_filter_equipment_by_status():
    equipment = {}
    add_equipment(equipment, "Ноутбук HP", 10245, "Рабочее")
    add_equipment(equipment, "Принтер", 10246, "Ремонт")
    found = filter_equipment_by_status(equipment, "Ремонт")
    assert len(found) == 1


def test_get_equipment_info():
    equipment = {}
    eq_id = add_equipment(
        equipment, "Ноутбук HP", 10245, "Рабочее"
    )
    info = get_equipment_info(equipment, eq_id)
    assert "Ноутбук HP" in info