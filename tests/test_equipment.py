"""Тесты класса Equipment и функций работы с оборудованием."""
from models import Equipment
from models.equipment import (
    add_equipment,
    find_equipment,
    filter_equipment_by_status,
    sort_equipment,
)


def test_equipment_creation():
    eq = Equipment(1, "Ноутбук HP", 10245, "Рабочее")
    assert eq.id == 1
    assert eq.name == "Ноутбук HP"
    assert eq.inventory_number == 10245
    assert eq.status == "Рабочее"
    assert eq.is_available is True


def test_equipment_is_available_for_issue():
    eq = Equipment(1, "Ноутбук HP", 10245, "Рабочее")
    assert eq.is_available_for_issue()
    eq.is_available = False
    assert not eq.is_available_for_issue()


def test_equipment_str():
    eq = Equipment(1, "Ноутбук HP", 10245, "Рабочее")
    assert "Ноутбук HP" in str(eq)
    assert "10245" in str(eq)


def test_equipment_from_data():
    data = {
        "id": 1,
        "name": "Ноутбук HP",
        "inventory_number": 10245,
        "status": "Рабочее",
        "is_available": True,
    }
    eq = Equipment.from_data(data)
    assert eq.id == 1
    assert eq.name == "Ноутбук HP"


def test_validate_inventory_number():
    assert Equipment.validate_inventory_number(100)
    assert not Equipment.validate_inventory_number(-5)


def test_add_equipment():
    equipment = []
    eq = add_equipment(equipment, "Ноутбук HP", 10245, "Рабочее")
    assert isinstance(eq, Equipment)
    assert eq.id == 1
    assert len(equipment) == 1


def test_find_equipment():
    equipment = []
    add_equipment(equipment, "Ноутбук HP", 10245, "Рабочее")
    add_equipment(equipment, "Монитор Dell", 10246, "Рабочее")
    found = find_equipment(equipment, "ноутбук")
    assert len(found) == 1
    assert found[0].name == "Ноутбук HP"


def test_filter_equipment_by_status():
    equipment = []
    add_equipment(equipment, "Ноутбук HP", 10245, "Рабочее")
    add_equipment(equipment, "Принтер", 10246, "Ремонт")
    found = filter_equipment_by_status(equipment, "Ремонт")
    assert len(found) == 1
    assert found[0].name == "Принтер"


def test_sort_equipment():
    equipment = []
    add_equipment(equipment, "Ноутбук HP", 10245, "Рабочее")
    add_equipment(equipment, "Монитор Dell", 10246, "Рабочее")
    sorted_eq = sort_equipment(equipment)
    assert sorted_eq[0].name == "Монитор Dell"
    assert sorted_eq[1].name == "Ноутбук HP"