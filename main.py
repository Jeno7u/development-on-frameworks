"""Точка запуска приложения учета оборудования."""
from equipment import (
    add_equipment,
    find_equipment,
    filter_equipment_by_status,
    sort_equipment,
    get_equipment_info,
)
from issuance import (
    is_equipment_available,
    issue_equipment,
    return_equipment,
    get_issuance_status,
)
from storage import (
    load_equipment,
    save_equipment,
    load_issuances,
    save_issuances,
)
from utils import input_int, input_str


def show_equipment(equipment: dict[int, dict]) -> None:
    """Вывести список оборудования."""
    if not equipment:
        print("Список оборудования пуст.")
        return
    for eq_id in sort_equipment(equipment):
        print(f"[{eq_id}] {get_equipment_info(equipment, eq_id)}")


def show_issuances(issuances: list[dict]) -> None:
    """Вывести список выдач."""
    if not issuances:
        print("Выдач пока нет.")
        return
    for item in issuances:
        print(
            f"[{item['id']}] Оборудование ID "
            f"{item['equipment_id']} -> "
            f"{item['employee']} ({item['date']})"
        )


def print_menu() -> None:
    """Напечатать меню приложения."""
    print("\n=== Система учета рабочего оборудования ===")
    print("1. Показать оборудование")
    print("2. Добавить оборудование")
    print("3. Найти оборудование по названию")
    print("4. Фильтр по состоянию")
    print("5. Проверить доступность")
    print("6. Выдать оборудование")
    print("7. Вернуть оборудование")
    print("8. Показать выдачи")
    print("0. Выход")


def main() -> None:
    """Точка запуска приложения."""
    equipment = load_equipment()
    issuances = load_issuances()

    while True:
        print_menu()
        choice = input("Выберите действие: ").strip()

        try:
            if choice == "1":
                show_equipment(equipment)

            elif choice == "2":
                name = input_str("Название: ")
                inv = input_int("Инвентарный номер: ")
                status = input_str("Состояние: ")
                eq_id = add_equipment(
                    equipment, name, inv, status
                )
                print(f"Добавлено оборудование с ID {eq_id}.")

            elif choice == "3":
                query = input_str("Подстрока для поиска: ")
                found = find_equipment(equipment, query)
                if not found:
                    print("Ничего не найдено.")
                for eq_id in found:
                    print(get_equipment_info(equipment, eq_id))

            elif choice == "4":
                status = input_str("Состояние: ")
                found = filter_equipment_by_status(
                    equipment, status
                )
                if not found:
                    print("Ничего не найдено.")
                for eq_id in found:
                    print(get_equipment_info(equipment, eq_id))

            elif choice == "5":
                eq_id = input_int("ID оборудования: ")
                available = is_equipment_available(
                    equipment, eq_id
                )
                print(get_issuance_status(available))

            elif choice == "6":
                eq_id = input_int("ID оборудования: ")
                employee = input_str("ФИО сотрудника: ")
                item = issue_equipment(
                    issuances, equipment, eq_id, employee
                )
                print(
                    f"Выдача №{item['id']} оформлена: "
                    f"{employee}."
                )

            elif choice == "7":
                iss_id = input_int("ID выдачи: ")
                return_equipment(issuances, equipment, iss_id)
                print("Оборудование возвращено.")

            elif choice == "8":
                show_issuances(issuances)

            elif choice == "0":
                save_equipment(equipment)
                save_issuances(issuances)
                print("Данные сохранены. Выход.")
                break

            else:
                print("Неизвестная команда.")

        except ValueError as error:
            print(f"Ошибка: {error}")
        except KeyError:
            print("Ошибка: объект не найден.")


if __name__ == "__main__":
    main()