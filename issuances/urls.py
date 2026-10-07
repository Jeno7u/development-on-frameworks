"""Маршруты страниц выдач."""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.issuance_list, name="issuance_list"),
    path(
        "<int:issuance_id>/",
        views.issuance_detail,
        name="issuance_detail",
    ),
]
