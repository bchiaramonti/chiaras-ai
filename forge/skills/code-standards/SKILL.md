---
name: code-standards
description: >-
  Defines and generates code standards for the project: linting, formatting,
  folder structure, naming conventions, commit patterns, and branching strategy.
  Use before any code is written. Produces 05-implementation/code-standards.md
  and configuration files.
user-invocable: false
---

# Code Standards

Define padrões de código completos e gera arquivos de configuração (lint, format, editorconfig) antes que qualquer código seja escrito. Lê a stack definida na arquitetura para gerar padrões e configs específicos. Consulta `references/conventions-by-stack.md` para convenções comuns por stack.

## Pré-requisitos

- `03-architecture/architecture-overview.md` com status `approved` (para saber a stack tecnológica)

## Processo

1. **Ler stack definida na arquitetura:**
   - Extrair de `architecture-overview.md`:
     - Linguagem(ns) e runtime (ex: TypeScript + Node.js, Python 3.12, Go 1.22)
     - Framework web — frontend (ex: Next.js, React, Vue) e backend (ex: Express, FastAPI, Gin)
     - Package manager (ex: npm, pnpm, bun, pip, poetry)
     - Bundler / build tool (ex: Vite, Webpack, esbuild, Turbopack)
   - Consultar `references/conventions-by-stack.md` para padrões recomendados da stack

2. **Definir e gerar configuração de linter:**
   - Escolher linter adequado à stack:
     - TypeScript/JavaScript: ESLint (flat config `eslint.config.mjs`) com regras recomendadas
     - Python: Ruff (pyproject.toml `[tool.ruff]`) ou Flake8
     - Go: `golangci-lint` (.golangci.yml)
   - Definir regras de lint:
     - Erros: regras que indicam bugs potenciais (sempre error)
     - Estilo: regras que indicam inconsistência (warn ou error conforme equipe)
     - Desabilitar regras controversas que geram mais ruído que valor
   - Gerar arquivo de configuração com comentários explicativos
   - Listar plugins recomendados (ex: `eslint-plugin-react`, `eslint-plugin-import`)

3. **Definir e gerar configuração de formatter:**
   - Escolher formatter:
     - TypeScript/JavaScript: Prettier (`.prettierrc`) ou Biome
     - Python: Ruff format ou Black (`pyproject.toml`)
     - Go: `gofmt` (built-in, zero config)
   - Definir regras de formatação:
     - Print width (80 ou 100 — justificar)
     - Tab width / indentation (2 ou 4 espaços — justificar)
     - Semicolons, trailing commas, quotes (single vs double)
   - Gerar `.prettierrc` ou equivalente + `.prettierignore` se necessário
   - Gerar `.editorconfig` (universal, independe de stack):
     - `root = true`
     - Indentation: style e size
     - End of line: `lf`
     - Charset: `utf-8`
     - Trim trailing whitespace: `true`
     - Insert final newline: `true`

4. **Definir estrutura de pastas do src/:**
   - Basear na arquitetura (C4 components) e no framework escolhido
   - Para cada camada/módulo: nome do diretório, responsabilidade, exemplos de arquivos
   - Padrões comuns (adaptar à stack):
     - Feature-based: `src/features/<feature>/` (controller, service, repository, types)
     - Layer-based: `src/controllers/`, `src/services/`, `src/repositories/`
     - Híbrido: features para domínio, layers para infra
   - Diretórios especiais:
     - `src/shared/` ou `src/common/` — código reutilizável entre features
     - `src/config/` — configuração da aplicação
     - `src/types/` ou `src/interfaces/` — tipos compartilhados
     - `tests/` — espelhar estrutura do src/ ou colocar junto (definir)
   - Documentar em árvore de diretórios com comentários

5. **Definir naming conventions:**
   - Arquivos:
     - Componentes/classes: `PascalCase.tsx`, `PascalCase.py`
     - Utilitários/funções: `kebab-case.ts`, `snake_case.py`
     - Testes: `<nome>.test.ts`, `test_<nome>.py`, `<nome>_test.go`
     - Configs: `kebab-case` (ex: `eslint.config.mjs`)
   - Código:
     - Variáveis e funções: `camelCase` (JS/TS), `snake_case` (Python/Go)
     - Classes e tipos: `PascalCase` (universal)
     - Constantes: `UPPER_SNAKE_CASE` (universal)
     - Interfaces/tipos: com ou sem prefixo `I` — definir e justificar
     - Componentes React: `PascalCase` — match com nome do arquivo
   - Database: `snake_case` para tabelas e colunas (conforme data model)
   - API: definir naming para rotas (kebab-case), query params, body fields

6. **Definir padrão de commit — Conventional Commits:**
   - Formato: `<type>(<scope>): <description>`
   - Tipos permitidos:
     - `feat` — nova funcionalidade
     - `fix` — correção de bug
     - `docs` — documentação
     - `style` — formatação (sem mudança de lógica)
     - `refactor` — refatoração (sem mudança de comportamento)
     - `test` — testes
     - `chore` — manutenção, configs, dependências
     - `perf` — performance
     - `ci` — CI/CD
   - Scopes: derivar dos nomes de features ou módulos da estrutura de pastas
   - Body: obrigatório para `feat` e `fix` com mais de 1 arquivo alterado
   - Breaking changes: `!` após tipo/scope (ex: `feat!: ...`) + nota `BREAKING CHANGE:` no body

7. **Definir estratégia de branch:**
   - Avaliar tamanho da equipe (extrair de premissas do PRD):
     - 1-3 devs: trunk-based development (branch curta + merge direto na main)
     - 4+ devs: gitflow simplificado (`main`, `develop`, `feature/*`, `hotfix/*`)
   - Definir:
     - Naming de branches: `feature/<ticket-ou-descricao>`, `fix/<descricao>`, `hotfix/<descricao>`
     - Política de merge: squash merge vs merge commit — justificar
     - Proteção de branches: `main` protegida, requer PR + review (se equipe > 1)
     - Release tagging: semantic versioning (vMAJOR.MINOR.PATCH)

8. **Gerar artefatos e atualizar `.status`:**
   - `05-implementation/code-standards.md` — documento narrativo com:
     - Stack resumida (linguagem, framework, ferramentas)
     - Linter: ferramenta, regras principais, como executar
     - Formatter: ferramenta, configuração, como executar
     - Estrutura de pastas (árvore comentada)
     - Naming conventions (tabela: contexto / padrão / exemplo)
     - Conventional Commits (tabela de tipos + exemplos)
     - Estratégia de branch (diagrama simples + regras)
     - Referência aos arquivos de configuração gerados
   - Arquivos de configuração na raiz do projeto (listados no code-standards.md):
     - Linter config (ex: `eslint.config.mjs`, `pyproject.toml [tool.ruff]`)
     - Formatter config (ex: `.prettierrc`, `.prettierignore`)
     - `.editorconfig`
   - Atualizar `.status`: artifact `code-standards` → `draft`

## Artefatos Gerados

- `05-implementation/code-standards.md`
- Arquivos de configuração na raiz do projeto (variável por stack)

## Referências

- Para convenções comuns por stack, ver [conventions-by-stack.md](references/conventions-by-stack.md)

## Validação

Antes de marcar como `draft`, verificar:

- [ ] Padrões são específicos para a stack escolhida na arquitetura (não genéricos)
- [ ] Linter config é válido e executável (sem erros de sintaxe)
- [ ] Formatter config é válido e executável
- [ ] `.editorconfig` presente com charset, indentation, EOL, trim whitespace
- [ ] Estrutura de pastas alinhada com os componentes do C4 Level 3
- [ ] Naming conventions cobrem: arquivos, variáveis, funções, classes, constantes, rotas
- [ ] Conventional Commits com tipos, scopes, e exemplos concretos
- [ ] Estratégia de branch definida com justificativa baseada no tamanho da equipe
- [ ] code-standards.md referencia todos os arquivos de configuração gerados
- [ ] Nenhuma regra contradiz decisões dos ADRs
- [ ] Scripts de lint/format com comandos de execução documentados (ex: `npm run lint`)
