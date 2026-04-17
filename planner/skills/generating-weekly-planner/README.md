# generating-weekly-planner · Skill Claude Code

Gera o weekly planner pessoal executivo em HTML aplicando o sistema de design **Planner Editorial Noturno** no horizonte semanal (seg-sex). Invocada automaticamente pelo Claude Code quando o Bruno pede seu planner da semana — tipicamente na sexta a tarde (olhando a proxima) ou domingo a noite / segunda de manha.

Complementa a skill `generating-daily-planner`: weekly planeja a orquestra dos 5 dias, daily executa dentro da semana planejada.

## Instalacao

### Via plugin `chiaras-ai/planner` (recomendado)

A skill ja vem instalada quando o plugin esta ativo. Basta ter o plugin instalado no Claude Code.

### Opcao manual · Skill pessoal

Disponivel em todos os projetos do Bruno no Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -r generating-weekly-planner ~/.claude/skills/
```

### Opcao manual · Skill de projeto

Apenas para o projeto atual:

```bash
mkdir -p .claude/skills
cp -r generating-weekly-planner .claude/skills/
```

## Como usar

### No Claude Code

Apos instalar, basta pedir em linguagem natural:

```
"cria o html do meu weekly planner"
"prepara a semana 17"
"monta meu sunday planning"
"gera o planner semanal da S17"
"atualiza minha pagina da semana com os dados novos"
"weekly preview para a proxima semana"
```

O Claude Code vai:

1. Reconhecer o trigger (planner semanal pessoal, nao corporativo)
2. Ler `SKILL.md` para entender o contexto
3. **Fase 1 · Extrair**: Google Calendar (5 dias), ClickUp (tarefas/delegadas da semana), TrainingPeaks (peso, TSS, sono, TSB), ClickUp goals (Metas Q2), perguntar retrospectiva S-1
4. **Fase 2 · Planejar**: aplicar as 8 regras de decisao (Tese, Criterio, Orquestra, Big 3, Prazos, Riscos, Preflight, Corpo)
5. **Fase 2b · Insight**: cruzamento de frameworks em `brain/3-resources/`
6. **Fase 3 · Renderizar**: template HTML com fit-screen 4 bands, Preflight ancorado ao fundo

### Via cron semanal (automacao)

Exemplo de script que roda toda sexta a tarde (para preparar a semana seguinte):

```bash
#!/bin/bash
# ~/scripts/weekly-planner-friday.sh

cd ~/planner-pessoal

# Calcula proxima semana (S+1)
NEXT_WEEK=$(date -v+Mon +%Y-%m-%d)

claude-code "Leia os dados em ./data/weekly-${NEXT_WEEK}.json (se existir)
e gere o weekly planner em ./output/weekly-${NEXT_WEEK}.html usando a skill
generating-weekly-planner. Se nao houver dados prontos, extrai via MCPs
(Calendar, ClickUp, TrainingPeaks). Pergunta a retrospectiva da semana que
acaba hoje e as Metas Q2 que nao estiverem sincronizadas."
```

Adicionar no crontab:

```
0 16 * * 5 /home/bruno/scripts/weekly-planner-friday.sh
```

Roda toda sexta as 16h, preparando a semana seguinte.

### Sunday planning manual

Para quem prefere o ritual dominical:

```bash
# Domingo 21h, preparar S+0
claude-code "Weekly planner para a proxima semana, usando generating-weekly-planner.
Extrai tudo via MCP e me pergunta a retrospectiva da semana que termina."
```

## Dependencias MCP

A skill consome 3 MCPs, todos declarados no `.mcp.json` do plugin raiz:

### TrainingPeaks MCP (adicionado na v1.5.0)

**Pre-requisitos:**
```bash
uv tool install --reinstall 'JamsusMaximus/trainingpeaks-mcp[browser]'
```

**Autenticacao (uma vez a cada ~30 dias):**
```bash
tp-mcp auth
# Se o getpass travar (VS Code, Cursor, Claude Code):
# pbpaste | python ~/.local/bin/tp-mcp auth
```

Ver README do plugin raiz (`chiaras-ai/planner/README.md`) para detalhes de cookie extraction e bypass getpass.

**Tools usadas:**
- `weight` — peso inicial e final da semana (calcula delta)
- `sleep` — media de sono nos 5 dias
- `HRV` — heart rate variability media
- `weekly_summary` — TSS total e contagem de treinos
- `fitness_metrics` — TSB (training stress balance / forma)

**Fallback:** se o MCP falhar ou auth expirar, perguntar ao usuario os 4-5 valores agregados.

### Google Calendar MCP

Extrai agenda seg-sex da semana alvo. Sem setup adicional (ja configurado).

### ClickUp MCP

Extrai tarefas, delegadas e goals (Metas Q2). Sem setup adicional.

## Estrutura da skill

```
generating-weekly-planner/
├── SKILL.md                          # ponto de entrada (orquestracao 3 fases)
├── README.md                         # este arquivo
└── references/
    ├── extracao-dados.md             # Fase 1 · fontes weekly + schema
    ├── metodologia-planejamento.md   # Fase 2 · 8 regras + checklist
    ├── insight-cruzamento.md         # Fase 2b · cruzamento semanal
    ├── tokens.css                    # Fase 3 · CSS variables + classes
    ├── tokens.json                   # Fase 3 · DTCG tokens
    ├── principios.md                 # Fase 3 · 6 principios fundadores
    ├── componentes.md                # Fase 3 · componentes weekly
    ├── regras-texto.md               # Fase 3 · tom editorial
    └── template-html.html            # Fase 3 · starter HTML
```

## Diferencas vs daily

| Dimensao | Daily | Weekly |
|---|---|---|
| Horizonte | 1 dia | 5 dias (seg-sex) |
| Hero visual | Data do dia (num gigante) | Orquestra (5 colunas lado a lado) |
| Cadencia | Diaria (manha) | Semanal (sexta tarde ou domingo) |
| Foco | Executar | Orquestrar |
| Corpo | Snapshot | Agregado (delta, medias, TSB) |
| Metodologia | 6 regras | 8 regras (+ Criterio + Preflight) |
| Altura | 900px natural | 1000px fit-screen forcado |

## Quando usar uma ou outra

- **Weekly**: no inicio da semana, para desenhar o arco. Uma vez por semana.
- **Daily**: toda manha, para executar dentro do arco. Todo dia util.

Idealmente os dois coexistem: o weekly fornece contexto estrategico (Tese, Big 3, Criterio), o daily refina para o dia especifico (MITs, agenda, pre-mortem individual).

## Interop com outras ferramentas

### Figma

Importe `references/tokens.json` via plugin **Tokens Studio** ou **Figma Tokens**. Formato DTCG.

### Tailwind CSS

Converta o JSON para `tailwind.config.js` — mesmos tokens da daily.

### React / Next.js

Importe `tokens.css` no `globals.css` do projeto.

## Versionamento

Ver `.claude-plugin/plugin.json` do plugin raiz — fonte canonica da versao.

## Licenca

Proprietario. Uso pessoal do Bruno Chiaramonti.
