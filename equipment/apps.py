"""Конфигурация приложения оборудования."""
from django.apps import AppConfig


class EquipmentConfig(AppConfig):
    """Конфигурация приложения equipment."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "equipment"
