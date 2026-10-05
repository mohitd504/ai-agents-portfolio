def tool_call(name, **arguments):
    """An assistant message asking for one tool, shaped like Ollama's."""
    return {"role": "assistant", "content": "", "tool_calls": [{"function": {"name": name, "arguments": arguments}}]}

def answer(text):
    """An assistant message with a final answer and no tool calls."""
    return {"role": "assistant", "content": text}

def make_fake_chat(replies):
    """A stand-in for chat(): returns scripted text replies in order and records every call."""
    calls = []
    def fake_chat(messages, temperature=0.7, format=None):
        calls.append(messages)
        reply = replies[len(calls) - 1]
        return reply, sum(len(m["content"]) for m in messages) // 4, len(reply) // 4
    fake_chat.calls = calls
    return fake_chat

def make_fake_model(script):
    """A stand-in for chat_message(): returns scripted assistant messages in order.
    A script entry can also be a function of the messages, for replies that depend on them."""
    calls = []
    def fake_model(messages, tools=None, temperature=0.2):
        calls.append([dict(m) for m in messages])
        step = script[len(calls) - 1]
        message = step(messages) if callable(step) else step
        tokens_in = sum(len(str(m.get("content", ""))) for m in messages) // 4
        return message, tokens_in, len(str(message.get("content", ""))) // 4 + 10
    fake_model.calls = calls
    return fake_model
