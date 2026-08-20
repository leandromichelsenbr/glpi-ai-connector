# Autenticação do Gateway MCP

A primeira camada de autenticação HTTP usa um Bearer Token estático para homologação.

## Objetivo

Sem autenticação, qualquer cliente capaz de alcançar `/mcp` poderia tentar executar as tools expostas. Com esta configuração, o endpoint exige:

```http
Authorization: Bearer <token>
```

O endpoint `/health` permanece público e não expõe configuração nem credenciais.

## Configuração local

No arquivo `gateway/.env`:

```dotenv
MCP_TRANSPORT=streamable-http
MCP_AUTH_ENABLED=true
MCP_BEARER_TOKEN=gere-um-token-longo-e-aleatorio
MCP_REQUIRED_SCOPES=glpi:mcp
MCP_AUTH_ISSUER=http://127.0.0.1:8000
MCP_RESOURCE_URL=http://127.0.0.1:8000/mcp
```

Nunca grave o token real em `.env.example`, documentação, logs ou Git.

## Homologação

1. Inicie o gateway.
2. `GET /health` deve continuar retornando HTTP 200 sem token.
3. Uma conexão a `/mcp` sem Bearer Token deve receber HTTP 401.
4. Token incorreto deve receber HTTP 401.
5. No MCP Inspector, adicione o header:

```text
Authorization: Bearer <seu-token>
```

6. Conecte e execute `list_categories` e uma operação de escrita em ticket de teste.

## Limitação desta fase

O token estático é deliberadamente uma etapa intermediária. Para conexão pública/multiusuário, o plano é adotar OAuth 2.1/JWT ou introspecção de token, preservando o gateway como Resource Server MCP.
