"""Веб-представления выдач из JSON-хранилища ПР3."""
from html import escape

from django.http import HttpResponse

from homepage.views import page
from models.issuances import find_issuance_by_id
from storage import load_employees, load_equipment, load_issuances


def _load_issuance_data():
    """Загрузить выдачи вместе со связанными объектами."""
    equipment_items = load_equipment()
    employees = load_employees()
    return load_issuances(equipment_items, employees)


def issuance_list(request):
    """Показать список выдач оборудования."""
    items = []
    for issuance in _load_issuance_data():
        status = "возвращено" if issuance.is_returned else "активно"
        badge = (
            "bg-secondary" if issuance.is_returned else "bg-success"
        )
        equipment_name = escape(issuance.equipment.name)
        employee_name = escape(issuance.employee.name)
        issue_date = escape(issuance.issue_date)
        items.append(
            f"""
<a href="/issuances/{issuance.id}/"
   class="list-group-item list-group-item-action">
  <div class="d-flex justify-content-between align-items-center">
    <div>
      <h2 class="h5 mb-1">{equipment_name}</h2>
      <small>{employee_name}; {issue_date}</small>
    </div>
    <span class="badge {badge}">{status}</span>
  </div>
</a>
"""
        )

    if items:
        list_content = "".join(items)
    else:
        list_content = '<p class="alert alert-info">Выдач пока нет.</p>'
    content = f"""
<h1 class="mb-3">Выдачи оборудования</h1>
<div class="list-group">{list_content}</div>
"""
    return HttpResponse(page("Сервис учета - выдачи", content))


def issuance_detail(request, issuance_id):
    """Показать карточку выдачи или ответ 404."""
    issuance = find_issuance_by_id(
        _load_issuance_data(),
        issuance_id,
    )
    if issuance is None:
        content = """
<div class="alert alert-danger" role="alert">
  <h1 class="alert-heading">Выдача не найдена</h1>
  <a href="/issuances/" class="btn btn-outline-danger">
    К списку выдач
  </a>
</div>
"""
        return HttpResponse(
            page("Выдача не найдена", content),
            status=404,
        )

    status = "возвращено" if issuance.is_returned else "активно"
    badge = "bg-secondary" if issuance.is_returned else "bg-success"
    equipment_name = escape(issuance.equipment.name)
    employee_name = escape(issuance.employee.name)
    employee_email = escape(issuance.employee.email)
    issue_date = escape(issuance.issue_date)
    content = f"""
<div class="card shadow-sm">
  <div class="card-body">
    <h1 class="card-title h3">Выдача №{issuance.id}</h1>
    <p class="card-text">
      <strong>Оборудование:</strong>
      <a href="/equipment/{issuance.equipment.id}/">
        {equipment_name}
      </a>
    </p>
    <p class="card-text">
      <strong>Сотрудник:</strong> {employee_name}
      ({employee_email})
    </p>
    <p class="card-text"><strong>Дата выдачи:</strong> {issue_date}</p>
    <p class="card-text">
      <strong>Статус:</strong>
      <span class="badge {badge}">{status}</span>
    </p>
    <a href="/issuances/" class="btn btn-outline-secondary">
      К списку выдач
    </a>
  </div>
</div>
"""
    title = f"Выдача №{issuance.id}"
    return HttpResponse(page(title, content), status=200)
