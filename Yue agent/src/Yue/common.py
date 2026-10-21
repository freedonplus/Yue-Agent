def _text(msg):
    c = msg.content
    if isinstance(c, str):
        return c
    return "".join(
        p.get("text", "") for p in c
        if isinstance(p, dict) and p.get("type") == "text"
    )