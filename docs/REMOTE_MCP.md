# MCP remoto

## Objetivo

Substituir o MCP local usado pelo Inspector por um endpoint HTTPS acessível pelo ChatGPT.

```text
ChatGPT
   |
   | MCP / HTTPS
   v
https://mcp.exemplo.com/mcp
   |
   | GLPI REST API
   v
GLPI
```

## Etapas

1. habilitar Streamable HTTP no Gateway;
2. testar localmente em HTTP;
3. adicionar autenticação;
4. configurar reverse proxy e TLS;
5. restringir hosts permitidos;
6. cadastrar o endpoint MCP no cliente de IA.

Não publicar as tools de escrita em um endpoint público sem autenticação.
