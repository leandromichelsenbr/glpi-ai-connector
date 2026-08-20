# GLPI AI Connector

Integração entre **GLPI** e agentes de IA, com **MCP (Model Context Protocol)** como primeiro protocolo de integração.

O objetivo principal é permitir interações como:

> “Crie um chamado no GLPI para verificar a divergência fiscal.”

O agente chama a ferramenta MCP `create_ticket`, o Gateway converte a ação para a API REST do GLPI e o ticket é criado no GLPI.

## Arquitetura

```text
ChatGPT / Claude / outro agente MCP
              |
              | MCP
              v
+-----------------------------+
| GLPI AI Connector Gateway   |
| Python / MCP                |
+-------------+---------------+
              |
              | GLPI REST API
              v
+-----------------------------+
| GLPI                        |
|                             |
| GLPI AI Connector Plugin    |
| configuração / auditoria    |
+-----------------------------+
```

O **Gateway** é o componente necessário para a integração do agente com o GLPI. O **Plugin** é a camada administrativa no GLPI e evoluirá para centralizar políticas, autenticação e auditoria.

## Estrutura do repositório

```text
glpi-ai-connector/
├── gateway/                  # Python + MCP
│   ├── src/
│   ├── tests/
│   ├── pyproject.toml
│   └── .env.example
├── plugin/
│   └── glpiaiconnector/      # Plugin PHP instalável no GLPI
├── docs/
├── LICENSE
└── README.md
```

## Gateway

A versão atual já foi validada contra GLPI 10 com as ferramentas:

- `get_ticket`
- `search_tickets`
- `create_ticket`
- `update_ticket`
- `add_followup`
- `list_categories`
- `list_entities`
- `list_users`
- `assign_technician`
- `set_ticket_status`
- `add_solution`
- `close_ticket`

### Desenvolvimento local

```powershell
cd gateway
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
pytest
mcp dev src/glpi_ai_connector/adapters/mcp/server.py
```

O `.env` contém a URL e os tokens da API REST do GLPI e **nunca deve ser versionado**.

## Plugin GLPI

O plugin atual é uma primeira versão administrativa. Ele já possui:

- instalação e ativação no GLPI 10;
- tela de configuração;
- habilitação/desabilitação das principais operações;
- restrição configurável de entidades;
- tabela de auditoria;
- fechamento de ticket desabilitado por padrão.

Para desenvolvimento, copie `plugin/glpiaiconnector` para `<GLPI>/plugins/glpiaiconnector` e use **Configurar → Plugins → GLPI AI Connector → Instalar → Ativar**.

## Status atual

- Gateway MCP local: **validado**
- Tools de leitura e escrita: **validadas**
- Plugin GLPI 10: **instalação validada**
- MCP remoto via HTTPS: **próxima etapa**
- Integração direta com ChatGPT: **objetivo da próxima fase**

## Próximos passos

1. disponibilizar o Gateway via MCP Streamable HTTP;
2. adicionar autenticação ao MCP remoto;
3. publicar o Gateway via HTTPS;
4. conectar o endpoint MCP ao ChatGPT;
5. fazer o Plugin fornecer políticas e auditoria centralizadas ao Gateway.
