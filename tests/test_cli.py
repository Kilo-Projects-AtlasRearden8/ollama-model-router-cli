"""CLI tests: exit codes and error handling without a live endpoint."""

from __future__ import annotations

import pytest

from ollama_router.cli import main


def test_help_exits_zero():
    with pytest.raises(SystemExit) as exc:
        main(["--help"])
    assert exc.value.code == 0


def test_missing_command_errors():
    with pytest.raises(SystemExit) as exc:
        main([])
    assert exc.value.code == 2


def test_route_unreachable_endpoint_returns_one():
    assert (
        main(
            [
                "--endpoint",
                "http://127.0.0.1:1",
                "--timeout",
                "1",
                "route",
                "hello",
            ]
        )
        == 1
    )


def test_list_models_unreachable_returns_one():
    assert (
        main(["--endpoint", "http://127.0.0.1:1", "--timeout", "1", "list-models"])
        == 1
    )


def test_bad_model_map_returns_two():
    assert main(["--model-map", "{not json", "route", "hi"]) == 2
