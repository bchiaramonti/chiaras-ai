---
name: deploy-strategy
description: >-
  Defines how the software goes to production: hosting platform, CI/CD pipeline,
  environment variables, rollback strategy, and domain/DNS configuration.
  Use after architecture is approved, before observability setup.
  Produces 07-deploy/deploy-strategy.md.
user-invocable: false
---

# Deploy Strategy

Define a estrategia completa de deploy do projeto: plataforma de hosting, pipeline CI/CD, variaveis de ambiente, rollback, e configuracao de dominio/DNS. Garante que a transicao de codigo para producao seja previsivel, repetivel e segura.

## Pre-requisitos

| Artefato | Status minimo |
|----------|---------------|
| `03-architecture/architecture-overview.md` | `approved` |

> **Nota:** A estrategia de deploy depende das decisoes arquiteturais (stack, componentes, infraestrutura). Se ADRs relevantes existirem (ex: ADR sobre hospedagem ou containerizacao), devem ser consultados como complemento.

## Processo

1. **Ler arquitetura para entender infraestrutura necessaria:**
   - Extrair de `architecture-overview.md`:
     - Stack tecnologica (linguagem, runtime, framework)
     - Componentes do sistema (frontend, backend, banco de dados, filas, cache)
     - Dependencias externas (APIs de terceiros, servicos cloud)
     - Diagrama de containers (C4 Level 2) para mapear o que precisa ser deployado
   - Extrair de `03-architecture/adrs/*.md` (se existirem):
     - Decisoes sobre containerizacao, cloud provider, ou infraestrutura
   - Listar todos os **artefatos deployaveis** (ex: app web, API, worker, banco, CDN)

2. **Recomendar plataforma de hosting com justificativa:**
   - Avaliar opcoes adequadas a stack e complexidade:
     - **PaaS simplificado:** Vercel, Netlify, Railway, Render, Fly.io
     - **PaaS com mais controle:** Heroku, DigitalOcean App Platform
     - **Container-based:** AWS ECS/Fargate, Google Cloud Run, Azure Container Apps
     - **Kubernetes:** AWS EKS, GKE, AKS (somente se justificado pela escala)
     - **VPS/IaaS:** EC2, Droplets, Linode (somente se necessario)
   - Criterios de decisao (documentar no artefato):
     - Complexidade operacional vs. tamanho da equipe
     - Custo estimado para carga inicial (MVP)
     - Suporte nativo a stack escolhida
     - Escalabilidade horizontal quando necessario
     - Regiao geografica (latencia para usuarios-alvo)
   - Se a decisao ja foi tomada em um ADR, referenciar o ADR e nao repetir a analise

3. **Definir pipeline CI/CD (build → test → deploy):**
   - Escolher ferramenta de CI/CD adequada:
     - **GitHub Actions** (default para repos GitHub)
     - **GitLab CI** (para repos GitLab)
     - **Outros:** CircleCI, Bitbucket Pipelines, Jenkins (somente se justificado)
   - Definir os **stages** do pipeline:
     - `lint` — linting e formatacao (conforme code-standards)
     - `test` — testes unitarios + integracao (conforme test-strategy)
     - `build` — compilacao/bundling do artefato deployavel
     - `deploy-staging` — deploy em ambiente de staging
     - `deploy-production` — deploy em producao (manual ou automatico)
   - Definir **triggers**:
     - Push para `main` → deploy staging automatico
     - Tag `v*` ou merge para `release` → deploy producao
     - Pull request → apenas lint + test (sem deploy)
   - Definir **gates** entre stages:
     - Testes devem passar antes de build
     - Build deve passar antes de deploy
     - Aprovacao manual para producao (recomendado para MVP)

4. **Listar variaveis de ambiente necessarias:**
   - Categorizar por tipo:
     - **Aplicacao:** PORT, NODE_ENV/APP_ENV, LOG_LEVEL
     - **Banco de dados:** DATABASE_URL, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
     - **Autenticacao:** JWT_SECRET, SESSION_SECRET, OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET
     - **APIs externas:** chaves de API de terceiros
     - **Infra:** REDIS_URL, QUEUE_URL, SMTP_HOST, SMTP_PORT
   - Para cada variavel, documentar em tabela:
     - Nome
     - Descricao
     - Obrigatoria? (sim/nao)
     - Valor default (se houver)
     - Sensivel? (sim/nao)
   - **REGRA CRITICA:** Nunca incluir valores reais de variaveis sensiveis no artefato
   - Recomendar ferramenta de gestao de secrets:
     - `.env` local + `.env.example` commitado (dev)
     - Secrets do CI/CD provider (staging/prod)
     - Vault, AWS Secrets Manager, ou equivalente (se escala justificar)

5. **Definir estrategia de rollback:**
   - Definir **como reverter** um deploy com problema:
     - **Redeploy da versao anterior:** re-executar pipeline com commit/tag anterior
     - **Feature flags:** desativar funcionalidade sem redeploy (se aplicavel)
     - **Blue/green ou canary:** manter versao anterior ativa em paralelo (se infra permitir)
   - Definir **quando acionar** rollback:
     - Health check falhou apos deploy
     - Error rate acima do threshold (definir threshold)
     - Metricas de performance degradadas
   - Definir **quem pode** acionar rollback:
     - Automatico via health check (recomendado)
     - Manual via dashboard do CI/CD ou plataforma
   - Definir **tempo maximo** para rollback (SLA):
     - MVP: < 5 minutos (manual)
     - Producao madura: < 1 minuto (automatico)

6. **Planejar dominio e DNS (se aplicavel):**
   - Definir dominio(s) do projeto:
     - Producao: `app.dominio.com` ou `dominio.com`
     - Staging: `staging.dominio.com` ou `app-staging.dominio.com`
     - API (se separada): `api.dominio.com`
   - Configuracao de DNS:
     - Registrar provedor (Cloudflare, Route53, Google Domains, etc.)
     - Tipo de registro (A, CNAME, ALIAS) conforme plataforma de hosting
   - SSL/TLS:
     - Certificado automatico via Let's Encrypt (default na maioria das plataformas)
     - Ou certificado gerenciado pela plataforma (Vercel, Netlify, Cloudflare)
   - Se o projeto nao tem dominio proprio, documentar como "N/A — usando dominio da plataforma"

7. **Gerar artefato e atualizar `.status`:**
   - Preencher template `deploy-strategy.tmpl.md` com todas as decisoes
   - Salvar em `07-deploy/deploy-strategy.md`
   - Atualizar `.status`:
     ```yaml
     deploy:
       artifacts:
         deploy-strategy:
           status: "draft"
           file: "07-deploy/deploy-strategy.md"
     ```

## Artefato Gerado

- `07-deploy/deploy-strategy.md` (a partir do template `templates/deploy-strategy.tmpl.md`)

## Validacao

Antes de marcar como `draft`, verificar:

- [ ] Plataforma de hosting definida com justificativa baseada nos criterios (custo, complexidade, stack)
- [ ] Pipeline CI/CD completo com todos os stages: lint, test, build, deploy-staging, deploy-production
- [ ] Triggers de CI/CD definidos (push, tag, PR) com comportamento esperado para cada um
- [ ] Gates entre stages documentados (o que bloqueia o avanço)
- [ ] Variaveis de ambiente listadas em tabela com nome, descricao, obrigatoriedade e sensibilidade
- [ ] Nenhum valor real de variavel sensivel presente no artefato
- [ ] Ferramenta de gestao de secrets recomendada para cada ambiente (dev, staging, prod)
- [ ] Estrategia de rollback definida com trigger (quando), metodo (como) e SLA (tempo maximo)
- [ ] Dominio/DNS planejado ou explicitamente marcado como N/A com justificativa
- [ ] SSL/TLS definido (certificado automatico ou gerenciado)
- [ ] Artefato referencia `architecture-overview.md` e ADRs relevantes
- [ ] Estrategia e viavel para o tamanho da equipe e fase do projeto (nao over-engineer)
