import os
import requests

try:                                  # load settings from .env if python-dotenv is installed
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
API_KEY = os.environ.get("OLLAMA_API_KEY") or None
MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

def _post(body):
    headers = {"Authorization": f"Bearer {API_KEY}"} if API_KEY else {}
    response = requests.post(f"{HOST}/api/chat", headers=headers, json=body, timeout=120)
    response.raise_for_status()
    return response.json()

def chat(messages, temperature=0.7, format=None):
    """Returns (reply text, input tokens, output tokens). format: optional JSON Schema."""
    body = {"model": MODEL, "messages": messages, "stream": False, "options": {"temperature": temperature}}
    if format is not None:
        body["format"] = format
    data = _post(body)
    return data["message"]["content"], data["prompt_eval_count"], data["eval_count"]

def chat_message(messages, tools=None, temperature=0.2):
    """Returns (assistant message, input tokens, output tokens).
    The message may contain "tool_calls": [{"function": {"name": ..., "arguments": {...}}}]."""
    body = {"model": MODEL, "messages": messages, "stream": False, "options": {"temperature": temperature}}
    if tools:
        body["tools"] = tools
    data = _post(body)
    return data["message"], data["prompt_eval_count"], data["eval_count"]
