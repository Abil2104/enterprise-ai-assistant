from backend.database.database import save_message, get_messages


def add_message(session_id: str, role: str, content: str):
    save_message(session_id, role, content)


def get_history(session_id: str):
    return get_messages(session_id)