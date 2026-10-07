"""Конфигурация приложения выдач."""
from django.apps import AppConfig


class IssuancesConfig(AppConfig):
    """Конфигурация приложения issuances."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "issuances"
