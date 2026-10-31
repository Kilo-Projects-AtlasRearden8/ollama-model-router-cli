"""Client tests against the mock endpoint."""

from __future__ import annotations

from ollama_router.client import OllamaClient, OllamaError


def test_chat_returns_assistant_message(mock_endpoint):
    client = OllamaClient(mock_endpoint)
    reply = client.chat("mock-model", [{"role": "user", "content": "hello"}])
    assert reply == "mock:mock-model::hello"


def test_chat_uses_requested_model(mock_endpoint):
    client = OllamaClient(mock_endpoint)
    client.chat("deepseek-coder-v2:latest", [{"role": "user", "content": "write a function"}])
    # The mock echoes the model into the response, proving the right model was sent.
    reply = client.chat("mistral-nemo:latest", [{"role": "user", "content": "x"}])
    assert reply.startswith("mock:mistral-nemo:latest::")


def test_list_models(mock_endpoint):
    client = OllamaClient(mock_endpoint)
    models = client.list_models()
    ids = {entry["id"] for entry in models}
    assert {"mock-model", "mock-other"} <= ids


def test_unreachable_endpoint_raises():
    client = OllamaClient("http://127.0.0.1:1", timeout=1)
    try:
        client.chat("mock-model", [{"role": "user", "content": "hi"}])
    except OllamaError as exc:
        assert "cannot reach endpoint" in str(exc)
    else:
        raise AssertionError("expected OllamaError for unreachable endpoint")
