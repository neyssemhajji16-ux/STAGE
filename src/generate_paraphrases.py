import json
import requests
import time

def generate_paraphrases(question, num=3):
    """Génère paraphrases via Ollama LLaMA 3.2"""
    prompt = f"""Generate {num} different ways to ask the same question in English.
Return ONLY the paraphrases, one per line, no numbering, no explanation.

Original question: {question}

Paraphrases:"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7}
        }
    )
    
    if response.status_code == 200:
        text = response.json()["response"].strip()
        paraphrases = [p.strip() for p in text.split("\n") 
                      if p.strip() and len(p.strip()) > 5]
        return paraphrases[:num]
    return []

# Test sur 5 examples d'abord
print("Loading normalized data...")
with open("data/processed/train_normalized.json", "r") as f:
    data = json.load(f)

print("Testing paraphrases on 5 examples...")
for i in range(5):
    ex = data[i]
    print(f"\nOriginal: {ex['question']}")
    paraphrases = generate_paraphrases(ex["question"], num=3)
    for p in paraphrases:
        print(f"  → {p}")
    time.sleep(0.5)