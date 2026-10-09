"""Проверки комментариев при взаимодействии разных ролей."""

import pytest

from support.assertions import assert_json_response


@pytest.mark.api
@pytest.mark.requirement("COMMENT-01")
def test_operator_comment_keeps_operator_as_author(user_api, operator_api):
    """Сохранить действующего автора, а не владельца заявки."""
    ticket = user_api.create_ticket("P09 комментарий оператора")

    me_response = operator_api.request("GET", "/auth/me")
    operator = assert_json_response(me_response, 200)

    comment_response = operator_api.request(
        "POST",
        f"/tickets/{ticket['id']}/comments",
        json={"text": "P09 отвечает оператор"},
    )
    comment = assert_json_response(comment_response, 201)

    assert comment["ticket_id"] == ticket["id"]
    assert comment["author_id"] == operator["id"]
    assert comment["author_id"] != ticket["author_id"]