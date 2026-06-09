from datasets import load_dataset
import json
import os

print("Loading Spider schemas...")

# Dataset elli 3andou el schemas mta3 kol database
schemas_dataset = load_dataset("richardr1126/spider-schema")
print(schemas_dataset)
print("\nFirst example:")
print(schemas_dataset["train"][0])