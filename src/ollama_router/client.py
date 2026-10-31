"""HTTP client for an OpenAI-compatible chat endpoint (default: Ollama)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Dict, List


class OllamaError(RuntimeError):
    """Raised when the OpenAI-compatible endpoint returns an error."""


class OllamaClient:
    """Thin client over an OpenAI-compatible /v1/chat/completions endpoint.

    Ollama serves this API natively at http://localhost:11434/v1/chat/completions,
    so no API keys are required and the endpoint is fully configurable.
    """

    def __init__(self, endpoint: str, timeout: int = 60) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.timeout = timeout

    def _post(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.endpoint}{path}",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise OllamaError(f"endpoint error {exc.code}: {body}") from exc
        except urllib.error.URLError as exc:
            raise OllamaError(f"cannot reach endpoint {self.endpoint}: {exc}") from exc

    def chat(self, model: str, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """Send a chat completion request and return the assistant's text."""
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": False,
        }
        body = self._post("/v1/chat/completions", payload)
        try:
            return body["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise OllamaError(f"unexpected response format: {body!r}") from exc

    def list_models(self) -> List[Dict[str, Any]]:
        """Return the models advertised by the endpoint (/v1/models)."""
        request = urllib.request.Request(f"{self.endpoint}/v1/models", method="GET")
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body_text = exc.read().decode("utf-8", errors="replace")
            raise OllamaError(f"endpoint error {exc.code}: {body_text}") from exc
        except urllib.error.URLError as exc:
            raise OllamaError(f"cannot reach endpoint {self.endpoint}: {exc}") from exc
        return body.get("data", [])
