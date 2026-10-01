"""Общая настройка для переносимых тестов студента."""

import os
import uuid

import pytest
import requests


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

    # Регистрация
    reg = requests.post(
        f"{base_url}/api/auth/register",
        json={"email": email, "password": password},
        timeout=10,
    )
    assert reg.status_code == 201, reg.text

    # Вход
    login = requests.post(
        f"{base_url}/api/auth/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    assert login.status_code == 200, login.text
    token = login.json().get("access_token") or login.json().get("token")
    assert token, login.json()
    return token