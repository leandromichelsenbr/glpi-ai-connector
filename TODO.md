# TODO

## Ponto de retomada

O Gateway MCP remoto está funcional e homologado externamente.

Endpoint:

```text
https://mcp.usinabr.com.br/mcp
```

Infraestrutura atual:

```text
Cliente MCP
   |
   | HTTPS + Bearer Token
   v
Apache
   |
   v
127.0.0.1:8000
   |
   v
Docker
   |
   v
GLPI AI Connector Gateway
   |
   v
GLPI REST API
```

A retomada principal depende de um workspace **ChatGPT Business** compatível com o fluxo MCP necessário para ações de escrita.

## Prioridade 1 — ChatGPT Business

- [ ] Migrar/habilitar workspace ChatGPT Business.
- [ ] Verificar o fluxo atual de criação de app/conector MCP no ChatGPT.
- [ ] Cadastrar `https://mcp.usinabr.com.br/mcp`.
- [ ] Verificar quais mecanismos de autenticação o ChatGPT aceita no momento da homologação.
- [ ] Confirmar a descoberta de todas as tools.
- [ ] Executar `list_categories` pelo ChatGPT.
- [ ] Executar `get_ticket` pelo ChatGPT.
- [ ] Executar o primeiro `create_ticket` diretamente pelo ChatGPT.
- [ ] Testar `add_followup`, atribuição, solução e alteração de status.
- [ ] Definir quais ações devem exigir confirmação explícita do usuário.

## Prioridade 2 — Segurança

- [ ] Substituir Bearer Token estático por autenticação adequada ao cenário multiusuário quando necessário.
- [ ] Avaliar OAuth 2.1/JWT/introspecção conforme requisitos do cliente MCP.
- [ ] Implementar identidade do agente/cliente nos registros de auditoria.
- [ ] Implementar rate limiting.
- [ ] Verificar entidade também nas alterações de tickets existentes.
- [ ] Revisar exposição do `/health` e informações retornadas.
- [ ] Definir política de rotação de credenciais.

## Prioridade 3 — Plugin GLPI

- [ ] Fazer o Gateway consumir as políticas configuradas pelo plugin.
- [ ] Eliminar duplicação de permissões entre plugin e `.env`.
- [ ] Persistir auditoria centralizada no GLPI.
- [ ] Exibir histórico de ações de IA na interface do plugin.
- [ ] Criar autenticação própria entre Plugin e Gateway.
- [ ] Avaliar endpoint interno do plugin para configuração/políticas.

## Prioridade 4 — Operação e distribuição

- [ ] Versionar/revisar `Dockerfile`, `docker-compose.yml` e documentação de implantação.
- [ ] Adicionar healthcheck do Docker Compose.
- [ ] Adicionar usuário não-root à imagem Docker.
- [ ] Definir política de logs e rotação.
- [ ] Criar CI com testes Python e validação do plugin PHP.
- [ ] Automatizar criação dos ZIPs/releases.
- [ ] Criar guia de instalação para Ubuntu/Debian.
- [ ] Criar guia para Apache e, posteriormente, outros reverse proxies.
- [ ] Documentar backup/restore da configuração.
- [ ] Criar matriz de compatibilidade com versões do GLPI.

## Prioridade 5 — Funcionalidades futuras

- [ ] Anexos em tickets.
- [ ] Paginação consistente nas listagens.
- [ ] Filtros avançados de tickets.
- [ ] Consulta de acompanhamentos e soluções.
- [ ] Grupos e filas de atendimento.
- [ ] Regras de atribuição.
- [ ] Catálogo de operações disponíveis por perfil.
- [ ] Recursos além de tickets conforme demanda real dos usuários.

## Estado atual

- [x] API REST GLPI validada.
- [x] MCP via `stdio` validado.
- [x] MCP Inspector validado.
- [x] Tools de leitura e escrita validadas.
- [x] Streamable HTTP validado.
- [x] Bearer Token validado.
- [x] Docker validado no Windows.
- [x] Docker validado no Ubuntu 22.04.
- [x] Apache reverse proxy validado.
- [x] HTTPS validado.
- [x] Endpoint MCP público validado no Inspector.
