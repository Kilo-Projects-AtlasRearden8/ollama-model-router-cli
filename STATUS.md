# STATUS

## What was built

`ollama-model-router` — a local-first Python CLI that routes prompts to
Ollama models by task type, compares responses across models, and saves every
result as a timestamped JSON file under `results/`. No API keys, no accounts,
nothing leaves your machine.

* `src/ollama_router/client.py` — thin client over an OpenAI-compatible
  `/v1/chat/completions` endpoint using only the Python standard library
  (urllib). Default endpoint: `http://localhost:11434` (Ollama).
* `src/ollama_router/router.py` — picks a model from a built-in task-to-model
  map (code, chat, summary, creative, analysis), falls back to a default
  model, supports per-request model overrides, and runs `compare` across
  multiple tasks or models.
* `src/ollama_router/store.py` — appends results to `results/` as JSON.
* `src/ollama_router/cli.py` — argparse CLI: `route`, `compare`,
  `list-models`; flags and environment variables (`OLLAMA_ENDPOINT`,
  `OLLAMA_MODEL_MAP`, `OLLAMA_MODEL`, `OLLAMA_TIMEOUT`, `OLLAMA_OUTPUT_DIR`)
  for configuration.
* `src/ollama_router/__main__.py` — allows `python -m ollama_router`.
* `pyproject.toml` — installs the `ollama-route` console script, no external
  dependencies.
* `tests/` — 22 tests against a mock OpenAI-compatible endpoint (no network,
  no API keys): client chat/models, unreachable endpoint handling, model map
  routing, default fallback, overrides, compare modes, file storage, config
  loading/env vars/validation, and CLI exit codes.
* `LICENSE` — MIT, Copyright (c) 2026 Asdale Dynamics, LLC.
* `README.md` — beginner-friendly usage, configuration, privacy notes,
  crediting Asdale Dynamics, LLC.
* `.gitignore` — excludes Python bytecode, caches, build artifacts, results.

## How to run

```bash
cd /workspace/kilo-lab/ollama-model-router-cli

# Run tests (mock endpoint, no Ollama needed, no keys)
PYTHONPATH=src python3 -m pytest

# Install the command (use a virtualenv on externally-managed Python)
pip install -e .

# Run directly without installing
PYTHONPATH=src python3 -m ollama_router --help

# Needs a local endpoint (Ollama default)
ollama serve
ollama pull llama3.1:8b

ollama-route "Explain MCP like I'm five" --task chat
ollama-route "Summarize this" --tasks summary creative analysis
ollama-route list-models
```

Global options like `--endpoint` go **before** the subcommand.

Results are saved to `results/` as timestamped JSON files.

## Verification

* `pytest`: 22 passed, 0 failed (mock endpoint, standard library only).
* CLI smoke-tested end-to-end against a mock endpoint: `route` prints the
  response and writes `results/`, `list-models` lists endpoint models,
  `compare` prints all responses and saves them.
* `pip install -e .` verified in a virtualenv; both the `ollama-route`
  entry point and `python -m ollama_router` work.

## Known gaps

* No real Ollama instance in this environment, so end-to-end against a live
  Ollama server was not executed; the client hits the standard
  `/v1/chat/completions` path Ollama serves natively.
* Streaming responses are not supported (`stream: False`).
* No authentication support (by design — no keys/secrets).
* Default task-to-model map models (e.g. `deepseek-coder-v2:latest`) must be
  pulled into Ollama before routing to them.
* argparse requires global options (`--endpoint`, etc.) before the subcommand;
  placing them after the subcommand is an error. Documented in the README.
