conversation_history = {}


def add_message(session_id: str, role: str, content: str):
    if session_id not in conversation_history:
        conversation_history[session_id] = []

    conversation_history[session_id].append({
        "role": role,
        "content": content
    })


def get_history(session_id: str):
    return conversation_history.get(session_id, [])