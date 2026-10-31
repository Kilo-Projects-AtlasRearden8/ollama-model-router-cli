# ollama-model-router

A small, local-first Python CLI that routes prompts to different Ollama models
by task type, compares responses side by side, and saves every result to your
machine. No API keys, no accounts, nothing leaves your computer unless you
choose to move it.

Built by **Asdale Dynamics, LLC** — beginner-friendly AI education, books, and
practical local-LLM tools (dylanasdale.github.io).

## What it does

* `route` — send one prompt to the model chosen for its task type (code, chat,
  summary, creative, analysis, or your own mapping).
* `compare` — send the same prompt to several models at once and read the
  responses together.
* `list-models` — see what models your endpoint advertises.

The endpoint is configurable (default: Ollama at `http://localhost:11434`) and
speaks the OpenAI-compatible chat format, so it works with Ollama and any
OpenAI-compatible local-LLM server.

## Install

```bash
# From this folder
pip install -e .
```

This installs the `ollama-route` command. No external Python packages are
required — only the standard library.

## Run

You need a local endpoint running (Ollama by default):

```bash
ollama serve        # if it isn't already running
ollama pull llama3.1:8b
```

Route one prompt:

```bash
ollama-route "Explain git rebase like I'm five" --task chat
```

Compare one prompt across tasks:

```bash
ollama-route "Summarize this meeting" --tasks summary creative analysis
```

Compare across explicit models:

```bash
ollama-route "Write a Python quicksort" --models deepseek-coder-v2:latest llama3.1:8b
```

List available models:

```bash
ollama-route list-models
```

Every response is saved as a timestamped JSON file in the `results/` folder.

## Configure

| Environment variable | Default | Meaning |
|---|---|---|
| `OLLAMA_ENDPOINT` | `http://localhost:11434` | OpenAI-compatible endpoint |
| `OLLAMA_MODEL` | `llama3.1:8b` | Fallback model for unknown task types |
| `OLLAMA_MODEL_MAP` | (built-in) | JSON map of task type → model |
| `OLLAMA_TIMEOUT` | `60` | Request timeout in seconds |
| `OLLAMA_OUTPUT_DIR` | `results` | Folder for saved results |

Flags `--endpoint`, `--model-map`, `--default-model`, `--timeout`, and
`--output-dir` override the environment.

Example:

```bash
export OLLAMA_ENDPOINT=http://localhost:11434
export OLLAMA_MODEL_MAP='{"code":"deepseek-coder-v2:latest","chat":"llama3.1:8b"}'
ollama-route "Refactor this function" --task code
```

## Built-in task → model map

* code → `deepseek-coder-v2:latest`
* chat → `llama3.1:8b`
* summary → `mistral-nemo:latest`
* creative → `llama3.1:8b`
* analysis → `deepseek-coder-v2:latest`

Unknown task types fall back to the default model.

## Test

No keys, no network to outside services:

```bash
PYTHONPATH=src python -m pytest
```

Tests spin up a mock OpenAI-compatible endpoint on localhost and verify model
routing, fallback, comparison, and local file storage.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.
