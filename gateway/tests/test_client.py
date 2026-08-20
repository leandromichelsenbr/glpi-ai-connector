import json

import httpx
import pytest

from glpi_ai_connector.core.client import GLPIClient
from glpi_ai_connector.core.config import Settings


def settings() -> Settings:
    return Settings(
        glpi_url="https://glpi.example/apirest.php",
        app_token="app-test",
        user_token="user-test",
        timeout=5,
    )


@pytest.mark.asyncio
async def test_get_ticket_opens_and_closes_session():
    calls: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)

        if request.url.path.endswith("/initSession"):
            assert request.headers["Authorization"] == "user_token user-test"
            assert request.headers["App-Token"] == "app-test"
            return httpx.Response(200, json={"session_token": "session-test"})

        if request.url.path.endswith("/Ticket/123"):
            assert request.headers["Session-Token"] == "session-test"
            return httpx.Response(200, json={"id": 123, "name": "Teste"})

        if request.url.path.endswith("/killSession"):
            assert request.headers["Session-Token"] == "session-test"
            return httpx.Response(200, json={})

        return httpx.Response(404)

    client = GLPIClient(
        settings(),
        transport=httpx.MockTransport(handler),
    )

    result = await client.get("Ticket/123")

    assert result["id"] == 123
    assert calls == [
        "/apirest.php/initSession",
        "/apirest.php/Ticket/123",
        "/apirest.php/killSession",
    ]


@pytest.mark.asyncio
async def test_create_ticket_posts_input_payload():
    payload = None

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal payload

        if request.url.path.endswith("/initSession"):
            return httpx.Response(200, json={"session_token": "session-test"})

        if request.url.path.endswith("/Ticket") and request.method == "POST":
            payload = json.loads(request.content.decode())
            return httpx.Response(201, json={"id": 9001, "message": "Item successfully added"})

        if request.url.path.endswith("/killSession"):
            return httpx.Response(200, json={})

        return httpx.Response(404)

    client = GLPIClient(
        settings(),
        transport=httpx.MockTransport(handler),
    )

    result = await client.post(
        "Ticket",
        json={"input": {"name": "Fiscal - teste", "content": "Descrição"}},
    )

    assert result["id"] == 9001
    assert payload == {
        "input": {
            "name": "Fiscal - teste",
            "content": "Descrição",
        }
    }
