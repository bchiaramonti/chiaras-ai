# Bank Statement Formats — Superavit

Especificações de layout por banco para parsing de extratos.

## Índice

- [Nubank CSV](#nubank-csv)
- [Nubank PDF](#nubank-pdf)
- [Itaú CSV](#itaú-csv)
- [Itaú OFX](#itaú-ofx)
- [Bradesco OFX](#bradesco-ofx)
- [Inter CSV](#inter-csv)
- [Notas Gerais](#notas-gerais)

---

## Nubank CSV

| Propriedade | Valor |
|-------------|-------|
| Encoding | UTF-8 BOM (`utf-8-sig`) |
| Separador | Vírgula (`,`) |
| Headers | `date,category,title,amount` |
| Formato de data | `YYYY-MM-DD` |
| Formato de valor | Ponto decimal, sem separador de milhar |
| Sinal de valor | Positivo = despesa (débito), Negativo = receita (crédito) |

**Exemplo:**
```csv
date,category,title,amount
2026-01-15,restaurante,IFOOD *RESTAURANTE XYZ,45.90
2026-01-16,transporte,Uber *TRIP,23.50
2026-01-20,pagamento,Pagamento recebido,-5000.00
```

**Atenção:** No Nubank, valor positivo é despesa. O parser inverte o sinal (`amount = -abs(raw)` se positivo).

---

## Nubank PDF

| Propriedade | Valor |
|-------------|-------|
| Formato | PDF com tabelas extraíveis |
| Keywords de detecção | `nubank`, `nu pagamentos` |
| Formato de data | `DD/MM/YYYY` ou `DD/MM` |
| Formato de valor | Brasileiro: `1.234,56` com `R$` |

**Notas:**
- Faturas de cartão de crédito vêm em PDF
- Tabelas extraídas via `pdfplumber`
- Layout pode variar entre meses — parsing é heurístico
- Recomendado: confirmar valores com o usuário para PDFs

---

## Itaú CSV

| Propriedade | Valor |
|-------------|-------|
| Encoding | Latin-1 (`latin-1` / `iso-8859-1`) |
| Separador | Ponto-e-vírgula (`;`) |
| Headers | `data;lançamento;valor` (pode variar: `data;histórico;valor`) |
| Formato de data | `DD/MM/YYYY` |
| Formato de valor | Vírgula decimal, sem separador de milhar |
| Sinal de valor | Negativo = despesa, Positivo = receita |

**Exemplo:**
```csv
data;lançamento;valor
15/01/2026;SAQUE 24H 012345;-200,00
16/01/2026;TED RECEBIDA 098765;3500,00
20/01/2026;PAG BOLETO ELETRON;-450,50
```

**Atenção:**
- Encoding Latin-1 é obrigatório — UTF-8 falha com caracteres acentuados
- Vírgula como separador decimal: `pandas.read_csv(..., decimal=",")`

---

## Itaú OFX

| Propriedade | Valor |
|-------------|-------|
| Formato | OFX 1.x (SGML, não XML) |
| BANKID | `0341` |
| Encoding | ASCII/Latin-1 |
| Campo de data | `DTPOSTED` (formato `YYYYMMDD`) |
| Campo de valor | `TRNAMT` (ponto decimal) |
| Campo de descrição | `MEMO` ou `NAME` |

**Exemplo OFX (SGML):**
```
OFXHEADER:100
DATA:OFXSGML
...
<STMTTRN>
<TRNTYPE>DEBIT
<DTPOSTED>20260115
<TRNAMT>-200.00
<MEMO>SAQUE 24H 012345
</STMTTRN>
```

**Parser:** `ofxtools.Parser.OFXTree` lida com SGML e XML automaticamente.

---

## Bradesco OFX

| Propriedade | Valor |
|-------------|-------|
| Formato | OFX 1.x (SGML) |
| BANKID | `0237` |
| Encoding | ASCII/Latin-1 |
| Campos | Mesmo padrão OFX: `DTPOSTED`, `TRNAMT`, `MEMO` |

**Notas:**
- Mesma lógica de parsing do Itaú OFX (usa `ofxtools`)
- Diferenciado pelo BANKID (`0237` vs `0341`)

---

## Inter CSV

| Propriedade | Valor |
|-------------|-------|
| Encoding | UTF-8 BOM (`utf-8-sig`) |
| Separador | Ponto-e-vírgula (`;`) |
| Headers | `Data Lançamento;Descrição;Valor;Saldo` |
| Formato de data | `DD/MM/YYYY` |
| Formato de valor | Vírgula decimal |
| Sinal de valor | Negativo = despesa, Positivo = receita |

**Exemplo:**
```csv
Data Lançamento;Descrição;Valor;Saldo
15/01/2026;PIX ENVIADO - FULANO;-150,00;3.500,00
16/01/2026;PIX RECEBIDO - EMPRESA;5.000,00;8.500,00
```

**Atenção:**
- Coluna `Saldo` é ignorada (calculado a partir dos dados no Supabase)
- Headers podem ter acentos — buscar por substring (`descri`, `data`, `valor`)

---

## Notas Gerais

### Detecção automática de banco

1. **CSV**: match por headers (exato)
2. **OFX**: match por `BANKID`
3. **PDF**: keywords no texto da primeira página
4. **Fallback**: nome do arquivo (ex: `nubank-2026-01.csv`)

### Conversão de datas

| Formato de entrada | Formato de saída |
|---------------------|------------------|
| `YYYY-MM-DD` | (já no formato correto) |
| `DD/MM/YYYY` | `YYYY-MM-DD` |
| `DD/MM` | `YYYY-MM-DD` (assume ano corrente) |
| `YYYYMMDD` (OFX) | `YYYY-MM-DD` (via `strftime`) |

### Normalização de valores

- Formato brasileiro (`1.234,56`): remover pontos, trocar vírgula por ponto → `1234.56`
- Remover `R$` e espaços
- Manter sinal original (depois ajustar por banco se necessário)
