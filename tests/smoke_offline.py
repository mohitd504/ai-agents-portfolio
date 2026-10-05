import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.fakes import make_fake_model, tool_call, answer

def fetch_news(topic):
    return [{"title": "OpenAI ships a faster reasoning model", "source": "TechCrunch"}]

model = make_fake_model([tool_call("fetch_news", topic="ai"),
                         answer("Today's top AI story: OpenAI ships a faster reasoning model (TechCrunch).")])
messages = [{"role": "user", "content": "What's the top AI story today?"}]
message, _, _ = model(messages)
messages.append(message)
for call in message["tool_calls"]:
    result = fetch_news(**call["function"]["arguments"])
    messages.append({"role": "tool", "tool_name": "fetch_news", "content": json.dumps(result)})
message, _, _ = model(messages)
print(message["content"])
print("OFFLINE SMOKE TEST PASSED")
