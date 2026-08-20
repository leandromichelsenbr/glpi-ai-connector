# Arquitetura

## Princípios

1. O core não conhece MCP.
2. Tokens do GLPI ficam somente na camada de configuração.
3. Cada operação de escrita passa por um serviço explícito.
4. Adaptadores devem poder ser substituídos sem alterar a comunicação REST.
5. O plugin GLPI futuro será uma camada adicional, não uma dependência do core.

## Fluxo

```text
MCP Host
  |
  | tool call
  v
MCP Adapter
  |
  | método Python
  v
TicketService
  |
  | operação GLPI
  v
GLPIClient
  |
  | REST/JSON
  v
GLPI
```

## Limite de confiança

O objetivo futuro é evitar que um agente receba credenciais administrativas
do GLPI. O conector deverá validar operação, entidade, usuário e política antes
de executar alterações.
