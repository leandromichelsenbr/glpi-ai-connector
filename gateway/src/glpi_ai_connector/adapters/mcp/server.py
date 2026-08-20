from __future__ import annotations

import logging
from typing import Any

from mcp.server import MCPServer

from glpi_ai_connector.core.client import GLPIClient
from glpi_ai_connector.core.audit import AuditLogger
from glpi_ai_connector.core.policy import SecurityPolicy
from glpi_ai_connector.core.config import Settings
from glpi_ai_connector.services.tickets import TicketService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = MCPServer("GLPI AI Connector")


def service() -> TicketService:
    settings = Settings.from_env()
    policy = SecurityPolicy(
        allowed_entity_ids=set(settings.allowed_entity_ids),
        allow_create=settings.allow_create,
        allow_update=settings.allow_update,
        allow_followup=settings.allow_followup,
        allow_assignment=settings.allow_assignment,
        allow_status_change=settings.allow_status_change,
        allow_solution=settings.allow_solution,
        allow_close=settings.allow_close,
    )
    return TicketService(
        GLPIClient(settings),
        policy=policy,
        audit=AuditLogger(settings.audit_file),
    )


@mcp.tool()
async def get_ticket(ticket_id: int) -> Any:
    """Consulta um ticket pelo ID, retornando campos normalizados."""
    return await service().get_ticket(ticket_id)


@mcp.tool()
async def search_tickets(query: str = "") -> Any:
    """Pesquisa tickets pelo título e retorna uma lista normalizada."""
    return await service().search_tickets(query)


@mcp.tool()
async def create_ticket(
    title: str,
    description: str,
    urgency: int = 3,
    ticket_type: int = 1,
    category_id: int | None = None,
    entity_id: int | None = None,
) -> Any:
    """Cria um ticket no GLPI."""
    return await service().create_ticket(
        title,
        description,
        urgency=urgency,
        ticket_type=ticket_type,
        category_id=category_id,
        entity_id=entity_id,
    )


@mcp.tool()
async def update_ticket(
    ticket_id: int,
    title: str | None = None,
    description: str | None = None,
    urgency: int | None = None,
    status: int | None = None,
    category_id: int | None = None,
) -> Any:
    """Atualiza campos explicitamente informados de um ticket."""
    return await service().update_ticket(
        ticket_id,
        title=title,
        description=description,
        urgency=urgency,
        status=status,
        category_id=category_id,
    )


@mcp.tool()
async def add_followup(ticket_id: int, content: str) -> Any:
    """Adiciona acompanhamento a um ticket."""
    return await service().add_followup(ticket_id, content)


@mcp.tool()
async def list_categories() -> Any:
    """Lista categorias ITIL normalizadas."""
    return await service().list_categories()


@mcp.tool()
async def list_entities() -> Any:
    """Lista entidades normalizadas."""
    return await service().list_entities()


@mcp.tool()
async def list_users() -> Any:
    """Lista usuários visíveis ao usuário da API."""
    return await service().list_users()


@mcp.tool()
async def assign_technician(ticket_id: int, user_id: int) -> Any:
    """Atribui um usuário como técnico responsável pelo ticket."""
    return await service().assign_technician(ticket_id, user_id)


@mcp.tool()
async def set_ticket_status(ticket_id: int, status: int) -> Any:
    """Altera o status do ticket. Valores GLPI: 1 novo, 2 atribuído, 3 planejado, 4 pendente, 5 solucionado, 6 fechado."""
    return await service().set_status(ticket_id, status)


@mcp.tool()
async def add_solution(
    ticket_id: int,
    content: str,
    solution_type_id: int = 0,
) -> Any:
    """Registra uma solução para o ticket."""
    return await service().add_solution(
        ticket_id,
        content,
        solution_type_id=solution_type_id,
    )


@mcp.tool()
async def close_ticket(ticket_id: int) -> Any:
    """Fecha o ticket usando o status 6 do GLPI."""
    return await service().close_ticket(ticket_id)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
