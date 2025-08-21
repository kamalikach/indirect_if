import json
import requests
import argparse
from utils import *

OLLAMA_URL = "http://localhost:11434/v1/completions"

def get_model_outputs(model, url, dataset):
    result = []
    for example in dataset:
        prompt = example['instruction']
        print('** Prompt: **' + prompt)
        response = query_ollama(model, prompt, url)
        result.append({'response': response})
        d = { 'response': response }
        print(d)
    return result

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Process input, output, and model parameters.")
    parser.add_argument("--input", required=True, help="Path to the input file")
    parser.add_argument("--output", required=True, help="Path to the output file")
    parser.add_argument("--model", required=True, help="Model name or path")

    args = parser.parse_args()

    # Access arguments
    input_path = args.input
    output_path = args.output
    model_name = args.model

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = get_model_outputs(model_name, OLLAMA_URL, data)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()

