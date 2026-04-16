---
name: wireframe-spec
description: >-
  Generates textual wireframe specifications for each screen identified in user flows.
  Use after user-flows are documented. Defines layout elements, information hierarchy,
  user actions, and all visual states (empty, loading, error, success) per screen.
  Identifies reusable components across screens. Produces files in 02-design/wireframes/.
user-invocable: false
---

# Wireframe Spec

Gera especificações textuais de wireframe para cada tela identificada nos user flows. Cada wireframe define o propósito da tela, sua estrutura de layout, hierarquia de informação, ações disponíveis ao usuário e todos os estados visuais possíveis — servindo como blueprint para implementação e para a skill `design-system-bootstrap`.

## Pré-requisitos

- `02-design/user-flows.md` com status `draft` ou `approved`

## Processo

1. **Ler user flows e extrair inventário de telas:**
   - Abrir `02-design/user-flows.md`
   - Identificar todas as telas mencionadas nos fluxos (coluna "Tela / Estado" das tabelas de passos)
   - Para cada tela, anotar:
     - Fluxo(s) onde aparece (IDs: FLOW-001, FLOW-002, ...)
     - User stories atendidas
     - Rota sugerida (se definida no user flow)
     - Ações do usuário já mapeadas no fluxo
   - Consolidar telas duplicadas (mesma tela referenciada em múltiplos fluxos)

2. **Definir estrutura de layout para cada tela:**
   - **Header:** logo, navegação, breadcrumbs, ações globais (perfil, notificações, logout)
   - **Conteúdo principal:** elementos centrais da tela, organizados por hierarquia de informação
   - **Sidebar** (se aplicável): filtros, navegação secundária, widgets auxiliares
   - **Footer:** links institucionais, copyright, versão
   - Descrever a hierarquia visual: o que o usuário vê primeiro, segundo, terceiro
   - Indicar a disposição geral dos blocos (ex: header fixo + conteúdo scrollável + sidebar à direita)

3. **Detalhar ações do usuário por tela:**
   - Listar todas as interações possíveis: cliques, inputs, submits, toggles, drag-and-drop, gestos
   - Para cada ação, definir:
     - Elemento que dispara (botão, link, campo, ícone)
     - Resultado esperado (navegação, modal, feedback visual, request ao backend)
     - Condição de disponibilidade (sempre, condicional, autenticado, role-specific)

4. **Mapear estados visuais para cada tela:**
   - **Empty state:** primeiro uso, lista/tabela sem dados, busca sem resultado — incluir mensagem e CTA
   - **Loading state:** skeleton, spinner ou placeholder — definir o que carrega e feedback visual
   - **Error state:** tipo de erro (validação, rede, permissão, 404), mensagem, ação de recuperação
   - **Success state:** confirmação visual (toast, banner, modal, redirect), próximo passo do usuário
   - **Disabled state** (se aplicável): elementos desabilitados, tooltip explicativo

5. **Identificar componentes reutilizáveis entre telas:**
   - Comparar layouts de todas as telas
   - Extrair padrões repetidos: cards, tabelas, modais, formulários, empty states, headers
   - Nomear cada componente reutilizável com nome consistente (ex: `DataTable`, `EmptyState`, `ConfirmModal`)
   - Anotar em quais telas cada componente aparece

6. **Gerar 1 arquivo por tela usando template:**
   - Usar `templates/wireframe-screen.tmpl.md` como base
   - Salvar em `02-design/wireframes/<nome-da-tela>.md`
   - Nomear arquivos com kebab-case derivado do nome da tela (ex: `dashboard-principal.md`, `login.md`)
   - Cada arquivo deve ser auto-suficiente: compreensível sem ler outros wireframes

7. **Atualizar `.status`:**
   - Artifact `wireframes` → `draft`

## Artefatos Gerados

- `02-design/wireframes/<nome-da-tela>.md` — 1 arquivo por tela (via `templates/wireframe-screen.tmpl.md`)

## Validação

Antes de marcar como `draft`, verificar:

- [ ] Toda tela mencionada nos user flows tem um wireframe correspondente
- [ ] Nenhum wireframe existe para tela não referenciada nos user flows
- [ ] Todos os 4 estados visuais (empty, loading, error, success) estão documentados para cada tela
- [ ] Toda ação do usuário tem elemento disparador e resultado esperado definidos
- [ ] Layout de cada tela tem pelo menos header e conteúdo principal descritos
- [ ] Hierarquia de informação está explícita (o que o usuário vê primeiro)
- [ ] Componentes reutilizáveis estão identificados e nomeados consistentemente entre telas
- [ ] Nomes dos arquivos seguem kebab-case e correspondem às rotas dos user flows
- [ ] Referências a fluxos usam IDs corretos (FLOW-001, FLOW-002, ...)
- [ ] User stories vinculadas são IDs válidos do PRD
