import json

import httpx
import pytest

from glpi_ai_connector.core.client import GLPIClient
from glpi_ai_connector.core.config import Settings
from glpi_ai_connector.services.tickets import TicketService


def make_client(handler) -> GLPIClient:
    return GLPIClient(
        Settings(
            glpi_url="https://glpi.example/apirest.php",
            app_token="a",
            user_token="u",
        ),
        transport=httpx.MockTransport(handler),
    )


@pytest.mark.asyncio
async def test_get_ticket_returns_normalized_data():
    raw = {
        "id": 123,
        "name": "Teste",
        "content": "<p>Descrição <b>HTML</b></p>",
        "status": 2,
        "type": 1,
        "urgency": 3,
        "impact": 3,
        "priority": 3,
        "entities_id": 0,
        "itilcategories_id": 1,
        "users_id_recipient": 4,
        "date": "2026-08-20 12:00:00",
        "date_mod": "2026-08-20 12:10:00",
        "solvedate": None,
        "closedate": None,
        "secret": "not exposed",
    }

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/initSession"):
            return httpx.Response(200, json={"session_token": "s"})
        if request.url.path.endswith("/Ticket/123"):
            return httpx.Response(200, json=raw)
        if request.url.path.endswith("/killSession"):
            return httpx.Response(200, json={})
        return httpx.Response(404)

    result = await TicketService(make_client(handler)).get_ticket(123)

    assert result["id"] == 123
    assert result["description"] == "Descrição HTML"
    assert "secret" not in result


@pytest.mark.asyncio
async def test_list_users_normalizes_and_hides_extra_fields():
    raw = [{
        "id": 9,
        "name": "tecnico",
        "firstname": "Tec",
        "realname": "Nico",
        "is_active": 1,
        "password": "not exposed",
    }]

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/initSession"):
            return httpx.Response(200, json={"session_token": "s"})
        if request.url.path.endswith("/User"):
            return httpx.Response(200, json=raw)
        if request.url.path.endswith("/killSession"):
            return httpx.Response(200, json={})
        return httpx.Response(404)

    result = await TicketService(make_client(handler)).list_users()

    assert result == [{
        "id": 9,
        "login": "tecnico",
        "first_name": "Tec",
        "last_name": "Nico",
        "active": True,
    }]


@pytest.mark.asyncio
async def test_assign_technician_posts_ticket_user_relation():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/initSession"):
            return httpx.Response(200, json={"session_token": "s"})
        if request.url.path.endswith("/Ticket_User"):
            captured["body"] = json.loads(request.content.decode())
            return httpx.Response(201, json={"id": 55})
        if request.url.path.endswith("/killSession"):
            return httpx.Response(200, json={})
        return httpx.Response(404)

    result = await TicketService(make_client(handler)).assign_technician(10, 9)

    assert result["id"] == 55
    assert captured["body"]["input"] == {
        "tickets_id": 10,
        "users_id": 9,
        "type": 2,
    }


@pytest.mark.asyncio
async def test_add_solution_posts_itil_solution():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/initSession"):
            return httpx.Response(200, json={"session_token": "s"})
        if request.url.path.endswith("/ITILSolution"):
            captured["body"] = json.loads(request.content.decode())
            return httpx.Response(201, json={"id": 70})
        if request.url.path.endswith("/killSession"):
            return httpx.Response(200, json={})
        return httpx.Response(404)

    result = await TicketService(make_client(handler)).add_solution(
        10,
        "Correção aplicada.",
    )

    assert result["id"] == 70
    assert captured["body"]["input"]["itemtype"] == "Ticket"
    assert captured["body"]["input"]["items_id"] == 10


@pytest.mark.asyncio
async def test_validation_rejects_invalid_urgency():
    service = TicketService(make_client(lambda request: httpx.Response(500)))

    with pytest.raises(ValueError, match="urgency"):
        await service.create_ticket("Teste", "Descrição", urgency=99)


@pytest.mark.asyncio
async def test_update_rejects_empty_change():
    service = TicketService(make_client(lambda request: httpx.Response(500)))

    with pytest.raises(ValueError, match="Nenhum campo"):
        await service.update_ticket(10)
