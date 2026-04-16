---
name: adr-writer
description: >-
  Documents technical decisions as Architecture Decision Records (ADRs) in the
  Michael Nygard format. Use whenever a significant technical decision is made,
  at any phase after Architecture. Each ADR is numbered sequentially and immutable
  after approval. Produces 03-architecture/adrs/NNN-titulo.md.
user-invocable: false
---

# ADR Writer

Documenta decisões técnicas como Architecture Decision Records no formato Michael Nygard. Cada ADR é numerado sequencialmente, imutável após aprovação, e cria um rastro auditável de decisões arquiteturais. Esta skill é invocada por outras skills (como `architecture-design` e `data-model-designer`) — nunca diretamente pelo pipeline.

## Pré-requisitos

- Contexto de uma decisão técnica a ser documentada (recebido da skill ou do owner que invocou)
- Diretório `03-architecture/adrs/` deve existir (criado por `forge:init`)

## Processo

1. **Receber contexto da decisão:**
   - A skill invocadora (ex: `architecture-design`) ou o owner fornece:
     - Qual decisão precisa ser documentada
     - Contexto: por que essa decisão é necessária
     - Alternativas já consideradas (se houver)
   - Se o contexto for insuficiente, perguntar ao owner para complementar

2. **Verificar numeração sequencial:**
   - Listar arquivos existentes em `03-architecture/adrs/`
   - Extrair o maior número NNN dos arquivos existentes (formato: `NNN-titulo.md`)
   - Se nenhum ADR existir, começar com `001`
   - Próximo número = maior + 1, com zero-padding para 3 dígitos (001, 002, ..., 010, ...)

3. **Estruturar o ADR:**
   - **Status** — `proposed` (inicial), depois `accepted` ou `rejected` via review
   - **Data** — data de criação (YYYY-MM-DD)
   - **Contexto** — por que a decisão é necessária, que forças ou requisitos estão em jogo
   - **Decisão** — o que foi decidido, de forma clara e direta
   - **Alternativas** — pelo menos 2 alternativas consideradas, cada uma com prós e contras
   - **Consequências** — impactos positivos, negativos e riscos da decisão tomada
   - Se este ADR substitui um anterior: incluir "Supersedes ADR-NNN" no campo Status

4. **Gerar arquivo usando template:**
   - Usar `templates/adr.tmpl.md` como base
   - Salvar em `03-architecture/adrs/NNN-titulo-da-decisao.md`
   - O título no nome do arquivo deve ser kebab-case, descritivo (ex: `002-usar-postgresql-como-banco-principal.md`)

5. **Preservar imutabilidade:**
   - **NUNCA** editar um ADR existente com status `accepted`
   - Se uma decisão anterior precisa ser revertida ou alterada:
     - Criar um **novo** ADR com status `proposed`
     - Incluir referência: "Supersedes ADR-NNN"
     - O ADR antigo permanece inalterado como registro histórico

6. **Atualizar `.status` (se aplicável):**
   - Se este é o primeiro ADR gerado na fase de Architecture:
     - Artifact `adrs` → `draft`
   - Se `adrs` já está em `draft`, manter — o status da collection não muda por ADR individual
   - ADRs individuais não têm status no `.status` — apenas o diretório como um todo

## Artefato Gerado

- `03-architecture/adrs/NNN-titulo-da-decisao.md` (via `templates/adr.tmpl.md`)

## Validação

Antes de considerar o ADR completo, verificar:

- [ ] Numeração sequencial correta (sem gaps, sem duplicatas)
- [ ] Nome do arquivo segue formato `NNN-titulo-kebab-case.md`
- [ ] Status é `proposed` (nunca `accepted` na criação — isso vem do review)
- [ ] Contexto explica claramente o "por quê" da decisão (não apenas o "quê")
- [ ] Decisão é afirmativa e direta ("Usaremos X", não "Talvez devêssemos considerar X")
- [ ] Pelo menos 2 alternativas documentadas com prós e contras
- [ ] Consequências incluem pelo menos 1 positiva e 1 negativa/risco
- [ ] Se substitui ADR anterior: referência "Supersedes ADR-NNN" presente
- [ ] Nenhum ADR existente com status `accepted` foi editado
