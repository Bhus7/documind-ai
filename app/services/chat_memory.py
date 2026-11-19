
from app.db.redis import redis_client


def save_message(
    session_id: str,
    role: str,
    content: str
) -> None:

    key = f"chat:{session_id}"

    redis_client.rpush(
        key,
        f"{role}|{content}"
    )


def get_chat_history(session_id: str) -> list[str]:

    key = f"chat:{session_id}"

    return redis_client.lrange(key, 0, -1)


def save_booking_status(
    session_id: str,
    booking_id: int
) -> None:

    key = f"booking_completed:{session_id}"

    redis_client.set(key, booking_id)


def get_booking_status(session_id: str) -> str | None:

    key = f"booking_completed:{session_id}"

    return redis_client.get(key)
