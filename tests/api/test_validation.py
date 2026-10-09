"""Проверки границ и отклонённых входных данных заявки."""

import pytest

from support.assertions import assert_error_response, assert_json_response


@pytest.mark.api
@pytest.mark.requirement("TICKET-01")
@pytest.mark.parametrize(
    ("length", "expected_status"),
    [(2, 422), (3, 201), (80, 201), (81, 422)],
    ids=["below-min", "min", "max", "above-max"],
)
def test_ticket_title_boundaries(user_api, length, expected_status):
    """Проверить соседние значения обеих границ заголовка."""
    response = user_api.request(
        "POST",
        "/tickets",
        json={"title": "x" * length, "priority": "normal"},
    )

    if expected_status == 201:
        body = assert_json_response(response, 201)
        assert len(body["title"]) == length
        assert body["status"] == "new"
    else:
        body = assert_error_response(response, 422)
        assert body["error"].get("fields")


@pytest.mark.api
@pytest.mark.requirement("TICKET-02")
def test_unknown_priority_is_rejected_without_side_effect(user_api):
    """Отклонить неизвестный приоритет и сохранить исходный список."""
    before_response = user_api.request("GET", "/tickets")
    before = assert_json_response(before_response, 200)

    response = user_api.request(
        "POST",
        "/tickets",
        json={
            "title": "P09 неизвестный приоритет",
            "priority": "urgent",
        },
    )
    assert_error_response(response, 422)

    after_response = user_api.request("GET", "/tickets")
    after = assert_json_response(after_response, 200)
    assert after == before