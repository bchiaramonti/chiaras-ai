# Service Desk M7

Plugin de criacao de chamados de TI para o [Cowork](https://claude.com/product/cowork). Guia o usuario por um processo conversacional para coletar informacoes e gera arquivos markdown formatados com Resumo e Descricao prontos para submissao ao service desk.

## O que faz

Este plugin da ao Claude a capacidade de criar chamados de suporte de TI estruturados:

- **Reportar Problema** — Erros de sistema, funcionalidades quebradas, comportamento inesperado. Coleta sistema afetado, erro exibido, frequencia, impacto e tentativas de solucao.
- **Gerar/Atualizar Base** — Solicitacoes de novas bases de dados ou atualizacao de bases existentes. Coleta empresa, periodo, sistema relacionado, formato e prazo.
- **Solicitar Algo Novo** — Pedidos de dashboards, relatorios, campos, botoes ou automacoes. Coleta necessidade, resultado esperado, beneficios, referencias e prioridade.

## Skills

| Skill | Descricao |
|-------|-----------|
| `creating-service-desk-tickets` | Guia conversacional para criar chamados de TI formatados em markdown |

## Exemplos de Uso

### Reportar um problema

```
Voce: O Bitrix travou quando tentei exportar o relatorio de vendas ontem.

Claude: [Identifica: REPORTAR PROBLEMA]
        [Pergunta: Qual mensagem de erro apareceu?]
        [Pergunta: Isso aconteceu so uma vez ou e recorrente?]
        [Pergunta: Qual o impacto na equipe?]
        [Valida informacoes com o usuario]
        [Gera: 2026-02-25_problema_bitrix24-erro-exportacao-relatorio.md]
```

### Solicitar uma base de dados

```
Voce: Preciso atualizar a base de performance comercial com dados do Q1 2026.

Claude: [Identifica: GERAR/ATUALIZAR BASE]
        [Pergunta: Qual empresa?]
        [Pergunta: Em qual sistema os dados serao usados?]
        [Pergunta: Mesmo formato da base anterior?]
        [Valida informacoes com o usuario]
        [Gera: 2026-02-25_base_m7-atualizacao-performance-q1.md]
```

### Pedir algo novo

```
Voce: Quero pedir um dashboard automatico de performance para os gestores.

Claude: [Identifica: SOLICITAR ALGO NOVO]
        [Pergunta: Que tipo de entrega? Dashboard, relatorio, campo?]
        [Pergunta: Qual o problema que isso resolve?]
        [Pergunta: Ja alinhou com o gestor?]
        [Valida informacoes com o usuario]
        [Gera: 2026-02-25_novo_cowork-dashboard-performance.md]
```

## Formato de Output

Cada chamado e gerado como um arquivo markdown com:

- **Cabecalho**: Data, solicitante, urgencia
- **Resumo**: Frase concisa no formato `[Sistema/Tipo] - [Acao] - [Contexto]`
- **Descricao**: Tabela estruturada com todos os campos obrigatorios
- **Evidencias**: Checklist de anexos recomendados
- **Observacoes**: Informacoes adicionais

**Naming convention**: `YYYY-MM-DD_tipo_sistema-resumo.md`

## Processo Conversacional

O plugin segue 5 fases:

1. **Identificar** — Classifica o tipo de chamado automaticamente
2. **Coletar** — Faz perguntas uma por vez, infere o que puder
3. **Validar** — Apresenta resumo para confirmacao do usuario
4. **Gerar** — Cria arquivo markdown formatado
5. **Orientar** — Instrui sobre proximos passos (revisar, anexar, submeter)
