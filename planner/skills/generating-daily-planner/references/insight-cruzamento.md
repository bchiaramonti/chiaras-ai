# Fase 2b · Insight · cruzamento · regras editoriais (v1.11.0)

Este arquivo **nao descreve mais um processo de geracao**. Desde v1.11.0, o Insight · cruzamento e as Notas do dia sao sempre geradas pelo agente [`pfeffer-power-analyst`](../../../agents/pfeffer-power-analyst.md), que le a agenda atraves das lentes do livro POWER (Pfeffer, 2010).

Este arquivo agora contem **as regras editoriais** que a saida do agente **deve** respeitar. A skill valida a saida do agente contra este checklist antes de renderizar no HTML.

## Por que Pfeffer como fonte unica

Commitment editorial alinhado a identidade do planner:

- O planner e committed ao design Editorial Noturno (dark mode quente, Georgia + Inter) — nao e tema configuravel. Consistencia diaria cria leitura acumulada.
- A partir de v1.11.0, o Insight e committed a Pfeffer — nao e framework configuravel. 90 dias lendo o trabalho atraves da mesma lente ensina mais que 90 frameworks diferentes.
- A lente Pfeffer cobre tanto dias politicos (Cap 1/4/6/7/8/9) quanto dias operacionais ou pessoais (Cap 2/10/11/13) — ver [agents/pfeffer-power-analyst.md](../../../agents/pfeffer-power-analyst.md) para o mapa completo de cruzamentos.
- Invencao de outro framework e proibida. Se Bruno quiser insight de outra fonte em algum dia especifico, deve pedir manualmente fora da skill.

## Indice

- [Formato do Insight](#formato-do-insight)
- [Formato das Notas do dia](#formato-das-notas-do-dia)
- [Regras editoriais](#regras-editoriais)
- [Anti-padroes](#anti-padroes)
- [Exemplos validados](#exemplos-validados)

## Formato do Insight

### Estrutura gramatical

O Insight gerado pelo agente Pfeffer deve respeitar o padrao visual estabelecido na zona `header__insight`:

```
[Conceito do Cap X] [verbo] [objeto conceitual].
[Conceito do Cap Y] [verbo] [objeto conceitual].
&mdash; sao leituras em tensao: <em>"[tensao do Cap X em 1 pergunta]"</em> vs <em>"[tensao do Cap Y em 1 pergunta]"</em>
```

Os dois `<em>` com perguntas em italico terracota sao **obrigatorios** — formam o "punch" visual da zona.

### Linha de citacao (header__insight-cite)

Formato canonico:

```
POWER &middot; Cap X (<nome curto>) &times; Cap Y (<nome curto>)
```

Exemplos validos:
- `POWER &middot; Cap 1 (Managing Up) &times; Cap 7 (Acting with Power)`
- `POWER &middot; Cap 9 (Opposition) &times; Cap 6 (Networks)`
- `POWER &middot; Cap 2 (Personal Qualities) &times; Cap 10 (Price of Power)`

A linha de citacao e sempre **POWER** como livro, seguida dos dois capitulos com nome curto entre parenteses. Consistencia total — e sempre o mesmo livro.

### Extensao

- **150-250 caracteres** no corpo do insight (sem contar a linha de citacao).
- Cabe na zona de 240px do header sem overflow.
- Acima disso quebra layout; abaixo vira telegrama.

## Formato das Notas do dia

### Estrutura

Cada nota e uma linha compativel com o componente `.note` do HTML:

```html
<div class="note">
  <span class="note__bullet">&mdash;</span>
  <div class="note__text">[texto da nota]</div>
  <div class="note__time">[hora opcional]</div>
</div>
```

### Regras de conteudo

- **1-3 notas** por dia (nunca mais, nunca zero)
- **30-80 caracteres** cada (1 linha visual)
- **Ancorada em capitulo** — o agente sabe de qual capitulo veio, mesmo que nao cite no texto
- **Acionavel hoje** — nao conselho perene, nao meta-observacao
- **Especifica a pessoas/eventos reais da agenda** — "Pedro", "WBR XP", "10h" — nunca "seu colega" ou "essa reuniao"
- **Hora** (`note__time`) aparece quando a nota e ancorada a evento da agenda

### Exemplos validos

- `— Antes da WBR, releia o deck em voz alta 1x. Pausa antes de responder.` (Cap 7)
- `— Com Pedro no 1:1, ouvir primeiro 10min sem interromper.` (Cap 9)
- `— Se Rafa trouxer dado novo, segure o impulso de corrigir.` (Cap 11)

## Regras editoriais

1. **Duas fontes sempre** — exatamente 2 capitulos do livro POWER. Nunca 1, nunca 3+.
2. **Tensao genuina** — os dois capitulos devem tensionar entre si. Se ambos dizem a mesma coisa, escolher outro par.
3. **Conectar a agenda concreta** — o insight nao e aleatorio; ele responde a tensao especifica do dia.
4. **Rotacionar pares ao longo da semana** — evitar o mesmo cruzamento em dias consecutivos. O agente pode reler dias anteriores para validar rotacao.
5. **Pt-BR no corpo, vocabulario Pfeffer em ingles quando natural** — "managing up", "weak ties", "self-promotion dilemma" sao aceitos e ate preferidos.
6. **Tom descritivo, nao moralizante** — "o dia pede X" e melhor que "voce deveria X".
7. **Bloco `## Rastro` obrigatorio na saida do agente** — lista sinais lidos + capitulos descartados. A skill usa para auditoria mas nao renderiza no HTML.

## Anti-padroes

| Ruim | Por que e ruim | Melhor |
|---|---|---|
| Cruzar Cap 1 + Cap 1 ou dois capitulos sinonimos | Sem tensao, viola regra do cruzamento binario | Escolher capitulos em tensao real (ex: Cap 1 vs Cap 7) |
| Insight generico "seja confiante" | Vago, nao cita capitulo, nao cruza | Citar capitulo especifico + aterrissar em pessoa da agenda |
| Citar livro ou autor que nao e Pfeffer | Viola fonte unica do sistema | Sempre POWER + dois capitulos |
| Nota com 2+ linhas | Nao cabe no `.note` | Cortar ou quebrar em duas notas |
| Nota meta ("aplicar Pfeffer hoje") | Meta, nao tatico | Acao concreta com pessoa, horario ou objeto |
| Tom motivacional ("voce pode fazer isso!") | Nao e Pfeffer | Descritivo, tatico ("o movimento de hoje e X") |
| Moralizar sobre jogo politico | Explicitamente anti-Pfeffer | Aceitar o jogo e ler melhor |
| Repetir cruzamento de ontem | Falta de rotacao, vira ruido | Variar par de capitulos |
| Gerar insight sem notas ou notas sem insight | Viola contrato de saida | Sempre ambos — insight + 1-3 notas |

## Exemplos validados

### Exemplo A · Dia politico (agenda com WBR + 1:1 em oposicao)

**Insight:**

> Cap 1 pede reverencia calibrada com Sergio. Cap 9 pede coopting com Pedro.
> &mdash; sao leituras em tensao: <em>"como faco o chefe se sentir bem?"</em> vs <em>"como deixo uma saida graciosa para o opositor?"</em>

**Cite:** `POWER &middot; Cap 1 (Managing Up) &times; Cap 9 (Opposition)`

**Notas:**
- `— 08h55: abrir review perguntando "como voces leem o numero?" antes de defender.`
- `— 11h Pedro: 10min de ouvir antes de propor. Leave him a graceful out.`
- `— 14h XP: confidence projection quando CFO perguntar. Pause before responding.`

### Exemplo B · Dia operacional (deep work solo + treino + leitura)

**Insight:**

> Cap 2 trata energia como atributo primario de poder. Cap 13 lembra que 80% de sucesso e apenas aparecer de novo amanha.
> &mdash; sao leituras em tensao: <em>"o que me da energia hoje?"</em> vs <em>"o que eu acumulo em silencio aqui?"</em>

**Cite:** `POWER &middot; Cap 2 (Personal Qualities) &times; Cap 13 (It's Easier Than You Think)`

**Notas:**
- `— Treino longo sem relogio. Energia e pre-requisito, nao luxo.`
- `— 1h de leitura apos almoco, sem email aberto. Cap 2: self-knowledge.`

### Exemplo C · Dia familia (almoco + tarde livre)

**Insight:**

> Cap 10 reconhece que o preco de poder e o tempo com familia. Cap 2 lembra que ambicao sem laco corroi os dois.
> &mdash; sao leituras em tensao: <em>"o que o poder custa?"</em> vs <em>"onde ele se sustenta?"</em>

**Cite:** `POWER &middot; Cap 10 (Price of Power) &times; Cap 2 (Personal Qualities)`

**Notas:**
- `— Almoco com Bia e filhos sem celular na mesa. Two-person single career.`
- `— Tarde sem agenda. Autonomia que dias de semana nao permitem.`

### Exemplo D · Dia pos-setback (reuniao anterior deu ruim)

**Insight:**

> Cap 9 diz: nao desista, continue fazendo o que te trouxe ate aqui. Cap 11 adverte: fatigue e overconfidence custam posicao.
> &mdash; sao leituras em tensao: <em>"o que insistir?"</em> vs <em>"o que descartar hoje?"</em>

**Cite:** `POWER &middot; Cap 9 (Opposition & Setbacks) &times; Cap 11 (How People Lose Power)`

**Notas:**
- `— Nao cancelar agenda do dia. Showing up pos-derrota e sinal.`
- `— Dormir 22h30. Cap 11: fatigue e precursor de proxima derrota.`
