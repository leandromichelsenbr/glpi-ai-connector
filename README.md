# GLPI AI Connector

Camada segura de integração entre GLPI e agentes de IA.

O núcleo conversa com a API REST do GLPI e não depende de MCP. MCP é o primeiro
adaptador, permitindo que agentes usem operações do GLPI como ferramentas.

## Arquitetura

```text
AI / MCP Host
     |
     v
adapters/mcp
     |
     v
services
     |
     v
core/client
     |
     v
GLPI REST API
```

## v0.2 — Workflow

Ferramentas MCP:

- `get_ticket`
- `search_tickets`
- `create_ticket`
- `update_ticket`
- `add_followup`
- `list_categories`
- `list_entities`
- `list_users`
- `assign_technician`
- `set_ticket_status`
- `add_solution`
- `close_ticket`

As respostas de tickets, categorias, entidades e usuários são normalizadas para
evitar expor campos internos desnecessários ao agente.

## Segurança

Crie `.env` a partir de `.env.example`:

```dotenv
GLPI_URL=https://suporte.usinabr.com.br/apirest.php
GLPI_APP_TOKEN=SEU_APP_TOKEN
GLPI_USER_TOKEN=SEU_USER_TOKEN
GLPI_TIMEOUT=30
```

Nunca versione `.env`.

## Instalação

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Testes

```powershell
pytest
```

## MCP Inspector

```powershell
mcp dev src/glpi_ai_connector/adapters/mcp/server.py
```

## Roteiro de teste v0.2

1. `list_users`
2. `get_ticket`
3. `search_tickets`
4. `assign_technician`
5. `add_followup`
6. `set_ticket_status`
7. `add_solution`
8. `close_ticket`

Use tickets de teste para as operações de escrita.
