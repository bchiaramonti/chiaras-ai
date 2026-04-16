# User Flows — <PROJECT_NAME>

> **Fase:** Design
> **Skill:** user-flow-mapping
> **Status:** draft
> **Data:** <YYYY-MM-DD>

---

## 1. Visão Geral dos Fluxos

<!-- Tabela resumo: 1 linha por fluxo, vinculando épico, user stories cobertas e quantidade de telas. -->

| ID | Fluxo | Épico | User Stories | Telas | Persona Principal |
|----|-------|-------|-------------|-------|-------------------|
| FLOW-001 | <NOME_FLUXO_1> | <EPICO_1> | <US-001, US-002, ...> | <N> | <PERSONA> |
| FLOW-002 | <NOME_FLUXO_2> | <EPICO_2> | <US-003, US-004, ...> | <N> | <PERSONA> |

<!-- Adicionar linhas conforme necessário. Todos os Must Have devem estar cobertos. -->

---

## 2. Fluxos Detalhados

<!-- Um sub-section por fluxo. Cada fluxo descreve o caminho do usuário passo a passo. -->

### FLOW-001: <NOME_FLUXO_1>

**Épico:** <EPICO_1>
**Persona:** <PERSONA>
**User Stories:** <US-001, US-002, ...>

#### Ponto de Entrada

<!-- Como o usuário chega a este fluxo: URL direta, botão, redirect, deeplink, etc. -->

<PONTO_DE_ENTRADA>

#### Passos do Fluxo

<!-- Descrever cada passo: tela visitada, ações disponíveis, transição para o próximo passo. -->

| Passo | Tela / Estado | Rota Sugerida | Ações do Usuário | Transição |
|-------|--------------|---------------|-------------------|-----------|
| 1 | <TELA_1> | <ROTA_1> | <ACOES_1> | <TRANSICAO_1> |
| 2 | <TELA_2> | <ROTA_2> | <ACOES_2> | <TRANSICAO_2> |
| 3 | <TELA_3> | <ROTA_3> | <ACOES_3> | <TRANSICAO_3> |

<!-- Adicionar passos conforme necessário. -->

#### Ponto de Saída

<!-- Onde o fluxo termina: tela de confirmação, redirect ao dashboard, logout, etc. -->

<PONTO_DE_SAIDA>

#### Diagrama

<!-- Referência ao diagrama Mermaid correspondente no arquivo .mermaid -->

> Ver diagrama `FLOW-001` em `02-design/user-flows.mermaid`

---

### FLOW-002: <NOME_FLUXO_2>

**Épico:** <EPICO_2>
**Persona:** <PERSONA>
**User Stories:** <US-003, US-004, ...>

#### Ponto de Entrada

<PONTO_DE_ENTRADA>

#### Passos do Fluxo

| Passo | Tela / Estado | Rota Sugerida | Ações do Usuário | Transição |
|-------|--------------|---------------|-------------------|-----------|
| 1 | <TELA_1> | <ROTA_1> | <ACOES_1> | <TRANSICAO_1> |
| 2 | <TELA_2> | <ROTA_2> | <ACOES_2> | <TRANSICAO_2> |

#### Ponto de Saída

<PONTO_DE_SAIDA>

#### Diagrama

> Ver diagrama `FLOW-002` em `02-design/user-flows.mermaid`

---

<!-- Repetir a estrutura acima para cada fluxo adicional (FLOW-003, FLOW-004, ...). -->

---

## 3. Estados Especiais

<!-- Mapear estados não-happy-path para cada tela principal dos fluxos acima. -->

### 3.1 Empty States

<!-- Telas que podem aparecer sem dados: primeiro uso, lista vazia, busca sem resultado. -->

| Tela | Condição | Comportamento Esperado |
|------|----------|----------------------|
| <TELA> | <CONDICAO_EMPTY> | <COMPORTAMENTO: mensagem, CTA, ilustração> |

### 3.2 Loading States

<!-- Telas que dependem de carregamento assíncrono. -->

| Tela | Tipo de Loading | Comportamento Esperado |
|------|----------------|----------------------|
| <TELA> | <skeleton / spinner / placeholder> | <COMPORTAMENTO> |

### 3.3 Error States

<!-- Telas onde erros podem ocorrer: validação, rede, permissão, 404. -->

| Tela | Tipo de Erro | Comportamento Esperado | Recuperação |
|------|-------------|----------------------|-------------|
| <TELA> | <validacao / rede / permissao / 404> | <MENSAGEM_ERRO> | <retry / redirect / fallback> |

### 3.4 Success States

<!-- Confirmações visuais após ações concluídas. -->

| Tela | Ação Concluída | Comportamento Esperado |
|------|---------------|----------------------|
| <TELA> | <ACAO> | <toast / redirect / modal de confirmação> |

---

## 4. Referência Mermaid

Os diagramas visuais de todos os fluxos estão consolidados em:

> `02-design/user-flows.mermaid`

<!-- Cada diagrama usa `flowchart TD` com a seguinte convenção de nós:
  - Retângulos arredondados ([texto]) → início/fim
  - Retângulos [texto] → telas/estados
  - Losangos {texto} → decisões/condições
  - Subgraphs → agrupamento por contexto (ex: checkout, onboarding)
  - Labels nas arestas → ações/transições
-->

Formato de cada diagrama no arquivo `.mermaid`:

```
%% FLOW-<NNN>: <Nome do Fluxo>
flowchart TD
    START([Início]) --> TELA1[Tela 1]
    TELA1 -->|ação| TELA2[Tela 2]
    TELA2 --> DECISAO{Condição?}
    DECISAO -->|sim| SUCESSO([Sucesso])
    DECISAO -->|não| ERRO[Erro]
    ERRO -->|retry| TELA2
```

---

## Status

- **Criado em:** <YYYY-MM-DD>
- **Última atualização:** <YYYY-MM-DD>
- **Status:** draft
- **Aprovado por:** —
- **Data de aprovação:** —
