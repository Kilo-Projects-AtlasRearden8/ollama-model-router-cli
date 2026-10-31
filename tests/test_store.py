"""Store tests: results are written to local JSON files."""

from __future__ import annotations

import json
import os

from ollama_router.store import save_result, save_results


def test_save_result_writes_json(tmp_path):
    result = {"task": "chat", "model": "mock-model", "prompt": "hi", "response": "mock:mock-model::hi"}
    path = save_result(result, output_dir=str(tmp_path))
    assert os.path.isfile(path)
    with open(path, encoding="utf-8") as handle:
        loaded = json.load(handle)
    assert loaded == result


def test_save_results_writes_many(tmp_path):
    results = [
        {"task": "a", "model": "m1", "prompt": "p", "response": "r1"},
        {"task": "b", "model": "m2", "prompt": "p", "response": "r2"},
    ]
    paths = save_results(results, output_dir=str(tmp_path))
    assert len(paths) == 2
    assert all(os.path.isfile(p) for p in paths)
    assert len(os.listdir(tmp_path)) == 2
