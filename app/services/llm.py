
import ollama


def generate_answer(prompt: str) -> str:
    response = ollama.chat(
        model="llama3",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


def generate_chat_response(messages: list[dict[str, str]]) -> str:
    response = ollama.chat(
        model="llama3",
        messages=messages
    )

    return response["message"]["content"]
