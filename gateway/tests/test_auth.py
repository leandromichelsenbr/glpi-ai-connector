import pytest

from glpi_ai_connector.adapters.mcp.auth import StaticBearerTokenVerifier


@pytest.mark.asyncio
async def test_static_bearer_accepts_expected_token():
    verifier = StaticBearerTokenVerifier("segredo", ["glpi:mcp"])

    access = await verifier.verify_token("segredo")

    assert access is not None
    assert access.client_id == "glpi-ai-client"
    assert access.scopes == ["glpi:mcp"]


@pytest.mark.asyncio
async def test_static_bearer_rejects_invalid_token():
    verifier = StaticBearerTokenVerifier("segredo", ["glpi:mcp"])

    assert await verifier.verify_token("incorreto") is None


def test_static_bearer_rejects_empty_configuration():
    with pytest.raises(ValueError, match="MCP_BEARER_TOKEN"):
        StaticBearerTokenVerifier("", ["glpi:mcp"])
