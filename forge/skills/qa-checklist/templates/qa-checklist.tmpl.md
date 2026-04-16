# QA Checklist

> **Fase:** Quality
> **Skill:** qa-checklist
> **Status:** draft
> **Data:** <YYYY-MM-DD>
> **Stack:** <STACK_DO_PROJETO ou "Genérico (sem architecture-overview)">

---

## Como Usar

Este checklist deve ser aplicado a **toda feature antes de ser considerada done**. Para cada critério:

- **[ ]** — não verificado ainda
- **[x]** — passa
- **[N/A]** — não aplicável (justificar ao lado)

<!-- Se a aplicação é API-only, marcar as categorias Acessibilidade e Responsividade como N/A com justificativa. -->

---

## 1. Funcionalidade

<!-- Verifica se a feature faz o que deveria fazer. Baseado nos critérios de aceite das tech specs. -->

- [ ] Todos os critérios de aceite da feature passam conforme definido na tech spec
- [ ] Fluxos happy path funcionam end-to-end (do input do usuário até a persistência/response)
- [ ] Edge cases documentados nas tech specs estão cobertos e tratados
- [ ] Não há regressões em funcionalidades existentes (testes de regressão passam)

<!-- Adicionar checks específicos da feature conforme necessário. -->

---

## 2. Performance

<!-- Verifica que a feature atende aos limites de desempenho. Métricas devem ser concretas e mensuráveis. -->

- [ ] Tempo de resposta dentro dos limites: API < 200ms (p95), página < 3s LCP
- [ ] Sem memory leaks detectáveis em uso normal (monitorar durante testes de integração)
- [ ] Queries de banco otimizadas: sem N+1, índices utilizados, EXPLAIN sem full table scan

<!-- Checks adicionais por stack:
  - Web (frontend): Lighthouse Performance score ≥ 90, bundle size < limite definido, Core Web Vitals no verde
  - API: tempo de resposta sob carga (definir RPS target), connection pooling configurado
  - Mobile: tempo de startup < 2s, consumo de memória estável durante navegação
-->

---

## 3. Segurança

<!-- Verifica que a feature não introduz vulnerabilidades. Baseado em OWASP Top 10 e ADRs de segurança. -->

- [ ] Input do usuário sanitizado em todos os pontos de entrada (formulários, query params, headers)
- [ ] Autenticação e autorização verificadas em todos os endpoints protegidos
- [ ] Dados sensíveis não expostos em logs, responses de API, ou client-side storage
- [ ] Dependências sem vulnerabilidades conhecidas (`npm audit` / `pip audit` / `govulncheck` limpo)

<!-- Checks adicionais recomendados:
  - [ ] CSRF protection ativo em formulários que alteram estado
  - [ ] Rate limiting configurado em endpoints públicos
  - [ ] Headers de segurança presentes (CSP, X-Frame-Options, HSTS)
  - [ ] Secrets e credenciais gerenciados via env vars (nunca hardcoded)
  Referência: OWASP Top 10 — https://owasp.org/www-project-top-ten/
-->

---

## 4. Acessibilidade

<!-- Verifica conformidade com WCAG 2.1 nível AA. Se aplicação é API-only, marcar categoria como N/A. -->

- [ ] Todas as imagens têm atributo `alt` descritivo (decorativas usam `alt=""`)
- [ ] Navegação por teclado funciona em todos os elementos interativos (Tab, Enter, Escape)
- [ ] Contraste de cores atende WCAG 2.1 AA: ≥ 4.5:1 (texto normal), ≥ 3:1 (texto grande)
- [ ] Formulários têm `<label>` associados e mensagens de erro acessíveis (`aria-describedby`)

<!-- Checks adicionais recomendados:
  - [ ] Estrutura de headings hierárquica (h1 → h2 → h3, sem pular níveis)
  - [ ] Screen reader consegue navegar o fluxo principal sem perder contexto
  - [ ] Focus indicators visíveis em todos os elementos focáveis
  - [ ] Textos não dependem apenas de cor para transmitir significado
  Referência: WCAG 2.1 — https://www.w3.org/TR/WCAG21/
-->

---

## 5. Responsividade

<!-- Verifica que o layout funciona em diferentes dispositivos. Se API-only, marcar como N/A. -->

- [ ] Layout funcional em mobile (≥ 320px), tablet (≥ 768px) e desktop (≥ 1024px)
- [ ] Elementos interativos têm área de toque mínima de 44x44px em mobile
- [ ] Sem scroll horizontal indesejado em nenhum breakpoint

<!-- Checks adicionais recomendados:
  - [ ] Tipografia legível em todos os tamanhos (min 16px em mobile)
  - [ ] Imagens e mídias responsivas (srcset ou CSS object-fit)
  - [ ] Modais e dropdowns não ultrapassam viewport em telas pequenas
-->

---

## 6. Código

<!-- Verifica qualidade e manutenibilidade do código. Alinhado com code-standards e test-strategy. -->

- [ ] Código passa em todas as regras de lint sem warnings ignorados
- [ ] Formatação consistente (formatter aplicado: Prettier / Ruff / gofmt)
- [ ] Cobertura de testes atende mínimo definido na test-strategy (unit ≥ 80%, global ≥ 70%)
- [ ] Nenhum `TODO` / `FIXME` / `HACK` sem issue associada no código novo

<!-- Checks adicionais recomendados:
  - [ ] Naming conventions seguidas conforme code-standards
  - [ ] Sem código morto ou imports não utilizados
  - [ ] Funções não excedem complexidade ciclomática definida (ex: ≤ 10)
  - [ ] Commits seguem Conventional Commits
-->

---

## Notas

<!-- Observações gerais, exceções justificadas, ou decisões sobre critérios N/A. -->

- <NOTA_1>

---

## Referências

- [Test Strategy](test-strategy.md) — cobertura mínima e ferramentas de teste
- [Code Standards](../../05-implementation/code-standards.md) — padrões de lint, format, naming
- [Architecture Overview](../../03-architecture/architecture-overview.md) — stack e tipo de aplicação
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) — vulnerabilidades de segurança
- [WCAG 2.1](https://www.w3.org/TR/WCAG21/) — acessibilidade

---

## Status

- **Criado em:** <YYYY-MM-DD>
- **Última atualização:** <YYYY-MM-DD>
- **Status:** draft
- **Aprovado por:** —
- **Data de aprovação:** —
