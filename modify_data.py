import json
import requests

OLLAMA_URL = "http://localhost:11434/v1/completions"  # Ollama API endpoint
MODEL_NAME = "gpt-oss:20b"  # Replace with your model name
MODIFICATION_PROMPT = "Rephrase the following instruction to make it indirect. Return only the answer: "

output_file = "alpaca_eval_modified.json"

def query_ollama(model, prompt, max_tokens=1000):
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
        response = requests.post(OLLAMA_URL, json=payload)
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to connect to Ollama server: {e}")

    if response.status_code != 200:
        raise RuntimeError(f"Ollama server returned {response.status_code}: {response.text}")

    try:
        data = response.json()
        return data.get("choices", [{}])[0].get("text", "")
    except ValueError:
        raise RuntimeError(f"Invalid JSON response from Ollama: {response.text}")



with open("alpaca_eval.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for example in data:
    original_instruction = example['instruction']
    print('***Original:***' + original_instruction)
    
    modified_instruction = query_ollama(MODEL_NAME, MODIFICATION_PROMPT + ' : '+ original_instruction)
    print('***Modified:***' + modified_instruction)

    example['instruction'] = modified_instruction

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

