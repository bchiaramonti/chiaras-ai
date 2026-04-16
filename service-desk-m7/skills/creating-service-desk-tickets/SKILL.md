---
name: creating-service-desk-tickets
description: >
  Cria chamados de TI estruturados para os sistemas M7. Guia o usuário conversacionalmente
  para coletar informações e gera arquivos markdown formatados com Resumo e Descrição prontos
  para submissão. Suporta 3 tipos: Reportar Problema, Gerar/Atualizar Base, e Solicitar Algo Novo.
  Use when the user asks to create a ticket, report a problem, request a database, open a support
  request, create a chamado, report an error, request a new feature, or mentions service desk, helpdesk,
  suporte TI, or sistema com erro.
---

# Criação de Chamados de Service Desk M7

Guie o usuário por um processo conversacional para coletar informações e gerar chamados
de TI formatados como arquivos markdown, prontos para submissão ao service desk.

## Filosofia

**"Um chamado bem escrito resolve metade do problema."**

Um bom chamado responde 3 perguntas:
1. **O que aconteceu?** (ou o que precisa ser feito)
2. **Qual o impacto?** (urgência, pessoas afetadas, processos parados)
3. **O que já foi tentado?** (contexto para a equipe de TI)

## Tipos de Chamado

Existem 3 categorias. Identifique qual se aplica antes de coletar informações.

### Tipo 1: REPORTAR PROBLEMA

**Quando usar**: Sistema com erro, funcionalidade quebrada, comportamento inesperado.

**Sinais no pedido do usuário**: "erro", "não funciona", "travou", "caiu", "bug", "problema",
"parou", "não carrega", "mensagem de erro", "tela branca".

**Campos obrigatórios**:

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| Sistema afetado | Nome do sistema ou módulo | Bitrix24 CRM, Power BI, Cowork |
| Quando ocorreu | Data e hora (ou frequência) | 25/02/2026 às 14:30 |
| Ação sendo executada | O que o usuário fazia no momento | Tentando exportar relatório de vendas |
| Mensagem de erro | Texto exato do erro (se houver) | "Error 500: Internal Server Error" |
| Frequência | Única vez ou recorrente | Toda vez que filtra por data > 30 dias |
| Impacto | Quem é afetado e como | Equipe de 8 pessoas sem acesso ao dashboard |
| Urgência | Crítico / Alto / Médio / Baixo | Crítico — processo parado |
| Tentativas de solução | O que já foi feito | Limpou cache, testou outro navegador |
| Evidências | Screenshots, logs, vídeos | (solicitar se disponível) |

### Tipo 2: GERAR OU ATUALIZAR BASE

**Quando usar**: Precisa de uma nova base de dados ou atualização de base existente.

**Sinais no pedido do usuário**: "base", "dados", "atualizar base", "gerar base", "extração",
"período", "empresa", "importar", "carregar dados".

**Campos obrigatórios**:

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| Tipo de solicitação | Nova base ou atualização | Atualização de base existente |
| Empresa | Empresa envolvida | M7 Investimentos |
| Período dos dados | Mês/ano ou intervalo | Janeiro a Março/2026 |
| Sistema relacionado | Onde os dados serão usados | Power BI Dashboard de Performance |
| Finalidade/contexto | Por que precisa dos dados | Fechamento trimestral de resultados |
| Formato esperado | Especificações técnicas | CSV com separador ; e encoding UTF-8 |
| Data desejada de entrega | Prazo ideal | Até 28/02/2026 |
| Documentos de apoio | Layouts, specs, amostras | (solicitar se disponível) |

### Tipo 3: SOLICITAR ALGO NOVO

**Quando usar**: Precisa de funcionalidade, relatório, dashboard, campo, ou botão novo.

**Sinais no pedido do usuário**: "novo", "criar", "implementar", "dashboard", "relatório",
"campo novo", "botão", "funcionalidade", "melhoria", "automatizar".

**Campos obrigatórios**:

| Campo | Descrição | Exemplo |
|-------|-----------|---------|
| Tipo de entrega | Dashboard, relatório, campo, botão, automação | Novo dashboard de acompanhamento |
| Necessidade/problema | O que motivou o pedido | Gestores perdem 4h/semana montando reports manuais |
| Sistema/processo impactado | Onde será implementado | Cowork — módulo de Performance |
| Resultado esperado | O que deve acontecer | Dashboard atualizado automaticamente toda segunda |
| Benefícios esperados | Ganhos concretos | Redução de 80% no tempo de reports |
| Usuários impactados | Quantidade e áreas | 12 gestores das 6 áreas de negócio |
| Referências/exemplos | Modelo, sketch, benchmark | "Similar ao dashboard X do time Y" |
| Prioridade | Alta / Média / Baixa | Alta — alinhado com gestor |
| Prazo desejado | Timeline ideal | Até final de março/2026 |
| Alinhamento com gestor | Se já foi validado | Sim — aprovado pelo Diretor de Performance |

## Workflow Conversacional

### Fase 1: Identificar Tipo do Chamado

Analise o pedido inicial do usuário e classifique:

```
┌─ Menciona erro, bug, sistema parado?
│  └─ SIM → REPORTAR PROBLEMA
├─ Menciona base de dados, extração, período?
│  └─ SIM → GERAR/ATUALIZAR BASE
├─ Menciona novo recurso, dashboard, relatório?
│  └─ SIM → SOLICITAR ALGO NOVO
└─ Não está claro?
   └─ Pergunte: "Você precisa reportar um problema, solicitar uma base de dados,
      ou pedir algo novo (dashboard, relatório, funcionalidade)?"
```

Informe o tipo identificado ao usuário e prossiga para coleta.

### Fase 2: Coleta Conversacional

**Regras de coleta:**

1. **Pergunte UMA informação por vez** — Não sobrecarregue o usuário
2. **Adapte a ordem** — Comece pelo mais relevante ao contexto dado
3. **Infira quando possível** — Se o usuário já deu informação, não pergunte de novo
4. **Sugira quando adequado** — Se o usuário diz "urgente", sugira "Prioridade: Crítico"
5. **Peça evidências** — Para problemas, sempre pergunte sobre screenshots
6. **Valide antes de gerar** — Confirme as informações coletadas antes de montar o chamado

**Frases-guia por tipo:**

| Tipo | Primeira pergunta |
|------|-------------------|
| Problema | "Para entender melhor, qual sistema específico está apresentando o erro?" |
| Base | "Você precisa criar uma nova base ou atualizar uma existente?" |
| Novo | "Que tipo de entrega você precisa? (dashboard, relatório, campo, botão, automação)" |

**Detecção de urgência por keywords:**

| Keyword | Urgência sugerida |
|---------|-------------------|
| "crítico", "parado", "urgente", "bloqueado" | Crítico |
| "importante", "impacta equipe", "prazo" | Alto |
| "quando puder", "melhoria", "seria bom" | Médio |
| "sugestão", "futuro", "sem pressa" | Baixo |

### Fase 3: Validação

Antes de gerar o arquivo, apresente um resumo das informações coletadas:

```markdown
## Resumo do Chamado

**Tipo**: [tipo identificado]
**Sistema**: [sistema]
**Resumo**: [frase resumo]

### Informações coletadas:
- Campo 1: valor
- Campo 2: valor
- ...

Está correto? Quer ajustar algo antes de eu gerar o chamado?
```

Aguarde confirmação do usuário. Se houver ajustes, aplique e revalide.

### Fase 4: Gerar Arquivo Markdown

Gere o arquivo seguindo os templates em [references/templates.md](references/templates.md).

**Naming convention**: `YYYY-MM-DD_tipo_sistema-resumo.md`

Exemplos:
- `2026-02-25_problema_bitrix24-erro-exportacao-relatorio.md`
- `2026-02-25_base_m7-atualizacao-dados-jan-mar.md`
- `2026-02-25_novo_cowork-dashboard-performance.md`

**Destino padrão**: Pergunte ao usuário onde salvar. Sugestões:
- Projeto ativo: `1-projects/<projeto>/chamados/`
- Área M7: `2-areas/m7/chamados/`
- Sem contexto: `0-inbox/` (para triagem posterior)

### Fase 5: Orientações Pós-Geração

Após gerar o arquivo, oriente o usuário:

1. **Revisar** o conteúdo gerado
2. **Anexar evidências** mencionadas (screenshots, logs, documentos)
3. **Copiar** Resumo e Descrição para o sistema de chamados
4. **Registrar** o número do chamado no arquivo (se desejar rastreabilidade)

## Regras de Qualidade

### Por Chamado

- [ ] Tipo de chamado identificado corretamente?
- [ ] Resumo é conciso (< 80 caracteres)?
- [ ] Resumo segue formato: `[Sistema/Tipo] - [Ação] - [Contexto]`?
- [ ] Descrição tem todos os campos obrigatórios preenchidos?
- [ ] Informações são específicas (datas, nomes, números)?
- [ ] Urgência está definida e justificada?
- [ ] Impacto está quantificado (pessoas, processos, tempo)?

### Anti-Patterns

- **Nunca gerar chamado sem coleta completa** — Pergunte o que falta antes de gerar
- **Nunca assumir sistema** — Sempre pergunte qual sistema está envolvido
- **Nunca pular validação** — Confirme com o usuário antes de gerar o arquivo
- **Nunca usar linguagem técnica excessiva** — O chamado deve ser compreensível para TI e negócio
- **Nunca inventar informações** — Se não foi dito, pergunte ou marque como "A definir"
- **Nunca gerar sem data** — Todo chamado tem data de criação
- **Nunca misturar tipos** — Se o usuário tem um problema E um pedido novo, gere 2 chamados separados

## Regras Importantes

1. **Conversacional** — A skill funciona como um diálogo, não um formulário. Seja natural
2. **1 pergunta por vez** — Nunca faça 3 perguntas de uma vez
3. **Inferência inteligente** — Se o usuário diz "o Bitrix travou quando tentei exportar ontem", você já tem: sistema (Bitrix), ação (exportar), quando (ontem)
4. **Português brasileiro** — Toda comunicação e arquivos em PT-BR
5. **Markdown formatado** — O output é um arquivo .md estruturado, não texto solto
6. **Data no nome** — Sempre prefixar com YYYY-MM-DD
7. **Evidências são opcionais** — Sugira, mas não bloqueie o chamado se não houver
