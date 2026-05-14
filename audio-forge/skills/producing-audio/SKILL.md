---
name: producing-audio
description: Produz arquivo MP3 segmentado em PT-BR a partir de um roteiro JSON estruturado, chamando o MCP server chatterbox para cada segmento e concatenando no áudio final. Use após a skill building-roteiros ou quando o usuário fornecer um roteiro JSON pronto e pedir para gerar o áudio.
---

# Producing Audio

Consome um roteiro JSON estruturado e produz o MP3 final, invocando ferramentas do MCP server `chatterbox` segmento a segmento.

## Pré-requisitos

- Roteiro JSON válido em `~/Documents/brain/3-resources/ai-mcp/chatterbox-mcp/output/roteiro_*.json` (produzido pela skill `building-roteiros` ou fornecido pelo usuário).
- MCP server `chatterbox` ativo (declarado em `.mcp.json` do plugin).
- Se usar voice cloning: arquivo WAV/MP3 em `chatterbox-mcp/voices/`.

## Workflow

### 1. Localizar e validar o roteiro

- Se o usuário não especificou caminho:
  - Liste `~/Documents/brain/3-resources/ai-mcp/chatterbox-mcp/output/roteiro_*.json` via `Bash`.
  - Pergunte qual usar (mostrando título + total de segmentos extraídos do JSON).
- Valide estrutura mínima com `Read`:
  - Tem `title` não-vazio
  - Tem `segments` não-vazio
  - Cada segmento tem `id`, `text`, `block`
  - Nenhum `text` excede 500 caracteres
- Se inválido: reporte erro específico (qual segmento, qual campo) e peça correção. **Não tente "consertar" silenciosamente.**

### 2. Pré-flight check

Antes de iniciar a geração, **sempre** mostre estimativas e peça confirmação:

| Métrica | Como calcular |
|---|---|
| Total de segmentos | `len(segments)` |
| Áudio estimado | `estimated_duration_min` do JSON |
| Tempo de produção (CPU) | `áudio_min × 3` (real-time factor típico 2-5x; use 3 como média) |
| Tempo de produção (GPU) | `áudio_min × 0.2` (real-time factor 0.1-0.3; use 0.2) |

Reporte em formato:

```
Roteiro: <título>
Segmentos: <N>
Áudio estimado: ~<X> min
Tempo de produção esperado:
- CPU (Mac/Linux sem GPU): ~<Y> min
- GPU (CUDA/MPS): ~<Z> min

Confirma prosseguir?
```

**Espere "sim" explícito** antes de chamar o MCP. Produção pode levar horas em CPU.

### 3. Geração segmento a segmento

Para cada segmento do JSON, **em ordem**, chame `chatterbox:generate_segment` com:

| Parâmetro | Valor |
|---|---|
| `text` | `segment.text` |
| `segment_id` | `<roteiro_slug>_<segment.id>` (prefixe com slug para evitar colisão entre roteiros) |
| `language_id` | `roteiro.language_id` (default `"pt"`) |
| `voice_reference` | `roteiro.voice_reference` (se houver) |
| `exaggeration` | `0.4` (mais neutro para conteúdo didático) |
| `cfg_weight` | `0.6` (mais aderente ao texto, menos variação criativa) |

**Estilos diferentes**:
- `audiobook`: `exaggeration=0.5`, `cfg_weight=0.5`
- `podcast`: `exaggeration=0.6`, `cfg_weight=0.4`
- `didático` (default): `exaggeration=0.4`, `cfg_weight=0.6`

**Log de progresso** (a cada segmento):

```
[i/N] segment <id> gerado · <duração>s · acumulado <total_min>min
```

**Tratamento de erro**:
- Se um segmento falhar, **continue** com os próximos.
- Mantenha lista `falhas[]` com `{segment_id, erro, texto_resumido}`.
- **Não aborte o lote** por falha pontual — usuário pode reprocessar depois.

### 4. Concatenação

Após processar todos os segmentos, chame `chatterbox:concatenate_segments`:

| Parâmetro | Valor |
|---|---|
| `segment_files` | Lista ordenada dos `segment_id` gerados com sucesso |
| `output_name` | `<roteiro_slug>_completo` |
| `silence_ms_between` | `600` (média entre intra-bloco 500ms e inter-bloco 1000ms) |
| `output_format` | `"mp3"` |

> Nota sobre pausas variáveis: a primeira versão usa `silence_ms_between` constante. Pausas variáveis por `pause_after_ms` de cada segmento ficam no roadmap.

### 5. Apresentação final

Reporte:

```
✅ Áudio produzido

Arquivo: <caminho absoluto do MP3>
Duração real: <X> min (estimado: <Y> min, delta <±Z%>)
Tamanho: <N> MB
Segmentos OK: <S>/<T>
Segmentos com falha: <F>

Abrir: open <caminho>
```

Se houver falhas, liste-as com os primeiros 60 chars do texto e ofereça retry segmentado:

```
Falhas detectadas:
- b2s4: "<primeiros 60 chars>..." (erro: <msg>)
- b3s1: "<primeiros 60 chars>..." (erro: <msg>)

Quer que eu refaça apenas estes <F> segmentos?
```

### 6. Limpeza opcional

Pergunte ao final:

> Manter os WAV individuais em `chatterbox-mcp/output/` para regenerar partes depois (recomendado), ou apagar para liberar espaço?

Default: **manter**. Se usuário pedir apagar, use `Bash` com `rm` apenas dos `.wav` cujo prefixo bate com `<roteiro_slug>_`.

## Anti-patterns

- **Não** chame `chatterbox:generate_segment` em paralelo — Chatterbox tem estado interno; serialização é obrigatória.
- **Não** invente segment_ids — sempre derive do JSON (`<slug>_<segment.id>`).
- **Não** abra arquivos `.wav` no chat pra "verificar" — o ouvido é o verificador final, peça ao usuário abrir o MP3.
- **Não** modifique o JSON do roteiro após início da geração — fix-then-reprocess, não fix-in-place.
- **Não** sobrescreva MP3 existente sem perguntar.

## Troubleshooting

| Sintoma | Causa provável | Ação |
|---|---|---|
| Geração muito lenta | Rodando em CPU sem GPU | Confirme `CHATTERBOX_DEVICE` no `.mcp.json`; em Mac com chip Apple, `mps` pode ajudar |
| Voz "estrangeira" em PT | `language_id` ausente ou errado | Force `language_id="pt"` |
| Cortes abruptos | Segmento estoura 500 chars | Volte à `building-roteiros` e recalibre |
| Pausas erradas | `silence_ms_between` único | Aceitar nesta v0.1; pausas variáveis em roadmap |
| Voz clone não bate | Path do WAV errado | Verifique `voices/<file>` existe e tem ≥10s de áudio limpo |
