---
name: product-definition
description: >-
  Transforms a validated problem into a complete Product Requirements Document
  with personas, user stories, and MoSCoW prioritization. Use after Discovery
  phase is complete. Produces 01-product/prd.md and 01-product/user-story-map.md.
user-invocable: false
---

# Product Definition

Transforma problema validado em PRD completo com visão, personas, user stories e priorização MoSCoW. Também gera o User Story Map com backbone, detalhamento por atividade e linha de corte MVP.

## Pré-requisitos

- `00-discovery/problem-statement.md` com status `approved`
- `00-discovery/landscape-analysis.md` com status `approved`

## Processo

1. **Ler todos os artefatos de Discovery:**
   - `00-discovery/problem-statement.md` — extrair: problema, público, JTBDs, KPIs, riscos
   - `00-discovery/landscape-analysis.md` — extrair: gaps, posicionamento, concorrentes
2. **Definir visão do produto:**
   - One-liner (max 15 palavras): o que é + para quem + diferencial
   - Parágrafo expandido (3-5 frases): visão completa com contexto
3. **Construir personas** (máximo 3 para MVP):
   - Nome fictício + papel
   - Contexto / cenário de uso
   - Dores (referenciar problem-statement)
   - Objetivos (referenciar JTBDs)
   - Nível técnico / familiaridade
4. **Mapear user stories** por persona, agrupadas por épico/atividade:
   - Formato obrigatório: "Como [persona], quero [ação], para [benefício]"
   - Cada story deve ser independente e testável
   - Agrupar em épicos que representam atividades do usuário
5. **Priorizar usando MoSCoW:**
   - **Must** — sem isso o MVP não faz sentido
   - **Should** — importante mas pode ser simplificado
   - **Could** — desejável, baixo esforço
   - **Won't** — explicitamente fora do MVP (mas pode entrar depois)
6. **Separar escopo:** MVP (Must + Should) vs. versão futura (Could + Won't)
7. **Definir KPIs de produto** — métricas de sucesso vinculadas às personas e stories
8. **Listar restrições, premissas e fora de escopo** — ser explícito sobre o que NÃO será feito
9. **Gerar artefatos:**
   - PRD via `templates/prd.tmpl.md` → salvar em `01-product/prd.md`
   - User Story Map via `templates/user-story-map.tmpl.md` → salvar em `01-product/user-story-map.md`
10. **Atualizar `.status`:** artifacts `prd` e `user-story-map` → `draft`

## Artefatos Gerados

- `01-product/prd.md` (via `templates/prd.tmpl.md`)
- `01-product/user-story-map.md` (via `templates/user-story-map.tmpl.md`)

## Validação

Antes de marcar como `draft`, verificar:

- [ ] Visão clara: 1 frase (max 15 palavras) + 1 parágrafo expandido
- [ ] Pelo menos 1 persona com todos os campos preenchidos (nome, papel, contexto, dores, objetivos, nível técnico)
- [ ] Todas as user stories no formato "Como [persona], quero [ação], para [benefício]"
- [ ] MoSCoW aplicado a cada story (nenhuma sem prioridade)
- [ ] KPIs de produto quantificáveis e vinculados a personas
- [ ] Fora de escopo explicitamente listado (nunca vazio)
- [ ] User Story Map com backbone coerente com os épicos do PRD
- [ ] Linha de corte MVP claramente definida no User Story Map
- [ ] JTBDs do problem-statement estão refletidos nas user stories
- [ ] Gaps da landscape-analysis estão endereçados no posicionamento do produto
