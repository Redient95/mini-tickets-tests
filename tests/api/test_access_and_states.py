"""Проверки владения, ролей, состояний и фильтра списка."""

import pytest

from support.assertions import assert_error_response, assert_json_response


@pytest.mark.api
@pytest.mark.requirement("AUTH-03")
def test_user_cannot_read_another_users_ticket(user_api, other_user_api):
    """Скрыть существование чужой заявки за единым ответом 404."""
    ticket = user_api.create_ticket("P09 заявка первого пользователя")

    response = other_user_api.request("GET", f"/tickets/{ticket['id']}")
    body = assert_error_response(response, 404)

    assert "author_id" not in body["error"]
    assert "title" not in body["error"]


@pytest.mark.api
@pytest.mark.requirement("TICKET-04")
def test_operator_cannot_move_new_ticket_directly_to_closed(
    user_api,
    operator_api,
):
    """Отклонить переход new → closed даже для роли operator."""
    ticket = user_api.create_ticket("P09 проверка перехода")
    path = f"/tickets/{ticket['id']}"

    response = operator_api.request(
        "PUT",
        path + "/status",
        json={"status": "closed"},
    )
    assert_error_response(response, 409)

    detail_response = user_api.request("GET", path)
    detail = assert_json_response(detail_response, 200)
    assert detail["status"] == "new"


@pytest.mark.api
@pytest.mark.requirement("TICKET-05")
def test_new_filter_contains_only_new_tickets(user_api, operator_api):
    """Вернуть новую заявку и исключить активную заявку того же автора."""
    new_ticket = user_api.create_ticket("P09 новая для фильтра")
    active_ticket = user_api.create_ticket("P09 активная для фильтра")

    transition = operator_api.request(
        "PUT",
        f"/tickets/{active_ticket['id']}/status",
        json={"status": "active"},
    )
    transition_body = assert_json_response(transition, 200)
    assert transition_body["status"] == "active"

    response = user_api.request("GET", "/tickets?status=new")
    tickets = assert_json_response(response, 200)
    returned_ids = {ticket["id"] for ticket in tickets}

    assert returned_ids == {new_ticket["id"]}
    assert active_ticket["id"] not in returned_ids
    assert all(ticket["status"] == "new" for ticket in tickets)