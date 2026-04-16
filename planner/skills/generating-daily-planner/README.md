# generating-daily-planner · Skill Claude Code

Gera o daily planner pessoal executivo em HTML aplicando o sistema de design **Planner Editorial Noturno**. Invocada automaticamente pelo Claude Code quando o Bruno pede seu planner do dia.

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

O Claude Code vai:

1. Reconhecer o trigger (planner pessoal, nao corporativo)
2. Ler `SKILL.md` para entender o contexto
3. Consultar `references/tokens.css` para cores e tipografia
4. Consultar `references/componentes.md` para classes CSS disponiveis
5. Consultar `references/regras-texto.md` para o tom editorial
6. Gerar o HTML usando `references/template-html.html` como starter

### Via cron matinal (automacao)

Exemplo de script que roda toda manha as 06:00:

```bash
#!/bin/bash
# ~/scripts/planner-matinal.sh

cd ~/planner-pessoal

claude-code "Leia os dados em ./data/$(date +%Y-%m-%d).json e gere
o planner do dia em ./output/$(date +%Y-%m-%d).html usando a skill
generating-daily-planner. Dados incluem: tres inadiaveis, agenda,
metricas de corpo, tarefas, delegadas, notas capturadas ontem."
```

Adicionar no crontab:

```
0 6 * * * /home/bruno/scripts/planner-matinal.sh
```

## Estrutura da skill

```
generating-daily-planner/
├── SKILL.md                       # ponto de entrada, invocado pelo Claude Code
├── README.md                      # este arquivo
└── references/
    ├── tokens.css                 # CSS variables prontas para colar
    ├── tokens.json                # design tokens em formato DTCG
    ├── principios.md              # 6 principios fundadores
    ├── componentes.md             # spec de cada componente central
    ├── regras-texto.md            # tom, labels, metadata de tempo
    └── template-html.html         # starter HTML completo e funcional
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
