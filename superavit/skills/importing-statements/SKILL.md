---
name: importing-statements
description: >-
  Importa extratos bancários (CSV, OFX, PDF) com pipeline completo:
  detecção de formato, parsing multi-banco, normalização, categorização
  automática por keywords + Claude fallback, dedup por hash SHA-256.
  Persiste no Supabase via MCP.

  <example>
  Context: Usuário tem extrato na pasta input/
  user: "importar meu extrato do nubank"
  assistant: Detecta arquivo em input/, parseia CSV, categoriza, persiste no Supabase
  </example>
user-invocable: true
allowed-tools: mcp__claude_ai_Supabase__execute_sql, Bash, Read, Write, Glob
---

# Importing Statements — Superavit

Pipeline de ingestão de extratos bancários: detecta formato, parseia, categoriza e persiste no Supabase.

## Pré-requisitos

- Setup concluído — verificar antes de qualquer operação:
  ```sql
  SELECT value FROM config WHERE key = 'setup_completed';
  ```
  Se `completed = false` ou não existe: orientar `/superavit:setting-up`

- **Python 3.11+** com as seguintes dependências:
  - `pandas` — parsing CSV
  - `ofxtools` — parsing OFX
  - `pdfplumber` — parsing PDF

  Instalar se necessário: `pip install pandas ofxtools pdfplumber`

### Bancos e formatos suportados

| Banco | CSV | OFX | PDF |
|-------|-----|-----|-----|
| Nubank | ✅ | — | ✅ |
| Itaú | ✅ | ✅ | — |
| Bradesco | — | ✅ | — |
| Inter | ✅ | — | — |

Para detalhes de encoding, separadores e layouts, ver [bank-formats.md](references/bank-formats.md).

## Pipeline (11 etapas)

### Etapa 1 — Localizar arquivos

Buscar extratos em `~/Documents/brain/2-areas/financas/input/` ou no path fornecido pelo usuário.

```bash
ls ~/Documents/brain/2-areas/financas/input/
```

Se múltiplos arquivos: listar e perguntar qual processar (ou "todos").

### Etapa 2 — Detectar formato e banco

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/parse_statement.py" detect "<filepath>"
```

Retorna JSON:
```json
{"format": "csv", "bank": "nubank", "confidence": "high"}
```

Se `confidence` não for `high`: confirmar com o usuário.

### Etapa 3 — Verificar/criar conta

Consultar contas existentes via MCP:

```sql
SELECT id, name, bank, type FROM accounts WHERE bank = '<banco>' AND is_active = true;
```

Se não existe conta para o banco detectado:
1. Perguntar nome da conta (ex: "Nubank Conta Corrente")
2. Perguntar tipo: `checking`, `savings`, ou `credit_card`
3. Criar:
   ```sql
   INSERT INTO accounts (name, bank, type) VALUES ('<nome>', '<banco>', '<tipo>') RETURNING id;
   ```

Guardar `account_id` para as próximas etapas.

### Etapa 4 — Parsear extrato

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/parse_statement.py" parse "<filepath>" "<banco>"
```

Retorna JSON normalizado:
```json
{
  "transactions": [
    {
      "date": "2026-01-15",
      "description": "IFOOD *RESTAURANTE",
      "original_description": "IFOOD *RESTAURANTE XYZ",
      "amount": -45.90,
      "hash": "sha256..."
    }
  ],
  "total_rows": 42,
  "date_range": {"start": "2026-01-01", "end": "2026-01-31"},
  "source_bank": "nubank",
  "source_format": "csv"
}
```

### Etapa 5 — Classificar tipo (income/expense/transfer)

Para cada transação, aplicar regras:

| Condição | Tipo |
|----------|------|
| `amount > 0` | `income` |
| `amount < 0` | `expense` |
| Description contém keyword de transferência | `transfer` |

**Keywords de transferência interna:**
`transferencia`, `ted enviada`, `ted recebida`, `pix enviado`, `pix recebido`, `transf entre contas`, `aplicacao`, `resgate`

**Keywords de pagamento de cartão:**
`pagto cartao`, `pgto cartao`, `pagamento de fatura`, `fatura cartao`

### Etapa 6 — Categorizar por keywords

Buscar categorias com keywords via MCP:

```sql
SELECT id, name, keywords FROM categories WHERE is_active = true;
```

Executar match determinístico:

```bash
echo '<transactions_json>' | python3 "${CLAUDE_SKILL_DIR}/scripts/categorize.py" - '<categories_json>'
```

Retorna para cada transação:
```json
{"index": 0, "category_id": "uuid", "category_name": "Alimentacao/Delivery", "matched_keyword": "ifood"}
```

Transações com `category_id: null` → fallback Claude (etapa 7).

### Etapa 7 — Categorizar fallback (Claude)

Para transações sem match de keyword, usar raciocínio próprio.

Contexto para decisão:
- Lista de categorias disponíveis (do passo 6)
- Description da transação
- Amount (valor pode indicar tipo — assinaturas costumam ser fixas)

Responder com JSON:
```json
[
  {"index": 3, "category_id": "<uuid>", "category_name": "Lazer", "reason": "Spotify é streaming de música"},
  {"index": 7, "category_id": "<uuid>", "category_name": "Outros", "reason": "Descrição ambígua"}
]
```

### Etapa 8 — Marcar transferências internas

Transações já classificadas como `transfer` na etapa 5:
- Setar `is_internal_transfer = true`
- Setar `type = 'transfer'`

### Etapa 9 — Marcar pagamento de cartão de crédito

Transações com keywords de pagamento CC (etapa 5):
- Setar `is_credit_card_payment = true`

### Etapa 10 — Deduplicar por hash

Para cada transação, verificar se o hash já existe:

```sql
SELECT id FROM transactions WHERE hash = '<hash>' LIMIT 1;
```

> **Otimização**: fazer check em batch com `WHERE hash IN (...)` para até 100 hashes por query.

Transações com hash existente: marcar como `skipped`. Contar para o resumo.

### Etapa 11 — Persistir no Supabase

1. **Criar import_batch**:
   ```sql
   INSERT INTO import_batches (account_id, filename, format, total_rows, imported_rows, duplicates_skipped, date_range_start, date_range_end)
   VALUES ('<account_id>', '<filename>', '<format>', <total>, <imported>, <skipped>, '<start>', '<end>')
   RETURNING id;
   ```

2. **Inserir transactions** em batches de até 100:
   ```sql
   INSERT INTO transactions (account_id, category_id, import_batch_id, date, description, original_description, amount, type, is_internal_transfer, is_credit_card_payment, hash, source_bank, source_format)
   VALUES
       ('<account_id>', '<cat_id>', '<batch_id>', '<date>', '<desc>', '<orig>', <amount>, '<type>', <transfer>, <cc_pay>, '<hash>', '<bank>', '<format>'),
       ...;
   ```

3. **Mover arquivo processado**:
   ```bash
   mkdir -p ~/Documents/brain/2-areas/financas/extratos/$(date -d '<date_range_start>' +%Y-%m 2>/dev/null || date -j -f '%Y-%m-%d' '<date_range_start>' +%Y-%m)
   mv "<filepath>" ~/Documents/brain/2-areas/financas/extratos/<YYYY-MM>/
   ```

## Resumo Final

Após completar o pipeline, apresentar:

| Item | Valor |
|------|-------|
| Arquivo | `<filename>` |
| Banco | `<banco>` |
| Formato | `<format>` |
| Período | `<start>` a `<end>` |
| Total de linhas | `<total_rows>` |
| Importadas | `<imported_rows>` |
| Duplicatas ignoradas | `<duplicates_skipped>` |
| Categorizadas (keyword) | `<N>` |
| Categorizadas (Claude) | `<N>` |
| Sem categoria | `<N>` |
| Transferências internas | `<N>` |
| Pagamentos CC | `<N>` |

**Próximos passos:**
- `"como está meu mês?"` — resumo rápido
- `"relatório de <mês>"` — relatório completo
- Colocar mais extratos em `input/` para importar

## Anti-Patterns

- ❌ Caminhos absolutos (`/Users/...`) — sempre `~/Documents/brain/...` ou `${CLAUDE_SKILL_DIR}`
- ❌ Inserir transação sem hash — sem hash não há dedup
- ❌ Deletar arquivo original antes de confirmar persistência no Supabase
- ❌ Batch de INSERT > 500 transações — usar batches de 100
- ❌ Pular verificação de setup — sempre checar `config.setup_completed` primeiro
- ❌ Assumir banco sem confirmar quando confidence não é high
