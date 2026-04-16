---
description: Inicializa um novo projeto Forge com estrutura de diretórios, .status, CLAUDE.md e templates base
argument-hint: <nome-do-projeto>
---

# Forge Init: $ARGUMENTS

## Objetivo

Criar a estrutura completa de um projeto Forge a partir de uma pasta vazia (ou quase vazia).

## Processo

### 1. Coletar informações

- **Nome do projeto:** `$ARGUMENTS` (se não fornecido, perguntar ao usuário)
- **Nome do owner:** perguntar ao usuário

### 2. Validar

- Se a pasta atual não estiver vazia, avisar e pedir confirmação antes de prosseguir
- Se já existir um arquivo `.status`, informar que o projeto já foi inicializado e PARAR (não sobrescrever)

### 3. Criar árvore de diretórios

Criar todos os diretórios do pipeline:

```
00-discovery/research/
01-product/
02-design/wireframes/
03-architecture/adrs/
04-specs/features/
05-implementation/src/
06-quality/
07-deploy/infra/
```

### 4. Gerar arquivos iniciais

Gerar os seguintes arquivos, substituindo `<PROJECT_NAME>` e `<OWNER_NAME>` pelos valores coletados, e `<YYYY-MM-DD>` pela data de hoje:

#### 4.1 `CLAUDE.md`

Ler o template do CLAUDE.md em `references/pipeline-overview.md` (seção 4) e gerar o arquivo na raiz do projeto, substituindo `<PROJECT_NAME>` pelo nome informado.

#### 4.2 `.status`

Ler o template do `.status` YAML em `references/pipeline-overview.md` (seção 3) e gerar o arquivo na raiz do projeto, substituindo:
- `<project-name>` pelo nome do projeto
- `<owner-name>` pelo nome do owner
- `<YYYY-MM-DD>` pela data de hoje
- Discovery deve iniciar com `status: "in_progress"` e `started_at` preenchido

#### 4.3 `README.md`

```markdown
# <PROJECT_NAME>

> Projeto gerenciado pelo [Forge Pipeline](https://github.com/bchiaramonti/chiaras-ai).

## Status

Use `/forge:status` para ver o progresso atual.
```

#### 4.4 `CHANGELOG.md`

```markdown
# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato segue [Keep a Changelog](https://keepachangelog.com/), e o versionamento segue [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Scaffolding do projeto via Forge
- Estrutura de diretórios para 8 fases do pipeline
- CLAUDE.md com regras do pipeline
- .status YAML para controle de estado
```

#### 4.5 `04-specs/spec-template.md`

Placeholder do template de spec técnica:

```markdown
# [Nome da Feature]

## Referência
- **User Story:** [ID / link]
- **Épico:** [nome]
- **Prioridade:** [Must/Should/Could]

## Descrição
[O que esta feature faz]

## Endpoints / Rotas
| Método | Rota | Auth | Descrição |
|--------|------|------|-----------|
| | | | |

## Modelo de Dados
[Entidades envolvidas e atributos relevantes]

## Regras de Negócio
1. [Regra]

## Validações
| Campo | Regra | Mensagem de Erro |
|-------|-------|------------------|
| | | |

## Tratamento de Erros
| Cenário | HTTP Status | Mensagem |
|---------|-------------|----------|
| | | |

## Dependências
- [Outras features ou serviços necessários]

## Critérios de Aceite Técnicos
- [ ] [Critério verificável]
```

#### 4.6 `.gitignore`

```
# OS
.DS_Store
Thumbs.db

# Editor
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local
.env.*.local

# Dependencies
node_modules/
__pycache__/
*.pyc

# Build
dist/
build/
.next/
```

### 5. Git

- Se a pasta **não** for um repositório git, executar `git init`
- Executar `git add -A && git commit -m "docs: project scaffolding via Forge"`

### 6. Output

Após criar tudo, apresentar ao usuário:

```
Projeto "<PROJECT_NAME>" inicializado com sucesso!

Estrutura criada:
  00-discovery/     Phase 0 — Discovery
  01-product/       Phase 1 — Product
  02-design/        Phase 2 — Design
  03-architecture/  Phase 3 — Architecture
  04-specs/         Phase 4 — Specs
  05-implementation/ Phase 5 — Implementation
  06-quality/       Phase 6 — Quality
  07-deploy/        Phase 7 — Deploy

Arquivos gerados:
  CLAUDE.md          Regras do pipeline
  .status            Controle de estado (YAML)
  README.md          Descrição do projeto
  CHANGELOG.md       Histórico de mudanças
  .gitignore         Exclusões do git

Fase atual: Discovery (0/8)

Vamos começar pela Discovery? Me conte sua ideia.
```
