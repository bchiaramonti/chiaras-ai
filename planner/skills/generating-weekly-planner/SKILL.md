---
name: generating-weekly-planner
description: Gera o weekly planner pessoal executivo de Bruno em HTML seguindo tres fases aplicadas ao horizonte semanal (seg-sex). Fase 1 (Extrair) le dados via Google Calendar MCP (5 dias), ClickUp MCP (tarefas da semana + workspace M7 com status=atrasada/bloqueada no workspace inteiro para alimentar Riscos), TrainingPeaks MCP (peso, TSS, sono, TSB - pos v1.5.0), metas Q2 (ClickUp goals ou filesystem brain/3-resources) e retrospectiva S-1 perguntada ao usuario. Fase 2 (Planejar) aplica 8 regras destiladas de Hyatt Weekly Preview (Tese + Big 3 + Critério), Cal Newport Time-Block (Orquestra dos 5 dias com deep work blocks), 4DX (Critério de vitória), Kahneman Pre-mortem (Riscos com mitigação pronta) e Newport Shutdown Reverso (Preflight com 4 perguntas editoriais), gerando o Insight cruzando frameworks de brain/3-resources. Fase 3 (Renderizar) aplica o design system Planner Editorial Noturno em fit-screen 1440x1000 com 4 bands (Contexto + Orquestra HERO + Compromissos + Preflight ancorado ao fundo). Use quando Bruno pedir para criar, editar ou gerar seu planner semanal, weekly preview, dashboard da semana ou HTML para sunday planning. Nao usar em apresentacoes M7, comunicados corporativos ou outputs para terceiros.
license: Proprietary
---

# Generating Weekly Planner

Gera o weekly planner pessoal executivo em HTML aplicando **tres fases**: extrair dados reais da semana (seg-sex), planejar a orquestra dos 5 dias, renderizar no design system Planner Editorial Noturno com fit-screen.

**Principio central:** o weekly e um artefato de **orquestracao** — daily e sobre execucao, weekly e sobre como os 5 dias se encaixam. Se a Orquestra nao conta uma historia coerente dos 5 dias, e so um daily x5 — e isso nao justifica o horizonte semanal.

## Quando usar esta skill

Invocada quando Bruno pede para gerar ou atualizar o planner da semana — tipicamente na sexta a tarde (olhando a proxima) ou domingo a noite / segunda de manha.

**Triggers tipicos:**
- "Cria meu weekly planner"
- "Prepara a semana 17"
- "Gera o planner semanal"
- "Monta meu sunday planning"
- "Atualiza minha pagina da semana"
- "Weekly preview para a S17"

**NAO usar esta skill para:**
- Apresentacoes M7 para diretoria ou XP
- Comunicados corporativos
- Documentos para terceiros
- Retrospectivas M7 (use outros outputs)
- Planner diario (use `generating-daily-planner`)

**Complementaridade com daily:** o weekly planeja a semana; o daily executa dentro da semana planejada. Os dois se relacionam — a Tese da semana do weekly alimenta o Lide dos dailies, e o Preflight do weekly valida que cada MIT diario serve aos Big 3 semanais.

## Workflow em tres passadas

### Fase 1 · Extrair (dados reais antes de pensar)

Ler [references/extracao-dados.md](references/extracao-dados.md) e reunir dados das 6 fontes:

| Fonte | Rota primaria | Fallback |
|---|---|---|
| Agenda (5 dias) | Google Calendar MCP (range seg-sex) | Pedir print/lista |
| Tarefas da semana | ClickUp MCP (due <= sex, assignee=Bruno) + filtro status whitelist/blacklist | Pedir lista |
| Workspace M7 | ClickUp MCP (statuses=[atrasada, bloqueada], workspace inteiro) — alimenta Riscos & fogos | Pedir resumo por frente |
| **Corpo · semana** | **TrainingPeaks MCP** (weight/sleep/HRV/weekly_summary/fitness_metrics) | Perguntar se MCP falhar |
| **Metas Q2** | ClickUp goals → brain/3-resources (metas-2026.md) → perguntar | Perguntar confidence (0-100%) |
| **Retrospectiva S-1** | *Sempre perguntar ao usuario* | — |
| Contexto insight | Filesystem `brain/3-resources/` (PARA) | — |

**Regra de ouro:** nunca inventar dado. Se nao conseguir extrair nem obter do usuario, secao vira `—` ou e omitida.

**Particularidade weekly:** a **Retrospectiva da semana passada** e pre-requisito da Tese. Sem saber o que ficou aberto/aprendido em S-1, a Tese vira generica. Sempre perguntar no inicio da extracao.

### Fase 2 · Planejar (metodologia antes de texto)

Ler [references/metodologia-planejamento.md](references/metodologia-planejamento.md) e aplicar as **8 regras de decisao** (weekly tem mais regras que daily porque tem mais dimensoes estruturais):

1. **Tese da semana** — aposta argumentativa unica (Hyatt Weekly Big Idea), 200-400 chars
2. **Critério de vitoria** — 4 outcomes verificaveis binarios (4DX + Hyatt)
3. **Orquestra dos 5 dias** — por dia: tema, deep work, meetings, entrega, energia (Newport Time-Block)
4. **Tres grandes da semana** — Weekly Big 3 derivados de Q2, com "pronto quando" (Hyatt)
5. **Prazos duros** — deadlines ancorados ao dia especifico (seg/ter/qua/qui/sex)
6. **Riscos & fogos** — pre-mortem com mitigacao ja escrita (Kahneman)
7. **Preflight** — 4 perguntas editoriais (Newport shutdown reverso): vitoria / deep work / dizer nao / maior risco
8. **Corpo · semana** — 4 KPIs agregados na ordem fixa `peso Δ → sono medio → TSS total → TSB`, cada um com tag de classificacao de 1 palavra (v1.8.0) · ver [extracao-dados.md secao 4](references/extracao-dados.md) para matriz de faixas

Em paralelo, gerar o **Insight · cruzamento** seguindo [references/insight-cruzamento.md](references/insight-cruzamento.md): derivar 2-3 tensionamentos estrategicos da semana (nao do dia) → dominios → scan de `brain/3-resources/` → cruzamento binario de frameworks.

**Alternativa Pfeffer (v1.10.0):** quando a semana contiver sinais politicos dominantes (multiplas reunioes com superiores, apresentacoes estrategicas, oposicao identificada na retrospectiva S-1, gargalo pessoal persistente no workspace M7 ou decisao consequente de posicionamento), invocar o agente `pfeffer-power-analyst` com horizonte=weekly. O agente cruza dois capitulos do livro POWER e retorna Markdown estruturado que alimenta o Insight **e** a Regra 6 (Riscos & fogos) com pre-mortem tatico. Ver [agents/pfeffer-power-analyst.md](../../agents/pfeffer-power-analyst.md).

Antes de avancar para Fase 3, validar o **checklist de sanidade** (final de metodologia-planejamento.md).

### Fase 3 · Renderizar (design system aplicado)

Com o plano validado:

1. Ler [references/tokens.css](references/tokens.css) e colar no `<style>` do output
2. Ler [references/principios.md](references/principios.md) antes de decisoes visuais (identicos aos da daily)
3. Ler [references/componentes.md](references/componentes.md) para replicar cada componente weekly
4. Ler [references/regras-texto.md](references/regras-texto.md) para manter o tom editorial
5. Usar [references/template-html.html](references/template-html.html) como starter e preencher com o plano

**Layout final (fit-screen adaptativo (100vw × 100vh, baseline de design 1440×1000)):**
- **Band 1 · Contexto**: Semana hero + Lide + Insight · cruzamento + 2026 year grid + Corpo · semana
- **Band 2 · Orquestra** (HERO, `flex:1`): 5 colunas seg-sex lado a lado
- **Band 3 · Compromissos**: Tres grandes + Prazos duros + Riscos & fogos
- **Band 4 · Preflight** (ancorado ao fundo via flex): 4 perguntas editoriais

O Preflight deve **sempre** ficar na base da tela — isso e feature do layout (fit-screen como one-pager report), nao bug. Band 2 cresce via `flex:1` para empurrar Band 4 ao fundo.

## Checklist pre-render

Antes de emitir o HTML final, confirmar:

```
[ ] Dados extraidos reais ou explicitamente perguntados (nenhum inventado)
[ ] Retrospectiva S-1 perguntada e alimenta a Tese
[ ] Tese tem UMA aposta argumentativa (nao lista de intencoes)
[ ] Criterio de vitoria tem 4 outcomes binarios (verificaveis)
[ ] Orquestra cobre 5 dias, cada um com tema + deep + meetings + entrega
[ ] Pelo menos 1 dia na semana tem "dia protegido" (sem meetings, maker day)
[ ] MIT #1 da semana tem >=4h protegidas em pelo menos 1 dia da Orquestra
[ ] Tres grandes derivam de Q2 e cada um tem criterio "pronto quando"
[ ] Prazos ancorados a dia especifico (seg/ter/qua/qui/sex)
[ ] Cada risco tem mitigacao escrita (nao generica)
[ ] Riscos usam extracao Workspace M7 como insumo (status=atrasada/bloqueada, workspace inteiro)
[ ] Nenhuma task em status blacklist (cancelada/descartada/won't do/arquivada) no weekly
[ ] Tasks em status ambiguo candidatas a Big 3 ou Prazos duros foram confirmadas via `AskUserQuestion`
[ ] Cada contador exibido tem entrada em `metricas` com query rastreavel
[ ] Contadores recalculados a partir das linhas extraidas (nao reusados da API)
[ ] "atrasadas_*" usa status unico como fonte (nao soma pendente+due-vencido)
[ ] Preflight tem 4 perguntas respondidas em italic curto
[ ] Insight cruza DUAS perguntas de frameworks distintos
[ ] Corpo tem 4 KPIs na ordem peso Δ → sono medio → TSS total → TSB, cada um com tag de classificacao (numero e tag compartilham a mesma classe CSS; dado ausente = &mdash; + tag omitida)
[ ] Layout ocupa 1440x1000 sem overflow, Preflight na base
```

## Quick reference

| Aspecto | Decisao |
|---|---|
| Modo | Dark mode quente nativo (nao ha light mode) |
| Fonte principal | Georgia serif (texto, labels, narrativa) |
| Fonte tabular | Inter sans (horas, numeros, %, TSS, TSB) |
| Cor primaria | Terracota #D97757 (trabalho, foco) |
| Cor secundaria | Azul petroleo #6B9EB0 (corpo, treino, TSB positivo) |
| Cor alerta | Terracota escuro #B8593C (atraso, sono <7h, TSB muito negativo) |
| Fundo | #1A1715 (escuro quente) |
| Estrutura | 4 bands: Contexto + Orquestra (hero) + Compromissos + Preflight |
| Layout | Fit-screen 1440×1000, Band 2 flex:1, Preflight ancorado ao fundo |
| Dias cobertos | Segunda a sexta (sem fim de semana) |
| Filosofia | Zero ornamento, hierarquia via tipografia |

## Principios fundadores (leia antes de qualquer output)

Sao os mesmos 6 principios da daily (identidade visual compartilhada). Ver [references/principios.md](references/principios.md):

1. **Tipografia antes de caixa** — hierarquia por tamanho/peso/italico/cor, nunca por bordas ou cartoes
2. **Densidade operacional, respiracao editorial** — dados acionaveis densos, narrativa respirada
3. **Cor e decisao, nao decoracao** — toda cor significa algo
4. **Dark mode quente nativo** — nunca implementar light mode
5. **Numero como escultura** — numeros sao protagonistas visuais
6. **Zero ornamento** — sem icones decorativos, sombras, gradientes, badges ou pills

## Nunca fazer

- Light mode
- Incluir sabado ou domingo na Orquestra (escopo weekday-only)
- Replicar a estrutura do daily com 7 dias (descaracteriza o weekly como orquestracao)
- Cartoes elevados ou bordas em torno de secoes
- Icones decorativos (emoji ou SVG) — so texto e italico para enfase
- Sombras, gradientes, blur
- UPPERCASE exceto em labels de dias da semana (SEG, TER, QUA, QUI, SEX)
- Formatos de data misturados — sempre "13 abril", nunca "13/04" nem "April 13"
- Introduzir cor nova sem redefinir o sistema
- Serif para dados tabulares, sans para texto narrativo
- **Inventar dados** quando a extracao falha (perguntar ao usuario ou omitir)
- **Pre-mortem ficticio** ("risco: tudo pode dar errado") — escrever `risco: —` se nao ha risco real
- **Mitigacao generica** ("mitigacao: me organizar melhor") — cada mitigacao deve ser acao concreta
- **Inventar tag de classificacao na Corpo** — se MCP TP falha, numero vira `—` e tag e OMITIDA (nao renderizar tag vazia ou `?`)
- **Usar sinonimos livres nas tags** — vocabulario e fixo por KPI (ver regras-texto.md): `estável/em queda/subindo`, `ideal/ok/baixo`, `saudável/leve/pesado/crítico`, `produtivo/neutro/fresco/overreach/destreino`
- Preflight sem ancoragem ao fundo — isso quebra o contrato visual de one-pager report
- **Weekly Big 3 desconectados de Q2** — se nao derivam das Metas Q2, nao sao Big 3, sao so tarefas grandes
- **Incluir task em status blacklist** (cancelada/descartada/won't do/arquivada/rejeitada) — validar via `status.type == closed`, `date_closed`, `archived` mesmo quando `status=aberta` na API
- **Tratar a extracao de Workspace M7 como "o que eu deleguei"** — o escopo e workspace inteiro (status=atrasada/bloqueada). Bruno responde pela saude das frentes, nao so pelo que assinou
- **Exibir numero sem rastreabilidade** — todo contador (Riscos, Big 3 confidence, prazos) precisa entrada em `extracao.metricas` com query reprodutivel
- **Somar `status=pendente+due-vencido` com `status=atrasada`** — duplica. Usar fonte unica (preferencia: status customizado `atrasada`)

## Arquivos da skill

```
generating-weekly-planner/
├── SKILL.md                          # este arquivo (orquestracao 3 fases)
├── README.md                         # instrucoes de instalacao e uso
└── references/
    ├── extracao-dados.md             # Fase 1 · 6 fontes, MCPs, fallbacks, schema
    ├── metodologia-planejamento.md   # Fase 2 · 8 regras + checklist de sanidade
    ├── insight-cruzamento.md         # Fase 2b · gerar insight criativo (horizonte semanal)
    ├── tokens.css                    # Fase 3 · CSS variables + classes (4 bands + fit-screen)
    ├── tokens.json                   # Fase 3 · DTCG format tokens (interop)
    ├── principios.md                 # Fase 3 · 6 principios fundadores (identicos a daily)
    ├── componentes.md                # Fase 3 · componentes weekly especificados
    ├── regras-texto.md               # Fase 3 · tom editorial, labels weekly, metadata
    └── template-html.html            # Fase 3 · starter HTML completo

Agente relacionado (pasta `agents/` do plugin):
└── pfeffer-power-analyst.md          # Atalho Fase 2b e insumo para Regra 6 (Riscos).
                                       Invocado quando semana tem sinais politicos
                                       dominantes (oposicao na retro, multiplas reunioes
                                       com superiores, apresentacao externa de alto risco,
                                       decisao de posicionamento).
```

## Output esperado

Ao aplicar esta skill, o Claude Code deve produzir um artefato que:

- Foi **planejado** usando as 8 regras de metodologia-planejamento.md (nao so preenchido)
- Foi **extraido** de fontes reais — TP MCP para Corpo, Calendar/ClickUp para agenda/tarefas
- Foi informado pela **Retrospectiva S-1** (perguntada ao usuario)
- Conecta com **Metas Q2** (Weekly Big 3 derivados, nao arbitrarios)
- Usa apenas as cores definidas em tokens.css
- Usa apenas Georgia (serif) e Inter (sans)
- Segue a estrutura 4 bands em fit-screen adaptativo (100vw × 100vh, baseline de design 1440×1000)
- Preflight ancorado ao fundo via flex:1 na Orquestra
- Implementa os componentes weekly especificos
- Respeita o tom editorial (ver regras-texto.md)
- Contem um Insight cruzando dois frameworks tensionados no horizonte semanal

Se o usuario pedir algo que contradiga os principios (ex: "adiciona sabado e domingo" ou "remove o Preflight"), a skill deve respeitar o style guide e sinalizar o conflito antes de implementar. Se o usuario pedir "pule o planejamento, so monta o HTML rapido", a skill deve avisar que o output sera raso e pedir confirmacao antes de pular as Fases 1 e 2.

## Diferencas vs `generating-daily-planner`

| Aspecto | Daily | Weekly |
|---|---|---|
| Horizonte | 1 dia | 5 dias (seg-sex) |
| Hero visual | Data do dia ("16") | Orquestra (5 cols lado a lado) |
| Header | 5 zonas (Dia/Lide/Insight/Mes/Corpo) | Mesmo, com "Semana 16" hero e "2026" grid de 52 semanas |
| Corpo | Snapshot (peso, TSS semana, sono ultima noite) | Agregado (peso Δ, TSS total, sono medio, TSB) |
| Metodologia | 6 regras (Lide/MITs/Agenda/Tarefas/Workspace M7/Amanha) | 8 regras (+ Criterio de vitoria, Preflight) |
| Fim | Footer 2-col (Notas + Amanha) | Preflight 4 perguntas ancorado ao fundo |
| Altura | 900px natural | 1000px fit-screen forcado |
| MCP Corpo | TP MCP (snapshot) | TP MCP (weekly_summary + fitness_metrics) |
| Cadencia de uso | Todo dia | Sexta tarde ou dom noite / seg manha |
