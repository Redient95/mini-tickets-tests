"""Практика №12. API-тест жизненного цикла заявки."""

from __future__ import annotations

import uuid

import pytest
import requests


@pytest.mark.api
@pytest.mark.requirement("TICKET-01")
def test_ticket_crud_flow(base_url: str, owner_token: str) -> None:
    """Проверить создание, чтение, изменение и удаление заявки."""
    unique = uuid.uuid4().hex[:8]
    title = f"Тестовая заявка {unique}"

    headers = {"Authorization": f"Bearer {owner_token}"}

    # 1. Создание заявки
    create_response = requests.post(
        f"{base_url}/api/tickets",
        json={"title": title, "priority": "normal"},
        headers=headers,
        timeout=10,
    )
    assert create_response.status_code == 201, create_response.text
    created = create_response.json()
    ticket_id = created["id"]

    # 2. Проверка серверных полей
    assert created["title"] == title
    assert created["status"] == "new"
    assert created["priority"] == "normal"
    assert "author_id" in created
    assert "password" not in created

    # 3. Чтение заявки
    read_response = requests.get(
        f"{base_url}/api/tickets/{ticket_id}",
        headers=headers,
        timeout=10,
    )
    assert read_response.status_code == 200
    assert read_response.json()["id"] == ticket_id

    # 4. Изменение заголовка
    update_response = requests.patch(
        f"{base_url}/api/tickets/{ticket_id}",
        json={"title": f"Обновлённая {unique}"},
        headers=headers,
        timeout=10,
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == f"Обновлённая {unique}"

    # 5. Удаление заявки
    delete_response = requests.delete(
        f"{base_url}/api/tickets/{ticket_id}",
        headers=headers,
        timeout=10,
    )
    assert delete_response.status_code in (200, 204)

    # 6. Проверка, что заявки больше нет
    after_delete = requests.get(
        f"{base_url}/api/tickets/{ticket_id}",
        headers=headers,
        timeout=10,
    )
    assert after_delete.status_code == 404