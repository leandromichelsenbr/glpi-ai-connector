# GLPI AI Connector Gateway

Gateway Python/MCP responsável por expor ferramentas de GLPI para agentes de IA.

## Instalação

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Preencha `.env` com os tokens da API REST do GLPI.

## Testes

```powershell
pytest
```

## MCP Inspector

```powershell
mcp dev src/glpi_ai_connector/adapters/mcp/server.py
```

A próxima etapa é disponibilizar o mesmo conjunto de tools através de MCP Streamable HTTP para uso remoto.
