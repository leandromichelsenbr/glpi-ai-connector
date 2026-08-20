from __future__ import annotations

import logging
from typing import Any

import httpx

from .config import Settings
from .exceptions import GLPIAuthenticationError, GLPIError

logger = logging.getLogger(__name__)


class GLPIClient:
    def __init__(
        self,
        settings: Settings,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.settings = settings
        self.transport = transport

    def _headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "App-Token": self.settings.app_token,
        }

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            timeout=self.settings.timeout,
            transport=self.transport,
        )

    async def init_session(self) -> str:
        headers = self._headers()
        headers["Authorization"] = f"user_token {self.settings.user_token}"

        async with self._client() as client:
            response = await client.get(
                f"{self.settings.glpi_url}/initSession",
                headers=headers,
            )

        if response.is_error:
            raise GLPIAuthenticationError(
                f"initSession falhou: HTTP {response.status_code} - {response.text}"
            )

        data = response.json()
        token = data.get("session_token")
        if not token:
            raise GLPIAuthenticationError("GLPI não retornou session_token.")

        logger.debug("Sessão GLPI iniciada.")
        return str(token)

    async def kill_session(self, session_token: str) -> None:
        headers = self._headers()
        headers["Session-Token"] = session_token

        async with self._client() as client:
            response = await client.get(
                f"{self.settings.glpi_url}/killSession",
                headers=headers,
            )

        if response.is_error:
            logger.warning(
                "killSession falhou: HTTP %s - %s",
                response.status_code,
                response.text,
            )

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        session_token = await self.init_session()
        headers = self._headers()
        headers["Session-Token"] = session_token

        try:
            async with self._client() as client:
                response = await client.request(
                    method,
                    f"{self.settings.glpi_url}/{endpoint.lstrip('/')}",
                    headers=headers,
                    params=params,
                    json=json,
                )

            if response.is_error:
                raise GLPIError(
                    f"{method} {endpoint} falhou: "
                    f"HTTP {response.status_code} - {response.text}"
                )

            if not response.content:
                return None

            return response.json()
        finally:
            await self.kill_session(session_token)

    async def get(self, endpoint: str, *, params: dict[str, Any] | None = None) -> Any:
        return await self.request("GET", endpoint, params=params)

    async def post(self, endpoint: str, *, json: dict[str, Any]) -> Any:
        return await self.request("POST", endpoint, json=json)

    async def put(self, endpoint: str, *, json: dict[str, Any]) -> Any:
        return await self.request("PUT", endpoint, json=json)
