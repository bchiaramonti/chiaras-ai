---
name: changelog-manager
description: >-
  Maintains CHANGELOG.md following Keep a Changelog and Semantic Versioning.
  Automatically invoked by forge:advance when a phase is completed. Can also
  be triggered when features are implemented or releases are cut. Updates
  CHANGELOG.md at the project root.
user-invocable: false
---

# Changelog Manager

Mantém `CHANGELOG.md` atualizado no formato Keep a Changelog + SemVer. Esta é uma skill **transversal** — diferente das outras skills que pertencem a uma fase, o changelog-manager é invocado automaticamente pelo `forge:advance` ao final de cada fase. Também pode ser invocado manualmente quando features são implementadas ou quando uma release é criada.

O arquivo `CHANGELOG.md` é criado pelo `forge:init` na raiz do projeto usando `templates/changelog.tmpl.md` como base.

## Pré-requisitos

- `CHANGELOG.md` existente na raiz do projeto (criado por `forge:init`)
- `.status` acessível (para saber o que mudou)

## Processo

1. **Ler estado atual:**
   - Ler `CHANGELOG.md` atual, preservando toda a formatação e conteúdo existente
   - Ler `.status` para identificar:
     - Qual fase acabou de ser completada (quando invocado via `forge:advance`)
     - Quais artefatos foram gerados/aprovados nessa fase
   - Se invocado fora do `forge:advance` (ex: feature implementada):
     - Receber do contexto: o que mudou e qual categoria (Added/Changed/Fixed/Removed)

2. **Determinar categoria da entrada:**
   - Mapear o evento à categoria Keep a Changelog:
     - **Added** — nova funcionalidade ou artefato criado
       - Conclusão de fase (via `forge:advance`): "Fase [Nome] concluída"
       - Nova feature implementada
       - Novo artefato gerado
     - **Changed** — alteração em funcionalidade existente
       - Artefato revisado e atualizado após review
       - Refatoração de código
     - **Fixed** — correção de bug
       - Bug corrigido durante implementação
       - Artefato corrigido após review
     - **Removed** — funcionalidade removida
       - Feature removida do escopo (movida para Won't Have)
       - Código deprecado removido
     - **Deprecated** — funcionalidade marcada para remoção futura
     - **Security** — correção de vulnerabilidade de segurança
   - Na maioria das invocações via `forge:advance`, a categoria será **Added**

3. **Adicionar entrada na seção `[Unreleased]`:**
   - Localizar a seção `## [Unreleased]` no `CHANGELOG.md`
   - Dentro de `[Unreleased]`, localizar ou criar a subcategoria adequada (ex: `### Added`)
   - Adicionar a entrada como bullet point:
     - **Para conclusão de fase:**
       ```
       - Fase [Nome] concluída: [lista dos artefatos gerados separados por vírgula]
       ```
       Exemplo:
       ```
       - Fase Discovery concluída: problem-statement.md, landscape-analysis.md
       ```
     - **Para feature implementada:**
       ```
       - [Descrição concisa da feature] ([referência à tech spec se aplicável])
       ```
     - **Para correção:**
       ```
       - [Descrição do que foi corrigido]
       ```
   - Manter entradas em ordem cronológica (mais recente no topo da categoria)
   - Nunca duplicar entradas — verificar se o mesmo evento já foi registrado

4. **Criar release versionada (quando solicitado):**
   - Este passo só é executado quando o owner explicitamente solicita uma release
   - **Determinar versão SemVer:**
     - `MAJOR` — mudanças incompatíveis com versão anterior (breaking changes)
     - `MINOR` — novas funcionalidades (backwards-compatible)
     - `PATCH` — correções de bugs
     - Se é a primeira release: usar `1.0.0`
     - Se é conclusão do pipeline completo: sugerir bump de `MINOR` ou `MAJOR` conforme impacto
   - **Mover conteúdo de `[Unreleased]` para versão numerada:**
     - Criar nova seção `## [X.Y.Z] — YYYY-MM-DD` logo abaixo de `## [Unreleased]`
     - Mover todas as categorias com suas entradas de `[Unreleased]` para a nova seção
     - Deixar `## [Unreleased]` vazio (pronto para próximas entradas)
   - **Atualizar links no rodapé:**
     - Adicionar link de comparação para a nova versão
     - Atualizar link do `[Unreleased]` para comparar com a nova versão

## Artefato Mantido

- `CHANGELOG.md` (raiz do projeto)

> **Nota:** Este artefato não aparece no `.status` como artifact individual. O `CHANGELOG.md` é um artefato transversal que acompanha o projeto do início ao fim. Seu template é usado pelo `forge:init` para criar o arquivo inicial.

## Regras de Formato (Keep a Changelog)

1. **Estrutura hierárquica:** `# Changelog` → `## [Versão]` → `### Categoria` → `- Entrada`
2. **Categorias válidas:** Added, Changed, Deprecated, Removed, Fixed, Security
3. **Ordem das versões:** mais recente no topo, `[Unreleased]` sempre primeiro
4. **Formato de data:** `YYYY-MM-DD` (ISO 8601)
5. **Links de comparação:** no rodapé, formato `[X.Y.Z]: https://github.com/owner/repo/compare/vA.B.C...vX.Y.Z`
6. **Nunca editar entradas de versões já publicadas** (imutabilidade — mesmo princípio dos ADRs)

## Validação

Antes de salvar o `CHANGELOG.md` atualizado, verificar:

- [ ] Formato Keep a Changelog válido (hierarquia correta de seções)
- [ ] Entrada adicionada na categoria correta (Added/Changed/Fixed/Removed/Deprecated/Security)
- [ ] Seção `[Unreleased]` existe e está no topo (abaixo do título)
- [ ] Entradas anteriores não foram modificadas ou removidas
- [ ] Data no formato ISO 8601 (YYYY-MM-DD) em versões numeradas
- [ ] Se release: versão SemVer válida e incremento correto
- [ ] Se release: links de comparação atualizados no rodapé
- [ ] Nenhuma entrada duplicada
- [ ] Descrições concisas e informativas (não genéricas como "atualizações diversas")
