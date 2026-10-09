"""Позитивные проверки создания и чтения заявки."""

from uuid import uuid4

import pytest

from support.assertions import assert_json_response


@pytest.mark.api
@pytest.mark.requirement("TICKET-01")
@pytest.mark.requirement("TICKET-02")
def test_create_and_read_ticket(user_api):
    """Сопоставить POST, карточку и отфильтрованный список одной заявки."""
    title = f"P09 позитивная заявка {uuid4().hex}"
    created_response = user_api.request(
        "POST",
        "/tickets",
        json={"title": title, "priority": "high"},
    )
    created = assert_json_response(created_response, 201)

    assert set(created) == {
        "id",
        "author_id",
        "title",
        "priority",
        "status",
        "created_at",
    }
    assert created["author_id"] == user_api.user["id"]
    assert created["title"] == title
    assert created["priority"] == "high"
    assert created["status"] == "new"

    detail_response = user_api.request("GET", f"/tickets/{created['id']}")
    detail = assert_json_response(detail_response, 200)
    assert detail == created

    list_response = user_api.request("GET", "/tickets?status=new")
    tickets = assert_json_response(list_response, 200)
    assert created["id"] in {ticket["id"] for ticket in tickets}
    assert all(ticket["status"] == "new" for ticket in tickets)