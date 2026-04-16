---
name: observability-setup
description: >-
  Configures structured logging, error tracking, health checks, and basic usage
  metrics for production observability. Reads architecture and deploy strategy
  to tailor recommendations to the project's stack and hosting platform.
  Produces 07-deploy/observability-setup.md.
user-invocable: false
---

# Observability Setup

Configura os pilares de observabilidade do projeto: logging estruturado, error tracking, health checks e metricas basicas de uso. Garante que a equipe consiga diagnosticar problemas em producao rapidamente e monitorar a saude do sistema desde o primeiro deploy.

## Pre-requisitos

| Artefato | Status minimo |
|----------|---------------|
| `03-architecture/architecture-overview.md` | `approved` |
| `07-deploy/deploy-strategy.md` | `approved` |

> **Nota:** A arquitetura define quais componentes precisam de observabilidade (API, workers, banco, filas). A deploy strategy define a plataforma de hosting e os triggers de rollback — ambos influenciam diretamente as escolhas de ferramentas e configuracoes de health check.

## Processo

1. **Ler arquitetura e deploy strategy para mapear o que monitorar:**
   - Extrair de `architecture-overview.md`:
     - Stack tecnologica (linguagem, runtime, framework)
     - Componentes do sistema (frontend, backend, banco de dados, filas, cache, workers)
     - Dependencias externas (APIs de terceiros, servicos cloud)
     - Diagrama de containers (C4 Level 2) para identificar pontos de falha
   - Extrair de `deploy-strategy.md`:
     - Plataforma de hosting (PaaS, containers, Kubernetes, VPS)
     - Environments definidos (dev, staging, production)
     - Triggers de rollback (health check, error rate, latencia)
     - Pipeline CI/CD (para integrar checks de observabilidade)
   - Listar todos os **componentes observaveis** (cada servico/container que precisa emitir logs, metricas ou responder a health checks)

2. **Definir logging estruturado: formato, niveis, retencao:**
   - Definir **formato** de log:
     - **JSON estruturado** (recomendado) — facilita parsing, busca e agregacao
     - Campos obrigatorios: `timestamp`, `level`, `message`, `service`, `requestId`/`traceId`
     - Campos opcionais: `userId`, `action`, `duration`, `error` (com stack trace)
   - Definir **niveis** de log e quando usar cada um:
     - `error` — falha que impede a operacao (exception, erro de banco, API indisponivel)
     - `warn` — situacao anormal mas recuperavel (retry, fallback, deprecation)
     - `info` — evento significativo de negocio (usuario criado, pedido processado, deploy)
     - `debug` — detalhe tecnico para diagnostico (query SQL, payload, estado interno)
   - Definir **nivel default** por ambiente:
     - Production: `info` (nunca `debug` em producao por default)
     - Staging: `debug`
     - Development: `debug`
   - Escolher **biblioteca de logging** adequada a stack:
     - **Node.js/TypeScript:** pino (JSON nativo, alta performance) ou winston
     - **Python:** structlog (JSON nativo) ou logging com json-log-formatter
     - **Go:** zerolog ou zap (ambos JSON nativo)
   - Definir **retencao** de logs:
     - Production: 30 dias (minimo) — ajustar conforme compliance
     - Staging: 7 dias
     - Development: sem retencao (apenas stdout)
   - Definir **destino** dos logs:
     - **PaaS (Vercel, Railway, Fly.io):** log drain nativo da plataforma
     - **Containers/Kubernetes:** stdout → log aggregator (Loki, ELK, CloudWatch Logs)
     - **VPS:** arquivo local → rotacao (logrotate) + envio para aggregator
   - **REGRA:** Nunca logar dados sensiveis (senhas, tokens, PII) — aplicar sanitizacao

3. **Definir error tracking: ferramenta e configuracao:**
   - Escolher **ferramenta** de error tracking:
     - **Sentry** (recomendado para maioria dos projetos) — SDK para todas as stacks, free tier generoso
     - **Bugsnag** — alternativa similar ao Sentry
     - **Plataforma nativa:** Vercel Analytics, Railway Logs (se suficiente para MVP)
     - **Self-hosted:** GlitchTip (open-source, compativel com SDK do Sentry)
   - Configurar **integracao** com a stack:
     - SDK no backend (captura automatica de exceptions nao tratadas)
     - SDK no frontend (captura erros de JavaScript, React Error Boundary)
     - Integracao com CI/CD (upload de source maps para stack traces legiveis)
   - Definir **contexto** a ser enviado com cada erro:
     - Environment (production/staging)
     - Release/version (tag de deploy)
     - User ID (anonimizado se necessario)
     - Request ID / Trace ID (para correlacionar com logs)
     - Breadcrumbs (ultimas acoes antes do erro)
   - Definir **alertas**:
     - Novo erro em producao → notificacao imediata (Slack, email)
     - Erro recorrente (> N ocorrencias em X minutos) → alerta de urgencia
     - Error rate acima do threshold definido na deploy strategy → trigger de rollback

4. **Definir health checks: endpoints e frequencia:**
   - Definir **endpoint de health check** principal:
     - Rota: `GET /health` ou `GET /healthz` (convenção)
     - Resposta success: `200 OK` com body `{ "status": "ok", "timestamp": "..." }`
     - Resposta failure: `503 Service Unavailable` com detalhes do componente falho
   - Definir **health check detalhado** (readiness):
     - Rota: `GET /health/ready` ou `GET /readyz`
     - Verifica dependencias criticas: banco de dados, cache, filas, APIs externas
     - Resposta inclui status individual de cada dependencia:
       ```json
       {
         "status": "ok",
         "checks": {
           "database": { "status": "ok", "latency_ms": 12 },
           "cache": { "status": "ok", "latency_ms": 3 },
           "external_api": { "status": "degraded", "latency_ms": 850 }
         }
       }
       ```
   - Definir **frequencia** de verificacao:
     - Plataforma de hosting: a cada 10-30 segundos (conforme configuracao da plataforma)
     - Monitoramento externo: a cada 1-5 minutos (UptimeRobot, Better Uptime, Checkly)
   - Integrar com **rollback automatico** (se definido na deploy strategy):
     - Health check falhou N vezes consecutivas → acionar rollback
   - Para **frontends SPA/SSG**: health check pode ser verificacao de HTTP 200 na rota principal

5. **Definir metricas basicas de uso:**
   - Definir **metricas de infraestrutura** (geralmente fornecidas pela plataforma):
     - CPU usage (% por servico)
     - Memory usage (% por servico)
     - Disk usage (se aplicavel)
     - Network I/O
   - Definir **metricas de aplicacao** (instrumentadas no codigo):
     - Request count (total de requests por endpoint)
     - Response time / latency (p50, p95, p99 por endpoint)
     - Error rate (% de respostas 4xx e 5xx)
     - Active users (DAU/MAU — se relevante para o produto)
   - Definir **metricas de negocio** (especificas do dominio — mapear a partir do PRD/KPIs):
     - Exemplos: conversao, cadastros, transacoes processadas, tempo de sessao
     - Instrumentar via eventos (analytics) ou contadores no banco
   - Escolher **ferramenta de metricas** adequada:
     - **PaaS nativo:** Vercel Analytics, Railway Metrics, Fly.io Metrics
     - **Third-party:** Datadog, New Relic, Grafana Cloud (free tier)
     - **Self-hosted:** Prometheus + Grafana (se escala justificar)
     - **Analytics de produto:** PostHog (open-source), Mixpanel, Amplitude
   - Definir **dashboards** minimos:
     - Overview: health status + request count + error rate + latency p95
     - Per-service: metricas individuais por componente
   - **MVP:** Priorizar metricas de infraestrutura (automaticas) + error rate + latency. Metricas de negocio podem ser adicionadas incrementalmente.

6. **Gerar artefato e atualizar `.status`:**
   - Preencher template `observability.tmpl.md` com todas as decisoes
   - Salvar em `07-deploy/observability-setup.md`
   - Atualizar `.status`:
     ```yaml
     deploy:
       artifacts:
         observability-setup:
           status: "draft"
           file: "07-deploy/observability-setup.md"
     ```

## Artefato Gerado

- `07-deploy/observability-setup.md` (a partir do template `templates/observability.tmpl.md`)

## Validacao

Antes de marcar como `draft`, verificar:

- [ ] Logging usa formato JSON estruturado com campos obrigatorios (timestamp, level, message, service, requestId)
- [ ] Niveis de log definidos com criterio claro de uso (error, warn, info, debug)
- [ ] Nivel default por ambiente definido (production: info, staging: debug)
- [ ] Biblioteca de logging escolhida e compativel com a stack da arquitetura
- [ ] Retencao de logs definida por ambiente (producao >= 30 dias)
- [ ] Regra explicita contra logging de dados sensiveis (senhas, tokens, PII)
- [ ] Ferramenta de error tracking definida com configuracao de SDK, contexto e alertas
- [ ] Health check endpoint principal (`/health`) definido com formato de resposta
- [ ] Health check detalhado (`/health/ready`) verifica dependencias criticas (banco, cache, APIs)
- [ ] Frequencia de health check definida (plataforma + monitoramento externo)
- [ ] Metricas basicas definidas: request count, latency (p95), error rate
- [ ] Ferramenta de metricas/dashboard escolhida e adequada a plataforma de hosting
