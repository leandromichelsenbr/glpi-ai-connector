# Milestones

## v0.1 — Ticket Management
- [x] Cliente REST e sessão GLPI
- [x] Consultar/pesquisar/criar/atualizar tickets
- [x] Categorias, entidades e acompanhamentos
- [x] Adaptador MCP

## v0.2 — Workflow
- [x] Usuários
- [x] Atribuição de técnico
- [x] Status
- [x] Solução
- [x] Fechamento
- [x] Normalização e validação

## v0.3 — Security Gateway
- [x] Política por operação
- [x] Allowlist de entidades na criação
- [x] Fechamento bloqueado por padrão
- [x] Auditoria JSONL
- [x] Configuração por ambiente
- [ ] Verificação de entidade em alterações de tickets existentes
- [ ] Identidade do agente
- [ ] Rate limiting
- [ ] Confirmação para ações sensíveis
- [ ] Auditoria persistida pelo plugin GLPI

## v0.4 — Remote MCP
- [x] Streamable HTTP
- [x] Endpoint `/health`
- [x] Proteção de Host/Origin
- [x] Autenticação Bearer Token
- [x] Homologação no MCP Inspector
- [x] Docker local
- [x] Docker em Ubuntu 22.04
- [x] Reverse proxy Apache
- [x] HTTPS público
- [x] Endpoint remoto homologado

## v0.5 — ChatGPT Integration
- [ ] Migrar/habilitar workspace ChatGPT Business
- [ ] Cadastrar o MCP remoto no ChatGPT
- [ ] Validar descoberta das tools
- [ ] Validar tool de leitura a partir do ChatGPT
- [ ] Validar `create_ticket` a partir do ChatGPT
- [ ] Validar confirmação e comportamento de ações sensíveis
- [ ] Definir estratégia definitiva de autenticação para o ChatGPT

## Fase posterior — Produto
- [ ] Integrar políticas do plugin com o Gateway
- [ ] Centralizar auditoria no GLPI
- [ ] OAuth 2.1/JWT ou introspecção para cenários multiusuário
- [ ] Empacotamento/release automatizado do Gateway e Plugin
- [ ] CI/CD
- [ ] Documentação de instalação para terceiros
- [ ] Matriz de compatibilidade GLPI
