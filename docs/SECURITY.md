# Security Gateway

A v0.3 introduz uma camada de política entre o agente e as operações de escrita.

## Princípios

- O agente não decide sozinho quais operações são permitidas.
- A conta GLPI continua sendo a última barreira de autorização.
- O conector adiciona uma barreira anterior, configurável.
- Fechamento de ticket é bloqueado por padrão.
- Operações de escrita geram eventos de auditoria.
- Tokens nunca são registrados no log.

## Configuração

```dotenv
GLPI_ALLOWED_ENTITY_IDS=0,2
GLPI_ALLOW_CREATE=true
GLPI_ALLOW_UPDATE=true
GLPI_ALLOW_FOLLOWUP=true
GLPI_ALLOW_ASSIGNMENT=true
GLPI_ALLOW_STATUS_CHANGE=true
GLPI_ALLOW_SOLUTION=true
GLPI_ALLOW_CLOSE=false
GLPI_AUDIT_FILE=logs/audit.jsonl
```

`GLPI_ALLOWED_ENTITY_IDS` vazio significa que o conector não adiciona restrição de
entidade além das permissões do próprio usuário GLPI.

## Auditoria

Formato JSON Lines:

```json
{"timestamp":"...","operation":"create_ticket","target_type":"Ticket","target_id":123,"success":true,"details":{"title":"Teste","entity_id":0}}
```

Não registrar conteúdo integral de chamados, tokens, senhas ou dados pessoais
desnecessários.
