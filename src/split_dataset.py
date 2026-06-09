import json
import random

print("Loading normalized data...")
with open("data/processed/train_normalized.json", "r") as f:
    data = json.load(f)

print(f"Total examples: {len(data)}")

random.seed(42)
random.shuffle(data)

n = len(data)
train_end = int(n * 0.8)
val_end   = int(n * 0.9)

train = data[:train_end]
val   = data[train_end:val_end]
test  = data[val_end:]

print(f"Train:      {len(train)} examples (80%)")
print(f"Validation: {len(val)}   examples (10%)")
print(f"Test:       {len(test)}  examples (10%)")

with open("data/processed/train_final.json", "w") as f:
    json.dump(train, f, indent=2)
with open("data/processed/val_final.json", "w") as f:
    json.dump(val, f, indent=2)
with open("data/processed/test_final.json", "w") as f:
    json.dump(test, f, indent=2)

print("\n✅ Stage 1 COMPLETE — data/processed/")