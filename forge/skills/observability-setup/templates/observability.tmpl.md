# Observability Setup

> **Fase:** Deploy
> **Skill:** observability-setup
> **Status:** draft
> **Data:** <YYYY-MM-DD>
> **Stack:** <STACK_DO_PROJETO>

---

## Como Usar

Este documento define como monitorar, diagnosticar e medir a saude do sistema em producao. Deve ser consultado durante a configuracao inicial de deploy e revisado sempre que novos componentes forem adicionados. Desenvolvedores devem seguir as convencoes de logging e instrumentacao aqui definidas.

---

## 1. Logging Estruturado

### Formato

| Aspecto | Detalhe |
|---------|---------|
| **Formato** | JSON estruturado |
| **Biblioteca** | <BIBLIOTECA_DE_LOGGING> |
| **Encoding** | UTF-8 |

### Campos Obrigatorios

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `timestamp` | ISO 8601 | Momento do evento |
| `level` | string | Nivel do log (error, warn, info, debug) |
| `message` | string | Descricao legivel do evento |
| `service` | string | Nome do servico/componente emissor |
| `requestId` | string | ID unico da request (para correlacao) |

### Campos Opcionais

| Campo | Tipo | Descricao | Quando usar |
|-------|------|-----------|-------------|
| `userId` | string | ID do usuario (anonimizado se PII) | Acoes autenticadas |
| `action` | string | Acao sendo executada | Eventos de negocio |
| `duration` | number | Duracao em ms | Operacoes com latencia |
| `error` | object | Detalhes do erro (message + stack) | Niveis error/warn |
| <CAMPO_ADICIONAL_1> | <TIPO> | <DESCRICAO> | <CONTEXTO> |

### Niveis de Log

| Nivel | Quando Usar | Exemplo |
|-------|-------------|---------|
| `error` | Falha que impede a operacao | Exception nao tratada, banco indisponivel, API de pagamento falhou |
| `warn` | Situacao anormal mas recuperavel | Retry em API externa, fallback ativado, funcao deprecada chamada |
| `info` | Evento significativo de negocio | Usuario criado, pedido processado, deploy realizado |
| `debug` | Detalhe tecnico para diagnostico | Query SQL executada, payload recebido, estado interno |

### Nivel Default por Ambiente

| Ambiente | Nivel | Justificativa |
|----------|-------|---------------|
| Production | `info` | Performance e volume; nunca `debug` por default |
| Staging | `debug` | Diagnostico completo em pre-producao |
| Development | `debug` | Maximo detalhe para desenvolvimento |

### Retencao

| Ambiente | Retencao | Destino |
|----------|----------|---------|
| Production | <RETENCAO_PROD> dias | <DESTINO_PROD> |
| Staging | <RETENCAO_STAGING> dias | <DESTINO_STAGING> |
| Development | Sem retencao | stdout |

### Sanitizacao

<!-- REGRA CRITICA: Nunca logar dados sensiveis. -->

Dados que **nunca** devem aparecer em logs:

- Senhas e hashes de senha
- Tokens de autenticacao (JWT, API keys, session tokens)
- Dados pessoais identificaveis (PII): CPF, email, telefone, endereco
- Numeros de cartao de credito
- Conteudo de requests/responses com dados sensiveis

> **Implementacao:** Utilizar middleware de sanitizacao ou allowlist de campos logaveis.

---

## 2. Error Tracking

### Ferramenta

| Aspecto | Detalhe |
|---------|---------|
| **Ferramenta** | <FERRAMENTA_ERROR_TRACKING> |
| **Plano/Tier** | <FREE / PAID — detalhe> |
| **Dashboard** | <URL_DASHBOARD_ERRORS> |

### Integracao com a Stack

| Componente | SDK / Metodo | Configuracao |
|------------|-------------|--------------|
| Backend | <SDK_BACKEND> | Captura automatica de exceptions + middleware |
| Frontend | <SDK_FRONTEND> | Error Boundary + captura global |
| CI/CD | <INTEGRACAO_CI> | Upload de source maps no build |

<!-- Se nao houver frontend, remover a linha correspondente. -->

### Contexto Enviado com Cada Erro

| Campo | Valor | Obrigatorio |
|-------|-------|-------------|
| Environment | production / staging | Sim |
| Release | Tag de deploy (ex: `v1.2.3`) | Sim |
| User ID | <ANONIMIZADO_SE_NECESSARIO> | Sim |
| Request ID | Mesmo `requestId` dos logs | Sim |
| Breadcrumbs | Ultimas N acoes antes do erro | Recomendado |

### Alertas

| Condicao | Canal | Urgencia |
|----------|-------|----------|
| Novo erro em producao | <CANAL_NOTIFICACAO> (ex: Slack #alerts) | Imediata |
| Erro recorrente (> <N> ocorrencias em <X> min) | <CANAL_NOTIFICACAO> | Alta |
| Error rate > <THRESHOLD_ERROR_RATE>% | <CANAL_NOTIFICACAO> + trigger de rollback | Critica |

---

## 3. Health Checks

### Health Check Principal (Liveness)

| Aspecto | Detalhe |
|---------|---------|
| **Rota** | `GET /health` |
| **Resposta OK** | `200 OK` — `{ "status": "ok", "timestamp": "..." }` |
| **Resposta Falha** | `503 Service Unavailable` — `{ "status": "error", "message": "..." }` |
| **Autenticacao** | Nenhuma (endpoint publico) |

### Health Check Detalhado (Readiness)

| Aspecto | Detalhe |
|---------|---------|
| **Rota** | `GET /health/ready` |
| **Autenticacao** | <NENHUMA / API_KEY / REDE_INTERNA> |

**Dependencias verificadas:**

| Dependencia | Tipo de Check | Timeout | Critica? |
|-------------|--------------|---------|----------|
| <BANCO_DE_DADOS> | Connection ping | <TIMEOUT>ms | Sim |
| <CACHE> | Connection ping | <TIMEOUT>ms | <SIM/NAO> |
| <FILA> | Connection ping | <TIMEOUT>ms | <SIM/NAO> |
| <API_EXTERNA> | HTTP GET | <TIMEOUT>ms | <SIM/NAO> |

<!-- Remover linhas de dependencias que nao existem no projeto. -->

**Formato de resposta:**

```json
{
  "status": "ok",
  "timestamp": "<ISO_8601>",
  "checks": {
    "<DEPENDENCIA_1>": { "status": "ok", "latency_ms": 0 },
    "<DEPENDENCIA_2>": { "status": "ok", "latency_ms": 0 }
  }
}
```

### Frequencia de Verificacao

| Origem | Frequencia | Acao em falha |
|--------|-----------|---------------|
| Plataforma de hosting | A cada <INTERVALO_PLATAFORMA> segundos | Restart automatico do container/processo |
| Monitoramento externo | A cada <INTERVALO_EXTERNO> minutos | Alerta via <CANAL_NOTIFICACAO> |
| CI/CD (post-deploy) | Uma vez apos cada deploy | Rollback se falha |

### Ferramenta de Monitoramento Externo

| Aspecto | Detalhe |
|---------|---------|
| **Ferramenta** | <UPTIMEROBOT / BETTER_UPTIME / CHECKLY / OUTRO> |
| **URL monitorada** | <URL_HEALTH_CHECK_PRODUCAO> |
| **Alerta** | <CANAL_NOTIFICACAO> |

<!-- Se nao houver monitoramento externo no MVP, documentar:
> **MVP:** Monitoramento externo sera configurado apos o primeiro deploy estavel.
-->

---

## 4. Metricas

### Metricas de Infraestrutura

<!-- Geralmente fornecidas automaticamente pela plataforma de hosting. -->

| Metrica | Fonte | Threshold de alerta |
|---------|-------|---------------------|
| CPU usage | <FONTE_PLATAFORMA> | > <THRESHOLD_CPU>% por <JANELA> min |
| Memory usage | <FONTE_PLATAFORMA> | > <THRESHOLD_MEMORY>% por <JANELA> min |
| Disk usage | <FONTE_PLATAFORMA> | > <THRESHOLD_DISK>% |
| Network I/O | <FONTE_PLATAFORMA> | N/A (monitoramento passivo) |

<!-- Remover metricas nao aplicaveis (ex: disk em PaaS serverless). -->

### Metricas de Aplicacao

| Metrica | Como medir | Threshold / Target |
|---------|-----------|-------------------|
| Request count | <INSTRUMENTACAO> | Monitoramento (sem threshold) |
| Response time (p50) | <INSTRUMENTACAO> | < <TARGET_P50>ms |
| Response time (p95) | <INSTRUMENTACAO> | < <TARGET_P95>ms |
| Response time (p99) | <INSTRUMENTACAO> | < <TARGET_P99>ms |
| Error rate (4xx + 5xx) | <INSTRUMENTACAO> | < <THRESHOLD_ERROR_RATE>% |

### Metricas de Negocio

<!-- Mapear a partir dos KPIs definidos no PRD. Instrumentar incrementalmente. -->

| Metrica | Descricao | Como medir | Prioridade MVP |
|---------|-----------|-----------|----------------|
| <METRICA_NEGOCIO_1> | <DESCRICAO> | <INSTRUMENTACAO> | <SIM / POS-MVP> |
| <METRICA_NEGOCIO_2> | <DESCRICAO> | <INSTRUMENTACAO> | <SIM / POS-MVP> |

### Ferramenta de Metricas e Dashboard

| Aspecto | Detalhe |
|---------|---------|
| **Ferramenta** | <FERRAMENTA_METRICAS> |
| **Dashboard URL** | <URL_DASHBOARD> |
| **Acesso** | <QUEM_TEM_ACESSO> |

### Dashboards Minimos

| Dashboard | Conteudo | Prioridade |
|-----------|----------|------------|
| Overview | Health status + request count + error rate + latency p95 | MVP |
| Per-service | Metricas individuais por componente | MVP |
| Business | Metricas de negocio / KPIs | Pos-MVP |

---

## Notas

<!-- Observacoes gerais, excecoes justificadas, ou decisoes sobre criterios N/A. -->

- <NOTA_1>

---

## Referencias

- [architecture-overview.md](../03-architecture/architecture-overview.md) — stack, componentes e pontos de falha
- [deploy-strategy.md](../07-deploy/deploy-strategy.md) — plataforma, environments e triggers de rollback

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
