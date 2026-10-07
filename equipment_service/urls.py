"""Корневая маршрутизация Django-проекта."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("equipment/", include("equipment.urls")),
    path("issuances/", include("issuances.urls")),
]

handler404 = "homepage.views.page_not_found"
