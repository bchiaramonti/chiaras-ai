---
name: security-baseline
description: >-
  Applies OWASP Top 10 security checks to the project and generates a security
  checklist with implementation recommendations. Reads architecture to understand
  the attack surface and maps each OWASP category to the project's specific context.
  Produces 06-quality/security-baseline.md.
user-invocable: false
---

# Security Baseline

Aplica verificações de segurança OWASP Top 10 ao contexto do projeto e gera checklist com recomendações concretas de implementação. Lê a arquitetura para entender a superfície de ataque (endpoints públicos, dados sensíveis, integrações externas) e mapeia cada uma das 10 categorias OWASP ao stack e padrões do projeto. O artefato resultante funciona como contrato de segurança: toda feature deve ser verificada contra esses critérios antes de ir para produção.

## Pré-requisitos

- `03-architecture/architecture-overview.md` com status `approved` (stack, containers, padrões de comunicação)
- **Opcional:** `03-architecture/adrs/*.md` (decisões que impactam segurança — auth, criptografia, storage)
- **Opcional:** `03-architecture/data-model.md` (para identificar dados sensíveis — PII, financeiro, credenciais)

## Processo

1. **Ler arquitetura para mapear superfície de ataque:**
   - Extrair de `architecture-overview.md`:
     - Stack tecnológica (linguagem, frameworks, runtime)
     - Containers expostos (API, frontend, workers, banco)
     - Padrões de autenticação/autorização (JWT, session, OAuth, API keys)
     - Comunicação: REST, GraphQL, WebSocket, filas de mensagem
     - Storage: banco relacional, NoSQL, cache, file storage, CDN
     - Integrações externas: APIs de terceiros, webhooks, serviços de email/SMS
   - Extrair de `data-model.md` (se disponível):
     - Entidades com dados sensíveis (users, payments, credentials)
     - Campos PII (nome, email, CPF, endereço, telefone)
     - Campos financeiros (saldo, transações, cartões)
   - Extrair de `adrs/*.md` (se disponíveis):
     - Decisões de auth (ex: ADR sobre JWT vs sessions)
     - Decisões de criptografia (ex: bcrypt cost factor, AES para dados em repouso)
     - Decisões de rate limiting, CORS, CSP

2. **Mapear OWASP Top 10 para o contexto do projeto:**
   - Consultar `references/owasp-top10-checklist.md` para cada categoria
   - Para cada uma das 10 categorias OWASP:
     - **Avaliar relevância:** a categoria se aplica ao projeto? (ex: SSRF só se aplica se o sistema faz requests server-side a URLs fornecidas pelo usuário)
     - **Identificar vetores de ataque concretos:** com base na stack e na arquitetura, quais pontos específicos estão expostos?
     - **Definir nível de risco:** Alto / Médio / Baixo — baseado na exposição e no impacto potencial

3. **Para cada categoria: definir risco, verificações e recomendações:**

   **A01 — Broken Access Control:**
   - Verificar: endpoints protegidos têm checagem de autorização (role/permission)
   - Verificar: recursos acessados por ID validam ownership (IDOR protection)
   - Recomendar: middleware de autorização centralizado, deny by default

   **A02 — Cryptographic Failures:**
   - Verificar: dados sensíveis criptografados em trânsito (TLS) e em repouso
   - Verificar: passwords armazenados com hash adequado (bcrypt/scrypt/argon2, nunca MD5/SHA1)
   - Recomendar: env vars para secrets, rotation policy para chaves

   **A03 — Injection:**
   - Verificar: queries parametrizadas (nunca concatenação de strings em SQL/NoSQL)
   - Verificar: output encoding para prevenir XSS (React escapa por default, mas `dangerouslySetInnerHTML` é risco)
   - Recomendar: ORM com prepared statements, sanitização de input, CSP headers

   **A04 — Insecure Design:**
   - Verificar: threat modeling documentado (quais atores maliciosos, quais cenários)
   - Verificar: rate limiting em endpoints sensíveis (login, signup, reset password)
   - Recomendar: abuse cases nas tech specs, feature flags para rollback rápido

   **A05 — Security Misconfiguration:**
   - Verificar: headers de segurança configurados (CSP, X-Frame-Options, HSTS, X-Content-Type-Options)
   - Verificar: debug mode desabilitado em produção, stack traces não expostos
   - Recomendar: checklist de hardening por stack, review de configs antes de deploy

   **A06 — Vulnerable and Outdated Components:**
   - Verificar: dependências auditadas (`npm audit`, `pip audit`, `govulncheck`)
   - Verificar: lockfile presente e atualizado (package-lock.json, poetry.lock, go.sum)
   - Recomendar: Dependabot/Renovate, CI gate que bloqueia PRs com vulnerabilidades críticas

   **A07 — Identification and Authentication Failures:**
   - Verificar: autenticação multi-fator disponível para ações sensíveis
   - Verificar: brute-force protection (lockout ou exponential backoff)
   - Recomendar: tokens com expiração curta, refresh token rotation, logout invalidation

   **A08 — Software and Data Integrity Failures:**
   - Verificar: CI/CD pipeline protegido (branch protection, signed commits se aplicável)
   - Verificar: dependências verificadas por hash (integrity check no lockfile)
   - Recomendar: Subresource Integrity (SRI) para CDN assets, webhook signature verification

   **A09 — Security Logging and Monitoring Failures:**
   - Verificar: logins, falhas de autenticação e operações sensíveis são logados
   - Verificar: logs não contêm dados sensíveis (passwords, tokens, PII em plain text)
   - Recomendar: alertas para padrões suspeitos (múltiplas falhas de login, escalação de privilégio)

   **A10 — Server-Side Request Forgery (SSRF):**
   - Verificar: URLs fornecidas pelo usuário são validadas (allowlist de domínios/IPs)
   - Verificar: requests internos não acessam metadata de cloud (169.254.169.254)
   - Recomendar: se não há requests server-side a URLs externas, marcar como N/A com justificativa

4. **Gerar artefato narrativo:**
   - `06-quality/security-baseline.md` com estrutura:
     - **Resumo:** 1 parágrafo com stack, superfície de ataque, nível geral de risco
     - **Superfície de Ataque:** tabela mapeando containers/endpoints → exposição → dados sensíveis
     - **OWASP Top 10 Mapping:** 1 seção por categoria com:
       - Relevância (Alta/Média/Baixa/N/A)
       - Vetores de ataque identificados no projeto
       - Verificações (checklist com [ ])
       - Recomendações de implementação (concretas, com exemplos de código quando possível)
     - **Priorização:** ordenar categorias por nível de risco (High → Medium → Low → N/A)
     - **Referências:** links para architecture-overview, ADRs, data-model, OWASP Top 10

5. **Atualizar `.status`:**
   - Artifact `security-baseline` → `draft`

## Artefato Gerado

- `06-quality/security-baseline.md`

## Referências

> Para guia detalhado das 10 categorias OWASP com exemplos e checklists, ver [owasp-top10-checklist.md](references/owasp-top10-checklist.md)

## Validação

Antes de marcar como `draft`, verificar:

- [ ] Todas as 10 categorias OWASP estão presentes (A01 a A10)
- [ ] Cada categoria tem: relevância, vetores de ataque, verificações e recomendações
- [ ] Recomendações são específicas para a stack do projeto (não genéricas)
- [ ] Dados sensíveis identificados no data model estão mapeados nas categorias relevantes (A02, A09)
- [ ] Decisões de segurança dos ADRs estão refletidas nas verificações (A01, A02, A07)
- [ ] Categorias não aplicáveis marcadas como N/A com justificativa (ex: A10 se não há SSRF surface)
- [ ] Priorização por nível de risco documentada (High/Medium/Low)
- [ ] Verificações são objetivas e acionáveis (não vagas)
- [ ] Referências cruzadas para architecture-overview, data-model e ADRs
- [ ] Checklist é utilizável como gate de segurança antes de cada release
