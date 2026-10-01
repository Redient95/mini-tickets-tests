"""Общая настройка для переносимых тестов студента."""

import os
import uuid

import pytest
import requests
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from pages.tickets_page import TicketsPage


@pytest.fixture
def base_url() -> str:
    """Взять BASE_URL личного стенда."""
    return os.getenv("BASE_URL", "http://127.0.0.1:8000")


@pytest.fixture
def url(base_url: str) -> str:
    """Совместимость со старой фикстурой."""
    return base_url


@pytest.fixture
def owner_token(base_url: str) -> str:
    """Зарегистрировать нового пользователя и вернуть его токен."""
    unique = uuid.uuid4().hex[:8]
    email = f"owner-{unique}@example.test"
    password = "LabPassword1!"

    reg = requests.post(
        f"{base_url}/api/auth/register",
        json={"email": email, "password": password},
        timeout=10,
    )
    assert reg.status_code == 201, reg.text

    login = requests.post(
        f"{base_url}/api/auth/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    assert login.status_code == 200, login.text
    token = login.json().get("access_token") or login.json().get("token")
    assert token, login.json()
    return token


@pytest.fixture
def prepared_user(base_url: str) -> dict:
    """Создать нового пользователя и вернуть его email и пароль."""
    unique = uuid.uuid4().hex[:8]
    email = f"ui-{unique}@example.test"
    password = "LabPassword1!"

    reg = requests.post(
        f"{base_url}/api/auth/register",
        json={"email": email, "password": password},
        timeout=10,
    )
    assert reg.status_code == 201, reg.text

    return {"email": email, "password": password}


class UiPage:
    """Простой контейнер для Page Object."""

    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url
        self.login_page = LoginPage(page)

    def login(self, email: str, password: str) -> None:
        """Открыть страницу входа и войти."""
        self.login_page.open(self.base_url)
        self.login_page.login(email, password)

    def open_tickets(self) -> TicketsPage:
        """Перейти на страницу заявок."""
        self.page.goto(f"{self.base_url}/tickets")
        return TicketsPage(self.page)


@pytest.fixture
def ui_page(page: Page, base_url: str) -> UiPage:
    """Собрать UI-обёртку со страницами."""
    return UiPage(page, base_url)