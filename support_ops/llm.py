"""LLM backends. Pick one with --backend:

  rules      No AI at all. Keyword rules + macros. Free, instant, works offline.
  ollama     A local model through Ollama (http://localhost:11434). Free, private.
  anthropic  Claude through the Anthropic API. Needs ANTHROPIC_API_KEY.

Everything uses the standard library, so there is nothing to pip install.
"""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request

DEFAULT_OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")
DEFAULT_ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-haiku-5-5")


class LLMError(RuntimeError):
    pass


def _post_json(url: str, payload: dict, headers: dict, timeout: int = 180) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers}, method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:500]
        raise LLMError(f"HTTP {e.code} from {url}: {detail}") from e
    except urllib.error.URLError as e:
        raise LLMError(f"Could not reach {url}: {e.reason}") from e


class OllamaLLM:
    name = "ollama"

    def __init__(self, model: str | None = None, host: str | None = None):
        self.model = model or DEFAULT_OLLAMA_MODEL
        self.host = (host or os.environ.get("OLLAMA_HOST", "http://localhost:11434")).rstrip("/")

    def complete(self, system: str, user: str, json_mode: bool = False) -> str:
        payload = {
            "model": self.model,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
            "stream": False,
            "options": {"temperature": 0.2, "num_ctx": 8192},
        }
        if json_mode:
            payload["format"] = "json"
        data = _post_json(f"{self.host}/api/chat", payload, {})
        return data.get("message", {}).get("content", "")


class AnthropicLLM:
    name = "anthropic"

    def __init__(self, model: str | None = None):
        self.model = model or DEFAULT_ANTHROPIC_MODEL
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise LLMError("Set the ANTHROPIC_API_KEY environment variable to use --backend anthropic.")

    def complete(self, system: str, user: str, json_mode: bool = False) -> str:
        if json_mode:
            system += "\n\nRespond with a single JSON object and nothing else."
        payload = {
            "model": self.model,
            "max_tokens": 1500,
            "temperature": 0.2,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }
        headers = {"x-api-key": self.api_key, "anthropic-version": "2023-06-01"}
        data = _post_json("https://api.anthropic.com/v1/messages", payload, headers)
        return "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")


def get_llm(backend: str, model: str | None = None):
    if backend == "rules":
        return None
    if backend == "ollama":
        return OllamaLLM(model)
    if backend == "anthropic":
        return AnthropicLLM(model)
    raise LLMError(f"Unknown backend: {backend}")


def extract_json(text: str) -> dict:
    """Pull the first JSON object out of a model reply (models sometimes add chatter)."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    depth = 0
    for i in range(start, len(text)) if start >= 0 else []:
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : i + 1])
    raise ValueError("No JSON object found in model output")
