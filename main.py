"""Точка запуска приложения учета рабочего оборудования."""
from typing import List

from models import Equipment, Employee, Issuance
from models.equipment import (
    add_equipment,
    find_equipment,
    find_equipment_by_id,
    filter_equipment_by_status,
    show_equipment,
)
from models.employees import (
    add_employee,
    find_employee,
    find_employee_by_id,
    show_employees,
)
from models.issuances import (
    create_issuance,
    find_issuance_by_id,
    get_issuance_status,
    is_equipment_available,
    return_issuance,
    show_issuances,
)
from storage import (
    load_equipment,
    load_employees,
    load_issuances,
    save_equipment,
    save_employees,
    save_issuances,
)
from utils import input_int, input_str


def print_menu() -> None:
    """Напечатать меню приложения."""
    print("\n=== Система учета рабочего оборудования ===")
    print("1. Показать оборудование")
    print("2. Добавить оборудование")
    print("3. Найти оборудование по названию")
    print("4. Фильтр оборудования по состоянию")
    print("5. Показать сотрудников")
    print("6. Добавить сотрудника")
    print("7. Проверить доступность оборудования")
    print("8. Выдать оборудование")
    print("9. Вернуть оборудование")
    print("10. Показать выдачи")
    print("0. Выход")


def create_new_issuance(
    issuances: List[Issuance],
    equipment_list: List[Equipment],
    employees: List[Employee],
) -> None:
    """Создать новую выдачу через взаимодействие объектов."""
    eq_id = input_int("ID оборудования: ")
    equipment = find_equipment_by_id(equipment_list, eq_id)
    if equipment is None:
        print("Оборудование с таким ID не найдено.")
        return

    emp_id = input_int("ID сотрудника: ")
    employee = find_employee_by_id(employees, emp_id)
    if employee is None:
        print("Сотрудник с таким ID не найден.")
        return

    issue_date = input_str("Дата выдачи (ГГГГ-ММ-ДД): ")

    if not is_equipment_available(equipment):
        print("Оборудование уже выдано.")
        return

    issuance = create_issuance(
        issuances, equipment, employee, issue_date
    )
    if issuance is None:
        print("Не удалось создать выдачу.")
    else:
        print(f"Выдача №{issuance.id} оформлена.")


def handle_return(
    issuances: List[Issuance],
) -> None:
    """Вернуть оборудование по ID выдачи."""
    issuance_id = input_int("ID выдачи: ")
    issuance = find_issuance_by_id(issuances, issuance_id)
    if issuance is None:
        print("Выдача с таким ID не найдена.")
        return
    if issuance.is_returned:
        print("Эта выдача уже закрыта.")
        return
    if return_issuance(issuances, issuance_id):
        print("Оборудование возвращено.")
    else:
        print("Не удалось вернуть оборудование.")


def main() -> None:
    """Точка запуска приложения."""
    equipment_list = load_equipment()
    employees = load_employees()
    issuances = load_issuances(equipment_list, employees)

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        try:
            if choice == "1":
                show_equipment(equipment_list)

            elif choice == "2":
                name = input_str("Название: ")
                inv = input_int("Инвентарный номер: ")
                status = input_str("Состояние: ")
                equipment = add_equipment(
                    equipment_list, name, inv, status
                )
                print(f"Добавлено оборудование: {equipment}")

            elif choice == "3":
                query = input_str("Подстрока для поиска: ")
                found = find_equipment(equipment_list, query)
                if not found:
                    print("Ничего не найдено.")
                for eq in found:
                    print(eq)

            elif choice == "4":
                status = input_str("Состояние: ")
                found = filter_equipment_by_status(
                    equipment_list, status
                )
                if not found:
                    print("Ничего не найдено.")
                for eq in found:
                    print(eq)

            elif choice == "5":
                show_employees(employees)

            elif choice == "6":
                name = input_str("ФИО: ")
                email = input_str("Email: ")
                employee = add_employee(employees, name, email)
                print(f"Добавлен сотрудник: {employee}")

            elif choice == "7":
                eq_id = input_int("ID оборудования: ")
                equipment = find_equipment_by_id(
                    equipment_list, eq_id
                )
                if equipment is None:
                    print("Оборудование не найдено.")
                else:
                    print(
                        get_issuance_status(
                            is_equipment_available(equipment)
                        )
                    )

            elif choice == "8":
                create_new_issuance(
                    issuances, equipment_list, employees
                )

            elif choice == "9":
                handle_return(issuances)

            elif choice == "10":
                show_issuances(issuances)

            elif choice == "0":
                save_equipment(equipment_list)
                save_employees(employees)
                save_issuances(issuances)
                print("Данные сохранены. Выход.")
                break

            else:
                print("Неизвестная команда.")

        except ValueError as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()