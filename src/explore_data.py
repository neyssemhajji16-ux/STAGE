import json

# Load train data
with open("data/raw/spider_train.json", "r") as f:
    train = [json.loads(line) for line in f]

# Shuf awel example
print("=== FIRST EXAMPLE ===")
print(json.dumps(train[0], indent=2))

print(f"\n=== KEYS AVAILABLE ===")
print(list(train[0].keys()))
# Databases différentes
db_ids = set(ex["db_id"] for ex in train)
print(f"\nNombre de databases: {len(db_ids)}")
print(f"Exemples de db_ids: {list(db_ids)[:10]}")

# Longueur queries
lengths = [len(ex["query"].split()) for ex in train]
print(f"\nQuery length - Min: {min(lengths)}, Max: {max(lengths)}, Avg: {sum(lengths)//len(lengths)}")