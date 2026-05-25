# Padrão: Parallel Subagent Dispatch para Research

## Quando usar

- 3+ sub-perguntas independentes (sem dependência entre elas)
- Cada pergunta requer leitura de file contents (vai poluir main thread se rodada no main)
- Output esperado de cada subagent = sumário curto, não dump bruto

## Quando NÃO usar

- 1-2 perguntas simples (overhead do subagent não compensa)
- Perguntas dependentes (resposta B precisa da resposta A)
- Você já está num contexto isolado (já é subagent, sem nesting)

## Template de prompt para Explore

```
Investigate: <SUB-PERGUNTA ESPECÍFICA>

Context: estou em fase research da tarefa <TASK_NAME>. A spec completa está em
.dev-loop/<task>/SPEC.md (linhas X-Y se relevante).

Search breadth: <quick | medium | very thorough>

Return:
1. Direct answer (1-3 sentences)
2. Key file paths (with line numbers if applicable)
3. Anything surprising or non-obvious
4. Mark each finding as [DURABLE] (applies project-wide, vai pro CLAUDE.md)
   ou [TASK-SPECIFIC] (só essa tarefa, vai pro research-notes.md)

Under 400 words total.
```

## Fan-out típico

```
Main thread:
  ├─ Dispatch subagent 1 (Explore): "Como X é implementado?"
  ├─ Dispatch subagent 2 (Explore): "Onde Y é usado?"
  └─ Dispatch subagent 3 (Explore): "Padrão Z existe?"
        ↓ ↓ ↓ (parallel)
  ← Receive 3 summaries
  Consolidate into research-notes.md
  Append durables to CLAUDE.md
```

## Erros comuns

1. **Não passar contexto suficiente** — subagent não vê `CLAUDE.md` por default; dê o caminho do SPEC.md.
2. **Pedir tudo num subagent só** — mata o paralelismo. 1 sub-pergunta = 1 subagent.
3. **Pedir file dumps em vez de sumários** — subagent vira proxy de Read, não agrega valor.
4. **Esquecer de classificar [DURABLE] vs [TASK-SPECIFIC]** — sem isso, a fase de consolidação fica adivinhando.
5. **Mais de 5 subagents simultâneos** — diminishing returns; preferir 3-4 perguntas bem formuladas.
