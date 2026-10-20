"""Повторяемые проверки транспортного контракта Mini Tickets API."""

import requests

from support.api_client import ApiClient


def assert_request_id(response: requests.Response) -> str:
    """Проверить сохранение клиентского X-Request-ID в ответе сервера."""
    sent = response.request.headers.get("X-Request-ID")
    received = response.headers.get("X-Request-ID")
    assert sent, ApiClient.describe(response)
    assert received == sent, ApiClient.describe(response)
    return received


def assert_json_response(
    response: requests.Response,
    expected_status: int,
) -> dict | list:
    """Проверить код, JSON Content-Type, request ID и вернуть разобранное тело."""
    assert response.status_code == expected_status, ApiClient.describe(response)
    content_type = response.headers.get("Content-Type", "")
    assert content_type.startswith("application/json"), ApiClient.describe(response)
    assert_request_id(response)
    return response.json()


def assert_error_response(
    response: requests.Response,
    expected_status: int,
) -> dict:
    """Проверить единый конверт ошибки и корреляцию тела с заголовком."""
    body = assert_json_response(response, expected_status)
    assert isinstance(body, dict), ApiClient.describe(response)
    assert set(body) == {"error"}, ApiClient.describe(response)
    assert isinstance(body["error"].get("message"), str)
    assert body["error"]["message"]
    assert body["error"]["request_id"] == response.headers["X-Request-ID"]
    return body