---
name: building-roteiros
description: Constrói um roteiro JSON estruturado em segmentos de até 500 caracteres a partir de material textual em PT-BR, pronto para geração de áudio longo via Chatterbox TTS. Use quando o usuário pedir áudio de estudo, aula falada, podcast didático, audiobook, narração de resumo, ou quando precisar segmentar texto para TTS antes da produção do áudio.
---

# Building Roteiros

Transforma material textual (PDF, DOCX, MD, TXT ou resumo colado) em roteiro JSON pronto para a skill `producing-audio`. Garante que cada segmento respeite o limite duro de 500 caracteres do Chatterbox e mantenha calibração natural para TTS em português brasileiro.

## Quando usar esta skill

Acione quando o usuário disser frases como:
- "Quero ouvir esse material enquanto corro"
- "Gera um áudio desse resumo"
- "Transforma essa aula em podcast pra eu escutar no carro"
- "Faz um audiobook didático sobre X"
- "Preciso de uma narração desse capítulo"

## Workflow

### 1. Ingestão do material

| Origem | Como ler |
|---|---|
| Arquivo PDF/DOCX | Use a tool `Read` (Claude Code lê PDFs nativamente) |
| Arquivo MD/TXT | Use a tool `Read` |
| Resumo colado no chat | Use direto da mensagem |
| Múltiplas fontes | Sintetize antes de estruturar |

### 2. Coleta de parâmetros (uma única vez)

Pergunte ao usuário em **uma rodada só**, oferecendo defaults:

1. **Duração alvo em minutos** — sugestões: 30, 60, 90. Default sugerido: 60.
2. **Estilo de narração** — opções:
   - `didático` (aula expositiva, frases declarativas)
   - `podcast` (conversacional, 1 voz, transições casuais)
   - `audiobook` (narrativa, ritmo mais lento)
3. **Voz** — `padrão Chatterbox` ou clone. Se clone, pergunte o nome do arquivo WAV/MP3 já presente em `chatterbox-mcp/voices/`.

### 3. Estruturação em blocos temáticos

Use estas heurísticas:

- **Áudio ≥ 60min**: 3-7 blocos temáticos
- **Áudio < 30min**: 2-3 blocos
- Cada bloco com **título descritivo** (não numérico)
- **Transições explícitas** entre blocos: "Vamos agora ao segundo eixo, sobre..."
- **Recapitulações curtas** a cada 3-4 segmentos do mesmo bloco

### 4. Calibração para TTS (regras duras)

Antes de gerar segmentos, normalize o texto:

| Regra | Aplicação |
|---|---|
| Frases curtas | 15-25 palavras por frase, sem subordinadas longas |
| Siglas | Primeira ocorrência por extenso ("LGPD, Lei Geral de Proteção de Dados") |
| Símbolos | Substituir por palavras: `%` → "por cento", `&` → "e", `/` → "ou", `→` → "leva a" |
| Números importantes | Por extenso quando críticos ("trezentos mil" em vez de "300k") |
| Quebra de segmento | Sempre em **ponto final**, nunca no meio de frase |
| Limite duro | 500 caracteres por segmento (limite do Chatterbox) |
| Pontuação | Vírgula gera micro-pausa; ponto final gera pausa de respiração |

### 5. Geração do JSON

Salve em `~/Documents/brain/3-resources/ai-mcp/chatterbox-mcp/output/roteiro_<slug>.json` (slug em kebab-case do título).

**Por que esse path?** Mantém roteiros + segmentos WAV + MP3 final no mesmo diretório `output/` do MCP server, evitando fragmentação.

Schema:

```json
{
  "title": "<título do material>",
  "estimated_duration_min": 0,
  "voice_reference": null,
  "language_id": "pt",
  "style": "didático|podcast|audiobook",
  "created_at": "<ISO 8601>",
  "segments": [
    {
      "id": "b1s1",
      "block": 1,
      "block_title": "<título do bloco>",
      "text": "<texto do segmento, máximo 500 chars>",
      "pause_after_ms": 500
    }
  ]
}
```

**Convenção de IDs**: `b<bloco>s<segmento>` (ex: `b3s7` = bloco 3, segmento 7).

**Convenção de pausas**:
- `500ms` entre segmentos do mesmo bloco
- `1000ms` na transição entre blocos (último segmento do bloco anterior)

### 6. Validação antes de salvar

Antes de gravar o arquivo, verifique:

- [ ] Todo segmento tem `len(text) <= 500`
- [ ] Toda quebra de segmento ocorre em ponto final
- [ ] Cada bloco tem ≥ 2 segmentos
- [ ] `block_title` único por bloco
- [ ] `language_id` = `"pt"` (PT-BR)

Se algum check falhar, corrija antes de gravar.

### 7. Reporte ao usuário

Apresente em formato compacto:

```
Roteiro pronto:
- Título: <título>
- Blocos: <N>
- Segmentos: <M>
- Duração estimada: ~<X> min (premissa: 150 palavras/min em PT-BR)
- Caminho: <caminho absoluto do JSON>

Próximo passo: invocar a skill `producing-audio` para gerar o MP3.
```

Pergunte: **"Posso prosseguir com a skill `producing-audio`?"**

## Anti-patterns

- **Não** quebre frases no meio para forçar 500 chars — encurte a frase original.
- **Não** gere blocos com 1 só segmento — funde com o vizinho ou divide o texto.
- **Não** use bullets dentro de `text` — TTS lê literalmente "asterisco asterisco".
- **Não** deixe URLs ou e-mails no texto — substitua por "endereço web" ou pule.
- **Não** persista o JSON fora de `chatterbox-mcp/output/` — quebra a convenção de localidade.

## Estimativa de duração

Use **150 palavras/min** como baseline em PT-BR didático. Para `audiobook` use 130 wpm (mais lento); para `podcast` use 170 wpm (mais ágil).

Fórmula: `duracao_min = total_palavras / wpm`.
