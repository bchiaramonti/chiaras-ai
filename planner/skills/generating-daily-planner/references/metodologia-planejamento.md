# Fase 2 · Metodologia de planejamento

A segunda passada transforma os dados extraidos (Fase 1) em decisoes de planejamento. Seis regras, uma por secao planejavel. Cada regra tem um **filtro**, um **teste de sanidade** e **anti-padroes** a evitar.

**Principio geral:** o planner nao e uma lista — e um **plano executavel**. Se o dia proposto nao cabe em 8-9 horas de trabalho acordado + 7-8h de sono + 2h de deslocamento/refeicao, o plano esta errado antes de ser bonito.

## Indice

- [Regra 1 · Lide do dia](#regra-1--lide-do-dia)
- [Regra 2 · Tres inadiaveis](#regra-2--tres-inadiaveis)
- [Regra 3 · Agenda](#regra-3--agenda)
- [Regra 4 · Tarefas ClickUp](#regra-4--tarefas-clickup)
- [Regra 5 · Workspace M7](#regra-5--workspace-m7)
- [Regra 6 · Amanha](#regra-6--amanha)
- [Checklist de sanidade final](#checklist-de-sanidade-final)

## Regra 1 · Lide do dia

**O que e:** o Lide e uma tese jornalistica, nao um resumo. Responde a pergunta *"qual e A tese do dia?"* — uma ideia unica com argumento e implicacao.

### Filtro

1. Olhar os 3 MITs + primeiros 3 eventos da agenda
2. Identificar o **arco narrativo**: qual o fio que conecta esses itens?
3. Escrever 1 frase-tese (nao "fazer X e Y e Z", mas "o dia pede X porque Y")
4. Completar em 2-3 frases adicionais que desenvolvem/implicam a tese
5. Destacar com `<em>` 2-4 **entidades ancora** (nao mais que isso — se destaca tudo, nao destaca nada)

### Teste de sanidade

Se voce remover a primeira frase, o resto ainda faz sentido? Se sim, a tese esta fraca (e um resumo descritivo). Reescreva.

### Anti-padroes

| Ruim | Por que e ruim | Melhor |
|---|---|---|
| "Bruno tem reuniao as 10h, mentoria as 11h, PDCA as 16h." | Lista de itens, sem tese | "Sexta virada ao programa **Viva Lideranca**: tres mentorias consecutivas forcam disciplina de devolutivas estruturadas." |
| "Dia cheio com varias coisas importantes." | Vago, sem entidade ancora | (reescrever com entidades concretas) |
| "O dia pede X e Y e Z e W." | 4 teses = 0 teses. Escolha UMA. | "O dia pede X — porque Y destrava Z." |

### Extensao

200-400 caracteres. Abaixo vira telegrama; acima vira relatorio.

## Regra 2 · Tres inadiaveis

**O que e:** os 3 MITs ("Most Important Tasks") — tasks que, se feitas, tornam o dia um sucesso mesmo que tudo mais falhe.

### Filtro em 3 passos

**Passo A · Eisenhower**

Classificar cada candidato (vindo de `grupo_a_candidatos_mit` da Fase 1) em:

| Quadrante | Criterio | Acao |
|---|---|---|
| Q1 Urgente + Importante | Queimando, SLA hoje | Incluir se estiver queimando HOJE; do contrario, decair para Q2 |
| Q2 Importante + Nao Urgente | Move a agulha estrategica | **Prioridade maxima** — este e o espaco onde MITs devem viver |
| Q3 Urgente + Nao Importante | Pressao social/notificacao | Delegar ou ignorar — nunca MIT |
| Q4 Nao Urgente + Nao Importante | Distracao | Deletar |

MITs devem ser preferencialmente **Q2**. Q1 so entra se estiver pegando fogo nas proximas 24h.

**Passo B · Eat-the-frog ordering**

Dos 3 escolhidos, o MIT #1 deve ser a tarefa **mais adiada, mais desconfortavel ou mais cognitivamente pesada**. Razoes:
- Willpower e finito e maximo na manha
- Tasks pesadas adiadas corroem a producao ate serem feitas
- Se so tiver tempo pra UMA coisa hoje, e essa

**Passo C · Balance de papeis**

Verificar que os 3 MITs cobrem pelo menos **2 das 3 dimensoes**:

| Dimensao | Exemplos |
|---|---|
| Trabalho | Definir KPIs, revisar WBR, follow-up com Pedro |
| Corpo | Treino, consulta, sono protegido, refeicao estruturada |
| Familia/Pessoal | Conversa adiada com filha, compromisso com Bia, estudo pessoal |

Se os 3 MITs sao todos de trabalho, o dia vai produzir output profissional e atrito domestico simultaneamente. **Recalibrar.**

### Pre-mortem (campo novo no template)

Para cada MIT, escrever **1 linha curta** respondendo: *"o que vai me impedir de terminar isso hoje?"*

Exemplos:
- MIT "Definir KPIs/PPIs do Ritual N2" → risco: "Pedro sem resposta → uso o template do Falconi como fallback"
- MIT "Validar indicadores YAML" → risco: "descobrir que falta schema → escopar para so 3 indicadores hoje"
- MIT "Treino longo" → risco: "reuniao as 18h estoura janela → mudar para 06h30"

Renderizado como `<span class="inadiaveis__risco">· risco: ...</span>` separado de `inadiaveis__meta`.

### Anti-padroes

| Ruim | Por que e ruim |
|---|---|
| 3 MITs que sao projetos ("Finalizar skill", "Terminar WBR") | Projeto nao e task. Escolher o proximo *passo concreto* (1-3h) |
| 3 MITs todos do mesmo projeto | Corrosao dos outros papeis; escolher 1 do projeto + 2 de dimensoes diferentes |
| MIT sem SLA claro ("fazer quando der") | SLA obriga agendamento. Default: "ate 18h de hoje" |
| MIT repetido 3 dias seguidos | O MIT virou tema. Reformular como projeto e escolher o proximo passo concreto |

## Regra 3 · Agenda

**O que e:** o bloco de tempo do dia. Nao e so a agenda do Google — e o **mapa de capacidade** alocado.

### Regra de capacidade

Em horas cognitivas uteis (tipicamente 9h-18h = 9h uteis), a regra 60/40:

- **Maximo 60% ocupado** com eventos + MITs agendados (5-6h de 9)
- **Minimo 40% buffer** para imprevistos, transicoes, respiracao (3-4h de 9)

Se os eventos do calendario ja somam >6h, sinalizar: *"agenda sobrealocada, algum MIT nao vai caber"* e pedir ao usuario para priorizar.

### Regra de energia (para Bruno especificamente)

Pico cognitivo matinal. Regras de alocacao:

| Janela | Uso ideal | Uso aceitavel | Evitar |
|---|---|---|---|
| 07h-09h | Treino ou leitura | Planejamento do dia | Reuniao rotineira |
| 09h-12h | **Deep work do MIT #1** | Reuniao estrategica critica | Admin, email, 1:1 rotineiro |
| 12h-14h | Almoco, descompressao | Reuniao leve com almoco | Deep work |
| 14h-17h | Reunioes, deep work do MIT #2 | Admin pesado | — |
| 17h-19h | Admin, email, follow-ups | Reuniao leve | Deep work novo |

### Bloco protegido obrigatorio

Reservar **>=90min contiguos** de manha para o MIT #1. Se a agenda ja come essa janela, renegociar a agenda ou **trocar o MIT #1** (principio: o MIT #1 e a coisa que vai acontecer, nao o que voce espera que aconteca).

### Gaps estruturais

- Almoco (12h30-13h30): sempre presente, mesmo que `—` no display, para marcar a quebra cognitiva
- Fim-de-turno (18h): sempre marcado, mesmo que vazio, para forcar o `shutdown ritual`

### Anti-padroes

| Ruim | Melhor |
|---|---|
| 9h-18h continuamente bloqueado | Inserir 2-3 gaps de 30min como "respiracao" |
| MIT #1 agendado para 16h | Mover para 9h-11h (pico) ou trocar o MIT |
| Reuniao no horario do almoco sem alternativa | Agendar reuniao com almoco OU mover reuniao |

## Regra 4 · Tarefas ClickUp

**O que e:** o bloco **abaixo** dos Tres inadiaveis. NAO e o backlog — e o *display curto* das 5-6 tarefas mais relevantes depois dos 3 MITs.

### Regra de corte

Mostrar no maximo **5-6 linhas visiveis**. O resto agrupa em `<div class="tasks__more">+ N tarefas · ver todas ↗</div>`.

### Regra de ordenacao (ABCDE aplicado)

Ordenar as 5-6 visiveis como:
1. **A** · Atrasadas urgentes (>=1d atraso + priority urgent/high)
2. **B** · Due hoje
3. **C** · Atrasadas normais
4. **D** · Due amanha ou ate sab/dom
5. **E** · Resto (proxima semana)

Dentro de cada banda, desempate por impacto (lista estrategica > lista rotineira).

### Regra de meta

Cada linha exibe `· <lista> · <tag(s)>` no `tasks__title-meta` (ver [componentes.md secao 9](componentes.md)). Lista primeiro, tag depois.

### Anti-padroes

| Ruim | Melhor |
|---|---|
| Listar todas as 27 tarefas abertas | Cortar em 5-6 + "+22 tarefas · ver todas" |
| Ordem aleatoria do ClickUp | Aplicar ABCDE acima |
| Mostrar so o titulo sem lista | Sempre `titulo · lista · tag` |

## Regra 5 · Workspace M7

**O que e (reformulado em v1.9.0):** tracking da **saude das frentes do workspace M7 inteiro**. Bruno e Head of Performance — responde pela execucao de todas as frentes, nao so pelas tasks que assinou ou delegou pessoalmente. Foco: *onde o trabalho esta travando, independente de quem e o assignee*?

### Escopo

- Query por **status** (`atrasada`, `bloqueada`), nao por assignee
- Cobertura: workspace inteiro (todas as listas visiveis ao Bruno)
- Bruno-as-assignee aparece destacado como sinal de gargalo pessoal (nao e filtrado fora)

### Regra de curadoria

- **Agrupar por frente** (lista/sprint/projeto do ClickUp). Cada grupo tem 2-3 linhas no maximo
- **Atrasadas no topo**, bloqueadas depois
- **Nome da frente sinaliza o que esta travando** (ex: `PA-Resultado · Seguros` = funil de seguros travado)
- Nunca mais de **4-5 grupos** visiveis. Se tiver mais frentes travadas, priorizar as com maior numero de atrasadas
- Contador no section-header mostra **total real no workspace** (nao o truncado): `<span class="alert">28 atrasadas</span> · 4 bloqueadas`

### Regra "Bruno e o gargalo"

Se Bruno aparece como assignee em uma task dessa coluna:
- Renderizar com modifier visual `.tasks__row--self` (ver componentes.md)
- Nao duplicar: se a task ja aparece na coluna 2 (Tarefas ClickUp), omitir aqui
- Se Bruno tem 3+ atrasadas proprias no workspace, header ganha meta extra `<span class="alert">N minhas</span>` — sinal claro de que ele e o gargalo

### Regra de follow-up visivel

Se uma frente tem 3+ atrasadas num mesmo responsavel, vira candidato a MIT ("Alinhar <pessoa> em <frente>"). Se as 3+ sao de Bruno, o MIT vira "Desafogar minha fila de <frente>".

### Anti-padroes

| Ruim | Melhor |
|---|---|
| Filtrar coluna 3 por `assignee != Bruno` | Escopo e workspace inteiro, inclui Bruno como sinal de gargalo |
| Filtrar coluna 3 por `created_by = Bruno` | Escopo e saude das frentes, nao "meu backlog delegado" |
| Coluna 3 vazia porque "nao deleguei hoje" | Coluna 3 vazia = workspace M7 sem atrasadas/bloqueadas (raro — questionar se extracao funcionou) |
| Contador `8 abertas` no header sem rastreabilidade | Cada numero precisa entrada em `metricas` com query |
| Tarefa de gargalo de Bruno duplicando entre col 2 e col 3 | Aparece so numa, com `--self` na col 3 se for atrasada/bloqueada |

## Regra 6 · Amanha

**O que e:** a secao MAIS importante do planner do ponto de vista de planejamento — porque e o **plano do proximo dia feito ainda hoje**. Disciplina de Cal Newport / Atomic Habits: planejar antes de dormir remove a paralisia matinal.

### Estrutura (template ajustado em v1.4.0)

**Ancora (1 frase imperativa):** o compromisso unico que define amanha.

**Preparar hoje (0-2 bullets curtos):** o que voce precisa fazer/deixar pronto HOJE para amanha funcionar.

### Regra de foco

Se a "Ancora" tem mais de uma frase, nao e uma ancora. Reduzir. A ancora deve caber em:

> Ancora: [verbo imperativo] [objeto] [qualificador de tempo se relevante].

Exemplos validos:
- *"Apresentar o WBR de Investimentos para a diretoria as 10h."*
- *"Fechar os Cards de Performance N2 antes do ritual de quarta."*

Exemplo invalido:
- *"Segunda dedica blocos profundos a criar os Cards de Performance N2 de Investimentos (YAML), aproveitando a validacao entregue por Pedro hoje, e a customizar POP e template de pauta, destravando o primeiro ciclo do Ritual N2 em 22/04."* (isso e um paragrafo inteiro — nao e ancora, e um mini-lide)

### Regra de preparacao

Cada item de "Preparar hoje" deve ser uma acao que **cabe em ate 15min hoje** e destrava amanha. Exemplos:
- *"Enviar para Pedro o template YAML para ele ja comecar."*
- *"Bloquear 9h-10h30 de amanha no calendario."*

Nao virem aqui 1h de preparacao. Isso vira MIT de hoje, nao preparacao.

### Anti-padroes

| Ruim | Melhor |
|---|---|
| Ancora e um paragrafo descritivo | Reduzir a 1 frase imperativa |
| "Preparar" tem 5 bullets | Cortar para 0-2. Resto vira MIT de hoje |
| Ancora cita 3 objetivos | Escolher UM |

## Checklist de sanidade final

Antes de passar para a Fase 3 (renderizacao), validar:

```
[ ] Lide tem UMA tese argumentativa (nao lista)?
[ ] Lide tem 2-4 entidades em <em>, nao mais?
[ ] Tres inadiaveis cobrem >=2 dimensoes (trabalho/corpo/familia)?
[ ] MIT #1 e Eat-the-frog (pior/maior/mais adiado)?
[ ] Cada MIT tem pre-mortem de 1 linha?
[ ] Agenda esta <=60% ocupada em 9h-18h?
[ ] MIT #1 tem bloco >=90min reservado em 9h-12h?
[ ] Almoco presente (mesmo que vazio) como quebra?
[ ] Tarefas ClickUp cortadas em 5-6 + "+N futuras"?
[ ] Tarefas ordenadas por ABCDE, nao por ordem do ClickUp?
[ ] Nenhuma task em status blacklist (cancelada/descartada/won't do) no planner?
[ ] Tasks em status ambiguo destinadas a MIT foram confirmadas via `AskUserQuestion`?
[ ] Coluna 3 usa query por status (atrasada/bloqueada) no workspace inteiro (nao filtro de assignee)?
[ ] Tasks com `assignee==Bruno` na coluna 3 aparecem com `--self` (gargalo)?
[ ] Nenhuma task duplicada entre coluna 2 e coluna 3?
[ ] Cada contador no HTML tem entrada em `extracao.metricas` com query rastreavel?
[ ] Contadores recalculados a partir das linhas extraidas (nao reusados do header da API)?
[ ] Numero de atrasadas usa UMA fonte (status=atrasada ou due vencido, nunca soma)?
[ ] Ancora de Amanha cabe em 1 frase imperativa?
[ ] Preparar hoje tem 0-2 bullets (cada um <=15min)?
```

Se algum item falhar, **voltar e ajustar antes de renderizar**. Plano errado bonito > plano errado feio, mas plano certo feio >> plano errado bonito.
