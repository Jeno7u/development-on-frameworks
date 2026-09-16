# Импорт модуля (требование ПР1)
from datetime import date

# Функция 1: Проверка доступности оборудования
def check_availability(available):
    if available:
        return "Статус: Доступно для выдачи"
    else:
        return "Статус: Занято (выдано другому сотруднику)"

# Функция 2: Формирование карточки оборудования
def get_equipment_info(name, inv_num, status):
    return f"Оборудование: {name} | Инв. №: {inv_num} | Состояние: {status}"

# Функция 3: Процесс выдачи оборудования
def process_issuance(employee, equipment, available):
    if available:
        return f"Успешно: Оборудование '{equipment}' выдано сотруднику {employee}."
    else:
        return f"Отказ: Оборудование '{equipment}' не может быть выдано сотруднику {employee}."

# === Основной сценарий с пользовательским вводом ===
print("=== Система учета рабочего оборудования ===")

# Запрос данных у пользователя
equipment_name = input("Введите название оборудования: ")
inventory_number = int(input("Введите инвентарный номер: "))  # преобразование типов
equipment_status = input("Введите состояние оборудования (например, Рабочее): ")
employee_name = input("Введите ФИО сотрудника: ")

# Запрос доступности с проверкой ввода (ветвление)
availability_input = input("Оборудование доступно для выдачи? (да/нет): ").strip().lower()

if availability_input == "да":
    is_available = True
elif availability_input == "нет":
    is_available = False
else:
    print("Некорректный ввод. По умолчанию считаем, что оборудование недоступно.")
    is_available = False

# Вывод результатов
print("\n--- Результат обработки ---")
print(f"Дата операции: {date.today()}")
print(get_equipment_info(equipment_name, inventory_number, equipment_status))
print(check_availability(is_available))
print(process_issuance(employee_name, equipment_name, is_available))