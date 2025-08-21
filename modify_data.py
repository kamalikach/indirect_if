import json
import requests
from utils import *

OLLAMA_URL = "http://localhost:11434/v1/completions"  # Ollama API endpoint
MODEL_NAME = "gpt-oss:20b"  # Replace with your model name
MODIFICATION_PROMPT = "Rephrase the following instruction to make it indirect. Return only the answer: "

output_file = "alpaca_eval_modified.json"




with open("alpaca_eval.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for example in data:
    original_instruction = example['instruction']
    print('***Original:***' + original_instruction)
    
    modified_instruction = query_ollama(MODEL_NAME, MODIFICATION_PROMPT + ' : '+ original_instruction, OLLAMA_URL)
    print('***Modified:***' + modified_instruction)

    example['instruction'] = modified_instruction

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

