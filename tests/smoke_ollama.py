import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import requests
from common.llm import chat, chat_message, MODEL, HOST

print(f"Using {MODEL} at {HOST}")
reply, tokens_in, tokens_out = chat([{"role": "user", "content": "Explain what an API is in one sentence."}])
print("chat():", reply)
print(f"tokens: {tokens_in} in, {tokens_out} out")

TOOLS = [{"type": "function", "function": {
    "name": "fetch_news", "description": "Get the latest headlines for a topic.",
    "parameters": {"type": "object", "properties": {"topic": {"type": "string", "enum": ["ai", "jobs"]}},
                   "required": ["topic"]}}}]
message, _, _ = chat_message([{"role": "user", "content": "What's the latest AI news? Use the tool."}], tools=TOOLS)
calls = message.get("tool_calls") or []
print("tool calls:", [(c["function"]["name"], c["function"]["arguments"]) for c in calls])

news = requests.get("https://faang-prep-app.vercel.app/api/news", params={"topic": "ai"}, timeout=30).json()
print("news API:", len(news["articles"]), "articles, e.g.", news["articles"][0]["title"][:60])
print("OLLAMA SMOKE TEST PASSED" if calls else "Model answered without calling the tool: try OLLAMA_MODEL=qwen3")
