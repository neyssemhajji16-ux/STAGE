from datasets import load_dataset
import os

print("Downloading Spider dataset...")
dataset = load_dataset("xlangai/spider")

os.makedirs("data/raw", exist_ok=True)

dataset["train"].to_json("data/raw/spider_train.json")
dataset["validation"].to_json("data/raw/spider_validation.json")

print(f"Train examples: {len(dataset['train'])}")
print(f"Validation examples: {len(dataset['validation'])}")
print("Done! Data saved to data/raw/")