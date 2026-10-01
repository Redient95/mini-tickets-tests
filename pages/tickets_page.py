"""Page Object для страницы заявок."""

from __future__ import annotations

from playwright.sync_api import Page, expect


class TicketsPage:
    """Страница со списком заявок и формой создания."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.status_message = page.get_by_test_id("status-message")
        self.title_input = page.get_by_label("Заголовок")
        self.create_button = page.get_by_role("button", name="Создать")

    def create_ticket(self, title: str) -> None:
        """Заполнить форму и отправить её."""
        self.title_input.fill(title)
        self.create_button.click()

    def ticket_row(self, title: str):
        """Найти строку заявки по заголовку."""
        return self.page.get_by_role("row", name=title)