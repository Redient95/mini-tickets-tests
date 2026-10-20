"""UI-регресс создания и обновления заявки на двух viewport."""

from uuid import uuid4

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage
from pages.tickets_page import TicketsPage


def login_as_prepared_user(page, url: str, user) -> TicketsPage:
    """Войти через UI подготовленным через API пользователем."""
    login = LoginPage(page)
    login.open(url)
    expect(login.heading).to_be_visible()
    login.login(user.email, user.password)

    tickets = TicketsPage(page)
    expect(tickets.heading).to_be_visible()
    expect(tickets.table).to_be_visible()
    return tickets


@pytest.mark.ui
@pytest.mark.requirement("UI-01")
@pytest.mark.requirement("TICKET-03")
def test_user_creates_ticket_through_ui(
    ui_page,
    url: str,
    prepared_user,
) -> None:
    """Создать заявку через форму и сопоставить карточку, таблицу и API."""
    tickets = login_as_prepared_user(ui_page, url, prepared_user)
    title = f"P13 UI create {uuid4().hex}"

    tickets.create_ticket(title, priority="normal")

    expect(tickets.status_message).to_have_text("Заявка создана")
    expect(tickets.card).to_be_visible()
    expect(tickets.selected_title()).to_have_value(title)
    expect(tickets.selected_priority()).to_have_value("normal")

    row = tickets.ticket_row_by_title(title)
    expect(row).to_be_visible()
    expect(row.get_by_test_id("ticket-priority")).to_have_text("Обычный")
    expect(row.get_by_text("Новая", exact=True)).to_be_visible()

    test_id = row.get_attribute("data-testid")
    assert test_id and test_id.startswith("ticket-")
    ticket_id = test_id.removeprefix("ticket-")
    prepared_user.track_ticket(ticket_id)

    stored = prepared_user.get_ticket(ticket_id)
    assert stored["title"] == title
    assert stored["priority"] == "normal"
    assert stored["status"] == "new"


@pytest.mark.ui
@pytest.mark.requirement("UI-02")
@pytest.mark.requirement("TICKET-03")
def test_priority_is_synchronized_without_reload(
    ui_page,
    url: str,
    prepared_user,
) -> None:
    """Обновить приоритет и увидеть одно значение в карточке и списке."""
    title = f"P13 UI update {uuid4().hex}"
    created = prepared_user.create_ticket(title, priority="low")
    tickets = login_as_prepared_user(ui_page, url, prepared_user)

    row = tickets.ticket_row(created["id"])
    expect(row).to_be_visible()
    expect(tickets.row_priority(created["id"])).to_have_text("Низкий")

    tickets.open_ticket(created["id"])
    expect(tickets.card).to_be_visible()
    expect(tickets.selected_title()).to_have_value(title)
    expect(tickets.selected_priority()).to_have_value("low")

    tickets.change_priority("high")

    expect(tickets.status_message).to_have_text("Изменения сохранены")
    expect(tickets.selected_priority()).to_have_value("high")
    expect(tickets.row_priority(created["id"])).to_have_text("Высокий")

    stored = prepared_user.get_ticket(created["id"])
    assert stored["priority"] == "high"
    assert stored["title"] == title
    assert stored["status"] == "new"