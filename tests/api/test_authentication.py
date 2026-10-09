"""Проверки Bearer-сессии и публичной модели пользователя."""

import pytest

from support.assertions import assert_error_response, assert_json_response


@pytest.mark.api
@pytest.mark.requirement("AUTH-02")
def test_me_requires_token(anonymous_api):
    """Вернуть 401 и Bearer challenge для запроса без сессии."""
    response = anonymous_api.request("GET", "/auth/me")
    assert_error_response(response, 401)
    assert response.headers.get("WWW-Authenticate") == "Bearer"


@pytest.mark.api
@pytest.mark.requirement("AUTH-02")
def test_me_returns_current_public_user(user_api):
    """Вернуть пользователя, которому принадлежит предъявленный токен."""
    response = user_api.request("GET", "/auth/me")
    body = assert_json_response(response, 200)

    assert body == user_api.user
    assert set(body) == {"id", "email", "role"}
    assert body["role"] == "user"
    assert "password" not in body
    assert "password_hash" not in body