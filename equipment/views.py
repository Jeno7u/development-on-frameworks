"""Веб-представления оборудования из JSON-хранилища ПР3."""
from html import escape

from django.http import HttpResponse

from homepage.views import page
from models.equipment import find_equipment_by_id
from models.issuances import is_equipment_available
from storage import load_equipment


def equipment_list(request):
    """Показать список оборудования."""
    items = []
    for item in load_equipment():
        availability = (
            "доступно"
            if is_equipment_available(item)
            else "выдано"
        )
        badge = "bg-success" if item.is_available else "bg-danger"
        name = escape(item.name)
        status = escape(item.status)
        items.append(
            f"""
<a href="/equipment/{item.id}/"
   class="list-group-item list-group-item-action">
  <div class="d-flex justify-content-between align-items-center">
    <div>
      <h2 class="h5 mb-1">{name}</h2>
      <small>Инв. № {item.inventory_number}; {status}</small>
    </div>
    <span class="badge {badge}">{availability}</span>
  </div>
</a>
"""
        )

    if items:
        list_content = "".join(items)
    else:
        list_content = (
            '<p class="alert alert-info">Оборудование не добавлено.</p>'
        )
    content = f"""
<h1 class="mb-3">Оборудование</h1>
<div class="list-group">{list_content}</div>
"""
    return HttpResponse(
        page("Сервис учета - оборудование", content)
    )


def equipment_detail(request, equipment_id):
    """Показать карточку оборудования или ответ 404."""
    equipment_items = load_equipment()
    item = find_equipment_by_id(equipment_items, equipment_id)
    if item is None:
        content = """
<div class="alert alert-danger" role="alert">
  <h1 class="alert-heading">Оборудование не найдено</h1>
  <a href="/equipment/" class="btn btn-outline-danger">
    К списку оборудования
  </a>
</div>
"""
        return HttpResponse(
            page("Оборудование не найдено", content),
            status=404,
        )

    available = is_equipment_available(item)
    availability = "доступно для выдачи" if available else "выдано"
    badge = "bg-success" if available else "bg-danger"
    name = escape(item.name)
    status = escape(item.status)
    content = f"""
<div class="card shadow-sm">
  <div class="card-body">
    <h1 class="card-title h3">{name}</h1>
    <p class="card-text"><strong>ID:</strong> {item.id}</p>
    <p class="card-text">
      <strong>Инвентарный номер:</strong> {item.inventory_number}
    </p>
    <p class="card-text"><strong>Состояние:</strong> {status}</p>
    <p class="card-text">
      <strong>Доступность:</strong>
      <span class="badge {badge}">{availability}</span>
    </p>
    <a href="/equipment/" class="btn btn-outline-secondary">
      К списку оборудования
    </a>
  </div>
</div>
"""
    return HttpResponse(page(name, content), status=200)
