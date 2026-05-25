# Subagent Dispatch — Decisões e Padrões

## Quando marcar `Subagent: yes` num step do PLAN.md

Um step vai para subagent quando satisfaz **2 dos 3** critérios:

1. **Self-contained**: o step pode ser feito sem ler arquivos fora do que está listado.
2. **Output resumível**: o que volta cabe em < 500 palavras (diff summary, não dumps).
3. **Context-heavy**: faria o main thread ler 5+ arquivos grandes só pra executar.

## Quando marcar `Subagent: no` (main thread)

- Step requer decisão de design ainda não tomada
- Step requer interação com o usuário
- Step é trivial (1-2 file edits curtos, custo do dispatch não compensa)

## Tipos de subagent

| Tipo | Quando |
|---|---|
| `general-purpose` | Default. Pode tudo, mas paga pelo overhead. |
| `Explore` | Read-only. Se o step é "encontre algo", não "modifique". |
| `Plan` | Read-only. Para repensar uma sub-parte do plano. |

## O prompt mandatory-first-read (literal)

Sempre que dispatcha:

```
Your FIRST ACTION must be: Read .dev-loop/<TASK_SLUG>/PLAN.md in full.
Then execute Step <N> as specified there.
You may read SPEC.md, research-notes.md, and any file referenced by Step <N>.

When done: return a summary of what was changed (files + diff hints) — do NOT
return full file contents. The main thread will verify and commit.
```

**Por que essa frase exata**: Anthropic blog 2026 e o workflow Superpowers documentam que omitir o mandatory-first-read em Opus 4.7 leva a drift. A frase força o subagent a ancorar no plano antes de qualquer outra leitura — sem isso, ele tende a "ir pelo título do step" e improvisar.

## Anti-padrões

1. **Subagent recebe só o título do step** — drift garantido.
2. **Subagent é instruído a também atualizar `.status`** — não. Main thread orquestra estado.
3. **Subagent recebe lista de mudanças desejadas em vez do step** — perde a relação com SPEC.md/PLAN.md.
4. **Dispatchar subagent para tomar decisão de design** — decisão pertence ao planning, não implementation.
5. **Nested subagents** — subagent dispachando subagent. Evite a não ser que o subagent já tenha acesso ao tipo (custo de contexto explode).
