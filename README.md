# ollama-model-router

A friendly, local-first Python CLI that sends your prompts to different Ollama
models based on the task at hand, lets you compare the responses side by side,
and saves everything to your own computer. No API keys, no accounts, nothing
leaves your machine unless you choose to move it.

Built by **Asdale Dynamics, LLC** — beginner-friendly AI education, books, and
practical local-LLM tools (dylanasdale.github.io).

## What it does

Think of this as a router for your prompts. You tell it what kind of task you're
working on (writing code, chatting, summarizing, getting creative, or analyzing
something), and it picks the right Ollama model for the job. It can also send
the same prompt to several models at once so you can read the answers together
and decide which you like best.

Three commands:

* `route` — send one prompt to the model chosen for its task type.
* `compare` — send one prompt to several models and read the responses together.
* `list-models` — see what models your local endpoint has available.

Every response is saved as a timestamped JSON file in a `results/` folder on
your computer, so you always have a local copy.

## Who this is for

This tool is written for people who are new to local AI and want something that
just works — no command-line wizardry, no credit cards, no accounts. If you can
copy and paste a command into a terminal, you can use this.

## Install

From this folder:

```bash
pip install -e .
```

That installs the `ollama-route` command. Nothing else is required — just
Python and the standard library, no extra packages to download.

### A note on where flags go

Global options like `--endpoint` go **before** the subcommand:

```bash
ollama-route --endpoint http://localhost:11434 route "hello" --task chat
```

Putting them after the subcommand (for example, `route --endpoint ...`) won't
work, because argparse treats options before and after the subcommand
differently. This is the one slightly fussy part — sorry about that!

## Run

You need a local endpoint running. Ollama is the default:

```bash
# Start Ollama if it isn't already running
ollama serve

# Pull a model you'd like to use
ollama pull llama3.1:8b
```

Then send a prompt:

```bash
ollama-route "Explain git rebase like I'm five" --task chat
```

You'll see the model's answer printed, and a copy saved to `results/`.

### Compare one prompt across tasks

Send the same prompt to the models chosen for several task types:

```bash
ollama-route "Summarize this meeting" --tasks summary creative analysis
```

### Compare across specific models

```bash
ollama-route "Write a Python quicksort" --models deepseek-coder-v2:latest llama3.1:8b
```

### See what models are available

```bash
ollama-route list-models
```

## Configure

The endpoint and models are fully configurable. Ollama at
`http://localhost:11434` is the default, but you can point this at any
OpenAI-compatible local-LLM server.

Set these as environment variables, or pass them as flags:

| Environment variable | Flag | Default | Meaning |
|---|---|---|---|
| `OLLAMA_ENDPOINT` | `--endpoint` | `http://localhost:11434` | Your OpenAI-compatible endpoint |
| `OLLAMA_MODEL` | `--default-model` | `llama3.1:8b` | Fallback model for unknown task types |
| `OLLAMA_MODEL_MAP` | `--model-map` | (built-in) | JSON map of task type → model |
| `OLLAMA_TIMEOUT` | `--timeout` | `60` | Seconds to wait for a response |
| `OLLAMA_OUTPUT_DIR` | `--output-dir` | `results` | Folder where results are saved |

Flags override environment variables.

Example:

```bash
export OLLAMA_ENDPOINT=http://localhost:11434
export OLLAMA_MODEL_MAP='{"code":"deepseek-coder-v2:latest","chat":"llama3.1:8b"}'
ollama-route "Refactor this function" --task code
```

### Built-in task → model map

* code → `deepseek-coder-v2:latest`
* chat → `llama3.1:8b`
* summary → `mistral-nemo:latest`
* creative → `llama3.1:8b`
* analysis → `deepseek-coder-v2:latest`

Task types not in the list fall back to the default model. You can override any
of these with `--model-map` or `--default-model`.

## Test

No keys, no network to outside services. The tests spin up a mock endpoint on
your own computer and check routing, fallback, comparison, and file storage:

```bash
PYTHONPATH=src python3 -m pytest
```

You can also run the package directly without installing:

```bash
PYTHONPATH=src python3 -m ollama_router --help
```

## Privacy

This tool is local-first. It talks only to the endpoint you configure (Ollama
on your machine by default). It never sends your prompts to Asdale Dynamics,
never asks for an API key, and never writes anything to the cloud. The only
files it creates are the `results/` JSON files on your own computer.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.
