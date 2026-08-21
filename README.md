# GLPI AI Connector

Integração entre **GLPI** e agentes de IA, com **MCP (Model Context Protocol)** como protocolo principal de integração.

O objetivo é permitir interações como:

> “Crie um chamado no GLPI para verificar a divergência fiscal.”

O agente chama a ferramenta MCP `create_ticket`, o Gateway converte a ação para a API REST do GLPI e o ticket é criado no GLPI.

## Arquitetura

```text
ChatGPT / Claude / outro cliente MCP
              |
              | HTTPS + MCP
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
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .env.example
├── plugin/
│   └── glpiaiconnector/      # Plugin PHP instalável no GLPI
├── docs/
├── TODO.md
├── LICENSE
└── README.md
```

## Gateway

A versão atual foi validada contra GLPI 10 com as ferramentas:

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

### Transportes MCP

O Gateway suporta:

- `stdio` para desenvolvimento e MCP Inspector;
- `Streamable HTTP` para acesso remoto.

O endpoint remoto foi homologado com autenticação Bearer Token e HTTPS.

### Execução local

```powershell
cd gateway
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
pytest
python -m glpi_ai_connector.adapters.mcp.server
```

O `.env` contém URL, tokens e configurações do Gateway e **nunca deve ser versionado**.

### Docker

O Gateway também foi homologado em Docker, com a porta MCP publicada apenas em `127.0.0.1:8000` e um reverse proxy responsável pelo HTTPS público.

Arquitetura validada em produção:

```text
Internet
   |
   | HTTPS
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

Endpoint atualmente homologado:

```text
https://mcp.usinabr.com.br/mcp
```

O endpoint `/health` permanece público para liveness. O endpoint `/mcp` exige autenticação Bearer.

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
- Streamable HTTP: **validado**
- Bearer Token: **validado**
- Docker: **validado em Windows e Ubuntu 22.04**
- Apache reverse proxy: **validado**
- HTTPS público: **validado**
- MCP Inspector externo: **validado**
- Integração direta com ChatGPT: **aguardando homologação em ChatGPT Business**

## Retomada

O projeto está em ponto estável de espera. Ao disponibilizar um workspace ChatGPT Business com suporte ao MCP necessário para ações de escrita, o próximo teste será conectar o endpoint remoto e executar uma operação real como:

> “Crie um chamado no GLPI.”

Consulte [TODO.md](TODO.md) para as próximas etapas e melhorias planejadas.
