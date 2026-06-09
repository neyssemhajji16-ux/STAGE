import requests
import json
import os

os.makedirs("data/raw", exist_ok=True)

# WikiSQL available as parquet on HF
from datasets import load_dataset

wiki = load_dataset("parquet", data_files={
    "train": "hf://datasets/wikisql/train-00000-of-00001.parquet",
    "validation": "hf://datasets/wikisql/validation-00000-of-00001.parquet",
    "test": "hf://datasets/wikisql/test-00000-of-00001.parquet"
})

print(f"Train: {len(wiki['train'])}")
print(f"First example: {wiki['train'][0]}")