---
name: competitive-landscape
description: >-
  Researches and documents the competitive landscape for a project.
  Use after problem-statement.md is approved. Searches for existing solutions,
  identifies market gaps, and positions the proposed solution. Produces
  00-discovery/landscape-analysis.md.
user-invocable: false
---

# Competitive Landscape

Pesquisa e documenta o cenário competitivo: concorrentes diretos e indiretos, gaps de mercado, posicionamento proposto.

## Pré-requisitos

- `00-discovery/problem-statement.md` com status `approved`

## Processo

1. **Ler `00-discovery/problem-statement.md`** — extrair: problema, público afetado, JTBD, hipótese de solução. Estes são os eixos de comparação.
2. **Pesquisar concorrentes** usando web search:
   - Ferramentas/produtos que resolvem o **mesmo problema** (concorrentes diretos)
   - Ferramentas que resolvem **problemas adjacentes** ou atendem o mesmo público com proposta diferente (concorrentes indiretos)
   - Discussões em fóruns, comunidades, e reviews sobre o problema e soluções existentes
3. **Documentar cada concorrente** com: nome, URL, o que faz, público-alvo, modelo de negócio (free/freemium/paid/open-source), pontos fortes, pontos fracos
4. **Identificar gaps** — o que nenhum concorrente faz bem? Onde há oportunidade clara? Cruzar com os JTBDs do problem-statement.
5. **Posicionar a solução proposta** — como ela se diferencia? Qual é o ângulo defensável? Por que alguém escolheria esta solução em vez das existentes?
6. **Gerar o artefato** usando template em `templates/landscape-analysis.tmpl.md` → salvar em `00-discovery/landscape-analysis.md`
7. **Atualizar `.status`:** artifact `landscape-analysis` → `draft`

## Artefato Gerado

- `00-discovery/landscape-analysis.md`

## Validação

Antes de marcar como `draft`, verificar:

- [ ] Pelo menos 3 concorrentes diretos documentados com todos os campos preenchidos
- [ ] Pelo menos 1 concorrente indireto documentado
- [ ] Gaps identificados com clareza — cada gap referencia o que falta no mercado
- [ ] Posicionamento proposto é defensável e referencia os gaps identificados
- [ ] Todas as fontes listadas com URL válida
- [ ] Análise é coerente com o problem-statement (mesmo problema, mesmo público)
