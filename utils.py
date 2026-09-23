"""Вспомогательные функции ввода с обработкой ошибок."""


def input_int(prompt: str) -> int:
    """Запросить целое число, повторяя при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_str(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: строка не может быть пустой.")
