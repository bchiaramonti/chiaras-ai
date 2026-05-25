# 5 Princípios para Trabalhar com Claude Opus 4.7

Destilação das fontes consultadas em 2026-05 (Anthropic blog, Tembo, CloudZero, Damian Galarza, Build This Now, ProductCompass, Firecrawl, Level Up Coding, claudefa.st) sobre como Opus 4.7 difere de modelos anteriores e o que isso muda no workflow.

## 1. Spec-first, single-turn

**Princípio**: Trate Opus 4.7 como engenheiro a quem você delega, não pair-programmer guiado linha-a-linha.

**Como aplicar**:
- Na primeira mensagem, entregue: **intent + constraints + acceptance criteria + arquivos relevantes**.
- Reduza turnos. Cada turn de clarificação adiciona overhead de raciocínio.
- Se faltar informação, faça TODAS as perguntas necessárias em UM bloco (use `AskUserQuestion`).

**Anti-padrão**: "Adicione um cache" → 5 turnos clarificando o que é "cache".

**Como o plugin aplica**: skill `writing-spec` força os 4 campos críticos antes de prosseguir; `spec-auditor` valida.

## 2. Plan-as-contract

**Princípio**: Subagents dispachados pelo executor devem ler o plano completo como **primeira ação**. Opus 4.7 segue instruções literalmente — planos vagos viram drift garantido.

**Como aplicar**:
- Escreva `PLAN.md` com passos numerados, dependências explícitas, file paths exatos.
- Inclua acceptance criteria do SPEC dentro de cada passo onde se aplicar.
- Antes de dispatchar subagent para um passo, o prompt do subagent começa com: "Read PLAN.md as your first action. Then execute step <N>."

**Anti-padrão**: "Faz a parte X" sem dizer que tem que ler o plano.

**Como o plugin aplica**: skill `implementing-plan` injeta a frase mandatory-first-read na linha 1 de cada dispatch; `plan-critic` audita literalidade.

## 3. Context engineering por isolamento

**Princípio**: Cada fase deve rodar em contexto fresco quando o trabalho é self-contained. Pesquisa pesada não pode poluir o thread principal.

**Como aplicar**:
- Pesquisa → subagent retorna **sumário**, não os file contents.
- Findings duráveis → `CLAUDE.md` (persiste entre sessões).
- Findings task-specific → `research-notes.md` no diretório da tarefa.

**Anti-padrão**: ler 30 arquivos no main thread "para entender o módulo".

**Como o plugin aplica**: skill `researching-task` dispatcha N subagents em paralelo, consolida em `research-notes.md` + apêndice em `CLAUDE.md` (durável).

## 4. Paralelismo onde compensa

**Princípio**: Subagents concorrentes têm payoff alto em **research/exploração** (tasks independentes, output resumível). Não tentar paralelizar implementação dependente.

**Como aplicar**:
- Research: 3-5 subagents paralelos, cada um com sub-pergunta específica.
- Implementação: sequencial, respeitando o grafo de dependência do `PLAN.md`.

**Anti-padrão**: "lance 5 subagents pra implementar 5 passos em paralelo" quando os passos dependem uns dos outros.

**Como o plugin aplica**: `researching-task` documenta padrão de fan-out; `implementing-plan` segue ordem do PLAN.md, paraleliza apenas steps independentes marcados `Subagent: yes`.

## 5. Verify-against-spec gate

**Princípio**: "Done" significa **acceptance criteria do SPEC.md todos verdadeiros**. Nada menos.

**Como aplicar**:
- Cada AC vira item de checklist em `VERIFY.md` com método de verificação (test/manual/inspect).
- Se algum AC falhar → não fecha. Volta para PLAN.md ou SPEC.md.
- Inclua testes automatizados + verificação manual (UI/feel) + edge cases.

**Anti-padrão**: "passou nos testes, tá pronto" sem cruzar a lista de ACs.

**Como o plugin aplica**: skill `verifying-against-spec` produz `VERIFY.md` que espelha a lista de ACs do SPEC.md 1-pra-1; gate explícito.

---

## Fontes

- [Best practices for using Claude Opus 4.7 with Claude Code (Anthropic)](https://claude.com/blog/best-practices-for-using-claude-opus-4-7-with-claude-code)
- [Claude Opus 4.7 Best Practices (claudefa.st)](https://claudefa.st/blog/guide/development/opus-4-7-best-practices)
- [Claude Code Subagents 2026 (Tembo)](https://www.tembo.io/blog/claude-code-subagents)
- [Claude Code Agents 2026 (CloudZero)](https://www.cloudzero.com/blog/claude-code-agents/)
- [Extended Context Tips (Damian Galarza)](https://www.damiangalarza.com/posts/2026-04-30-claude-opus-4-7-claude-code-tips-extended-context/)
- [Forcing Claude Code to TDD (alexop.dev)](https://alexop.dev/posts/custom-tdd-workflow-claude-code-vue/)
- [Mental Model for Claude Code (Level Up Coding)](https://levelup.gitconnected.com/a-mental-model-for-claude-code-skills-subagents-and-plugins-3dea9924bf05)
- [Extend Claude with skills (Claude Code Docs)](https://code.claude.com/docs/en/skills)
- [Create custom subagents (Claude Code Docs)](https://code.claude.com/docs/en/sub-agents)
