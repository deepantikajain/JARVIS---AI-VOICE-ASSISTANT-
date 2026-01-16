import requests

def aiProcess(command):
    prompt = f"You are Jarvis, a helpful assistant. Answer simply.\nQuestion: {command}\nAnswer:"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]
