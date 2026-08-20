from __future__ import annotations

from html import unescape
import re
from typing import Any

from ..core.client import GLPIClient
from ..core.audit import AuditLogger
from ..core.policy import SecurityPolicy
from ..core.validation import (
    validate_non_empty,
    validate_status,
    validate_ticket_id,
    validate_ticket_type,
    validate_urgency,
    validate_user_id,
)


_HTML_RE = re.compile(r"<[^>]+>")


def _plain_text(value: Any) -> str | None:
    if value is None:
        return None
    text = unescape(str(value))
    text = _HTML_RE.sub("", text)
    return text.strip()


class TicketService:
    def __init__(
        self,
        client: GLPIClient,
        *,
        policy: SecurityPolicy | None = None,
        audit: AuditLogger | None = None,
    ) -> None:
        self.client = client
        self.policy = policy or SecurityPolicy()
        self.audit = audit or AuditLogger()

    @staticmethod
    def _as_list(data: Any) -> list[dict[str, Any]]:
        if data is None:
            return []
        if isinstance(data, list):
            return [item for item in data if isinstance(item, dict)]
        if isinstance(data, dict):
            return [data]
        return []

    @staticmethod
    def _normalize_ticket(item: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": item.get("id"),
            "title": item.get("name"),
            "description": _plain_text(item.get("content")),
            "status": item.get("status"),
            "type": item.get("type"),
            "urgency": item.get("urgency"),
            "impact": item.get("impact"),
            "priority": item.get("priority"),
            "entity_id": item.get("entities_id"),
            "category_id": item.get("itilcategories_id"),
            "requester_id": item.get("users_id_recipient"),
            "date_created": item.get("date"),
            "date_modified": item.get("date_mod"),
            "solved_at": item.get("solvedate"),
            "closed_at": item.get("closedate"),
        }

    @staticmethod
    def _normalize_category(item: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": item.get("id"),
            "name": item.get("name"),
            "full_name": item.get("completename"),
            "entity_id": item.get("entities_id"),
            "parent_category_id": item.get("itilcategories_id"),
            "level": item.get("level"),
            "recursive": bool(item.get("is_recursive")),
            "helpdesk_visible": bool(item.get("is_helpdeskvisible")),
            "incident": bool(item.get("is_incident")),
            "request": bool(item.get("is_request")),
            "problem": bool(item.get("is_problem")),
            "change": bool(item.get("is_change")),
        }

    @staticmethod
    def _normalize_entity(item: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": item.get("id"),
            "name": item.get("name"),
            "full_name": item.get("completename"),
            "parent_id": item.get("entities_id"),
            "level": item.get("level"),
            "default_ticket_type": item.get("tickettype"),
            "default_ticket_template_id": item.get("tickettemplates_id"),
            "notifications_enabled": bool(item.get("is_notif_enable_default")),
        }

    @staticmethod
    def _normalize_user(item: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": item.get("id"),
            "login": item.get("name"),
            "first_name": item.get("firstname"),
            "last_name": item.get("realname"),
            "active": bool(item.get("is_active")),
        }

    async def get_ticket(self, ticket_id: int) -> dict[str, Any]:
        validate_ticket_id(ticket_id)
        data = await self.client.get(f"Ticket/{ticket_id}")
        if not isinstance(data, dict):
            return {}
        return self._normalize_ticket(data)

    async def search_tickets(self, query: str = "", range_: str = "0-49") -> dict[str, Any]:
        params: dict[str, Any] = {
            "range": range_,
            "forcedisplay[0]": 1,
            "forcedisplay[1]": 2,
            "forcedisplay[2]": 12,
        }

        if query:
            params.update({
                "criteria[0][field]": 1,
                "criteria[0][searchtype]": "contains",
                "criteria[0][value]": query,
            })

        data = await self.client.get("search/Ticket", params=params)

        rows = []
        if isinstance(data, dict):
            for row in data.get("data", []) or []:
                if not isinstance(row, dict):
                    continue
                rows.append({
                    "id": row.get("2") or row.get("id"),
                    "title": row.get("1") or row.get("name"),
                    "status": row.get("12") or row.get("status"),
                })

            return {
                "total_count": data.get("totalcount"),
                "count": data.get("count", len(rows)),
                "tickets": rows,
            }

        return {"total_count": 0, "count": 0, "tickets": []}

    async def create_ticket(
        self,
        title: str,
        description: str,
        *,
        urgency: int = 3,
        ticket_type: int = 1,
        category_id: int | None = None,
        entity_id: int | None = None,
    ) -> Any:
        validate_non_empty(title, "title")
        validate_non_empty(description, "description")
        validate_urgency(urgency)
        validate_ticket_type(ticket_type)
        self.policy.require("create_ticket")
        self.policy.check_entity(entity_id)

        item: dict[str, Any] = {
            "name": title.strip(),
            "content": description.strip(),
            "urgency": urgency,
            "type": ticket_type,
        }

        if category_id is not None:
            item["itilcategories_id"] = category_id

        if entity_id is not None:
            item["entities_id"] = entity_id

        result = await self.client.post("Ticket", json={"input": item})
        self.audit.record(
            "create_ticket",
            target_id=result.get("id") if isinstance(result, dict) else None,
            details={"title": title.strip(), "entity_id": entity_id},
        )
        return result

    async def update_ticket(
        self,
        ticket_id: int,
        *,
        title: str | None = None,
        description: str | None = None,
        urgency: int | None = None,
        status: int | None = None,
        category_id: int | None = None,
    ) -> Any:
        validate_ticket_id(ticket_id)
        self.policy.require("update_ticket")

        item: dict[str, Any] = {"id": ticket_id}

        if title is not None:
            validate_non_empty(title, "title")
            item["name"] = title.strip()

        if description is not None:
            validate_non_empty(description, "description")
            item["content"] = description.strip()

        if urgency is not None:
            validate_urgency(urgency)
            item["urgency"] = urgency

        if status is not None:
            validate_status(status)
            item["status"] = status

        if category_id is not None:
            item["itilcategories_id"] = category_id

        if len(item) == 1:
            raise ValueError("Nenhum campo foi informado para atualização.")

        result = await self.client.put(
            f"Ticket/{ticket_id}",
            json={"input": item},
        )
        self.audit.record(
            "update_ticket",
            target_id=ticket_id,
            details={"fields": sorted(k for k in item if k != "id")},
        )
        return result

    async def add_followup(self, ticket_id: int, content: str) -> Any:
        validate_ticket_id(ticket_id)
        validate_non_empty(content, "content")
        self.policy.require("add_followup")

        result = await self.client.post(
            "ITILFollowup",
            json={
                "input": {
                    "itemtype": "Ticket",
                    "items_id": ticket_id,
                    "content": content.strip(),
                }
            },
        )
        self.audit.record("add_followup", target_id=ticket_id)
        return result

    async def assign_technician(self, ticket_id: int, user_id: int) -> Any:
        validate_ticket_id(ticket_id)
        validate_user_id(user_id)
        self.policy.require("assign_technician")

        result = await self.client.post(
            "Ticket_User",
            json={
                "input": {
                    "tickets_id": ticket_id,
                    "users_id": user_id,
                    "type": 2,
                }
            },
        )
        self.audit.record(
            "assign_technician",
            target_id=ticket_id,
            details={"user_id": user_id},
        )
        return result

    async def set_status(self, ticket_id: int, status: int) -> Any:
        validate_ticket_id(ticket_id)
        validate_status(status)
        self.policy.require("set_ticket_status")
        result = await self.update_ticket(ticket_id, status=status)
        self.audit.record(
            "set_ticket_status",
            target_id=ticket_id,
            details={"status": status},
        )
        return result

    async def add_solution(
        self,
        ticket_id: int,
        content: str,
        solution_type_id: int = 0,
    ) -> Any:
        validate_ticket_id(ticket_id)
        validate_non_empty(content, "content")
        self.policy.require("add_solution")

        payload: dict[str, Any] = {
            "itemtype": "Ticket",
            "items_id": ticket_id,
            "content": content.strip(),
        }

        if solution_type_id:
            payload["solutiontypes_id"] = solution_type_id

        result = await self.client.post(
            "ITILSolution",
            json={"input": payload},
        )
        self.audit.record("add_solution", target_id=ticket_id)
        return result

    async def close_ticket(self, ticket_id: int) -> Any:
        validate_ticket_id(ticket_id)
        self.policy.require("close_ticket")
        # Evita depender de set_status, pois fechamento possui política própria.
        result = await self.update_ticket(ticket_id, status=6)
        self.audit.record("close_ticket", target_id=ticket_id)
        return result

    async def list_categories(self, range_: str = "0-99") -> list[dict[str, Any]]:
        data = await self.client.get(
            "ITILCategory",
            params={"range": range_, "order": "ASC"},
        )
        return [self._normalize_category(item) for item in self._as_list(data)]

    async def list_entities(self, range_: str = "0-99") -> list[dict[str, Any]]:
        data = await self.client.get(
            "Entity",
            params={"range": range_, "order": "ASC"},
        )
        return [self._normalize_entity(item) for item in self._as_list(data)]

    async def list_users(self, range_: str = "0-99") -> list[dict[str, Any]]:
        data = await self.client.get(
            "User",
            params={"range": range_, "order": "ASC"},
        )
        return [self._normalize_user(item) for item in self._as_list(data)]
