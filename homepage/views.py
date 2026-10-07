"""Представления главной страницы и общий HTML-каркас."""
from html import escape

from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """Собрать HTML-документ с Bootstrap и общей навигацией."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/"
        "dist/css/bootstrap.min.css"
    )
    safe_title = escape(title)
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_title}</title>
  <link rel="stylesheet" href="{bootstrap}">
</head>
<body class="bg-light">
  <nav class="navbar navbar-expand-md bg-dark mb-4"
       data-bs-theme="dark">
    <div class="container">
      <a class="navbar-brand" href="/">Equipment Service</a>
      <div class="navbar-nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/equipment/">Оборудование</a>
        <a class="nav-link" href="/issuances/">Выдачи</a>
      </div>
    </div>
  </nav>
  <main class="container pb-5">{content}</main>
</body>
</html>"""


def index(request):
    """Показать главную страницу сервиса."""
    content = """
<section class="p-5 mb-4 bg-white rounded-3 shadow-sm">
  <h1 class="display-4">Сервис учета оборудования</h1>
  <p class="lead">
    Контроль рабочего оборудования, его состояния и выдачи сотрудникам.
  </p>
  <a href="/equipment/" class="btn btn-primary me-2">
    Оборудование
  </a>
  <a href="/issuances/" class="btn btn-secondary">Выдачи</a>
</section>
"""
    return HttpResponse(page("Сервис учета оборудования", content))


def page_not_found(request, exception):
    """Вернуть оформленную страницу для неизвестного URL."""
    content = """
<div class="alert alert-danger" role="alert">
  <h1 class="alert-heading">404 - страница не найдена</h1>
  <p>Проверьте адрес или вернитесь на главную страницу.</p>
  <a href="/" class="btn btn-primary">На главную</a>
</div>
"""
    return HttpResponse(
        page("404 - страница не найдена", content),
        status=404,
    )
