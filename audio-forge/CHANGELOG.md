# Changelog

All notable changes to the audio-forge plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-05-14

Initial preview release. Pipeline básico de geração de áudio longo em PT-BR via Chatterbox Multilingual TTS, consumindo o MCP server externo `chatterbox-mcp` mantido em `~/Documents/brain/3-resources/ai-mcp/chatterbox-mcp/`. Versão `0.x` sinaliza WIP — bumpar para `1.0.0` após validação em uso real (pipeline end-to-end estável, real-time factor medido, qualidade PT-BR aceita).

### Added

#### Infrastructure
- Plugin manifest (`.claude-plugin/plugin.json`) com `name`, `version`, `description`, `author`, `homepage`, `repository`, `license: MIT`, `keywords`
- MCP server declarado em `.mcp.json` apontando para `chatterbox-mcp` externo (paths absolutos para `.venv/bin/python` e `server.py`)
- `env` do MCP: `CHATTERBOX_DEVICE=cpu` (default seguro), `PYTHONUNBUFFERED=1`
- Defaults do server preservados (`CHATTERBOX_OUTPUT_DIR` e `CHATTERBOX_VOICES_DIR` não sobrescritos) — todos os artefatos consolidam em `chatterbox-mcp/output/` e `chatterbox-mcp/voices/`

#### Skills (2)
- `building-roteiros` — transforma material textual (PDF, DOCX, MD, TXT ou resumo colado) em roteiro JSON segmentado pronto para TTS. Coleta parâmetros (duração alvo, estilo: didático/podcast/audiobook, voz), aplica regras de calibração TTS (limite duro de 500 chars por segmento, normalização de siglas/símbolos/números, quebra apenas em ponto final), gera JSON em `chatterbox-mcp/output/roteiro_<slug>.json` com schema `{title, estimated_duration_min, voice_reference, language_id, style, segments[]}`. Convenção de pausas: 500ms intra-bloco, 1000ms entre blocos. Validação pré-gravação obrigatória.
- `producing-audio` — consome o roteiro JSON e produz MP3 final via MCP tools `chatterbox:generate_segment` (serial, com `exaggeration` + `cfg_weight` por estilo) e `chatterbox:concatenate_segments` (silêncio constante de 600ms). Pré-flight com estimativa de tempo de produção (CPU ~3x real-time, GPU ~0.2x), reporte de progresso por segmento, tratamento de falhas sem abortar o lote, opção de retry segmentado e limpeza opcional dos WAVs intermediários.

#### Marketplace
- Entry em `chiaras-ai/.claude-plugin/marketplace.json` com `source: "./audio-forge"`, `category: "productivity"`, keywords alinhadas ao `plugin.json`

#### Documentation
- `README.md` — propósito, arquitetura (plugin "thin client" sobre MCP externo), instruções de instalação via marketplace ou `--plugin-dir`, fluxo de uso end-to-end com exemplo de sessão, voice cloning, limites técnicos, troubleshooting, roadmap
- `CHANGELOG.md` — este arquivo

### Design Decisions

- **Skills em gerúndio** (`building-roteiros`, `producing-audio`) seguindo convenção do `claude-code-toolkit:creating-skills`
- **Plugin "thin client"** sem ambiente Python próprio — toda dependência de TTS isolada em `chatterbox-mcp` (separado em `ai-mcp/`)
- **Paths absolutos no `.mcp.json`** aceitos como trade-off explícito: plugin é pessoal (chiaras-ai), single-machine; portabilidade entre máquinas exige edição manual. Documentado no README.
- **Persistência de roteiros em `chatterbox-mcp/output/`** (não em diretório do plugin) — consolida JSONs + WAVs intermediários + MP3 final no mesmo diretório, evita fragmentação
- **Concatenação com silêncio constante** (`silence_ms_between=600`) nesta v0.1; pausas variáveis por `pause_after_ms` de cada segmento ficam no roadmap (v0.2)

### Known Limitations

- Real-time factor em CPU (~2-5x) torna geração de áudios >1h cansativa em Mac sem GPU/MPS — confirmar `CHATTERBOX_DEVICE` apropriado por máquina
- Pausas inter-segmento são constantes na v0.1 (variável só na v0.2)
- Voice cloning depende de arquivo WAV/MP3 com ≥10s de áudio limpo presente em `chatterbox-mcp/voices/`
- Paralelismo não suportado (Chatterbox tem estado interno; geração paralela quebra) — pipeline é estritamente serial

### Roadmap

- **v0.2** — pausas variáveis por bloco usando `pause_after_ms` de cada segmento
- **v0.3** — suporte multi-voz (alternância em formato podcast 2-vozes)
- **v0.4** — integração com `~/Documents/brain/0-inbox/audio-queue/` para batch
- **v0.5** — capítulos MP3 (ID3v2 CHAP) para navegação por bloco
- **v1.0.0** — após validação end-to-end em uso real

[0.1.0]: https://github.com/bchiaramonti/chiaras-ai/releases/tag/audio-forge-v0.1.0
