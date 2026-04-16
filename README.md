# chiaras-ai

> Marketplace pessoal de plugins Claude Code do Bruno Chiaramonti — developer tools, gestao de projetos, financas pessoais, daily planner, IT tickets.

## Instalacao

```
/plugin marketplace add bchiaramonti/chiaras-ai
```

Depois instale os plugins que quiser:

```
/plugin install <plugin-name>@chiaras-ai
```

## Plugins disponiveis

| Plugin | Descricao | Versao |
|---|---|---|
| [claude-code-toolkit](./claude-code-toolkit) | Meta-plugin para criar e validar skills, agents, commands, hooks, plugins e marketplaces do Claude Code | 2.2.1 |
| [forge](./forge) | Pipeline de engenharia de software em 8 fases — da ideia a producao | 1.0.2 |
| [gestao-de-projetos](./gestao-de-projetos) | Planeja e rastreia projetos em sprints + gera PPTX executivos + integracao ClickUp | 1.6.2 |
| [planner](./planner) | Gera daily planner pessoal em HTML dark editorial (Georgia + Inter, terracota + azul petroleo) | 1.0.0 |
| [service-desk-m7](./service-desk-m7) | Cria tickets estruturados de TI (problemas, base de dados, novas funcionalidades) | 1.0.0 |
| [superavit](./superavit) | Controle financeiro pessoal conversacional — importa extratos, categoriza, gera relatorios mensais | 1.0.1 |

## Estrutura

```
chiaras-ai/
├── .claude-plugin/
│   └── marketplace.json       # registro central dos 6 plugins
├── claude-code-toolkit/
├── forge/
├── gestao-de-projetos/
├── planner/
├── service-desk-m7/
└── superavit/
```

Cada plugin e auto-contido com sua propria `plugin.json`, `README.md`, skills, agents e assets.

## Dependencias

Alguns plugins precisam de MCPs ou pacotes externos:

| Plugin | Requisito |
|---|---|
| `gestao-de-projetos` | ClickUp MCP, `python-pptx`, `puppeteer@^22` |
| `superavit` | Supabase MCP, Python 3.11+ |
| `m7-apresentacoes` (nao incluso aqui) | `python-pptx`, `puppeteer@^22` |

Consulte o README.md de cada plugin pra detalhes.

## Design Systems

- **Planner Editorial Noturno** (`planner`) — Dark mode quente, Georgia serif + Inter sans, paleta terracota `#D97757` + azul petroleo `#6B9EB0`. Uso estritamente pessoal.
- **M7-2026** (usado em plugins M7 de outros marketplaces) — TWK Everett, paleta `#424135` Verde Caqui + `#EEF77C` Lime.

Estes sistemas **nunca se misturam**. Plugins deste marketplace sao para uso pessoal — plugins corporativos M7 ficam em marketplaces separados.

## Autor

Bruno Chiaramonti
