"""Command-line interface for the Ollama model router."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .client import OllamaClient, OllamaError
from .config import Config
from .router import Router
from .store import save_result, save_results


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ollama-route",
        description=(
            "Route prompts to Ollama models by task type, compare responses, "
            "and save results locally. No API keys required."
        ),
    )
    parser.add_argument("--endpoint", default=None, help="OpenAI-compatible endpoint (default: http://localhost:11434)")
    parser.add_argument(
        "--model-map",
        default=None,
        help='JSON mapping of task types to models, e.g. {"code":"deepseek-coder-v2:latest"}',
    )
    parser.add_argument("--default-model", default=None, help="Fallback model for unknown task types")
    parser.add_argument("--timeout", type=int, default=None, help="Request timeout in seconds (default: 60)")
    parser.add_argument("--output-dir", default=None, help="Directory for saved results (default: results)")

    sub = parser.add_subparsers(dest="command", required=True)

    p_route = sub.add_parser("route", help="Route one prompt to one model")
    p_route.add_argument("prompt", help="Prompt text to send")
    p_route.add_argument("--task", default="chat", help="Task type used to pick the model (default: chat)")
    p_route.add_argument("--model", default=None, help="Override the model used for this request")

    p_compare = sub.add_parser("compare", help="Send one prompt to several models and compare responses")
    p_compare.add_argument("prompt", help="Prompt text to send")
    p_compare.add_argument("--tasks", nargs="*", default=None, help="Task types to compare (uses model map)")
    p_compare.add_argument("--models", nargs="*", default=None, help="Explicit models to compare")

    p_list = sub.add_parser("list-models", help="List models advertised by the endpoint")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        config = Config.from_env(
            {
                "endpoint": args.endpoint,
                "model_map": args.model_map,
                "default_model": args.default_model,
                "timeout": args.timeout,
                "output_dir": args.output_dir,
            }
        )
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    client = OllamaClient(config.endpoint, config.timeout)
    router = Router(client, model_map=config.model_map, default_model=config.default_model)

    if args.command == "list-models":
        try:
            models = client.list_models()
        except OllamaError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        for entry in models:
            print(entry.get("id", entry))
        return 0

    if args.command == "route":
        try:
            result = router.route(args.prompt, task_type=args.task, model=args.model)
        except OllamaError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(result["response"])
        path = save_result(result, config.output_dir)
        print(f"saved: {path}", file=sys.stderr)
        return 0

    if args.command == "compare":
        try:
            results = router.compare(args.prompt, task_types=args.tasks, models=args.models)
        except OllamaError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        for result in results:
            print(f"--- {result['task']} ({result['model']}) ---")
            print(result["response"])
            print()
        paths = save_results(results, config.output_dir)
        for path in paths:
            print(f"saved: {path}", file=sys.stderr)
        return 0

    parser.print_help(sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
