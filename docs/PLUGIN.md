# Plugin GLPI AI Connector

O plugin é a camada administrativa instalada dentro do GLPI. Ele **não é necessário para o protocolo MCP funcionar**, mas será responsável por centralizar segurança e administração do produto.

## Responsabilidades

- configuração;
- operações permitidas;
- entidades permitidas;
- auditoria;
- futuramente autenticação do Gateway;
- futuramente endpoint seguro de configuração/políticas.

## Estado atual

A versão inicial foi instalada e validada em GLPI 10. Durante a homologação foi corrigida a compatibilidade de banco de dados para usar `$DB->query()`.

## Arquitetura alvo

```text
Agente de IA
    |
    | MCP
    v
Gateway
    |
    | HTTPS autenticado
    v
Plugin GLPI
    |
    v
GLPI
```
