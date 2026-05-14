# audio-forge

Plugin Claude Code para geração de áudios longos em PT-BR via Chatterbox Multilingual TTS, voltado a reforço de estudos e produção de conteúdo educacional.

## Propósito

Transforma material textual (PDF, DOCX, MD ou resumo colado) em **MP3 longo segmentado**, com voz natural em português brasileiro, pronto para ouvir no carro, durante corrida, ou em qualquer momento de tempo morto.

Casos de uso:

- Aulas faladas a partir de resumos
- Podcasts didáticos de capítulos de livro
- Audiobooks personalizados de PDFs
- Reforço de estudo por escuta (estilo *active recall* auditivo)

## Arquitetura

```
audio-forge (plugin)        →  chatterbox-mcp (MCP server)  →  Chatterbox TTS
  skills/                       server.py (FastMCP)             (Multilingual)
    building-roteiros           generate_segment
    producing-audio             concatenate_segments
```

O plugin **não** carrega o modelo Chatterbox diretamente. Ele consome o MCP server `chatterbox-mcp` (mantido em `~/Documents/brain/3-resources/ai-mcp/chatterbox-mcp/`), que isola o ambiente Python + GPU/CPU + modelo.

### Dependência externa

Este plugin depende do MCP server `chatterbox-mcp` rodando em:

```
~/Documents/brain/3-resources/ai-mcp/chatterbox-mcp/
├── .venv/bin/python    # Python 3.13 com dependências instaladas
├── server.py           # FastMCP entrypoint
├── output/             # WAVs intermediários + MP3 final + JSONs de roteiro
└── voices/             # Vozes para clonagem (opcional)
```

O plugin declara o MCP em `.mcp.json` com **paths absolutos** apontando para esse diretório. Isso significa:

- ✅ Funciona em uso pessoal local (instalação via `--plugin-dir` ou via marketplace local)
- ⚠️ **Não portável** entre máquinas sem ajuste manual dos paths absolutos
- ⚠️ Se mover `ai-mcp/chatterbox-mcp/` de lugar, atualize `.mcp.json`

## Instalação

Como parte do marketplace `chiaras-ai`:

```bash
/plugin marketplace add ~/Documents/brain/3-resources/ai-plugins/chiaras-ai
/plugin install audio-forge@chiaras-ai
```

Para desenvolvimento local sem instalar:

```bash
claude --plugin-dir ~/Documents/brain/3-resources/ai-plugins/chiaras-ai/audio-forge
```

## Fluxo de uso

```
material textual  ─►  building-roteiros  ─►  roteiro_<slug>.json  ─►  producing-audio  ─►  <slug>_completo.mp3
```

### Exemplo de sessão

```
Você: "Quero ouvir esse PDF de aula enquanto corro hoje. 60 minutos, didático."
Claude: [invoca building-roteiros]
        Roteiro pronto:
        - Título: <título>
        - Blocos: 5
        - Segmentos: 87
        - Duração estimada: ~58 min
        - Caminho: ~/.../output/roteiro_aula-x.json
        Posso prosseguir com producing-audio?

Você: "sim"
Claude: [invoca producing-audio]
        Tempo de produção esperado: CPU ~3h, GPU ~12min. Confirma?

Você: "sim"
Claude: [gera 87 segmentos em sequência, concatena]
        ✅ Áudio produzido
        Arquivo: ~/.../output/aula-x_completo.mp3
        Duração real: 57 min (estimado: 58, delta -2%)
        Tamanho: 41 MB
        Segmentos OK: 87/87

Você: "open <path>"
```

## Voice cloning

Para usar uma voz clonada em vez do default Chatterbox:

1. Coloque um arquivo `.wav` ou `.mp3` em `chatterbox-mcp/voices/` (≥10s de áudio limpo, mono, 24kHz preferencialmente).
2. Ao invocar `building-roteiros`, responda com o **nome do arquivo** (sem extensão) quando perguntado pela voz.
3. O `voice_reference` será gravado no JSON do roteiro e propagado automaticamente para `producing-audio`.

Boa prática: nomeie a voz como `pessoa-<nome>.wav` (ex: `pessoa-bruno.wav`) para evitar colisão com nomes genéricos.

## Skills

| Skill | O que faz | Trigger natural |
|---|---|---|
| [building-roteiros](skills/building-roteiros/SKILL.md) | Estrutura texto em roteiro JSON segmentado | "Gera um áudio desse material" |
| [producing-audio](skills/producing-audio/SKILL.md) | Consome roteiro JSON e produz MP3 final | Após `building-roteiros`, ou ao apontar roteiro existente |

## Limites técnicos

| Limite | Valor | Origem |
|---|---|---|
| Tamanho máx. por segmento | 500 chars | Chatterbox (hard cap) |
| Idioma | `pt` (PT-BR) | Modelo Multilingual; outros idiomas possíveis ajustando `language_id` |
| Real-time factor CPU | ~2-5x | Geração em Mac sem GPU |
| Real-time factor GPU | ~0.1-0.3x | CUDA ou MPS (Apple Silicon) |
| Paralelismo | 1 (serial) | Chatterbox tem estado interno; geração paralela quebra |

## Troubleshooting

**Geração muito lenta** → confirme se `CHATTERBOX_DEVICE` no `.mcp.json` está apropriado. Em Mac com chip Apple (M1/M2/M3/M4), testar `mps` pode acelerar significativamente.

**Sotaque estranho em PT-BR** → garanta que `language_id="pt"` esteja no roteiro (a skill `building-roteiros` força isso).

**Cortes abruptos no áudio** → algum segmento estourou 500 chars. Revise o JSON de roteiro e recalibre.

**MP3 final tem pausas irregulares** → na v0.1 o `silence_ms_between` é constante (600ms). Pausas variáveis por bloco entram no roadmap.

**Plugin não acha o MCP** → verifique os paths absolutos em `.mcp.json`. Se moveu `ai-mcp/chatterbox-mcp/`, atualize os caminhos.

## Roadmap

- v0.1 (atual): pipeline básico `building-roteiros` → `producing-audio` com pausas constantes.
- v0.2: pausas variáveis por bloco usando `pause_after_ms` de cada segmento durante concatenação.
- v0.3: suporte multi-voz (alternância em formato podcast 2-vozes).
- v0.4: integração com a pasta `~/Documents/brain/0-inbox/audio-queue/` para batch de processamento.
- v0.5: capítulos MP3 (ID3v2 CHAP) para navegação por bloco.

## Design system

Plugin pessoal — não usa tokens M7. Outputs são MP3 (sem visual), então a única consideração de UX é o **formato do reporte ao usuário** (tabelas curtas + caminhos absolutos clicáveis).

## Licença

MIT.
