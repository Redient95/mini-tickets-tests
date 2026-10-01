"""Практика №13. UI-тесты с Page Object."""

from __future__ import annotations

import uuid

import pytest
from playwright.sync_api import expect


@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.requirement("UI-01")
def test_user_creates_ticket_through_ui(
    ui_page,
    url: str,
    prepared_user,
) -> None:
    """Пользователь создаёт заявку через UI."""
    unique = uuid.uuid4().hex[:8]
    title = f"UI-заявка {unique}"

    # Логин через UI
    ui_page.login(prepared_user["email"], prepared_user["password"])

    # Создание заявки
    tickets = ui_page.open_tickets()
    tickets.create_ticket(title)

    # Проверка сообщения об успехе
    expect(tickets.status_message).to_have_text("Заявка создана")

    # Проверка появления заявки в списке
    expect(tickets.ticket_row(title)).to_be_visible()