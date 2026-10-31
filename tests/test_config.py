"""Configuration tests: env vars, overrides, and validation."""

from __future__ import annotations

import os

from ollama_router.config import DEFAULT_MODEL_MAP, Config


def test_defaults(monkeypatch):
    monkeypatch.delenv("OLLAMA_ENDPOINT", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL_MAP", raising=False)
    monkeypatch.delenv("OLLAMA_TIMEOUT", raising=False)
    monkeypatch.delenv("OLLAMA_OUTPUT_DIR", raising=False)

    config = Config.from_env()
    assert config.endpoint == "http://localhost:11434"
    assert config.default_model == "llama3.1:8b"
    assert config.model_map == dict(DEFAULT_MODEL_MAP)
    assert config.timeout == 60
    assert config.output_dir == "results"


def test_env_variables(monkeypatch):
    monkeypatch.setenv("OLLAMA_ENDPOINT", "http://localhost:9999")
    monkeypatch.setenv("OLLAMA_MODEL", "llama3.1:8b")
    monkeypatch.setenv(
        "OLLAMA_MODEL_MAP", '{"code":"deepseek-coder-v2:latest","chat":"llama3.1:8b"}'
    )
    monkeypatch.setenv("OLLAMA_TIMEOUT", "120")
    monkeypatch.setenv("OLLAMA_OUTPUT_DIR", "out")

    config = Config.from_env()
    assert config.endpoint == "http://localhost:9999"
    assert config.default_model == "llama3.1:8b"
    assert config.model_map == {
        "code": "deepseek-coder-v2:latest",
        "chat": "llama3.1:8b",
        "summary": "mistral-nemo:latest",
        "creative": "llama3.1:8b",
        "analysis": "deepseek-coder-v2:latest",
    }
    assert config.timeout == 120
    assert config.output_dir == "out"


def test_overrides_win_over_env(monkeypatch):
    monkeypatch.setenv("OLLAMA_ENDPOINT", "http://env:1111")
    monkeypatch.setenv("OLLAMA_MODEL", "env-model")

    config = Config.from_env(
        {"endpoint": "http://override:2222", "default_model": "override-model"}
    )
    assert config.endpoint == "http://override:2222"
    assert config.default_model == "override-model"


def test_model_map_merge_with_defaults(monkeypatch):
    monkeypatch.delenv("OLLAMA_MODEL_MAP", raising=False)

    config = Config.from_env({"model_map": {"poetry": "llama3.1:8b"}})
    assert config.model_map["poetry"] == "llama3.1:8b"
    assert config.model_map["code"] == "deepseek-coder-v2:latest"


def test_invalid_model_map_json_raises(monkeypatch):
    monkeypatch.setenv("OLLAMA_MODEL_MAP", "{not json")
    try:
        Config.from_env()
    except ValueError as exc:
        assert "not valid JSON" in str(exc)
    else:
        raise AssertionError("expected ValueError for bad JSON")


def test_invalid_timeout_raises(monkeypatch):
    monkeypatch.setenv("OLLAMA_TIMEOUT", "not-a-number")
    try:
        Config.from_env()
    except ValueError as exc:
        assert "must be an integer" in str(exc)
    else:
        raise AssertionError("expected ValueError for bad timeout")
