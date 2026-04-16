---
name: problem-framing
description: >-
  Structures a raw project idea into a Problem Statement Canvas with JTBD.
  Use when starting any new project in the Forge pipeline or when the user
  describes a new idea that needs structuring. Reads user input and produces
  00-discovery/problem-statement.md.
user-invocable: false
---

# Problem Framing

Estrutura uma ideia bruta em documento analítico usando Problem Statement Canvas (IDEO) + Jobs To Be Done (Christensen).

## Pré-requisitos

- Nenhum artefato prévio (é o ponto de partida do pipeline)
- Owner deve ter descrito a ideia (mesmo que informalmente)

## Processo

1. **Ler a descrição** fornecida pelo owner
2. **Identificar gaps de informação** — fazer no MÁXIMO 5 perguntas direcionadas para preencher lacunas críticas. Não perguntar o óbvio; inferir o que for razoável a partir do contexto.
3. **Estruturar o Problem Statement Canvas:**
   - **Problema** — descrever sem mencionar solução. Foco na dor, não no remédio.
   - **Contexto** — cenário, mercado, momento, restrições externas
   - **Público afetado** — específico, nunca "todo mundo". Segmentar por papel/perfil.
   - **Dor atual / workaround** — como o público lida hoje sem a solução
   - **Impacto de não resolver** — consequências tangíveis (custo, tempo, risco)
   - **Hipótese de solução** — 1 parágrafo, é direção, não spec
   - **JTBD** — formato: "Quando [situação], eu quero [motivação], para que [resultado]"
   - **Métricas de sucesso** — KPIs quantificáveis com baseline e target
   - **Riscos iniciais** — probabilidade × impacto, com mitigação proposta
4. **Gerar o artefato** usando template em `templates/problem-statement.tmpl.md` → salvar em `00-discovery/problem-statement.md`
5. **Atualizar `.status`:** artifact `problem-statement` → `draft`

## Artefato Gerado

- `00-discovery/problem-statement.md`

## Validação

Antes de marcar como `draft`, verificar:

- [ ] Todos os campos do template preenchidos (nenhuma seção com placeholder)
- [ ] JTBD está no formato correto: "Quando [situação], eu quero [motivação], para que [resultado]"
- [ ] Pelo menos 1 KPI quantificável com baseline e target
- [ ] Pelo menos 2 riscos identificados com probabilidade e impacto
- [ ] Problema descrito sem mencionar a solução
- [ ] Público afetado é específico (nunca genérico)
