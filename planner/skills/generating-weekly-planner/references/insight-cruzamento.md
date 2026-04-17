# Fase 2b · Insight · cruzamento (horizonte semanal)

O bloco "Insight · cruzamento" nao e decorativo nem randomico. E uma **provocacao criativa sintetizada a partir dos tensionamentos reais da semana**, cruzando dois frameworks/ideias distintas encontrados em `brain/3-resources/` (seu sistema PARA).

**Funcao:** forcar voce a olhar o arco da semana por um angulo que nao e o default. Se a Tese diz *"a semana aposta em X"*, o Insight responde *"mas considere Y"*.

**Diferenca em relacao ao daily:** o daily cruza **desafios do dia** (tensionamentos imediatos de execucao); o weekly cruza **tensionamentos estrategicos** da semana (dilemas sobre direcao, alocacao de capacidade, prioridade entre objetivos Q2). O horizonte muda, o padrao de cruzamento e o mesmo.

## Indice

- [Quando gerar o insight](#quando-gerar-o-insight)
- [Processo em 7 passos](#processo-em-7-passos)
- [Regras do texto final](#regras-do-texto-final)
- [Padrao de cruzamento](#padrao-de-cruzamento)
- [Anti-padroes](#anti-padroes)
- [Exemplos comentados](#exemplos-comentados)
- [Fallback quando 3-resources nao ajuda](#fallback-quando-3-resources-nao-ajuda)

## Quando gerar o insight

Apos a Fase 2 principal (8 regras de planejamento), antes da Fase 3 (renderizacao). Pre-requisitos:
- Tese da semana ja escrita
- Tres grandes (Big 3) ja definidos
- Riscos ja mapeados (contem muitos tensionamentos uteis)
- Tensionamentos derivados na Fase 1 (ver [extracao-dados.md secao 7](extracao-dados.md#7-contexto-para-o-insight))

## Processo em 7 passos

### Passo 1 · Extrair 2-3 tensionamentos centrais da semana

Ler a Tese + Big 3 + Riscos e identificar os **tensionamentos estrategicos** da semana (nao as tarefas, mas os dilemas de direcao). Exemplos tipicos no horizonte semanal:

| Tese / Big 3 / Risco | Tensionamento central |
|---|---|
| "Fechar m7-controle com diretoria" | Validacao externa vs iteracao autonoma (buscar aprovacao agora ou continuar refinando) |
| "SQL consorcios parado no Rafa ha 5d" | Delegacao vs fazer eu mesmo (escalar pressao ou reassumir o trabalho) |
| "Desdobrar metas Q2 em 4 verticais" | Rigor metrico vs flexibilidade estrategica (formalizar KPIs agora ou deixar orgânico) |
| "Qua 15 protegida vs demandas do time" | Disponibilidade vs deep work (ser acessivel vs produzir profundamente) |

### Passo 2 · Mapear cada desafio a um dominio de conhecimento

Para cada desafio, listar 2-3 dominios de onde *poderia* vir uma resposta util. Exemplos:

| Desafio | Dominios relevantes |
|---|---|
| Escolher poucos indicadores | Lean, ToC, OKR, GPD, Balanced Scorecard, sistemas complexos |
| Pressionar sem desengajar | Lideranca situacional, nonviolent communication, accountability, coaching |
| Feedback que move | Radical Candor, SBI, Crucial Conversations, Situational Leadership |

### Passo 3 · Buscar materiais em `brain/3-resources/`

Para cada dominio identificado, fazer uma busca ampla:

```
Glob: brain/3-resources/**/*.md
Grep (paralelo por dominio): "Lean|ToC|Goldratt|Womack" em *.md
```

Priorizar:
1. Arquivos cujo **nome** contenha o dominio (`lean-thinking.md`, `goldratt-toc.md`)
2. Arquivos em **subpastas** relacionadas (`3-resources/metodologias/`, `3-resources/livros/`, `3-resources/lideranca/`)
3. Arquivos com **tags** ou headers relacionados

Ler ate 4-5 arquivos candidatos (leitura parcial das primeiras 50-100 linhas de cada para captar a essencia).

### Passo 4 · Extrair a *pergunta fundadora* de cada framework

Todo framework pode ser reduzido a **uma pergunta que ele faz melhor que os outros**. Exemplos ja na biblioteca:

| Framework | Pergunta fundadora |
|---|---|
| Lean (Womack) | "O que podemos cortar? (elimina desperdicio)" |
| ToC (Goldratt) | "O que trava o fluxo? (encontra o gargalo)" |
| Shape Up (Basecamp) | "Quanto vale investigar?" (Appetite) |
| GPD (Falconi) | "Por que isso acontece?" (Why-Why) |
| Radical Candor (Scott) | "Eu me importo pessoalmente O SUFICIENTE para desafiar diretamente?" |
| Situational Leadership (Hersey) | "Qual e o nivel de prontidao do liderado para esta tarefa?" |
| OKR (Doerr) | "Qual e o resultado mensuravel que prova o progresso?" |
| First Principles (Feynman/Musk) | "Desmontar ate ficar sem suposicao — o que sobrou?" |
| Systems Thinking (Meadows) | "Onde estao os leverage points no sistema?" |

Se o arquivo em `3-resources/` nao deixa a pergunta clara, **extrair** lendo a introducao do autor ou a tese central.

### Passo 5 · Escolher DUAS perguntas que tensionam

O cruzamento funciona quando as duas perguntas sao **fundamentalmente diferentes — e as duas sao legitimas** para o desafio. NAO usar duas que concordam. NAO usar uma certa e uma errada.

Exemplos de cruzamentos bem tensionados:

| Tensionamento da semana | Framework 1 | Framework 2 | Tensao |
|---|---|---|---|
| Escolher indicadores | Lean ("o que cortar?") | ToC ("o que trava?") | Cortar vs encontrar — duas perguntas diferentes sobre o mesmo sistema |
| Feedback a Igor/Katrine | Situational Leadership ("qual nivel?") | Radical Candor ("importo o suficiente?") | Calibracao por maturidade vs coragem de dizer |
| Cobrar Pedro | Situational Leadership ("qual toque?") | GPD ("por que?") | Gesto de lideranca vs causa-raiz |

### Passo 6 · Redigir o cruzamento (150-250 chars)

Formato-canon (ja estabelecido nos planners anteriores):

```
<Framework 1> <verbo> <objeto>. <Framework 2> <verbo> <objeto>.
— sao perguntas diferentes: <"pergunta1"> vs <"pergunta2">
```

Exemplos reais dos planners 16 e 17:
- *"Lean quer eliminar o desperdicio. ToC quer achar o gargalo. — sao perguntas diferentes: 'o que podemos cortar?' vs 'o que trava o fluxo?'"*
- *"Situational Leadership muda o estilo conforme o nivel do liderado. GPD pergunta Why-Why ate a causa raiz. — sao perguntas diferentes: 'que toque dar agora?' vs 'por que isso acontece?'"*

### Passo 7 · Adicionar citacao de fontes

Linha final `header__insight-cite` com as duas fontes:

```
<Framework 1> · <Autor 1> × <Framework 2> · <Autor 2>
```

Exemplos:
- `Lean · Toyota × ToC · Goldratt`
- `Situational Leadership · Hersey-Blanchard × GPD · Falconi`
- `Radical Candor · Scott × Situational Leadership · Hersey`

## Regras do texto final

1. **Duas fontes sempre** — nunca 3+. O insight e um cruzamento binario.
2. **150-250 caracteres** — cabe na zona de 240px do header.
3. **Tensao explicita** — as perguntas precisam ser distintas. Se ambas podem ser respondidas "sim", o cruzamento esta fraco.
4. **Conectar ao tensionamento da semana** — o insight nao e aleatorio; ele responde a uma tensao especifica que a Tese, os Big 3 ou os Riscos levantaram.
5. **Escolher cruzamento que voce NAO ja usou** — evitar repetir "Shape Up × GPD" tres dias seguidos. Rotacionar entre dominios.

## Padrao de cruzamento

Estrutura gramatical consistente:

```
[Framework 1] [verbo transitivo/modal] [objeto conceitual 1].
[Framework 2] [verbo transitivo/modal] [objeto conceitual 2].
&mdash; sao perguntas diferentes: <em>"[pergunta1 curta]"</em> vs <em>"[pergunta2 curta]"</em>
```

Os dois `<em>` com perguntas em italico terracota sao obrigatorios — formam o "punch" visual da zona.

## Anti-padroes

| Ruim | Por que e ruim |
|---|---|
| "Deep Work defende foco. Flow state defende foco." | As duas concordam — sem tensao |
| "Lean elimina desperdicio. Six Sigma elimina variabilidade. Agile elimina ciclos longos." | 3 frameworks — confuso, pula a regra do binario |
| "Insight da semana: leia o livro X" | Nao e cruzamento, e recomendacao |
| "Pense fora da caixa e seja criativo." | Banal, sem conteudo especifico, sem fontes |
| Cruzamento que nao toca no tensionamento da semana | Viraria fortune cookie. Irrelevante para a acao |

## Exemplos comentados

### Exemplo A · Desafio: selecionar indicadores

**Contexto:** Big 3 da semana e "Definir KPIs/PPIs do Ritual N2 Investimentos". Pergunta subjacente: *como escolher poucos indicadores que importam?*

**Cruzamento:**
> *"Balanced Scorecard soma 4 perspectivas para cobertura. Hoshin Kanri derruba a um unico X Matrix para foco. — sao perguntas diferentes: 'o que estamos deixando de medir?' vs 'o que e indiscutivelmente mais importante?'"*
>
> Balanced Scorecard · Kaplan-Norton × Hoshin Kanri · Toyota

**Por que funciona:** os dois frameworks sao sobre o mesmo objeto (metricas estrategicas) mas com filosofias opostas (cobertura vs foco). Voce passa o dia considerando AMBOS.

### Exemplo B · Desafio: mentorar com devolutiva

**Contexto:** 3 mentorias na sexta (Igor, Katrine, PDCA de Julianne). Pergunta subjacente: *como dar feedback que move?*

**Cruzamento:**
> *"Radical Candor pergunta se voce se importa o suficiente para desafiar. Situational Leadership pergunta qual e a prontidao do liderado. — sao perguntas diferentes: 'tenho coragem?' vs 'qual o toque certo?'"*
>
> Radical Candor · Scott × Situational Leadership · Hersey

**Por que funciona:** duas perguntas legitimas, nao intercambiaveis. Voce pode ter coragem (Candor) mas errar o nivel (Situational), ou vice-versa.

### Exemplo C · Desafio: follow-up desconfortavel

**Contexto:** cobrar Pedro nos 4 chamados TI. Pergunta subjacente: *como pressionar sem queimar?*

**Cruzamento:**
> *"Accountability Ladder (Partners in Leadership) pergunta em que degrau a pessoa esta. Nonviolent Communication (Rosenberg) pergunta qual a necessidade por tras do comportamento. — sao perguntas diferentes: 'como subo 1 degrau?' vs 'o que ele precisa?'"*
>
> Accountability Ladder · Partners in Leadership × NVC · Rosenberg

## Fallback quando 3-resources nao ajuda

Se a busca em `brain/3-resources/` retorna zero candidatos relevantes para os tensionamentos da semana:

**Opcao 1 · Usar pares classicos conhecidos** (sempre validos para dominios universais):
- Lean × ToC (eliminar vs destravar)
- Shape Up × GPD (apetite vs causa-raiz)
- OKR × Hoshin Kanri (mensurar vs focar)
- Deep Work × Shallow Work (profundidade vs superficie)
- First Principles × Analogia (desmontar vs copiar)

**Opcao 2 · Pedir ao usuario:**

> Nao encontrei material em 3-resources sobre o desafio <X>. Voce quer:
> (a) Deixar o Insight vazio hoje
> (b) Sugerir duas leituras/frameworks que voce quer cruzar
> (c) Usar um cruzamento classico (ex: Lean × ToC)

**Nunca** gerar cruzamento ficticio citando autor ou livro inexistente. Preferir insight vazio a insight falso.
