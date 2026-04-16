---
name: data-model-designer
description: >-
  Designs the complete data model with entities, attributes, relationships,
  constraints, and indexes. Generates ER diagrams in Mermaid and documentation.
  Use after architecture is defined. Triggers adr-writer for denormalization
  decisions. Produces 03-architecture/data-model.md and
  03-architecture/data-model.mermaid.
user-invocable: false
---

# Data Model Designer

Projeta modelo de dados completo com entidades, atributos, relacionamentos, constraints e índices. Gera diagramas ER em Mermaid e documentação estruturada. Lê o PRD para identificar entidades do domínio e a arquitetura para alinhar o tipo de banco e padrões de acesso. Invoca `adr-writer` para documentar qualquer desnormalização consciente.

## Pré-requisitos

- `03-architecture/architecture-overview.md` com status `approved`
- `01-product/prd.md` com status `approved`

## Processo

1. **Ler PRD para identificar entidades do domínio:**
   - Extrair substantivos recorrentes: personas, objetos, conceitos (ex: "Usuário", "Pedido", "Produto")
   - Mapear cada user story para entidades que ela pressupõe
   - Listar entidades candidatas com descrição de 1 frase cada
   - Atenção a entidades implícitas (ex: "enviar notificação" implica entidade `Notification`)

2. **Ler user stories para identificar atributos necessários:**
   - Para cada entidade candidata, percorrer todas as user stories que a mencionam
   - Extrair atributos explícitos ("email do usuário") e implícitos ("quando o pedido foi criado" → `created_at`)
   - Atenção a atributos derivados vs armazenados (ex: "total do pedido" pode ser calculado ou armazenado)
   - Listar atributos candidatos por entidade

3. **Ler arquitetura para alinhar tipo de banco:**
   - Verificar em `architecture-overview.md`: banco escolhido (SQL/NoSQL), ORM/ODM, estratégia de migrations
   - Adaptar tipos de dados ao dialeto do banco (ex: `varchar` vs `text` no PostgreSQL, `ObjectId` no MongoDB)
   - Se NoSQL: modelar pensando em padrões de acesso (query-driven design) em vez de normalização
   - Se SQL: modelar em 3NF como ponto de partida

4. **Para cada entidade — definir atributos, tipos e constraints:**
   - Atributo: nome em `snake_case`
   - Tipo: adequado ao banco escolhido (ex: `uuid`, `varchar(255)`, `timestamp with time zone`, `jsonb`)
   - Constraints:
     - `PK` — Primary Key (preferencialmente `id uuid` ou auto-increment)
     - `FK` — Foreign Key (referenciando entidade.atributo)
     - `UNIQUE` — quando o domínio exige unicidade
     - `NOT NULL` — padrão para campos obrigatórios (explícito é melhor que implícito)
     - `DEFAULT` — valores padrão quando aplicável
     - `CHECK` — validações no nível do banco quando críticas
   - Incluir `created_at` e `updated_at` em TODAS as entidades (auditoria básica)
   - Se soft-delete necessário: incluir `deleted_at` (nullable)

5. **Mapear relacionamentos com cardinalidade e cascade:**
   - Para cada par de entidades relacionadas:
     - Tipo: `1:1`, `1:N`, `N:N`
     - FK: qual entidade carrega a foreign key
     - Se `N:N`: criar tabela de junção explícita com nome descritivo (ex: `order_items`, não `orders_products`)
   - Regras de cascade:
     - `ON DELETE CASCADE` — quando filhos não fazem sentido sem o pai
     - `ON DELETE SET NULL` — quando o relacionamento é opcional
     - `ON DELETE RESTRICT` — quando a exclusão precisa ser bloqueada (proteção de integridade)
   - Documentar em tabela: entidade A | relação | entidade B | FK | cascade

6. **Identificar índices para queries frequentes:**
   - Analisar user stories e user flows para prever queries mais comuns
   - Índices obrigatórios: PKs (automáticos), FKs (explícitos)
   - Índices recomendados:
     - Colunas usadas em `WHERE` frequente
     - Colunas usadas em `ORDER BY`
     - Colunas com constraint `UNIQUE`
   - Índices compostos quando queries filtram por múltiplas colunas
   - Documentar: entidade | coluna(s) | tipo de índice | justificativa

7. **Normalizar até 3NF — desnormalizar conscientemente se justificado:**
   - Verificar:
     - 1NF: todos os atributos são atômicos (sem listas, sem objetos aninhados em SQL)
     - 2NF: sem dependências parciais em chaves compostas
     - 3NF: sem dependências transitivas (atributo depende só da PK)
   - Se uma desnormalização for necessária por performance ou simplicidade:
     - Documentar a justificativa
     - **Invocar skill `adr-writer`** para criar ADR da desnormalização
     - Exemplo: "armazenar `total_amount` no `Order` em vez de calcular na hora" → ADR

8. **Gerar artefatos:**
   - `03-architecture/data-model.md` — usando `templates/data-model.tmpl.md`:
     - Resumo do modelo (1 parágrafo: quantas entidades, que domínio, tipo de banco)
     - Entidades (1 seção por entidade com tabela de atributos)
     - Relacionamentos (tabela consolidada)
     - Índices (tabela consolidada)
     - Notas de normalização (justificativas de desnormalização com referência a ADRs)
     - Referência ao diagrama ER
   - `03-architecture/data-model.mermaid` — diagrama ER completo:
     - Usar sintaxe `erDiagram` do Mermaid
     - Todas as entidades com atributos tipados
     - Todos os relacionamentos com cardinalidade (`||--o{`, `||--||`, `}o--o{`)
     - Nomes de relacionamentos descritivos em inglês (ex: `places`, `contains`, `belongs-to`)

9. **Atualizar `.status`:**
   - Artifact `data-model` → `draft`
   - Artifact `data-model-diagram` → `draft`

## Artefatos Gerados

- `03-architecture/data-model.md` (via `templates/data-model.tmpl.md`)
- `03-architecture/data-model.mermaid`

## Validação

Antes de marcar como `draft`, verificar:

- [ ] Todas as entidades do PRD estão representadas (nenhum substantivo relevante ficou de fora)
- [ ] Cada entidade tem PK definida
- [ ] Cada entidade tem `created_at` e `updated_at`
- [ ] Todos os atributos têm tipo adequado ao banco escolhido na arquitetura
- [ ] Constraints `NOT NULL` explícitos em campos obrigatórios
- [ ] Relacionamentos têm cardinalidade explícita (`1:1`, `1:N`, `N:N`)
- [ ] Tabelas de junção criadas para todos os relacionamentos `N:N`
- [ ] Regras de cascade definidas para todas as FKs
- [ ] Índices definidos para FKs e colunas de busca frequente
- [ ] Modelo em 3NF ou desnormalizações justificadas com ADR
- [ ] Diagrama Mermaid `erDiagram` renderiza sem erros de sintaxe
- [ ] Diagrama inclui todas as entidades e relacionamentos do documento
- [ ] Terminologia consistente entre `data-model.md` e `data-model.mermaid`
- [ ] Tipos de dados consistentes com o banco definido em `architecture-overview.md`
