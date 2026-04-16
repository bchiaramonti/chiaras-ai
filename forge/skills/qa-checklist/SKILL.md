---
name: qa-checklist
description: >-
  Provides a standardized quality checklist (functionality, performance, security,
  accessibility, responsiveness, code quality) that every feature must pass before
  being considered done. Based on Definition of Done and WCAG 2.1 standards.
  Produces 06-quality/qa-checklist.md.
user-invocable: false
---

# QA Checklist

Fornece checklist padronizado de qualidade baseado em Definition of Done + WCAG 2.1. Cobre 6 dimensões: funcionalidade, performance, segurança, acessibilidade, responsividade e código. Se a arquitetura já estiver definida, customiza critérios para a stack do projeto. Serve como contrato de qualidade: toda feature só é "done" quando passa em todos os checks aplicáveis.

## Pré-requisitos

- Nenhum obrigatório (pode ser gerado no scaffold inicial)
- **Opcional:** `03-architecture/architecture-overview.md` com status `approved` (permite customizar critérios por stack)
- **Opcional:** `05-implementation/code-standards.md` (permite alinhar checks de código com padrões definidos)

## Processo

1. **Verificar contexto disponível:**
   - Se `architecture-overview.md` existe e está `approved`:
     - Extrair stack tecnológica (linguagem, frameworks, runtime)
     - Extrair tipo de aplicação (web, API, mobile, CLI, desktop)
     - Identificar se tem frontend (para responsividade/acessibilidade) ou é API-only
   - Se `code-standards.md` existe:
     - Extrair regras de lint, format, naming, cobertura de testes
   - Se nenhum contexto disponível:
     - Gerar checklist genérico (aplicável a qualquer stack web)

2. **Gerar critérios por categoria:**
   - Usar `templates/qa-checklist.tmpl.md` como base
   - Para cada categoria, gerar critérios verificáveis (não vagos):

   **Funcionalidade (4 checks mínimos):**
   - Todos os critérios de aceite da feature passam
   - Fluxos happy path funcionam end-to-end
   - Edge cases documentados nas tech specs estão cobertos
   - Não há regressões em funcionalidades existentes

   **Performance (3 checks mínimos):**
   - Tempo de resposta dentro dos limites definidos (ex: API < 200ms p95, página < 3s LCP)
   - Sem memory leaks detectáveis em uso normal
   - Queries de banco otimizadas (sem N+1, índices utilizados)
   - Se web: Lighthouse Performance score ≥ 90 (customizar por stack)

   **Segurança (4 checks mínimos):**
   - Input do usuário sanitizado em todos os pontos de entrada
   - Autenticação e autorização verificadas em endpoints protegidos
   - Dados sensíveis não expostos em logs, responses, ou client-side storage
   - Dependências sem vulnerabilidades conhecidas (CVE check)
   - Referência: OWASP Top 10 e ADRs de segurança do projeto

   **Acessibilidade (4 checks mínimos):**
   - Todas as imagens têm `alt` text descritivo
   - Navegação por teclado funciona em todos os elementos interativos
   - Contraste de cores atende WCAG 2.1 AA (mínimo 4.5:1 para texto normal)
   - Formulários têm labels associados e mensagens de erro acessíveis
   - Se aplicável: screen reader consegue navegar o fluxo principal

   **Responsividade (3 checks mínimos):**
   - Layout funcional em mobile (≥ 320px), tablet (≥ 768px) e desktop (≥ 1024px)
   - Elementos interativos têm área de toque mínima de 44x44px em mobile
   - Sem scroll horizontal indesejado em nenhum breakpoint
   - Se API-only: categoria marcada como N/A com justificativa

   **Código (4 checks mínimos):**
   - Código passa em todas as regras de lint sem warnings ignorados
   - Formatação consistente (formatter aplicado)
   - Cobertura de testes atende mínimo definido na test-strategy
   - Nenhum TODO/FIXME/HACK sem issue associada
   - Se code-standards existir: naming conventions seguidas

3. **Customizar critérios com base no contexto do projeto:**
   - Se a arquitetura define stack específica:
     - **TypeScript/JavaScript web:** adicionar checks de Lighthouse, bundle size, Core Web Vitals
     - **Python API:** adicionar checks de type hints, docstrings, async handling
     - **Go:** adicionar checks de race conditions, goroutine leaks, golangci-lint
     - **Mobile (React Native/Flutter):** adaptar responsividade para tamanhos de tela nativos
   - Se a aplicação é API-only (sem frontend):
     - Marcar Acessibilidade e Responsividade como N/A
     - Adicionar checks específicos de API: rate limiting, versionamento, documentação OpenAPI
   - Se há design system definido (`02-design/design-system.md`):
     - Adicionar check de aderência ao design system (tokens, componentes)

4. **Gerar artefato usando template:**
   - Preencher `templates/qa-checklist.tmpl.md` com os critérios
   - Cada critério deve ser:
     - **Verificável:** descreve condição objetiva (não "código bom", mas "lint passa sem warnings")
     - **Acionável:** se falhar, fica claro o que corrigir
     - **Rastreável:** referencia padrão externo quando aplicável (WCAG, OWASP, code-standards)
   - Salvar como `06-quality/qa-checklist.md`

5. **Atualizar `.status`:**
   - Artifact `qa-checklist` → `draft`

## Artefato Gerado

- `06-quality/qa-checklist.md`

## Validação

Antes de marcar como `draft`, verificar:

- [ ] Todas as 6 categorias presentes: funcionalidade, performance, segurança, acessibilidade, responsividade, código
- [ ] Cada categoria tem o número mínimo de checks: funcionalidade (4), performance (3), segurança (4), acessibilidade (4), responsividade (3), código (4)
- [ ] Critérios são verificáveis (não vagos) — cada um descreve condição objetiva
- [ ] Critérios de acessibilidade referenciam WCAG 2.1 AA
- [ ] Critérios de segurança referenciam OWASP Top 10 ou ADRs do projeto
- [ ] Performance tem métricas concretas (tempos, scores, limites)
- [ ] Responsividade cobre os 3 breakpoints (mobile, tablet, desktop) ou justifica N/A
- [ ] Código alinha com code-standards (se existir) e test-strategy (se existir)
- [ ] Categorias não aplicáveis marcadas como N/A com justificativa (ex: Responsividade em API-only)
- [ ] Checklist é utilizável tanto para MVP quanto para releases futuras
