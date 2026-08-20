from __future__ import annotations

import hmac
import os

from mcp.server.auth.provider import AccessToken, TokenVerifier


class StaticBearerTokenVerifier(TokenVerifier):
    """Valida um único Bearer Token configurado por variável de ambiente.

    Esta implementação é destinada à primeira homologação do gateway remoto.
    Em produção multiusuário, deve ser substituída por JWT/OAuth 2.1 ou
    introspecção RFC 7662.
    """

    def __init__(self, expected_token: str, scopes: list[str]) -> None:
        if not expected_token:
            raise ValueError("MCP_BEARER_TOKEN não pode estar vazio quando MCP_AUTH_ENABLED=true.")
        self.expected_token = expected_token
        self.scopes = scopes

    async def verify_token(self, token: str) -> AccessToken | None:
        if not hmac.compare_digest(token, self.expected_token):
            return None

        return AccessToken(
            token=token,
            client_id="glpi-ai-client",
            scopes=self.scopes,
            subject="glpi-ai-connector",
        )


def auth_enabled() -> bool:
    return os.getenv("MCP_AUTH_ENABLED", "false").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
        "sim",
    }
