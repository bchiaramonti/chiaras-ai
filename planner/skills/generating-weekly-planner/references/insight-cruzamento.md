# Fase 2b · Insight · cruzamento (horizonte semanal) · regras editoriais (v1.11.0)

Este arquivo **nao descreve mais um processo de geracao**. Desde v1.11.0, o Insight · cruzamento do weekly e sempre gerado pelo agente [`pfeffer-power-analyst`](../../../agents/pfeffer-power-analyst.md) com horizonte=weekly, que le a Tese + Big 3 + Retrospectiva + Riscos atraves das lentes do livro POWER (Pfeffer, 2010).

Este arquivo agora contem **as regras editoriais** que a saida do agente **deve** respeitar. A skill valida a saida do agente contra este checklist antes de renderizar no HTML.

## Por que Pfeffer como fonte unica

Commitment editorial alinhado a identidade do planner (mesma racional do daily):

- Consistencia diaria e semanal cria leitura acumulada. Ler Tese + semana atraves da mesma lente por 90 dias ensina mais que 90 frameworks diferentes.
- A lente Pfeffer cobre semanas politicas (Cap 1/4/6/7/8/9), semanas de recovery ou deep work (Cap 2/10/11/13), semanas pos-setback (Cap 9 × Cap 13), e semanas de transicao (Cap 5 × Cap 10).
- Alem do Insight, o agente pode alimentar a **Regra 6 (Riscos & fogos)** com bloco opcional `## Riscos Pfeffer` — pre-mortem ancorado em capitulos especificos.

## Diferenca em relacao ao daily

| Aspecto | Daily | Weekly |
|---|---|---|
| Horizonte de analise | Desafios do dia (execucao) | Tensionamentos estrategicos da semana (direcao) |
| Insumos para o agente | Agenda + MITs + Workspace M7 + Lide | Retrospectiva S-1 + Tese + Big 3 + Orquestra + Riscos + Corpo semanal |
| Output | Insight + 1-3 Notas do dia | Insight + (opcional) Riscos Pfeffer + (opcional) Notas taticas para preflight |
| Capitulos tipicos | Cap 1 × Cap 7, Cap 9 × Cap 6 | Cap 5 × Cap 10 (alocacao de capital), Cap 2 × Cap 11 (energia sustentada), Cap 1 × Cap 8 (reputacao apos review) |

O padrao de cruzamento binario e identico — muda o horizonte e a profundidade da tese.

## Indice

- [Formato do Insight semanal](#formato-do-insight-semanal)
- [Formato dos Riscos Pfeffer](#formato-dos-riscos-pfeffer)
- [Regras editoriais](#regras-editoriais)
- [Anti-padroes](#anti-padroes)
- [Exemplos validados](#exemplos-validados)

## Formato do Insight semanal

### Estrutura gramatical

O Insight semanal respeita o mesmo padrao visual da Band 1 do weekly, com leitura em dois capitulos em tensao:

```
[Conceito do Cap X] [verbo] [objeto conceitual da semana].
[Conceito do Cap Y] [verbo] [objeto conceitual da semana].
&mdash; sao leituras em tensao: <em>"[tensao do Cap X em 1 pergunta]"</em> vs <em>"[tensao do Cap Y em 1 pergunta]"</em>
```

### Linha de citacao

Formato canonico, consistente com daily:

```
POWER &middot; Cap X (<nome curto>) &times; Cap Y (<nome curto>)
```

### Extensao

- **200-350 caracteres** no corpo (maior que daily porque a Band 1 do weekly tem mais espaco)
- O peso estrategico da semana justifica mais densidade que o insight do dia

## Formato dos Riscos Pfeffer

Quando a semana tem material politico relevante, o agente retorna bloco opcional `## Riscos Pfeffer` que alimenta a **Regra 6 (Riscos & fogos)** da metodologia:

```markdown
## Riscos Pfeffer

- **<Risco 1 em italic curto>** · Cap X
  mitigacao: <acao concreta ancorada em dia da semana>

- **<Risco 2>** · Cap Y
  mitigacao: <acao concreta>

- **<Risco 3>** · Cap Z (opcional)
  mitigacao: <acao concreta>
```

Cada risco:
- E uma frase curta (30-80 chars) em italico
- Referencia 1 capitulo especifico
- Tem mitigacao acionavel ancorada em dia da semana (seg/ter/qua/qui/sex)
- Nao duplica com riscos vindos da retrospectiva ou do workspace M7 (a Regra 6 consolida todas as fontes)

Quando **nao** retornar riscos Pfeffer:
- Semana sem stakeholders externos
- Semana sem eventos de alto risco politico
- Quando os riscos ja capturados pela retrospectiva S-1 ou pelo Workspace M7 sao suficientes

Nesse caso, retornar apenas o bloco de Insight e omitir `## Riscos Pfeffer`. Nao forcar conteudo onde nao ha.

## Regras editoriais

1. **Duas fontes sempre** — exatamente 2 capitulos do livro POWER.
2. **Tensao genuina** — os dois capitulos devem tensionar entre si.
3. **Conectar a Tese e aos Big 3** — o insight responde a uma tensao especifica da semana.
4. **Rotacionar pares semana a semana** — evitar o mesmo cruzamento em semanas consecutivas.
5. **Pt-BR no corpo, vocabulario Pfeffer em ingles quando natural**.
6. **Tom descritivo, nao moralizante**.
7. **Bloco `## Rastro` obrigatorio** na saida do agente, para auditoria.

## Anti-padroes

| Ruim | Por que e ruim | Melhor |
|---|---|---|
| Cruzar dois capitulos sinonimos | Sem tensao | Escolher capitulos em tensao real |
| Insight generico sobre "semana dificil" | Nao cita Pfeffer, nao cruza | Citar dois capitulos especificos + aterrissar na Tese |
| Riscos Pfeffer duplicando Riscos vindos da retro | Redundancia na Regra 6 | Omitir ou integrar ao risco existente |
| Citar outro autor ou livro que nao Pfeffer | Viola fonte unica do sistema | Sempre POWER + dois capitulos |
| Insight tratando semana como serie de dias | Nao e horizonte semanal, e concatenacao | Ler o **arco** da semana, nao cada dia |
| Retornar `## Riscos Pfeffer` em semana sem risco politico | Forca material onde nao ha | Omitir o bloco |

## Exemplos validados

### Exemplo A · Semana politica (retro com oposicao + 3 reviews agendados)

**Insight:**

> Cap 9 diz que a opcao mais barata com Pedro e coopting antes da retro oficial.
> Cap 7 diz que em front de Sergio na review anger/confidence projection vale mais que defesa detalhada.
> &mdash; sao leituras em tensao: <em>"onde eu abro a saida graciosa?"</em> vs <em>"onde eu projeto autoridade?"</em>

**Cite:** `POWER &middot; Cap 9 (Opposition) &times; Cap 7 (Acting with Power)`

**Riscos Pfeffer:**

- **Pedro organizar aliados antes da review de sexta** · Cap 9 (seize the initiative)
  mitigacao: 1:1 privado com Pedro na terca antes que ele recrute apoio

- **Perder postura em front de Sergio se ele contestar o numero** · Cap 7 (anger > sadness)
  mitigacao: ensaiar sabado; pause antes de responder; nunca ceder tom submisso

- **Compensar submissao com Sergio sendo duro com o time** · Cap 11 (disinhibition)
  mitigacao: bloquear 1:1 com Lu sexta-feira apos review para decompressao real

### Exemplo B · Semana de deep work (sem stakeholders externos)

**Insight:**

> Cap 2 lembra que energia e ambicao sao pre-requisitos de poder, nao decorrencias.
> Cap 13 observa que 80% do sucesso e apenas aparecer — pequenas tarefas feitas todos os dias.
> &mdash; sao leituras em tensao: <em>"o que recarregar?"</em> vs <em>"o que acumular em silencio?"</em>

**Cite:** `POWER &middot; Cap 2 (Personal Qualities) &times; Cap 13 (It's Easier Than You Think)`

*(Sem bloco Riscos Pfeffer — semana sem material politico.)*

### Exemplo C · Semana pos-setback

**Insight:**

> Cap 9 reforca: continue fazendo o que te trouxe ate aqui. Nao giveway preemptive.
> Cap 11 adverte: fatigue e overcommitment apos derrota sao os gatilhos classicos de segunda queda.
> &mdash; sao leituras em tensao: <em>"o que insistir?"</em> vs <em>"o que descartar antes do ciclo recomecar?"</em>

**Cite:** `POWER &middot; Cap 9 (Overcoming Setbacks) &times; Cap 11 (How People Lose Power)`

**Riscos Pfeffer:**

- **Cancelar o 1:1 com Sergio por embaraco** · Cap 9 (don't give up)
  mitigacao: manter o 1:1 de quarta, abrir com "o que eu aprendi da ultima reuniao"

- **Sobrecarregar a agenda tentando compensar** · Cap 11 (fatigue)
  mitigacao: recusar 2 convites opcionais na sex; manter quinta como maker day
