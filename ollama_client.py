import requests

OLLAMA_URL = "http://localhost:11434/api"

def get_embedding(text):
    """Asks Ollama to convert text to math."""
    response = requests.post(f"{OLLAMA_URL}/embeddings", json={
        "model": "nomic-embed-text",
        "prompt": text
    })
    return response.json()["embedding"]

def chat_with_model(messages):
    """Sends the chat to Qwen and gets the response."""
    response = requests.post(f"{OLLAMA_URL}/chat", json={
        "model": "qwen2.5:1.5b",
        "messages": messages,
        "stream": False
    })
    return response.json()["message"]["content"]