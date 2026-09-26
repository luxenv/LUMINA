from tools import calculate

def maybe_calculate(message):
    low=message.lower().strip()
    for prefix in ("calculate ","calc "):
        if low.startswith(prefix):
            expr=message[len(prefix):].strip()
            try: return calculate(expr)
            except Exception: return None
    return None
