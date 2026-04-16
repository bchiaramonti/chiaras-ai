# Wireframe — <NOME_DA_TELA>

> **Fase:** Design
> **Skill:** wireframe-spec
> **Status:** draft
> **Data:** <YYYY-MM-DD>

---

## 1. Propósito

<!-- Qual o objetivo desta tela? Que problema do usuário ela resolve? -->

**User Stories atendidas:** <US-001, US-002, ...>
**Fluxo(s):** <FLOW-001, FLOW-002, ...>
**Persona principal:** <PERSONA>

<DESCRICAO_DO_PROPOSITO>

---

## 2. URL / Rota

| Campo | Valor |
|-------|-------|
| Rota | `<ROTA>` |
| Método de acesso | <URL direta / botão / redirect / deeplink> |
| Autenticação requerida | <Sim / Não> |
| Permissões | <público / autenticado / role específica> |

---

## 3. Layout

<!-- Descrever a disposição geral: header fixo, sidebar colapsável, conteúdo scrollável, etc. -->

**Disposição geral:** <DESCRICAO_DISPOSICAO>

### 3.1 Header

<!-- Elementos do topo da página: logo, navegação, breadcrumbs, ações globais. -->

| Elemento | Descrição | Comportamento |
|----------|-----------|---------------|
| <ELEMENTO_1> | <DESCRICAO> | <COMPORTAMENTO> |
| <ELEMENTO_2> | <DESCRICAO> | <COMPORTAMENTO> |

### 3.2 Conteúdo Principal

<!-- Área central: elementos organizados por hierarquia de informação (o que o usuário vê primeiro). -->

**Hierarquia de informação:**

1. <ELEMENTO_PRIMARIO> — o que o usuário vê primeiro
2. <ELEMENTO_SECUNDARIO> — segunda prioridade visual
3. <ELEMENTO_TERCIARIO> — informações complementares

**Elementos:**

| Elemento | Tipo | Descrição | Prioridade |
|----------|------|-----------|------------|
| <ELEMENTO_1> | <título / tabela / formulário / card / lista / gráfico> | <DESCRICAO> | Alta |
| <ELEMENTO_2> | <título / tabela / formulário / card / lista / gráfico> | <DESCRICAO> | Média |
| <ELEMENTO_3> | <título / tabela / formulário / card / lista / gráfico> | <DESCRICAO> | Baixa |

### 3.3 Sidebar

<!-- Se aplicável. Filtros, navegação secundária, widgets auxiliares. Remover seção se não houver sidebar. -->

| Elemento | Descrição | Comportamento |
|----------|-----------|---------------|
| <ELEMENTO_1> | <DESCRICAO> | <COMPORTAMENTO> |

### 3.4 Footer

<!-- Elementos do rodapé: links, copyright, versão. -->

| Elemento | Descrição |
|----------|-----------|
| <ELEMENTO_1> | <DESCRICAO> |

---

## 4. Ações do Usuário

<!-- Todas as interações possíveis nesta tela. -->

| Ação | Elemento Disparador | Tipo | Resultado Esperado | Disponibilidade |
|------|---------------------|------|-------------------|-----------------|
| <ACAO_1> | <botão / link / campo / ícone> | <click / submit / input / toggle / drag> | <navegação / modal / toast / request> | <sempre / condicional / role> |
| <ACAO_2> | <botão / link / campo / ícone> | <click / submit / input / toggle / drag> | <navegação / modal / toast / request> | <sempre / condicional / role> |

<!-- Adicionar linhas conforme necessário. -->

---

## 5. Estados Visuais

### 5.1 Empty State

<!-- Quando não há dados para exibir: primeiro uso, lista vazia, busca sem resultado. -->

| Condição | Mensagem | CTA | Ilustração |
|----------|----------|-----|------------|
| <CONDICAO_1> | <MENSAGEM> | <TEXTO_BOTAO → DESTINO> | <Sim / Não — descrição> |

### 5.2 Loading State

<!-- Feedback visual durante carregamento assíncrono. -->

| Elemento em loading | Tipo | Comportamento |
|---------------------|------|---------------|
| <ELEMENTO> | <skeleton / spinner / placeholder / progress bar> | <DESCRICAO> |

### 5.3 Error State

<!-- Falhas de rede, validação, permissão, 404. -->

| Tipo de Erro | Condição | Mensagem | Recuperação |
|-------------|----------|----------|-------------|
| <validação / rede / permissão / 404 / timeout> | <CONDICAO> | <MENSAGEM_ERRO> | <retry / redirect / fallback / contato suporte> |

### 5.4 Success State

<!-- Confirmação visual após ações concluídas com sucesso. -->

| Ação Concluída | Tipo de Feedback | Comportamento | Próximo Passo |
|---------------|-----------------|---------------|---------------|
| <ACAO> | <toast / banner / modal / redirect / animação> | <DESCRICAO> | <PROXIMA_ACAO_USUARIO> |

### 5.5 Disabled State

<!-- Elementos desabilitados e razão. Remover seção se não aplicável. -->

| Elemento | Condição para Desabilitar | Tooltip / Explicação |
|----------|--------------------------|---------------------|
| <ELEMENTO> | <CONDICAO> | <TEXTO_TOOLTIP> |

---

## 6. Componentes Reutilizáveis

<!-- Componentes desta tela que aparecem em outras telas. Usar nomes consistentes. -->

| Componente | Descrição | Também usado em |
|-----------|-----------|-----------------|
| <NOME_COMPONENTE> | <DESCRICAO_BREVE> | <TELA_1, TELA_2, ...> |

---

## 7. Notas

<!-- Observações adicionais: decisões de design, restrições técnicas, dúvidas, referências. -->

- <NOTA_1>
- <NOTA_2>

---

## Status

- **Criado em:** <YYYY-MM-DD>
- **Última atualização:** <YYYY-MM-DD>
- **Status:** draft
- **Aprovado por:** —
- **Data de aprovação:** —
