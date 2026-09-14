import requests


OLLAMA_URL = "http://localhost:11434/api/chat"
DEFAULT_MODEL = "qwen3.5:9b"


def ask_model(prompt, model=DEFAULT_MODEL, timeout=600):
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "options": {
            "num_predict": 250
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=timeout
    )

    response.raise_for_status()

    data = response.json()

    print("\n--- Ollama Performance ---")
    print(f"Prompt tokens: {data.get('prompt_eval_count')}")
    print(f"Output tokens: {data.get('eval_count')}")

    if data.get("eval_duration"):
        tokens_per_second = (
            data["eval_count"] /
            (data["eval_duration"] / 1_000_000_000)
        )
        print(f"Generation speed: {tokens_per_second:.2f} tokens/sec")

    return data["message"]["content"]
