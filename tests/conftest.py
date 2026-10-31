"""Mock OpenAI-compatible endpoint for tests."""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler
from socketserver import TCPServer
from typing import Dict


class _MockHandler(BaseHTTPRequestHandler):
    """Handles /v1/chat/completions (POST) and /v1/models (GET).

    The chat response echoes the requested model so tests can verify routing.
    """

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/chat/completions":
            self._reply(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length) or b"{}")
        model = body.get("model", "unknown")
        prompt = (body.get("messages") or [{}])[-1].get("content", "")
        self._reply(200, {"choices": [{"message": {"content": f"mock:{model}::{prompt}"}}]})

    def do_GET(self) -> None:  # noqa: N802
        if self.path != "/v1/models":
            self._reply(404, {"error": "not found"})
            return
        self._reply(200, {"data": [{"id": "mock-model"}, {"id": "mock-other"}]})

    def _reply(self, code: int, obj: Dict) -> None:
        payload = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *args) -> None:
        pass


class MockEndpoint:
    """Context-managed mock server on a free localhost port."""

    def __init__(self) -> None:
        self.server = TCPServer(("127.0.0.1", 0), _MockHandler)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def __enter__(self) -> str:
        self.thread.start()
        return f"http://127.0.0.1:{self.port}"

    def __exit__(self, *exc) -> None:
        self.server.shutdown()
        self.server.server_close()


import pytest  # noqa: E402


@pytest.fixture
def mock_endpoint():
    with MockEndpoint() as url:
        yield url
