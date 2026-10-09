"""Общая конфигурация и независимые HTTP-сессии API-тестов."""

import os
from collections.abc import Callable, Iterator

import pytest

from support.api_client import ApiClient


@pytest.fixture(scope="session")
def base_url() -> str:
    """Вернуть внешний адрес выбранной среды без завершающего слеша."""
    return os.getenv("BASE_URL", "http://127.0.0.1:8000").rstrip("/")


@pytest.fixture(scope="session")
def api_timeout() -> float:
    """Вернуть единый тайм-аут HTTP-запроса."""
    return float(os.getenv("API_TIMEOUT_SECONDS", "10"))


@pytest.fixture(scope="session")
def user_password() -> str:
    """Вернуть пароль создаваемых через API пользователей."""
    return os.getenv("TEST_USER_PASSWORD", "LabPassword1!")


@pytest.fixture(scope="session")
def operator_credentials() -> tuple[str, str]:
    """Вернуть учётные данные seed-оператора локальной среды."""
    return (
        os.getenv("TEST_OPERATOR_EMAIL", "operator@example.test"),
        os.getenv("TEST_OPERATOR_PASSWORD", "LabPassword1!"),
    )


@pytest.fixture
def client_factory(
    base_url: str,
    api_timeout: float,
) -> Iterator[Callable[[], ApiClient]]:
    """Создавать отдельные HTTP-сессии и закрывать их после теста."""
    clients: list[ApiClient] = []

    def create() -> ApiClient:
        client = ApiClient(base_url, api_timeout)
        clients.append(client)
        return client

    yield create

    for client in clients:
        client.close()


@pytest.fixture
def anonymous_api(client_factory) -> ApiClient:
    """Вернуть клиента без Bearer-сессии."""
    return client_factory()


@pytest.fixture
def user_api(client_factory, user_password: str) -> ApiClient:
    """Создать уникального пользователя и его авторизованную сессию."""
    return client_factory().register_and_login(user_password)


@pytest.fixture
def other_user_api(client_factory, user_password: str) -> ApiClient:
    """Создать второго независимого пользователя для проверки владения."""
    return client_factory().register_and_login(user_password)


@pytest.fixture
def operator_api(client_factory, operator_credentials) -> ApiClient:
    """Создать отдельную сессию seed-оператора."""
    email, password = operator_credentials
    return client_factory().login(email, password)