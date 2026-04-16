---
description: Revisa artefatos da fase atual do Forge verificando completude e coerência
---

# Forge Review

## Objetivo

Verificar qualidade dos artefatos da fase atual antes de avançar. Gerar relatório de completude e coerência, e solicitar aprovação do owner para cada artefato.

## Processo

### 1. Ler `.status`

Ler o arquivo `.status` na raiz do projeto. Identificar a `current_phase` e listar todos os artefatos da fase com seus status.

Se não existir `.status`:
"Nenhum projeto Forge encontrado. Execute `/forge:init <nome>` para começar."

### 2. Verificar pré-condição

Se existem artefatos com status `pending` na fase atual:
- Informar: "Existem artefatos ainda não gerados nesta fase. Execute `/forge:next` antes de revisar."
- Listar os artefatos pendentes
- PARAR — não revisar com artefatos faltando

### 3. Ler TODOS os artefatos da fase

Para cada artefato da fase atual com status `draft` ou `approved`:
- Ler o arquivo completo no caminho indicado pelo `.status`
- Se o arquivo não existir, marcar como erro crítico

### 4. Verificar completude

Para cada artefato, verificar:
- **Campos preenchidos** — nenhum placeholder (`<PLACEHOLDER>`) remanescente
- **Seções vazias** — nenhuma seção com conteúdo faltando
- **Tabelas completas** — todas as linhas de tabela preenchidas (sem células vazias marcadas com `<...>`)

### 5. Verificar coerência intra-fase

Artefatos dentro da mesma fase devem ser consistentes entre si:

| Fase | Verificação Intra-fase |
|------|------------------------|
| discovery | problem-statement e landscape-analysis referenciam o mesmo problema e público |
| product | PRD referencia JTBDs do problem-statement; user-story-map cobre os épicos do PRD; mvp-definition é subconjunto do PRD |
| design | wireframes cobrem todas as telas dos user-flows; design-system é consistente com wireframes |
| architecture | C4 diagrams são consistentes com architecture-overview; data-model suporta as entidades referenciadas |
| specs | feature-specs referenciam entidades do data-model e endpoints da architecture |
| implementation | code-standards são compatíveis com a stack definida na architecture; implementation-plan referencia todas as feature-specs |
| quality | test-strategy referencia as feature-specs; qa-checklist é aplicável à stack |
| deploy | deploy-strategy é compatível com a architecture; observability cobre os endpoints definidos |

### 6. Verificar coerência inter-fases

Artefatos devem ser consistentes com fases anteriores:

| Fase Atual | Verificar contra |
|------------|------------------|
| product | discovery: JTBDs, problema, público |
| design | product: épicos, user stories, MVP |
| architecture | product + design: features, telas, fluxos |
| specs | architecture + product: entidades, endpoints, regras |
| implementation | specs: todas as features cobertas |
| quality | specs + implementation: features testáveis |
| deploy | architecture + implementation: infra compatível |

### 7. Gerar relatório

Apresentar ao usuário um relatório estruturado:

```
Revisão da Fase: [Nome da Fase]
Data: [YYYY-MM-DD]

[nome-do-artefato-1]
  ✅ Campos completos
  ✅ Coerência intra-fase OK
  ⚠️ [Descrição do problema encontrado]
  💡 [Sugestão de melhoria opcional]

[nome-do-artefato-2]
  ✅ Campos completos
  ✅ Coerência intra-fase OK
  ✅ Coerência inter-fase OK

Resumo:
  Total de artefatos: [N]
  Sem problemas: [N]
  Com avisos: [N]
  Com erros críticos: [N]
```

### 8. Resolver problemas

Para cada item com ⚠️ ou erro:
- Apresentar o problema ao owner
- Perguntar: "Deseja corrigir agora, ignorar, ou adicionar nota?"
- Se corrigir: fazer a correção no artefato e revalidar
- Se ignorar: registrar a decisão no relatório

### 9. Solicitar aprovação

Após resolver (ou ignorar) todos os problemas, para cada artefato em `draft`:
- Perguntar ao owner: "Aprovar [nome-do-artefato]? (sim/não)"
- Se **sim**: atualizar `.status` → `approved`
- Se **não**: manter como `draft` e registrar feedback do owner para correção posterior

### 10. Resumo final

```
Resultado da revisão:
  ✅ [artefato-1]: approved
  ✅ [artefato-2]: approved
  📝 [artefato-3]: permanece em draft (motivo: [feedback])

Próximo passo:
  - Se todos approved → Execute /forge:advance
  - Se algum em draft → Corrija e execute /forge:review novamente
```
