# GLPI AI Connector Gateway

Gateway Python/MCP que expõe operações do GLPI para agentes compatíveis com MCP.

## Instalação

```powershell
cd gateway
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Preencha `GLPI_APP_TOKEN` e `GLPI_USER_TOKEN` no `.env`. Nunca versione o `.env`.

## Testes

```powershell
pytest
```

## Modo local / MCP Inspector

Mantenha:

```dotenv
MCP_TRANSPORT=stdio
```

E execute:

```powershell
mcp dev src/glpi_ai_connector/adapters/mcp/server.py
```

## MCP via HTTP

Altere no `.env`:

```dotenv
MCP_TRANSPORT=streamable-http
MCP_HOST=127.0.0.1
MCP_PORT=8000
MCP_PATH=/mcp
```

Execute:

```powershell
python -m glpi_ai_connector.adapters.mcp.server
```

Endpoints locais:

```text
MCP:    http://127.0.0.1:8000/mcp
Health: http://127.0.0.1:8000/health
```

O transporte HTTP usa modo stateless com respostas JSON.

## Teste no Inspector usando HTTP

Com o servidor HTTP em execução, abra o Inspector e conecte usando Streamable HTTP para:

```text
http://127.0.0.1:8000/mcp
```

As mesmas tools já validadas via stdio devem aparecer.

## Produção

Não exponha diretamente a porta 8000 na internet. O desenho previsto é:

```text
ChatGPT
   |
   | HTTPS / MCP
   v
Reverse Proxy / TLS / autenticação
   |
   v
GLPI AI Connector Gateway
   |
   | HTTPS REST
   v
GLPI
```

Antes de publicar em domínio real, configure `MCP_ALLOWED_HOSTS` e autenticação. O próximo marco do projeto é adicionar autorização ao endpoint MCP e então publicar por HTTPS.
