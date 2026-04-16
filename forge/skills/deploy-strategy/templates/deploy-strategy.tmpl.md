# Deploy Strategy

> **Fase:** Deploy
> **Skill:** deploy-strategy
> **Status:** draft
> **Data:** <YYYY-MM-DD>
> **Stack:** <STACK_DO_PROJETO>

---

## Como Usar

Este documento define como o software vai para producao. Deve ser consultado por todo desenvolvedor antes de configurar pipelines ou fazer o primeiro deploy. Atualize este documento sempre que a infraestrutura mudar.

---

## 1. Plataforma de Hosting

### Plataforma Escolhida

| Aspecto | Detalhe |
|---------|---------|
| **Plataforma** | <NOME_DA_PLATAFORMA> |
| **Tipo** | <PaaS / Container / Kubernetes / IaaS> |
| **Regiao** | <REGIAO_PRIMARIA> |
| **URL do dashboard** | <URL_DO_DASHBOARD> |

### Justificativa

<!-- Documentar os criterios que levaram a escolha. Referenciar ADR se existir. -->

| Criterio | Avaliacao |
|----------|-----------|
| Complexidade operacional | <BAIXA / MEDIA / ALTA> |
| Custo estimado (MVP) | <CUSTO_MENSAL_ESTIMADO> |
| Suporte nativo a stack | <SIM / PARCIAL / NAO> |
| Escalabilidade horizontal | <AUTOMATICA / MANUAL / N/A> |
| Regiao adequada aos usuarios | <SIM / NAO — justificar> |

<!-- Se a decisao foi tomada em ADR, referenciar:
> Decisao documentada em [ADR-NNN](../03-architecture/adrs/adr-NNN-<titulo>.md).
-->

### Alternativas Consideradas

<!-- Listar 1-2 alternativas que foram avaliadas e descartadas. -->

| Alternativa | Motivo da rejeicao |
|-------------|-------------------|
| <ALTERNATIVA_1> | <MOTIVO_1> |
| <ALTERNATIVA_2> | <MOTIVO_2> |

---

## 2. Pipeline CI/CD

### Ferramenta

| Aspecto | Detalhe |
|---------|---------|
| **Ferramenta** | <GITHUB_ACTIONS / GITLAB_CI / OUTRO> |
| **Arquivo de config** | <CAMINHO_DO_ARQUIVO> (ex: `.github/workflows/deploy.yml`) |

### Stages

```
lint → test → build → deploy-staging → deploy-production
```

| Stage | Descricao | Condicao de execucao |
|-------|-----------|---------------------|
| `lint` | <DESCRICAO_LINT> | Sempre |
| `test` | <DESCRICAO_TEST> | Sempre |
| `build` | <DESCRICAO_BUILD> | Apos lint + test passarem |
| `deploy-staging` | <DESCRICAO_DEPLOY_STAGING> | Push para `main` |
| `deploy-production` | <DESCRICAO_DEPLOY_PROD> | Tag `v*` ou aprovacao manual |

### Triggers

| Evento | Acao |
|--------|------|
| Push para `main` | lint → test → build → deploy-staging |
| Tag `v*` / merge para `release` | lint → test → build → deploy-production |
| Pull request | lint → test (sem deploy) |

### Gates

<!-- Definir o que bloqueia o avanco entre stages. -->

- [ ] Testes devem passar com cobertura >= <COBERTURA_MINIMA>%
- [ ] Build deve completar sem erros
- [ ] <GATE_ADICIONAL_1>
- [ ] Aprovacao manual para deploy-production: <SIM / NAO>

---

## 3. Environments

| Environment | Proposito | URL | Branch/Trigger |
|-------------|-----------|-----|----------------|
| **Development** | Desenvolvimento local | `localhost:<PORTA>` | -- |
| **Staging** | Validacao pre-producao | <URL_STAGING> | Push `main` |
| **Production** | Usuarios finais | <URL_PRODUCAO> | Tag `v*` |

<!-- Adicionar environments extras se necessario (ex: preview per-PR). -->

---

## 4. Variaveis de Ambiente

### Aplicacao

| Nome | Descricao | Obrigatoria | Default | Sensivel |
|------|-----------|-------------|---------|----------|
| `PORT` | Porta do servidor | Sim | `3000` | Nao |
| `NODE_ENV` / `APP_ENV` | Ambiente de execucao | Sim | `development` | Nao |
| `LOG_LEVEL` | Nivel de log | Nao | `info` | Nao |
| <VAR_APP_1> | <DESCRICAO> | <SIM/NAO> | <DEFAULT> | <SIM/NAO> |

### Banco de Dados

| Nome | Descricao | Obrigatoria | Default | Sensivel |
|------|-----------|-------------|---------|----------|
| `DATABASE_URL` | Connection string completa | Sim | -- | Sim |
| <VAR_DB_1> | <DESCRICAO> | <SIM/NAO> | <DEFAULT> | <SIM/NAO> |

<!-- Se usar connection string unica (DATABASE_URL), nao precisa listar DB_HOST, DB_PORT, etc. separadamente. -->

### Autenticacao

| Nome | Descricao | Obrigatoria | Default | Sensivel |
|------|-----------|-------------|---------|----------|
| <VAR_AUTH_1> | <DESCRICAO> | <SIM/NAO> | -- | Sim |
| <VAR_AUTH_2> | <DESCRICAO> | <SIM/NAO> | -- | Sim |

### APIs Externas

| Nome | Descricao | Obrigatoria | Default | Sensivel |
|------|-----------|-------------|---------|----------|
| <VAR_API_1> | <DESCRICAO> | <SIM/NAO> | -- | Sim |

### Infraestrutura

| Nome | Descricao | Obrigatoria | Default | Sensivel |
|------|-----------|-------------|---------|----------|
| <VAR_INFRA_1> | <DESCRICAO> | <SIM/NAO> | <DEFAULT> | <SIM/NAO> |

<!-- Remover categorias que nao se aplicam ao projeto. -->

### Gestao de Secrets

| Ambiente | Metodo | Ferramenta |
|----------|--------|------------|
| Development | `.env` local (nao commitado) + `.env.example` commitado | dotenv |
| Staging | Secrets do CI/CD | <FERRAMENTA_CI_SECRETS> |
| Production | <METODO_PROD> | <FERRAMENTA_PROD_SECRETS> |

---

## 5. Estrategia de Rollback

### Metodo

| Aspecto | Detalhe |
|---------|---------|
| **Metodo principal** | <REDEPLOY_ANTERIOR / BLUE_GREEN / CANARY / FEATURE_FLAGS> |
| **SLA de rollback** | < <TEMPO_MAXIMO> minutos |
| **Quem aciona** | <AUTOMATICO_VIA_HEALTH_CHECK / MANUAL_VIA_DASHBOARD / AMBOS> |

### Triggers para Rollback

<!-- Definir as condicoes que justificam um rollback. -->

- [ ] Health check falha apos deploy (endpoint `/health` retorna != 200)
- [ ] Error rate acima de <THRESHOLD_ERROR_RATE>% por <JANELA_TEMPO> minutos
- [ ] Tempo de resposta medio acima de <THRESHOLD_LATENCIA>ms
- [ ] <TRIGGER_ADICIONAL>

### Procedimento

<!-- Passos para executar o rollback. Deve ser simples e executavel sob pressao. -->

1. <PASSO_1> (ex: Acessar dashboard da plataforma)
2. <PASSO_2> (ex: Selecionar deploy anterior)
3. <PASSO_3> (ex: Confirmar redeploy)
4. <PASSO_4> (ex: Verificar health check da versao revertida)

---

## 6. Dominio e DNS

<!-- Se o projeto nao tem dominio proprio, substituir esta secao por:
> **N/A** — Projeto utiliza dominio fornecido pela plataforma: `<URL_DA_PLATAFORMA>`.
> Dominio proprio sera configurado em fase futura se necessario.
-->

### Dominios

| Ambiente | Dominio | Tipo |
|----------|---------|------|
| Production | <DOMINIO_PROD> | <A / CNAME / ALIAS> |
| Staging | <DOMINIO_STAGING> | <A / CNAME / ALIAS> |
| API | <DOMINIO_API> | <A / CNAME / ALIAS> |

### Provedor de DNS

| Aspecto | Detalhe |
|---------|---------|
| **Provedor** | <CLOUDFLARE / ROUTE53 / GOOGLE_DOMAINS / OUTRO> |
| **Proxy/CDN** | <SIM — Cloudflare / NAO> |

### SSL/TLS

| Aspecto | Detalhe |
|---------|---------|
| **Metodo** | <LETS_ENCRYPT_AUTO / GERENCIADO_PELA_PLATAFORMA / CERTIFICADO_PROPRIO> |
| **Renovacao** | <AUTOMATICA / MANUAL — periodicidade> |

---

## Notas

<!-- Observacoes gerais, excecoes justificadas, ou decisoes sobre criterios N/A. -->

- <NOTA_1>

---

## Referencias

- [architecture-overview.md](../03-architecture/architecture-overview.md) — decisoes de stack e infraestrutura
- [code-standards.md](../05-implementation/code-standards.md) — padroes de lint/format usados nos stages de CI
- [test-strategy.md](../06-quality/test-strategy.md) — estrategia de testes executada no pipeline

<!-- Adicionar ADRs relevantes:
- [ADR-NNN](../03-architecture/adrs/adr-NNN-<titulo>.md) — <descricao>
-->

---

## Status

- **Criado em:** <YYYY-MM-DD>
- **Ultima atualizacao:** <YYYY-MM-DD>
- **Status:** draft
- **Aprovado por:** --
- **Data de aprovacao:** --
