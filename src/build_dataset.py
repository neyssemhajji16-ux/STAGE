import json
from datasets import load_dataset

print("Loading data...")
train_dataset = load_dataset("xlangai/spider", split="train")
schemas_dataset = load_dataset("richardr1126/spider-schema", split="train")

# Créer dict: db_id → schema
schemas = {ex["db_id"]: ex["Schema (values (type))"] for ex in schemas_dataset}

print(f"Schemas loaded: {len(schemas)}")

# Merger
merged = []
skipped = 0
for ex in train_dataset:
    db_id = ex["db_id"]
    if db_id in schemas:
        merged.append({
            "db_id": db_id,
            "schema": schemas[db_id],
            "question": ex["question"],
            "sql": ex["query"]
        })
    else:
        skipped += 1

print(f"Merged examples: {len(merged)}")
print(f"Skipped (no schema): {skipped}")
print("\nFirst example:")
print(json.dumps(merged[0], indent=2))

# Sauvegardi
with open("data/processed/train_merged.json", "w") as f:
    json.dump(merged, f, indent=2)

print("\nSaved to data/processed/train_merged.json")