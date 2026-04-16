---
name: user-flow-mapping
description: >-
  Transforms user stories into visual navigation flows with Mermaid diagrams.
  Use after Product phase is complete. Maps user journeys including entry points,
  screens, actions, transitions, and error/empty states. Produces
  02-design/user-flows.md and 02-design/user-flows.mermaid.
user-invocable: false
---

# User Flow Mapping

Transforma user stories em fluxos visuais de navegação com diagramas Mermaid. Cada fluxo mapeia a jornada do usuário desde o ponto de entrada, passando por telas e ações, até o ponto de saída — incluindo estados especiais (empty, loading, erro, sucesso).

## Pré-requisitos

- `01-product/prd.md` com status `approved`
- `01-product/mvp-definition.md` com status `approved`

## Processo

1. **Ler todos os artefatos de Product:**
   - `01-product/prd.md` — extrair: personas, épicos, user stories (Must + Should), KPIs
   - `01-product/mvp-definition.md` — extrair: escopo MVP, appetite, riscos, limites de corte
   - `01-product/user-story-map.md` (se existir) — extrair: backbone, atividades, linha de corte

2. **Mapear fluxos por épico:**
   - Para cada épico do MVP, identificar o fluxo principal (happy path)
   - Nomear cada fluxo com padrão: `FLOW-<NNN>: <Nome Descritivo>`
   - Vincular cada fluxo às user stories que ele cobre (IDs do PRD)

3. **Detalhar cada fluxo passo a passo:**
   - Ponto de entrada: como o usuário chega (URL, botão, redirect, deeplink)
   - Telas/estados: cada parada do fluxo (com nome de rota sugerido)
   - Ações do usuário por tela: o que o usuário pode fazer em cada ponto
   - Transições: o que conecta uma tela à próxima (submit, click, auto-redirect)
   - Ponto de saída: onde o fluxo termina (confirmação, dashboard, logout)

4. **Mapear estados especiais para cada tela:**
   - **Empty state** — sem dados para exibir (primeiro uso, lista vazia)
   - **Loading** — aguardando resposta (skeleton, spinner, placeholder)
   - **Erro** — falha de rede, validação, permissão, 404
   - **Sucesso** — confirmação visual, toast, redirect

5. **Gerar diagramas Mermaid:**
   - Usar `flowchart TD` (top-down) como direção padrão
   - Um diagrama por épico/fluxo principal
   - Nós: retângulos para telas, losangos para decisões, retângulos arredondados para início/fim
   - Arestas: labels descritivos nas transições
   - Subgraphs para agrupar telas de um mesmo contexto (ex: checkout, onboarding)
   - Consolidar todos os diagramas em `02-design/user-flows.mermaid`

6. **Documentar em texto:**
   - Gerar o documento narrativo via `templates/user-flows.tmpl.md`
   - Salvar em `02-design/user-flows.md`
   - Cada fluxo deve ser auto-explicativo mesmo sem o diagrama

7. **Atualizar `.status`:**
   - Artifact `user-flows` → `draft`
   - Artifact `user-flows-diagram` → `draft`

## Artefatos Gerados

- `02-design/user-flows.md` (via `templates/user-flows.tmpl.md`)
- `02-design/user-flows.mermaid`

## Validação

Antes de marcar como `draft`, verificar:

- [ ] Toda user story "Must Have" do PRD tem pelo menos um fluxo mapeado
- [ ] Toda user story "Should Have" do MVP tem fluxo mapeado ou justificativa de exclusão
- [ ] Cada fluxo tem ponto de entrada e ponto de saída explícitos
- [ ] Cada tela tem pelo menos 1 ação do usuário documentada
- [ ] Estados especiais (empty, loading, erro, sucesso) identificados para cada tela principal
- [ ] Diagramas Mermaid renderizam sem erros de sintaxe
- [ ] Nomes de rotas/telas são consistentes entre texto e diagrama
- [ ] Fluxos são navegáveis: nenhum beco sem saída (exceto estados de erro com retry)
- [ ] Personas do PRD estão mapeadas nos fluxos correspondentes
- [ ] Épicos do PRD estão representados como fluxos distintos
