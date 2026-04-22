---
description: Imprime o .md canonico do planner do dia no chat, em code fence, para debug e inspeçao rapida.
---

Le `~/Documents/brain/0-inbox/plan-review/daily/YYYY/MM/daily-YYYY-MM-DD.md` e imprime o conteudo integral em code fence markdown no chat.

Util para:

- Ver o estado atual do planejamento antes de editar manualmente
- Diagnosticar problemas de parsing no `/planner sync` (ver o YAML/body exatamente como o sync vai consumir)
- Conferir o historico em `edits[]` apos multiplas ediçoes no dia
- Copiar o .md para outro editor ou compartilhar snippet

## Fluxo

1. Resolver data atual em `YYYY-MM-DD` (America/Sao_Paulo)
2. Construir path: `~/Documents/brain/0-inbox/plan-review/daily/YYYY/MM/daily-YYYY-MM-DD.md`
3. Se arquivo nao existe → responder: `"O daily de {data} ainda nao foi gerado. Rode generating-daily-planner."` e encerrar
4. Ler o arquivo (UTF-8)
5. Imprimir o conteudo no chat dentro de um code fence:

   ~~~
   ```markdown
   <conteudo integral do .md>
   ```
   ~~~

6. Abaixo do code fence, imprimir um resumo curto:
   - `date`, `weekday`, `iso_week` do frontmatter
   - Contagem de: MITs (3 fixo), eventos de agenda, tasks, frentes no workspace
   - Quantidade de entradas em `edits[]` (se houver) com timestamp da ultima
   - Aviso se detectar algum campo obrigatorio ausente (sem abortar — so sinalizar)

## Nunca fazer

- Escrever ou modificar o .md — comando e read-only
- Chamar MCPs — tudo vive no arquivo local
- Invocar a skill ou o agente Pfeffer
- Tentar renderizar HTML — isso e tarefa do `/sync`

## Tempo esperado

<2s. Um unico `read_file` + formataçao de resumo.
