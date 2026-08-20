# MCP remoto

O objetivo deste estágio é substituir o MCP Inspector pelo ChatGPT como cliente do gateway.

## Desenvolvimento local

O gateway continua suportando `stdio` para desenvolvimento:

```dotenv
MCP_TRANSPORT=stdio
```

```powershell
cd gateway
.venv\Scripts\Activate.ps1
mcp dev src/glpi_ai_connector/adapters/mcp/server.py
```

## Streamable HTTP local

No `.env`:

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

O gateway ficará disponível em:

```text
http://127.0.0.1:8000/mcp
```

E o health check em:

```text
http://127.0.0.1:8000/health
```

Teste primeiro o health check e depois conecte o MCP Inspector ao endpoint HTTP `/mcp`.

## Segurança de transporte

O SDK MCP valida `Host` e `Origin` para mitigar DNS rebinding. Em localhost, a configuração padrão deste projeto permite apenas endereços locais.

Para um hostname de produção, configure explicitamente, por exemplo:

```dotenv
MCP_ALLOWED_HOSTS=mcp.example.com,mcp.example.com:*
MCP_ALLOWED_ORIGINS=https://chatgpt.com
```

Isso não substitui autenticação. `MCP_ALLOWED_HOSTS` é proteção de transporte, não controle de acesso.

## Produção prevista

```text
ChatGPT
   |
   | HTTPS / MCP
   v
mcp.example.com
   |
   | reverse proxy + TLS + autenticação
   v
Gateway MCP
   |
   | HTTPS REST
   v
GLPI
```

A porta interna do gateway não deve ser publicada diretamente. O próximo estágio é implementar autorização do endpoint MCP e colocar TLS/reverse proxy na frente do serviço.
