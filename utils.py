import json
import requests

def query_ollama(model, prompt, url,  max_tokens=4096):
    """
    Query the Ollama server with proper error checking.
    Returns the completion text or raises an exception on error.
    """
    payload = {
        "model": model,
        "prompt": prompt,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(url, json=payload)
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to connect to Ollama server: {e}")

    if response.status_code != 200:
        raise RuntimeError(f"Ollama server returned {response.status_code}: {response.text}")

    try:
        data = response.json()
        return data.get("choices", [{}])[0].get("text", "")
    except ValueError:
        raise RuntimeError(f"Invalid JSON response from Ollama: {response.text}")

