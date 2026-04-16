# Templates de Chamados

Templates completos para os 3 tipos de chamado. Use como base para gerar os arquivos markdown.

---

## 1. Template: Reportar Problema

```markdown
# Chamado: Reportar Problema

**Data**: DD/MM/YYYY
**Solicitante**: [nome]
**Urgência**: [Crítico / Alto / Médio / Baixo]

---

## Resumo

[Sistema] - [Tipo de Erro] - [Funcionalidade]

## Descrição

### Contexto
[1-2 frases descrevendo o que aconteceu]

### Detalhes

| Campo | Informação |
|-------|-----------|
| **Sistema afetado** | [nome do sistema/módulo] |
| **Quando ocorreu** | [data/hora ou frequência] |
| **Ação sendo executada** | [o que estava fazendo] |
| **Mensagem de erro** | [texto exato do erro, se houver] |
| **Frequência** | [única vez / recorrente — detalhar] |
| **Impacto** | [quem é afetado e como] |
| **Tentativas de solução** | [o que já foi tentado] |

### Evidências

[Screenshots, logs, ou referências a arquivos anexos]
- [ ] Screenshot anexado
- [ ] Log de erro anexado

### Observações

[Informações adicionais relevantes]
```

### Exemplo Preenchido: Reportar Problema

```markdown
# Chamado: Reportar Problema

**Data**: 25/02/2026
**Solicitante**: Bruno Chiaramonti
**Urgência**: Alto

---

## Resumo

Bitrix24 CRM - Erro de exportação - Relatório de vendas por período

## Descrição

### Contexto
Ao tentar exportar o relatório de vendas filtrado por período superior a 30 dias,
o sistema retorna erro 500 e a exportação não é concluída.

### Detalhes

| Campo | Informação |
|-------|-----------|
| **Sistema afetado** | Bitrix24 CRM — Módulo de Relatórios |
| **Quando ocorreu** | 25/02/2026 às 14:30 (recorrente desde 24/02) |
| **Ação sendo executada** | Exportar relatório de vendas com filtro de período > 30 dias |
| **Mensagem de erro** | "Error 500: Internal Server Error — Request timeout" |
| **Frequência** | Recorrente — toda vez que o filtro de período excede 30 dias |
| **Impacto** | Equipe de Performance (8 pessoas) sem acesso ao relatório trimestral. Bloqueia o fechamento do mês |
| **Tentativas de solução** | Limpeza de cache, teste em Chrome e Edge, redução do período para 25 dias (funciona) |

### Evidências

- [ ] Screenshot do erro 500 anexado
- [x] Teste com período de 25 dias funciona (evidência de que o problema é no filtro > 30 dias)

### Observações

O problema parece estar relacionado ao timeout da query quando o período é muito grande.
Relatórios com filtros de até 25 dias funcionam normalmente.
```

---

## 2. Template: Gerar ou Atualizar Base

```markdown
# Chamado: Gerar/Atualizar Base de Dados

**Data**: DD/MM/YYYY
**Solicitante**: [nome]
**Urgência**: [Crítico / Alto / Médio / Baixo]

---

## Resumo

[Tipo: Nova/Atualização] de base - [Empresa] - [Período]

## Descrição

### Contexto
[1-2 frases descrevendo a necessidade]

### Detalhes

| Campo | Informação |
|-------|-----------|
| **Tipo de solicitação** | [nova base / atualização de base existente] |
| **Empresa** | [nome da empresa] |
| **Período dos dados** | [mês/ano ou intervalo] |
| **Sistema relacionado** | [onde os dados serão usados] |
| **Finalidade** | [por que precisa dos dados] |
| **Formato esperado** | [especificações técnicas] |
| **Data desejada de entrega** | [prazo] |

### Documentos de Apoio

[Layouts, specs, amostras, ou referências]
- [ ] Layout de importação anexado
- [ ] Amostra de dados anexada

### Observações

[Informações adicionais relevantes]
```

### Exemplo Preenchido: Gerar/Atualizar Base

```markdown
# Chamado: Gerar/Atualizar Base de Dados

**Data**: 25/02/2026
**Solicitante**: Bruno Chiaramonti
**Urgência**: Médio

---

## Resumo

Atualização de base - M7 Investimentos - Jan-Mar/2026

## Descrição

### Contexto
Necessário atualizar a base de dados de performance comercial com os dados do primeiro
trimestre de 2026 para alimentar o dashboard de fechamento.

### Detalhes

| Campo | Informação |
|-------|-----------|
| **Tipo de solicitação** | Atualização de base existente |
| **Empresa** | M7 Investimentos |
| **Período dos dados** | Janeiro a Março/2026 |
| **Sistema relacionado** | Power BI — Dashboard de Performance Comercial |
| **Finalidade** | Fechamento trimestral de resultados para apresentação à diretoria |
| **Formato esperado** | CSV com separador `;`, encoding UTF-8, mesma estrutura da base anterior |
| **Data desejada de entrega** | Até 05/04/2026 |

### Documentos de Apoio

- [x] Layout da base anterior disponível em `2-areas/m7/sandbox/bases/layout-performance.csv`
- [ ] Nenhum documento adicional necessário

### Observações

Manter a mesma estrutura de colunas da base do Q4/2025. Se houver novos campos disponíveis
(ex: NPS por funil), incluir como colunas opcionais no final.
```

---

## 3. Template: Solicitar Algo Novo

```markdown
# Chamado: Solicitar Algo Novo

**Data**: DD/MM/YYYY
**Solicitante**: [nome]
**Urgência**: [Crítico / Alto / Médio / Baixo]

---

## Resumo

[Tipo de Entrega] - [Sistema] - [Área]

## Descrição

### Contexto
[1-2 frases descrevendo a necessidade e motivação]

### Detalhes

| Campo | Informação |
|-------|-----------|
| **Tipo de entrega** | [dashboard / relatório / campo / botão / automação / funcionalidade] |
| **Necessidade/problema** | [o que motivou o pedido] |
| **Sistema/processo impactado** | [onde será implementado] |
| **Resultado esperado** | [o que deve acontecer quando pronto] |
| **Benefícios esperados** | [ganhos concretos e mensuráveis] |
| **Usuários impactados** | [quantidade e áreas] |
| **Prioridade** | [Alta / Média / Baixa — com justificativa] |
| **Prazo desejado** | [timeline ideal] |
| **Alinhamento com gestor** | [se já foi validado e por quem] |

### Referências e Exemplos

[Modelos, sketches, benchmarks, ou exemplos de outros sistemas]
- [ ] Sketch/wireframe anexado
- [ ] Referência visual anexada

### Especificações (se aplicável)

[Detalhes técnicos, regras de negócio, filtros, campos específicos]

### Observações

[Informações adicionais relevantes]
```

### Exemplo Preenchido: Solicitar Algo Novo

```markdown
# Chamado: Solicitar Algo Novo

**Data**: 25/02/2026
**Solicitante**: Bruno Chiaramonti
**Urgência**: Alto

---

## Resumo

Dashboard - Cowork Performance - M7 Investimentos

## Descrição

### Contexto
Os gestores das 6 áreas de negócio gastam em média 4h/semana montando reports manuais
em Excel. Um dashboard automatizado no Cowork eliminaria esse retrabalho e padronizaria
a visão de performance.

### Detalhes

| Campo | Informação |
|-------|-----------|
| **Tipo de entrega** | Dashboard de acompanhamento de performance |
| **Necessidade/problema** | Gestores perdem 4h/semana com reports manuais em Excel |
| **Sistema/processo impactado** | Cowork — módulo de Performance |
| **Resultado esperado** | Dashboard atualizado automaticamente toda segunda às 8h |
| **Benefícios esperados** | Redução de 80% no tempo de reports, padronização da visão entre áreas |
| **Usuários impactados** | 12 gestores + 6 diretores das áreas de negócio |
| **Prioridade** | Alta — alinhado com Diretor de Performance |
| **Prazo desejado** | MVP até final de março/2026, versão completa até abril/2026 |
| **Alinhamento com gestor** | Sim — aprovado pelo Diretor de Performance em reunião de 20/02 |

### Referências e Exemplos

- [x] Referência: Dashboard similar do time de Crédito (`2-areas/m7/referencias/dashboard-credito.png`)
- [ ] Wireframe em elaboração

### Especificações

- KPIs por funil: captação líquida, NPS, ticket médio, taxa de conversão
- Filtros: período (mês/trimestre/ano), funil, gestor
- Atualização: automática via API do CRM, toda segunda às 8h
- Acesso: gestores N2 e diretores N3

### Observações

O MVP deve conter apenas captação líquida e NPS por funil. Demais KPIs entram na versão completa.
Priorizar a visão consolidada (todos os funis) sobre a visão individual.
```

---

## Checklist de Geração

Ao gerar um chamado, confirme:

- [ ] Tipo de chamado está correto?
- [ ] Resumo segue o formato `[X] - [Y] - [Z]` e tem < 80 caracteres?
- [ ] Todos os campos obrigatórios estão preenchidos?
- [ ] Informações são específicas (não genéricas)?
- [ ] Urgência está definida?
- [ ] Impacto está quantificado?
- [ ] Data de criação está no cabeçalho e no nome do arquivo?
- [ ] Nome do arquivo segue `YYYY-MM-DD_tipo_sistema-resumo.md`?
- [ ] Seção de evidências orienta sobre anexos?
