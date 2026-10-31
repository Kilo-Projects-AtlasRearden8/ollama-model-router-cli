"""Router tests: model selection by task type and comparison."""

from __future__ import annotations

from ollama_router.client import OllamaClient
from ollama_router.router import Router


def test_route_uses_model_map(mock_endpoint):
    client = OllamaClient(mock_endpoint)
    router = Router(
        client,
        model_map={"code": "deepseek-coder-v2:latest", "chat": "llama3.1:8b"},
    )
    result = router.route("write a sort function", task_type="code")
    assert result["model"] == "deepseek-coder-v2:latest"
    assert result["response"] == "mock:deepseek-coder-v2:latest::write a sort function"
    assert result["task"] == "code"
    assert result["prompt"] == "write a sort function"


def test_route_falls_back_to_default_model(mock_endpoint):
    client = OllamaClient(mock_endpoint)
    router = Router(client, default_model="llama3.1:8b")
    result = router.route("just chatting", task_type="weird-task")
    assert result["model"] == "llama3.1:8b"


def test_route_model_override(mock_endpoint):
    client = OllamaClient(mock_endpoint)
    router = Router(client)
    result = router.route("hello", task_type="chat", model="override-model")
    assert result["model"] == "override-model"


def test_compare_by_tasks(mock_endpoint):
    client = OllamaClient(mock_endpoint)
    router = Router(client, model_map={"a": "model-a", "b": "model-b"})
    results = router.compare("same prompt", task_types=["a", "b"])
    assert [r["model"] for r in results] == ["model-a", "model-b"]
    assert all(r["prompt"] == "same prompt" for r in results)
    assert len(results) == 2


def test_compare_by_models(mock_endpoint):
    client = OllamaClient(mock_endpoint)
    router = Router(client)
    results = router.compare("same prompt", models=["m1", "m2"])
    assert [r["model"] for r in results] == ["m1", "m2"]
    assert all(r["task"] == "compare" for r in results)
