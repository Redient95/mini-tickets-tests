"""Небольшой внешний REST-клиент для независимых API-тестов."""

import json
from uuid import uuid4

import requests


class ApiClient:
    """Хранить HTTP-сессию одной роли и общие правила отправки запросов."""

    sensitive_keys = {
        "access_token",
        "authorization",
        "password",
        "password_hash",
        "token_hash",
    }

    def __init__(self, base_url: str, timeout: float) -> None:
        """Подготовить адрес API, тайм-аут и пустую пользовательскую сессию."""
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.user: dict | None = None

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        """Отправить запрос с уникальным идентификатором для диагностики."""
        if not path.startswith("/"):
            raise ValueError("Путь API должен начинаться с /")

        headers = dict(kwargs.pop("headers", {}))
        headers.setdefault("X-Request-ID", f"p09-{uuid4().hex[:24]}")

        return self.session.request(
            method=method,
            url=f"{self.base_url}/api{path}",
            headers=headers,
            timeout=self.timeout,
            **kwargs,
        )

    def login(self, email: str, password: str) -> "ApiClient":
        """Получить Bearer и сохранить его только в текущей HTTP-сессии."""
        response = self.request(
            "POST",
            "/auth/login",
            json={"email": email, "password": password},
        )
        assert response.status_code == 200, self.describe(response)
        token = response.json()["access_token"]
        self.session.headers["Authorization"] = f"Bearer {token}"
        return self

    def register_and_login(self, password: str) -> "ApiClient":
        """Создать уникального пользователя и авторизовать его сессию."""
        email = f"p09-{uuid4().hex}@example.test"
        response = self.request(
            "POST",
            "/auth/register",
            json={"email": email, "password": password},
        )
        assert response.status_code == 201, self.describe(response)
        self.user = response.json()
        return self.login(email, password)

    def create_ticket(
        self,
        title: str | None = None,
        priority: str = "normal",
    ) -> dict:
        """Создать уникальную заявку как предусловие другого теста."""
        body = {
            "title": title or f"P09 заявка {uuid4().hex}",
            "priority": priority,
        }
        response = self.request("POST", "/tickets", json=body)
        assert response.status_code == 201, self.describe(response)
        return response.json()

    @staticmethod
    def redact(value):
        """Рекурсивно скрыть чувствительные значения диагностического JSON."""
        if isinstance(value, dict):
            return {
                key: (
                    "[REDACTED]"
                    if key.lower() in ApiClient.sensitive_keys
                    else ApiClient.redact(item)
                )
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [ApiClient.redact(item) for item in value]
        return value

    @staticmethod
    def describe(response: requests.Response) -> str:
        """Сформировать сообщение с безопасным фрагментом ответа."""
        request_id = response.request.headers.get("X-Request-ID", "missing")
        try:
            payload = ApiClient.redact(response.json())
            response_summary = json.dumps(payload, ensure_ascii=False)[:500]
        except requests.exceptions.JSONDecodeError:
            response_summary = f"<не-JSON: {len(response.content)} байт>"
        return (
            f"{response.request.method} {response.request.url}; "
            f"status={response.status_code}; request_id={request_id}; "
            f"body={response_summary}"
        )

    def close(self) -> None:
        """Закрыть соединения HTTP-сессии после теста."""
        self.session.close()