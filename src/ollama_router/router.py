"""Prompt routing: pick a model by task type, or compare across models."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .client import OllamaClient
from .config import DEFAULT_MODEL, DEFAULT_MODEL_MAP


class Router:
    """Routes prompts to models by task type and compares responses."""

    def __init__(
        self,
        client: OllamaClient,
        model_map: Optional[Dict[str, str]] = None,
        default_model: str = DEFAULT_MODEL,
    ) -> None:
        self.client = client
        self.model_map: Dict[str, str] = dict(DEFAULT_MODEL_MAP)
        if model_map:
            self.model_map.update(model_map)
        self.default_model = default_model

    def model_for(self, task_type: str) -> str:
        """Return the model configured for a task type, falling back to default."""
        return self.model_map.get(task_type, self.default_model)

    def route(self, prompt: str, task_type: str = "chat", model: Optional[str] = None) -> Dict[str, Any]:
        """Route a single prompt to one model and return the result record."""
        model = model or self.model_for(task_type)
        messages = [{"role": "user", "content": prompt}]
        response = self.client.chat(model, messages)
        return {
            "task": task_type,
            "model": model,
            "prompt": prompt,
            "response": response,
        }

    def compare(
        self,
        prompt: str,
        task_types: Optional[List[str]] = None,
        models: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Send one prompt to several model/task combinations and return all results."""
        if models is not None:
            combinations = [("compare", model) for model in models]
        elif task_types is not None:
            combinations = [(task, self.model_for(task)) for task in task_types]
        else:
            combinations = list(self.model_map.items())

        results: List[Dict[str, Any]] = []
        for task, model in combinations:
            result = self.route(prompt, task_type=task, model=model)
            results.append(result)
        return results
