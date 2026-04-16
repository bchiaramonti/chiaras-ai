# Conventions by Stack — Guia de Referência

> Referência para a skill `code-standards`.
> Padrões comuns por stack tecnológica, configs típicos de linter/formatter, naming conventions, e estrutura de pastas recomendada.

---

## Sumário

1. [Node.js / TypeScript](#1-nodejs--typescript)
2. [Python](#2-python)
3. [Go](#3-go)
4. [Full-Stack (Frontend + Backend)](#4-full-stack-frontend--backend)
5. [Configurações Universais](#5-configurações-universais)

---

## 1. Node.js / TypeScript

### Linter — ESLint (Flat Config)

**Arquivo:** `eslint.config.mjs`

Plugins recomendados:

| Plugin | Propósito |
|--------|-----------|
| `@typescript-eslint/eslint-plugin` | Regras específicas para TypeScript |
| `eslint-plugin-import` | Ordenação e validação de imports |
| `eslint-plugin-react` | Regras para React (se frontend) |
| `eslint-plugin-react-hooks` | Regras de hooks do React |
| `eslint-plugin-jsx-a11y` | Acessibilidade em JSX |

Regras principais:

```js
// eslint.config.mjs (flat config)
import tseslint from 'typescript-eslint';
import pluginImport from 'eslint-plugin-import';

export default tseslint.config(
  ...tseslint.configs.recommended,
  {
    rules: {
      // Erros (potenciais bugs)
      'no-unused-vars': 'off',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'warn',
      'no-console': ['warn', { allow: ['warn', 'error'] }],

      // Estilo (consistência)
      '@typescript-eslint/consistent-type-imports': 'error',
      'import/order': ['error', {
        'groups': ['builtin', 'external', 'internal', 'parent', 'sibling'],
        'newlines-between': 'always',
        'alphabetize': { order: 'asc' }
      }],
    }
  }
);
```

### Formatter — Prettier

**Arquivo:** `.prettierrc`

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "always",
  "endOfLine": "lf"
}
```

**`.prettierignore`:**
```
node_modules/
dist/
build/
coverage/
*.min.js
```

### Naming Conventions

| Contexto | Padrão | Exemplo |
|----------|--------|---------|
| Arquivos — componentes | `PascalCase.tsx` | `UserProfile.tsx` |
| Arquivos — utilitários | `kebab-case.ts` | `format-date.ts` |
| Arquivos — testes | `<nome>.test.ts` | `format-date.test.ts` |
| Arquivos — tipos | `kebab-case.types.ts` | `user.types.ts` |
| Variáveis / funções | `camelCase` | `getUserById` |
| Classes / tipos / interfaces | `PascalCase` | `UserRepository` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Enums | `PascalCase` (members também) | `UserRole.Admin` |
| Componentes React | `PascalCase` | `<UserCard />` |
| Hooks React | `camelCase` com prefixo `use` | `useAuth()` |

### Estrutura de Pastas (Feature-Based)

```
src/
├── app/                  # Entry point, providers, routing
├── features/             # Feature modules
│   ├── auth/
│   │   ├── components/   # UI components desta feature
│   │   ├── hooks/        # Custom hooks
│   │   ├── services/     # API calls, business logic
│   │   ├── types/        # Tipos e interfaces
│   │   └── index.ts      # Public API da feature
│   └── users/
│       └── ...
├── shared/               # Código reutilizável
│   ├── components/       # UI components genéricos
│   ├── hooks/            # Hooks genéricos
│   ├── utils/            # Funções utilitárias
│   └── types/            # Tipos compartilhados
├── config/               # App config, env vars
├── lib/                  # Third-party wrappers
└── tests/                # Test utilities, fixtures, mocks
```

### Package Manager

| Manager | Quando usar |
|---------|------------|
| `pnpm` | Monorepos, projetos que priorizam performance de install e disk space |
| `npm` | Projetos simples, máxima compatibilidade |
| `bun` | Projetos que querem runtime + bundler + package manager unificado |

---

## 2. Python

### Linter — Ruff

**Arquivo:** `pyproject.toml`

```toml
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort (import ordering)
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "SIM",  # flake8-simplify
    "RUF",  # Ruff-specific rules
]
ignore = [
    "E501",  # line-length handled by formatter
]

[tool.ruff.lint.isort]
known-first-party = ["app"]
```

### Formatter — Ruff Format

```toml
[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"
```

### Naming Conventions

| Contexto | Padrão | Exemplo |
|----------|--------|---------|
| Arquivos / módulos | `snake_case.py` | `user_service.py` |
| Arquivos — testes | `test_<nome>.py` | `test_user_service.py` |
| Variáveis / funções | `snake_case` | `get_user_by_id` |
| Classes | `PascalCase` | `UserRepository` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Pacotes | `snake_case` (sem hífens) | `my_package` |
| Métodos privados | `_snake_case` | `_validate_input` |
| "Dunder" methods | `__snake_case__` | `__init__` |

### Estrutura de Pastas

```
src/
├── app/                  # Entry point, FastAPI/Flask app
│   ├── main.py
│   └── config.py
├── features/             # Feature modules
│   ├── auth/
│   │   ├── router.py     # Endpoints
│   │   ├── service.py    # Business logic
│   │   ├── repository.py # Data access
│   │   ├── schemas.py    # Pydantic models
│   │   └── models.py     # ORM models
│   └── users/
│       └── ...
├── shared/               # Código reutilizável
│   ├── database.py       # DB connection, session
│   ├── dependencies.py   # FastAPI dependencies
│   ├── exceptions.py     # Custom exceptions
│   └── utils.py          # Funções utilitárias
├── migrations/           # Alembic migrations
└── tests/
    ├── conftest.py       # Fixtures compartilhadas
    ├── features/
    │   ├── auth/
    │   └── users/
    └── shared/
```

### Gerenciamento de Dependências

| Ferramenta | Quando usar |
|-----------|------------|
| `poetry` | Lock file, virtual env integrado, publicação no PyPI |
| `pip` + `requirements.txt` | Máxima simplicidade, containers Docker |
| `uv` | Performance de install, drop-in replacement para pip |

---

## 3. Go

### Linter — golangci-lint

**Arquivo:** `.golangci.yml`

```yaml
linters:
  enable:
    - errcheck      # Erros não tratados
    - govet         # Código suspeito
    - staticcheck   # Análise estática avançada
    - unused        # Código não utilizado
    - gosimple      # Simplificações sugeridas
    - ineffassign   # Atribuições ineficientes
    - gocritic      # Padrões problemáticos
    - gofumpt       # Formatação estrita
    - misspell      # Typos em comentários/strings

linters-settings:
  govet:
    check-shadowing: true
  gocritic:
    enabled-tags:
      - diagnostic
      - style
      - performance

run:
  timeout: 5m
```

### Formatter — gofumpt

Go tem `gofmt` built-in. `gofumpt` adiciona regras adicionais (superset de `gofmt`):

```bash
# Sem arquivo de configuração — gofumpt é zero-config
gofumpt -w .
```

### Naming Conventions

| Contexto | Padrão | Exemplo |
|----------|--------|---------|
| Arquivos | `snake_case.go` | `user_handler.go` |
| Arquivos — testes | `<nome>_test.go` | `user_handler_test.go` |
| Variáveis / funções (exportadas) | `PascalCase` | `GetUserByID` |
| Variáveis / funções (privadas) | `camelCase` | `validateInput` |
| Pacotes | `lowercase` (uma palavra, sem underscore) | `auth`, `users` |
| Interfaces | `PascalCase` + sufixo `-er` | `Reader`, `UserStore` |
| Constantes | `PascalCase` (exportadas) ou `camelCase` (privadas) | `MaxRetryCount` |
| Acrônimos | Manter maiúsculas completas | `HTTPClient`, `userID` |

### Estrutura de Pastas

```
cmd/
├── server/
│   └── main.go           # Entry point
internal/                  # Código privado do projeto
├── auth/
│   ├── handler.go         # HTTP handlers
│   ├── service.go         # Business logic
│   ├── repository.go      # Data access
│   └── models.go          # Domain models
├── users/
│   └── ...
├── shared/
│   ├── database/          # DB connection
│   ├── middleware/         # HTTP middleware
│   └── config/            # App config
pkg/                       # Código reutilizável (público)
├── httputil/
└── validator/
migrations/                # SQL migrations
tests/                     # Integration tests (e2e)
```

---

## 4. Full-Stack (Frontend + Backend)

Quando o projeto tem frontend e backend separados (monorepo ou repos distintos):

### Monorepo (pnpm workspaces / Turborepo)

```
apps/
├── web/                   # Frontend (Next.js, React, etc.)
│   ├── src/
│   └── package.json
├── api/                   # Backend (Express, FastAPI, etc.)
│   ├── src/
│   └── package.json
packages/
├── shared/                # Código compartilhado (types, utils)
│   ├── src/
│   └── package.json
├── ui/                    # Design system / component library
│   ├── src/
│   └── package.json
├── eslint-config/         # Shared ESLint config
└── tsconfig/              # Shared TypeScript config
turbo.json                 # Turborepo config
pnpm-workspace.yaml
```

### Repos Separados

Quando frontend e backend são repos independentes, cada um segue as convenções da sua stack (seções 1-3 acima). Pontos de atenção:

- **Tipos compartilhados:** gerar tipos do backend (OpenAPI → TypeScript) em vez de manter duplicados
- **API contract:** definir esquema OpenAPI no backend, consumir no frontend
- **Naming consistency:** mesmos nomes de entidades no frontend e backend (alinhados com data model)

---

## 5. Configurações Universais

### .editorconfig

**Aplicável a TODAS as stacks:**

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 2
trim_trailing_whitespace = true
insert_final_newline = true

[*.py]
indent_size = 4

[*.go]
indent_style = tab
indent_size = 4

[*.md]
trim_trailing_whitespace = false

[Makefile]
indent_style = tab
```

### Conventional Commits — Referência Rápida

| Tipo | Quando usar | Exemplo |
|------|------------|---------|
| `feat` | Nova funcionalidade | `feat(auth): add password reset flow` |
| `fix` | Correção de bug | `fix(users): prevent duplicate email registration` |
| `docs` | Documentação | `docs: update API endpoint descriptions` |
| `style` | Formatação sem mudança de lógica | `style: apply prettier formatting` |
| `refactor` | Refatoração sem mudança de comportamento | `refactor(auth): extract token validation to service` |
| `test` | Testes | `test(users): add integration tests for CRUD` |
| `chore` | Manutenção, configs | `chore: update eslint to v9` |
| `perf` | Performance | `perf(db): add index on users.email` |
| `ci` | CI/CD | `ci: add lint check to PR pipeline` |

### Estratégias de Branch

| Estratégia | Equipe | Fluxo |
|-----------|--------|-------|
| **Trunk-based** | 1-3 devs | `main` ← `feature/xxx` (vida curta, < 2 dias). Sem `develop`. Feature flags para código incompleto. |
| **Gitflow simplificado** | 4+ devs | `main` ← `develop` ← `feature/xxx`. Release branches opcionais. Hotfixes direto da `main`. |

Naming de branches:

```
feature/<ticket-ou-descricao>   # Ex: feature/user-auth
fix/<descricao>                 # Ex: fix/duplicate-email-check
hotfix/<descricao>              # Ex: hotfix/login-crash
release/<versao>                # Ex: release/1.2.0 (se gitflow)
```

### .gitignore — Entradas Comuns

```gitignore
# Dependencies
node_modules/
__pycache__/
*.pyc
vendor/

# Build
dist/
build/
.next/
out/

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Coverage
coverage/
htmlcov/
.coverage
```
