"""Configuration for the Ollama model router."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

DEFAULT_ENDPOINT = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1:8b"
DEFAULT_TIMEOUT = 60
DEFAULT_OUTPUT_DIR = "results"

DEFAULT_MODEL_MAP: Dict[str, str] = {
    "code": "deepseek-coder-v2:latest",
    "chat": "llama3.1:8b",
    "summary": "mistral-nemo:latest",
    "creative": "llama3.1:8b",
    "analysis": "deepseek-coder-v2:latest",
}


@dataclass
class Config:
    """Router configuration loaded from flags, environment, and defaults."""

    endpoint: str = DEFAULT_ENDPOINT
    model_map: Dict[str, str] = field(default_factory=lambda: dict(DEFAULT_MODEL_MAP))
    default_model: str = DEFAULT_MODEL
    timeout: int = DEFAULT_TIMEOUT
    output_dir: str = DEFAULT_OUTPUT_DIR

    @classmethod
    def from_env(cls, overrides: Optional[Dict[str, Any]] = None) -> "Config":
        overrides = dict(overrides or {})

        endpoint = overrides.get("endpoint") or os.environ.get("OLLAMA_ENDPOINT") or DEFAULT_ENDPOINT
        default_model = overrides.get("default_model") or os.environ.get("OLLAMA_MODEL") or DEFAULT_MODEL

        model_map = dict(DEFAULT_MODEL_MAP)
        raw_map = overrides.get("model_map") or os.environ.get("OLLAMA_MODEL_MAP")
        if raw_map:
            if isinstance(raw_map, str):
                try:
                    raw_map = json.loads(raw_map)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"OLLAMA_MODEL_MAP is not valid JSON: {exc}") from exc
            if not isinstance(raw_map, dict):
                raise ValueError("OLLAMA_MODEL_MAP must be a JSON object mapping task types to models")
            model_map.update({str(k): str(v) for k, v in raw_map.items()})

        try:
            timeout = int(overrides.get("timeout") or os.environ.get("OLLAMA_TIMEOUT") or DEFAULT_TIMEOUT)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"OLLAMA_TIMEOUT must be an integer: {exc}") from exc

        output_dir = overrides.get("output_dir") or os.environ.get("OLLAMA_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR

        return cls(
            endpoint=endpoint,
            model_map=model_map,
            default_model=default_model,
            timeout=timeout,
            output_dir=output_dir,
        )
