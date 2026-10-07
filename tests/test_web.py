"""Тесты маршрутов и страниц Django-приложения."""
from django.test import Client, SimpleTestCase, override_settings


class WebPagesTests(SimpleTestCase):
    """Проверка базового цикла URL -> view -> response."""

    def setUp(self):
        """Создать тестовый HTTP-клиент."""
        self.client = Client()

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Сервис учета оборудования")
        self.assertContains(response, "bootstrap@5.3.3")

    def test_equipment_list(self):
        response = self.client.get("/equipment/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ноутбук Lenovo ThinkPad")

    def test_equipment_detail(self):
        response = self.client.get("/equipment/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "10001")
        self.assertContains(response, "выдано")

    def test_missing_equipment(self):
        response = self.client.get("/equipment/999/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(
            response,
            "Оборудование не найдено",
            status_code=404,
        )

    def test_issuance_list(self):
        response = self.client.get("/issuances/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Иванов Иван Иванович")

    def test_issuance_detail(self):
        response = self.client.get("/issuances/1/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Выдача №1")
        self.assertContains(response, "ivanov@example.com")

    def test_missing_issuance(self):
        response = self.client.get("/issuances/999/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(
            response,
            "Выдача не найдена",
            status_code=404,
        )

    @override_settings(DEBUG=False)
    def test_custom_404_page(self):
        response = self.client.get("/nonexistent/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(
            response,
            "404 - страница не найдена",
            status_code=404,
        )
