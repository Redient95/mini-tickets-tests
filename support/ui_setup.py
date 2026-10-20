"""API-предусловия и адресная очистка данных UI-тестов."""

from dataclasses import dataclass, field
from uuid import uuid4

import requests


@dataclass
class PreparedUser:
    """Хранить уникального пользователя и его авторизованную API-сессию."""

    base_url: str
    email: str
    password: str
    session: requests.Session
    ticket_ids: list[str] = field(default_factory=list)
    timeout: float = 10.0

    @classmethod
    def register(
        cls,
        base_url: str,
        password: str = "LabPassword1!",
    ) -> "PreparedUser":
        """Зарегистрировать пользователя и получить Bearer для подготовки."""
        session = requests.Session()
        email = f"p13-{uuid4().hex}@example.test"
        credentials = {"email": email, "password": password}

        register = session.post(
            f"{base_url.rstrip('/')}/api/auth/register",
            json=credentials,
            headers={"X-Request-ID": f"p13-{uuid4().hex[:24]}"},
            timeout=10,
        )
        assert register.status_code == 201, cls.coordinates(register)

        login = session.post(
            f"{base_url.rstrip('/')}/api/auth/login",
            json=credentials,
            headers={"X-Request-ID": f"p13-{uuid4().hex[:24]}"},
            timeout=10,
        )
        assert login.status_code == 200, cls.coordinates(login)
        session.headers["Authorization"] = (
            f"Bearer {login.json()['access_token']}"
        )
        return cls(base_url.rstrip("/"), email, password, session)

    @staticmethod
    def coordinates(response: requests.Response) -> str:
        """Вернуть безопасные координаты ответа без тела и Authorization."""
        return (
            f"{response.request.method} {response.request.url}; "
            f"status={response.status_code}; "
            f"request_id="
            f"{response.request.headers.get('X-Request-ID', 'missing')}"
        )

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        """Отправить авторизованный API-запрос с новым request ID."""
        headers = dict(kwargs.pop("headers", {}))
        headers["X-Request-ID"] = f"p13-{uuid4().hex[:24]}"
        return self.session.request(
            method,
            f"{self.base_url}/api{path}",
            headers=headers,
            timeout=self.timeout,
            **kwargs,
        )

    def create_ticket(self, title: str, priority: str = "normal") -> dict:
        """Создать новую заявку как предусловие и запомнить её UUID."""
        response = self.request(
            "POST",
            "/tickets",
            json={"title": title, "priority": priority},
        )
        assert response.status_code == 201, self.coordinates(response)
        ticket = response.json()
        self.track_ticket(ticket["id"])
        return ticket

    def get_ticket(self, ticket_id: str) -> dict:
        """Прочитать заявку после UI-действия для независимого подтверждения."""
        response = self.request("GET", f"/tickets/{ticket_id}")
        assert response.status_code == 200, self.coordinates(response)
        return response.json()

    def track_ticket(self, ticket_id: str) -> None:
        """Добавить созданный через UI UUID в адресную очистку."""
        if ticket_id not in self.ticket_ids:
            self.ticket_ids.append(ticket_id)

    def cleanup(self) -> None:
        """Удалить новые заявки пользователя и закрыть HTTP-сессию."""
        discovered = self.request("GET", "/tickets")
        if discovered.status_code == 200:
            for ticket in discovered.json():
                self.track_ticket(ticket["id"])

        errors: list[str] = []
        for ticket_id in reversed(self.ticket_ids):
            response = self.request("DELETE", f"/tickets/{ticket_id}")
            if response.status_code not in {204, 404}:
                errors.append(self.coordinates(response))

        self.session.close()
        assert not errors, "Cleanup не завершён: " + "; ".join(errors)