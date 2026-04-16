# OWASP Top 10 — Checklist de Referência

Guia detalhado das 10 categorias OWASP (edição 2021) para uso pela skill `security-baseline`. Cada categoria inclui descrição, exemplos concretos de vulnerabilidade, e checklist de verificação.

> **Fonte:** OWASP Top 10 (2021) — https://owasp.org/www-project-top-ten/

---

## Índice

1. [A01 — Broken Access Control](#a01--broken-access-control)
2. [A02 — Cryptographic Failures](#a02--cryptographic-failures)
3. [A03 — Injection](#a03--injection)
4. [A04 — Insecure Design](#a04--insecure-design)
5. [A05 — Security Misconfiguration](#a05--security-misconfiguration)
6. [A06 — Vulnerable and Outdated Components](#a06--vulnerable-and-outdated-components)
7. [A07 — Identification and Authentication Failures](#a07--identification-and-authentication-failures)
8. [A08 — Software and Data Integrity Failures](#a08--software-and-data-integrity-failures)
9. [A09 — Security Logging and Monitoring Failures](#a09--security-logging-and-monitoring-failures)
10. [A10 — Server-Side Request Forgery (SSRF)](#a10--server-side-request-forgery-ssrf)

---

## A01 — Broken Access Control

**Descrição:** Falhas em restringir o que usuários autenticados podem fazer. Um atacante pode acessar recursos de outros usuários, modificar permissões, ou acessar funcionalidades administrativas sem autorização.

**Posição no ranking:** #1 (subiu de #5 em 2017). 94% das aplicações testadas apresentaram alguma forma de broken access control.

**Exemplos de vulnerabilidade:**

- **IDOR (Insecure Direct Object Reference):** Alterar `GET /api/users/123/orders` para `GET /api/users/456/orders` e acessar pedidos de outro usuário
- **Escalação de privilégio vertical:** Usuário comum acessa `/admin/dashboard` por falta de checagem server-side
- **Falta de verificação de ownership:** `DELETE /api/posts/789` deleta post de outro usuário porque o endpoint só valida autenticação, não autorização
- **Path traversal:** Upload de arquivo com nome `../../../etc/passwd` que escapa do diretório permitido

**Checklist de verificação:**

- [ ] Todos os endpoints protegidos verificam autenticação E autorização
- [ ] Recursos acessados por ID validam ownership do usuário logado (IDOR protection)
- [ ] Política "deny by default" — endpoints sem regra explícita são bloqueados
- [ ] Middleware de autorização centralizado (não checagem manual em cada handler)
- [ ] CORS configurado para aceitar apenas origens permitidas (não `Access-Control-Allow-Origin: *`)
- [ ] Testes automatizados para cenários de acesso não autorizado (ex: user A tenta acessar recurso de user B)
- [ ] Rate limiting em endpoints de admin/management

---

## A02 — Cryptographic Failures

**Descrição:** Proteção inadequada de dados sensíveis — em trânsito e em repouso. Inclui uso de algoritmos fracos, chaves hardcoded, falta de criptografia, e exposição acidental de dados.

**Posição no ranking:** #2 (subiu de #3 em 2017). Anteriormente chamado "Sensitive Data Exposure".

**Exemplos de vulnerabilidade:**

- **Passwords em plain text ou com hash fraco:** Usar MD5 ou SHA1 em vez de bcrypt/scrypt/argon2
- **Dados sensíveis em trânsito sem TLS:** API interna comunicando via HTTP em vez de HTTPS
- **Chaves e secrets hardcoded:** `const API_KEY = "sk-abc123"` no código-fonte
- **Backup de banco sem criptografia:** Dump SQL com dados de clientes em storage público

**Checklist de verificação:**

- [ ] Todas as comunicações externas usam TLS 1.2+ (HTTP → HTTPS redirect)
- [ ] Passwords armazenados com hash adaptativo (bcrypt cost ≥ 10, scrypt, ou argon2id)
- [ ] Dados sensíveis em repouso criptografados (AES-256 para PII, financeiros, saúde)
- [ ] Secrets gerenciados via env vars ou secret manager (nunca hardcoded no código)
- [ ] Chaves de criptografia com rotation policy definida
- [ ] Nenhum dado sensível em logs (passwords, tokens, números de cartão)
- [ ] Headers `Strict-Transport-Security` (HSTS) configurado
- [ ] Certificados TLS válidos e com renovação automática

---

## A03 — Injection

**Descrição:** Dados não confiáveis enviados a um interpretador como parte de um comando ou query. O atacante injeta código malicioso que é executado pelo servidor. Inclui SQL injection, NoSQL injection, command injection, LDAP injection, e Cross-Site Scripting (XSS).

**Posição no ranking:** #3 (caiu de #1 em 2017). Agora inclui XSS como subcategoria.

**Exemplos de vulnerabilidade:**

- **SQL Injection:** `SELECT * FROM users WHERE id = '${req.params.id}'` — atacante envia `1' OR '1'='1`
- **NoSQL Injection:** `db.users.find({ email: req.body.email })` — atacante envia `{ "$gt": "" }` como email
- **Command Injection:** `exec('ping ' + userInput)` — atacante envia `; rm -rf /`
- **XSS (Reflected/Stored):** Input do usuário renderizado em HTML sem escaping — atacante injeta `<script>document.cookie</script>`
- **Template Injection (SSTI):** `render("Hello {{name}}")` com input não sanitizado em engines como Jinja2, EJS

**Checklist de verificação:**

- [ ] Queries SQL/NoSQL usam parametrização (prepared statements, query builders, ORM)
- [ ] Nunca concatenação de strings para construir queries
- [ ] Output encoding habilitado (React escapa por default; atenção com `dangerouslySetInnerHTML`, `v-html`, `| safe`)
- [ ] Content-Security-Policy (CSP) header configurado (bloqueia inline scripts)
- [ ] Input validation com allowlist (não blocklist) para formatos esperados
- [ ] Sanitização de HTML em campos rich-text (DOMPurify, bleach)
- [ ] Nenhum `eval()`, `exec()`, ou `Function()` com input do usuário
- [ ] Testes automatizados com payloads maliciosos nos inputs

---

## A04 — Insecure Design

**Descrição:** Falhas de design que não podem ser corrigidas apenas com código — o sistema foi projetado sem considerar cenários de abuso. Diferente de implementação insegura: aqui o design em si é vulnerável.

**Posição no ranking:** #4 (nova categoria em 2021).

**Exemplos de vulnerabilidade:**

- **Falta de rate limiting no login:** Permite brute force de passwords sem limite
- **Pergunta de segurança como único recovery:** "Qual o nome do seu pet?" é facilmente descoberto em redes sociais
- **Falta de confirmação em ações destrutivas:** `DELETE /api/account` sem confirmação por email/senha
- **Lógica de negócio explorável:** Cupom de desconto aplicável infinitas vezes porque não valida uso único

**Checklist de verificação:**

- [ ] Threat modeling documentado (atores maliciosos, cenários de abuso)
- [ ] Rate limiting em endpoints sensíveis (login: max 5 tentativas/min, signup: max 3/hora)
- [ ] Ações destrutivas requerem confirmação (re-autenticação, código por email, ou "type DELETE to confirm")
- [ ] Abuse cases documentados nas tech specs ("E se o usuário tentar X?")
- [ ] Limites de negócio implementados (ex: cupom com `max_uses`, transfer com `daily_limit`)
- [ ] Feature flags para rollback rápido de funcionalidades com risco

---

## A05 — Security Misconfiguration

**Descrição:** Configurações de segurança ausentes, incompletas, ou com defaults inseguros. Inclui permissões excessivas, features desnecessárias habilitadas, e headers de segurança ausentes.

**Posição no ranking:** #5 (subiu de #6 em 2017). 90% das aplicações testadas apresentaram alguma misconfiguration.

**Exemplos de vulnerabilidade:**

- **Debug mode em produção:** Stack traces expostos com informações internas
- **Defaults inseguros:** Credenciais default do banco (admin/admin) não alteradas
- **Directory listing habilitado:** Atacante navega `/uploads/` e vê todos os arquivos
- **Headers de segurança ausentes:** Sem CSP, X-Frame-Options, X-Content-Type-Options
- **Permissões excessivas:** Service account do banco com `GRANT ALL` em vez de permissões mínimas

**Checklist de verificação:**

- [ ] Debug mode / stack traces desabilitados em produção
- [ ] Headers de segurança configurados:
  - `Content-Security-Policy` (CSP)
  - `X-Frame-Options: DENY` (ou `SAMEORIGIN`)
  - `X-Content-Type-Options: nosniff`
  - `Strict-Transport-Security` (HSTS)
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Permissions-Policy` (câmera, microfone, geolocation)
- [ ] Error responses genéricos para usuários (sem stack traces, sem nomes de tabelas)
- [ ] Features desnecessárias desabilitadas (ex: GraphQL introspection em produção)
- [ ] Permissões mínimas para service accounts (princípio do menor privilégio)
- [ ] Directory listing desabilitado
- [ ] Checklist de hardening aplicado por ambiente (dev vs staging vs prod)

---

## A06 — Vulnerable and Outdated Components

**Descrição:** Uso de bibliotecas, frameworks, ou componentes com vulnerabilidades conhecidas (CVEs). Inclui dependências desatualizadas, componentes sem manutenção, e falta de monitoramento de vulnerabilidades.

**Posição no ranking:** #6 (subiu de #9 em 2017).

**Exemplos de vulnerabilidade:**

- **Log4Shell (CVE-2021-44228):** Vulnerabilidade crítica em Log4j que permitia RCE via JNDI injection
- **Prototype pollution em lodash:** Versões antigas de lodash permitiam manipulação de protótipos JavaScript
- **Dependência abandonada:** Biblioteca sem atualizações há 3+ anos com CVEs conhecidos
- **Transitive dependency vulnerável:** Projeto não usa diretamente a lib vulnerável, mas uma dependência dela sim

**Checklist de verificação:**

- [ ] Audit de dependências executado e limpo (`npm audit`, `pip audit`, `govulncheck`, `cargo audit`)
- [ ] Lockfile presente e atualizado (package-lock.json, poetry.lock, go.sum, Cargo.lock)
- [ ] Dependabot, Renovate, ou equivalente configurado para PRs automáticas
- [ ] CI gate que bloqueia PRs com vulnerabilidades de severidade alta/crítica
- [ ] Inventário de dependências documentado (SBOM — Software Bill of Materials)
- [ ] Nenhuma dependência com vulnerabilidade conhecida de severidade alta/crítica
- [ ] Dependências sem manutenção (>2 anos sem update) identificadas e com plano de migração

---

## A07 — Identification and Authentication Failures

**Descrição:** Falhas na verificação de identidade do usuário. Inclui brute force de passwords, sessões mal gerenciadas, credenciais fracas, e falta de proteção contra automação.

**Posição no ranking:** #7 (caiu de #2 em 2017). Anteriormente chamado "Broken Authentication".

**Exemplos de vulnerabilidade:**

- **Brute force sem proteção:** Login permite tentativas ilimitadas de password
- **Session fixation:** Sessão não é regenerada após login, permitindo roubo de sessão
- **Tokens sem expiração:** JWT com `exp` ausente ou muito longo (30 dias)
- **Password policy fraca:** Aceita "123456" como password válido
- **Credential stuffing:** Atacante usa listas de credenciais vazadas em login automatizado

**Checklist de verificação:**

- [ ] Brute-force protection: lockout temporário ou exponential backoff após N falhas
- [ ] Password policy com requisitos mínimos (comprimento ≥ 8, complexidade, ou check contra lista de passwords comuns)
- [ ] Tokens (JWT) com expiração curta (access: 15min, refresh: 7 dias max)
- [ ] Refresh token rotation (novo refresh token a cada uso, invalidar o anterior)
- [ ] Sessão regenerada após login (previne session fixation)
- [ ] Logout efetivo: token/sessão invalidado server-side (não apenas removido do client)
- [ ] MFA disponível para ações sensíveis (alterar password, transações financeiras)
- [ ] Mensagens de erro genéricas ("credenciais inválidas", nunca "usuário não encontrado" vs "password incorreto")

---

## A08 — Software and Data Integrity Failures

**Descrição:** Código e infraestrutura que não verificam integridade de atualizações, dados críticos, e pipelines de CI/CD. Inclui desserialização insegura e supply chain attacks.

**Posição no ranking:** #8 (nova categoria em 2021). Anteriormente era subcategoria "Insecure Deserialization".

**Exemplos de vulnerabilidade:**

- **CI/CD comprometido:** Atacante injeta código malicioso via PR sem review em pipeline sem proteção
- **Desserialização insegura:** `pickle.loads(user_input)` em Python permite execução de código arbitrário
- **CDN sem SRI:** Script de CDN modificado por atacante e servido sem verificação de hash
- **Auto-update sem verificação:** Aplicação baixa updates sem verificar assinatura digital

**Checklist de verificação:**

- [ ] CI/CD pipeline protegido: branch protection, PR obrigatório com review, secrets não expostos em logs
- [ ] Dependências verificadas por hash (integrity check via lockfile)
- [ ] Subresource Integrity (SRI) para assets de CDN (`<script integrity="sha384-...">`)
- [ ] Nenhuma desserialização de dados não confiáveis (evitar `pickle`, `eval`, `unserialize` com input externo)
- [ ] Webhook payloads verificados via signature (HMAC)
- [ ] Signed commits habilitados (recomendado, não obrigatório para projetos pequenos)

---

## A09 — Security Logging and Monitoring Failures

**Descrição:** Falta de logging adequado e monitoramento de eventos de segurança. Sem isso, ataques em andamento não são detectados e investigações pós-incidente ficam impossíveis.

**Posição no ranking:** #9 (subiu de #10 em 2017). Anteriormente chamado "Insufficient Logging & Monitoring".

**Exemplos de vulnerabilidade:**

- **Login failures não logados:** Brute force attack passa despercebido por semanas
- **Logs com dados sensíveis:** Password do usuário aparece em plain text no log de requests
- **Sem alertas:** 1000 tentativas de login falhadas em 1 hora não geram notificação
- **Logs sem retenção:** Logs deletados após 24h, impossibilitando investigação forense

**Checklist de verificação:**

- [ ] Eventos de segurança logados: login (sucesso/falha), alteração de permissões, operações sensíveis, erros de autorização
- [ ] Logs não contêm dados sensíveis: passwords, tokens, PII em plain text são mascarados
- [ ] Formato de log estruturado (JSON) com timestamp, user_id, action, result, IP
- [ ] Retenção de logs definida (mínimo 90 dias para logs de segurança)
- [ ] Alertas configurados para padrões suspeitos:
  - Múltiplas falhas de login do mesmo IP (>10 em 5min)
  - Tentativa de escalação de privilégio
  - Acesso a endpoints de admin por usuários não-admin
- [ ] Logs centralizados (não apenas em stdout do container)
- [ ] Log tampering prevention (logs em storage append-only ou com integridade verificada)

---

## A10 — Server-Side Request Forgery (SSRF)

**Descrição:** O servidor faz requests HTTP a URLs fornecidas ou influenciadas pelo usuário sem validação adequada. O atacante pode acessar serviços internos, metadados de cloud, ou fazer port scanning.

**Posição no ranking:** #10 (nova categoria em 2021).

**Exemplos de vulnerabilidade:**

- **Acesso a metadata de cloud:** Atacante fornece `http://169.254.169.254/latest/meta-data/` como URL de avatar e obtém credenciais da instância AWS
- **Port scanning interno:** Atacante fornece `http://internal-service:8080/health` para descobrir serviços na rede interna
- **Bypass de firewall:** Aplicação faz request a URL interna que o usuário não teria acesso direto
- **File protocol:** Atacante fornece `file:///etc/passwd` como URL

**Checklist de verificação:**

- [ ] URLs fornecidas pelo usuário validadas contra allowlist de domínios/IPs permitidos
- [ ] Blocklist para IPs internos: `127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16`
- [ ] Protocolos permitidos restritos a `http` e `https` (bloquear `file://`, `ftp://`, `gopher://`)
- [ ] Redirect following desabilitado ou com re-validação (open redirect → SSRF chain)
- [ ] Se não há funcionalidade que aceita URLs do usuário: marcar como **N/A** com justificativa
- [ ] Testes com payloads de SSRF: metadata endpoints, IPs internos, protocolos não-HTTP

---

## Referências Gerais

- [OWASP Top 10 — 2021 Edition](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [OWASP Testing Guide v4](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
- [CWE/SANS Top 25 Most Dangerous Software Weaknesses](https://cwe.mitre.org/top25/)
