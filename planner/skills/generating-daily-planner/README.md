# generating-daily-planner · Skill Claude Code

Gera o daily planner pessoal executivo em **dois artefatos sincronizados**: (1) um `.md` canonico editavel em `~/Documents/brain/0-inbox/plan-review/daily/YYYY/MM/daily-YYYY-MM-DD.md` e (2) um HTML estatico publicado no live artifact `daily-planner-live` do Cowork via `mcp__cowork__update_artifact`. Aplica o design system **Planner Editorial Noturno**. Invocada automaticamente pelo Claude Code quando o Bruno pede seu planner do dia.

**Arquitetura v2:** o `.md` e fonte de verdade; o HTML e derivado. Ediçao manual do `.md` durante o dia + comando `/planner sync` propaga as mudanças para o artifact sem re-extrair dados nem re-invocar o agente Pfeffer.

## Instalacao

### Opcao 1 · Skill pessoal (recomendado)

Disponivel em todos os projetos do Bruno no Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -r generating-daily-planner ~/.claude/skills/
```

### Opcao 2 · Skill de projeto

Apenas para o projeto atual:

```bash
mkdir -p .claude/skills
cp -r generating-daily-planner .claude/skills/
```

### Opcao 3 · Referencia via CLAUDE.md

Se preferir nao usar skills, adicione ao `CLAUDE.md` do projeto:

```markdown
## Design system para artefatos pessoais

Quando eu pedir meu planner, daily ou dashboard pessoal, aplique o sistema
em ./design/generating-daily-planner/. Leia SKILL.md antes e siga os
principios la definidos.
```

E coloque a pasta em `./design/generating-daily-planner/` no repo.

## Como usar

### No Claude Code

Apos instalar, basta pedir em linguagem natural:

```
"cria o html do meu planner de hoje"
"atualiza minha pagina de planejamento com os dados novos"
"gera um daily dashboard com os compromissos de hoje"
"monta uma visao executiva do meu dia"
```

O Claude Code vai (v2, 4 fases):

1. Reconhecer o trigger (planner pessoal, nao corporativo)
2. Ler `SKILL.md` para entender o contexto e as 4 fases
3. **Fase 1** — Extrair dados reais (ClickUp + Calendar + perguntar corpo)
4. **Fase 2** — Planejar (6 regras de metodologia-planejamento.md) e invocar o agente `pfeffer-power-analyst` para Insight + Notas
5. **Fase 3** — Emitir `.md` canonico em `~/Documents/brain/0-inbox/plan-review/daily/YYYY/MM/daily-YYYY-MM-DD.md` conforme `references/schema-md.md`
6. **Fase 4** — Renderizar HTML a partir do .md e publicar via `mcp__cowork__update_artifact({id: 'daily-planner-live', ...})` conforme `references/render-from-md.md`

### Re-render sem re-extrair (`/planner sync`)

Apos editar manualmente o .md durante o dia (concluir uma MIT, adicionar uma nota, reescrever a lide), rodar `/planner sync`. O comando le o .md, re-renderiza o HTML, publica no artifact e faz append em `edits[]` no frontmatter registrando o diff. Nao chama Pfeffer, nao chama MCPs de extraçao, roda em segundos.

### Debug (`/planner show`)

Imprime o .md integral do dia no chat para inspeçao rapida (estado atual, historico de `edits[]`, campos ausentes).

### Via cron matinal (automacao)

Exemplo de script que roda toda manha as 06:00:

```bash
#!/bin/bash
# ~/scripts/planner-matinal.sh

cd ~/planner-pessoal

claude-code "Leia os dados em ./data/$(date +%Y-%m-%d).json e gere
o planner do dia em ./output/$(date +%Y-%m-%d).html usando a skill
generating-daily-planner. Dados incluem: tres inadiaveis, agenda,
metricas de corpo, tarefas, workspace m7 (atrasadas + bloqueadas), notas capturadas ontem."
```

Adicionar no crontab:

```
0 6 * * * /home/bruno/scripts/planner-matinal.sh
```

## Estrutura da skill (v2)

```
generating-daily-planner/
├── SKILL.md                       # ponto de entrada, 4 fases
├── README.md                      # este arquivo
└── references/
    ├── extracao-dados.md          # Fase 1 · fontes, MCPs, fallbacks
    ├── metodologia-planejamento.md # Fase 2 · 6 regras + checklist
    ├── insight-cruzamento.md      # Fase 2b · regras do output do agente Pfeffer
    ├── schema-md.md               # Fase 3 · spec do .md canonico
    ├── render-from-md.md          # Fase 4 · pipeline parse → render → publish
    ├── tokens.css                 # Fase 4 · CSS variables prontas para colar
    ├── tokens.json                # Fase 4 · design tokens DTCG
    ├── principios.md              # Fase 4 · 6 principios fundadores
    ├── componentes.md             # Fase 4 · spec de cada componente
    ├── regras-texto.md            # Fase 4 · tom, labels, inlines MD
    └── template-html.html         # Fase 4 · starter HTML completo
```

Comandos (na raiz do plugin `planner/commands/`):

```
commands/
├── sync.md                        # /planner sync — re-render sem re-extrair
└── show.md                        # /planner show — imprime o .md no chat (debug)
```

## Interop com outras ferramentas

### Figma

Importe `references/tokens.json` via plugin **Tokens Studio** ou **Figma Tokens**. O formato DTCG (Design Tokens Community Group) e suportado nativamente.

### Tailwind CSS

Converta o JSON para `tailwind.config.js`:

```bash
npx @tokens-studio/sd-transforms build
```

Ou mapeie manualmente os tokens principais:

```js
// tailwind.config.js
module.exports = {
  theme: {
    colors: {
      bg: '#1A1715',
      'bg-elevated': '#2A2320',
      'text-primary': '#F5F0E6',
      accent: '#D97757',
      'accent-2': '#6B9EB0',
      alert: '#B8593C',
    },
    fontFamily: {
      serif: ['Georgia', 'serif'],
      sans: ['Inter', 'sans-serif'],
    }
  }
}
```

### React / Next.js

Importe `tokens.css` no `globals.css` do projeto. As CSS variables ficam disponiveis em todos os componentes.

## Versionamento

Ver `.claude-plugin/plugin.json` do plugin raiz — fonte canonica da versao.

## Principios que guiaram as 20 decisoes

O sistema foi destilado iterativamente de:

1. Dark mode vs light → dark
2. Frio azulado vs quente acinzentado → quente
3. Terracota vs verde salvia → terracota
4. Sans geometrico vs serif editorial → serif
5. Cartoes elevados vs fluxo editorial → fluxo
6. Minimalista focado vs painel denso → minimalista
7. Numeros gigantes vs bullets discretos → numeros gigantes
8. Caixa alta monospace vs italico editorial → italico
9. Terracota generoso vs cirurgico → generoso
10. Monocromatico vs duocromatico → duocromatico
11. Mesmo registro vs registros opostos → opostos
12. Numeros inline vs grid de metricas → inline
13. Timeline vertical vs lista narrativa → timeline
14. Coluna unica vs 3 colunas → 3 colunas
15. Respiracao generosa vs densa editorial → densa
16. Grid classico vs semana linear → semana linear
17. Notas marginalia vs lista direta → lista direta
18. Data dominante vs cabecalho horizontal → data dominante
19. So tipografia vs marcadores laterais → so tipografia
20. Lide volumoso vs enxuto → volumoso

## Licenca

Proprietario. Uso pessoal do Bruno Chiaramonti.
