---
description: Inicializa o dev-loop para uma nova tarefa (cria diretório, status, e invoca writing-spec)
argument-hint: <nome-da-tarefa>
disable-model-invocation: true
---

# /dev-loop:start

Inicializa o loop de desenvolvimento para uma nova tarefa.

## Argumento

- `$ARGUMENTS` = nome completo da tarefa (todos os tokens passados após o command), será convertido para `kebab-case` automaticamente

## Processo

1. **Slug**: converter `$ARGUMENTS` para `kebab-case` (lowercase, espaços→hífen, sem acentos, sem caracteres especiais).
2. **Verificar projeto**: ler `.dev-loop/.status` se existir. Se não existir OU `project_initialized: false`, invocar a skill `scaffolding-project` ANTES de prosseguir.
3. **Criar diretório**: `mkdir -p .dev-loop/<slug>/`.
4. **Atualizar `.dev-loop/.status`**:
   - `current_task: <slug>`
   - `tasks.<slug>` = `{ phase: "spec", started_at: <today>, artifacts: { "SPEC.md": null, "research-notes.md": null, "PLAN.md": null, "VERIFY.md": null } }`
5. **Invocar skill `writing-spec`** passando o nome da tarefa e qualquer contexto adicional que o usuário tenha dado na linha do comando.

## Exemplo

```
/dev-loop:start adicionar cache Redis nos endpoints de leitura
```

→ slug `adicionar-cache-redis-nos-endpoints-de-leitura` → cria `.dev-loop/<slug>/` → fase `spec` → invoca `writing-spec` para começar o SPEC.md.

## Pós-condição

- `.dev-loop/<slug>/` existe
- `.dev-loop/.status` aponta para a tarefa com fase `spec`
- Skill `writing-spec` foi invocada — usuário começa a preencher SPEC.md interativamente

## Notas

- Se já existe tarefa com mesmo slug, perguntar ao usuário: retomar (continuar do phase atual) ou recriar (apagar e começar de novo).
- Se `.dev-loop/` está no `.gitignore` e o usuário ainda não decidiu, perguntar (a skill `scaffolding-project` cuida disso, mas re-confirmar não é caro).
