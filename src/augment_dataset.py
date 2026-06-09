import json
import requests
import time
from tqdm import tqdm

def generate_paraphrases(question, num=3):
    prompt = f"""Generate {num} different ways to ask the same question in English.
Return ONLY the paraphrases, one per line, no numbering, no explanation.

Original question: {question}

Paraphrases:"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7}
            },
            timeout=30
        )
        if response.status_code == 200:
            text = response.json()["response"].strip()
            paraphrases = [
                p.strip() for p in text.split("\n")
                if p.strip() 
                and len(p.strip()) > 10
                and not p.strip().lower().startswith("here")
                and not p.strip().lower().startswith("note")
                and ":" not in p.strip()[:20]
            ]
            return paraphrases[:num]
    except:
        pass
    return []

print("Loading normalized data...")
with open("data/processed/train_normalized.json", "r") as f:
    data = json.load(f)

SAMPLE = 3000
sample_data = data[:SAMPLE]

print(f"Generating paraphrases for {SAMPLE} examples...")

augmented = []
for i, ex in enumerate(tqdm(sample_data)):
    # Garder original
    augmented.append(ex)
    
    # Générer paraphrases
    paraphrases = generate_paraphrases(ex["question"], num=3)
    for p in paraphrases:
        augmented.append({
            "db_id": ex["db_id"],
            "schema": ex["schema"],
            "question": p,
            "sql": ex["sql"]
        })
    
    time.sleep(0.2)
    
    # Save checkpoint kol 100 examples
    if (i + 1) % 100 == 0:
        with open("data/augmented/train_augmented_checkpoint.json", "w") as f:
            json.dump(augmented, f)
        print(f"Checkpoint saved: {i+1} examples processed, {len(augmented)} total")

print(f"\nOriginal:  {SAMPLE} examples")
print(f"Augmented: {len(augmented)} examples")
print(f"Ratio:     {len(augmented)/SAMPLE:.1f}x")

with open("data/augmented/train_augmented_sample.json", "w") as f:
    json.dump(augmented, f, indent=2)

print("Saved to data/augmented/train_augmented_sample.json")