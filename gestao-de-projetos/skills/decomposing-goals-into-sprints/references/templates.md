# Templates de Output

Dois templates completos com exemplos preenchidos. Copie, adapte e gere para cada projeto.

---

## 1. Template: ROADMAP.md

```markdown
# Roadmap: [Nome do Projeto]

## Big Goal

> [QUEM] terá [O QUE] funcionando até [QUANDO], resultando em [IMPACTO].

## Visão Geral

| Sprint | Título | Período | Produto | Responsável | Status |
|--------|--------|---------|---------|-------------|--------|
| S0 | [Título](sprints/SPRINT-00.md) | DD/MM → DD/MM | [Entregável concreto] | [Nome] | ⬚ |
| S1 | [Título](sprints/SPRINT-01.md) | DD/MM → DD/MM | [Entregável concreto] | [Nome] | ⬚ |
| ... | | | | | |

**Legenda:** ⬚ Pendente · 🔵 Em andamento · ✅ Concluído · 🔴 Bloqueado

## Dependências

| Sprint | Depende de | Desbloqueia |
|--------|-----------|-------------|
| S0 | — | S1, S2 |
| S1 | S0 | S3 |
| S2 | S0 | S3 |
| S3 | S1, S2 | S4 |
| S4 | S3 | — |

## Riscos

| # | Risco | Probabilidade | Impacto | Contramedida |
|---|-------|--------------|---------|-------------|
| R1 | [Descrição] | Alta/Média/Baixa | Alto/Médio/Baixo | [Ação preventiva] |
| R2 | [Descrição] | | | |

## Decisões de Escopo

| Decisão | Justificativa |
|---------|--------------|
| [O que foi incluído/excluído] | [Por quê] |
```

### Exemplo preenchido

```markdown
# Roadmap: Padronização dos Rituais de Gestão

## Big Goal

> A equipe de Performance terá rituais de gestão padronizados para 6 funis
> até mai/2026, reduzindo 80% do tempo em reports manuais.

## Visão Geral

| Sprint | Título | Período | Produto | Responsável | Status |
|--------|--------|---------|---------|-------------|--------|
| S0 | [Fundação](sprints/SPRINT-00.md) | 24/fev → 07/mar | Mapeamento AS-IS completo | Bruno | ⬚ |
| S1 | [Investimentos](sprints/SPRINT-01.md) | 10/mar → 21/mar | Ritual N2 de Investimentos rodando | Bruno + Gestor | ⬚ |
| S2 | [Crédito](sprints/SPRINT-02.md) | 24/mar → 04/abr | Ritual N2 de Crédito rodando | Bruno + Gestor | ⬚ |
| S3 | [Seguros](sprints/SPRINT-03.md) | 07/abr → 18/abr | Ritual N2 de Seguros rodando | Bruno + Gestor | ⬚ |
| S4 | [Consolidação](sprints/SPRINT-04.md) | 21/abr → 02/mai | N3 + funis restantes + manual | Performance | ⬚ |

## Dependências

| Sprint | Depende de | Desbloqueia |
|--------|-----------|-------------|
| S0 | — | S1, S2, S3 |
| S1 | S0 | S4 |
| S2 | S0 | S4 |
| S3 | S0 | S4 |
| S4 | S1, S2, S3 | — |

## Riscos

| # | Risco | Probabilidade | Impacto | Contramedida |
|---|-------|--------------|---------|-------------|
| R1 | Baixa adesão dos gestores | Alta | Crítico | Sponsor valida cadência antes do rollout |
| R2 | Dados do CRM incompletos | Média | Alto | Sprint 0 inclui limpeza de dados |
| R3 | Performance sobrecarregada | Baixa | Médio | Priorizar 1 funil por sprint |

## Decisões de Escopo

| Decisão | Justificativa |
|---------|--------------|
| Banking, Câmbio e Prev ficam no S4 | Menor volume — padronizar após aprendizado dos 3 maiores |
| Ritual N1 fora do escopo | Comitê Executivo tem dinâmica própria, não cabe em sprint |
```

---

## 2. Template: SPRINT-NN.md

```markdown
# Sprint [N] — [Título]

**Período:** Sem. X-Y: DD/MM → DD/MM
**Responsável:** [Nome/Equipe]
**Status:** ⬚ Pendente

## Objetivo

[1-2 frases descrevendo o que este sprint busca alcançar.]

## Produto do Sprint

> [O que estará **rodando/publicado/validado** ao final — não artefato intermediário.]

## Depende de

- Sprint [N-1] — [Título] (motivo da dependência)

## Tarefas

### [Grupo Lógico 1]

- [ ] **Verbo objeto** — detalhe (arquivo, ferramenta, comportamento)
- [ ] **Verbo objeto** — detalhe
- [ ] **Verbo objeto** — detalhe

### [Grupo Lógico 2]

- [ ] **Verbo objeto** — detalhe
- [ ] **Verbo objeto** — detalhe

### Validação

- [ ] **Validar [critério]** — como testar
- [ ] **Confirmar [critério]** — com quem

## Critérios de Aceite

- [ ] [Critério objetivo e verificável]
- [ ] [Critério objetivo e verificável]
- [ ] [Critério objetivo e verificável]

## Notas

[Decisões tomadas, riscos específicos, aprendizados durante execução.]
```

### Exemplo preenchido

```markdown
# Sprint 0 — Fundação

**Período:** Sem. 1-2: 24/fev → 07/mar
**Responsável:** Bruno (Performance)
**Status:** ⬚ Pendente

## Objetivo

Mapear todos os processos atuais de gestão dos 6 funis e produzir diagnóstico
consolidado para embasar a padronização.

## Produto do Sprint

> Documento de mapeamento AS-IS com fluxos, dores e oportunidades por funil,
> validado pela diretoria.

## Depende de

- Nenhuma dependência (primeiro sprint).

## Tarefas

### Diagnóstico

- [ ] **Entrevistar 8 gestores** — roteiro semi-estruturado, 30min cada
- [ ] **Mapear fluxos AS-IS** — um diagrama por funil (Investimentos, Crédito, Seguros, Banking, Câmbio, Prev)
- [ ] **Levantar KPIs atuais** — extrair do BI quais métricas cada gestor acompanha
- [ ] **Identificar dores e gaps** — consolidar em matriz (dor × impacto × frequência)

### Dados

- [ ] **Auditar qualidade do CRM** — checar completude dos campos críticos por funil
- [ ] **Limpar dados inconsistentes** — corrigir registros com campos obrigatórios vazios
- [ ] **Documentar fontes de dados** — mapear origem de cada KPI (CRM, BI, Cowork)

### Validação

- [ ] **Apresentar diagnóstico à diretoria** — reunião de 1h com deck de 10 slides
- [ ] **Coletar feedback e ajustes** — registrar decisões no CHANGELOG

## Critérios de Aceite

- [ ] 6 funis mapeados com fluxo AS-IS documentado
- [ ] Matriz de dores consolidada e priorizada
- [ ] Diretoria validou diagnóstico (ata de reunião)
- [ ] Dados do CRM auditados com relatório de qualidade

## Notas

[Preencher durante/após execução.]
```

---

## Checklist de Geração

Ao gerar os arquivos para um projeto, confirme:

- [ ] ROADMAP.md tem Big Goal em 1 frase?
- [ ] Tabela de sprints tem links para cada SPRINT-NN.md?
- [ ] Sprint 0 é fundação/diagnóstico?
- [ ] Último sprint inclui consolidação/handoff?
- [ ] Dependências não formam ciclo?
- [ ] Todos os SPRINT-NN.md têm produto concreto?
- [ ] Tarefas começam com verbo em negrito?
- [ ] Max 15 tarefas por sprint?
- [ ] Critérios de aceite são verificáveis?
- [ ] Riscos têm contramedidas?
