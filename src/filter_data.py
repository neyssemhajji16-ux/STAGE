import json
import sqlparse
from sqlparse.sql import Statement

def is_valid_sql(sql):
    """Vérifi belli el SQL parseable"""
    try:
        parsed = sqlparse.parse(sql)
        return len(parsed) > 0 and len(str(parsed[0]).strip()) > 0
    except:
        return False

def is_too_complex(sql):
    """Filtra queries trop complexes / ambiguës"""
    sql_upper = sql.upper()
    # Supprimer nested subqueries complexes
    if sql_upper.count('SELECT') > 2:
        return True
    # Supprimer queries trop longues
    if len(sql.split()) > 50:
        return True
    return False

def is_too_simple(sql):
    """Filtra queries trop simples (mch intéressantes lil training)"""
    sql_upper = sql.upper()
    tokens = sql.split()
    # Trop courte
    if len(tokens) < 4:
        return True
    return False

def is_vague_question(question):
    """Filtra questions vagues"""
    # Questions trop courtes
    if len(question.split()) < 3:
        return True
    return False

# Load data
print("Loading merged data...")
with open("data/processed/train_merged.json", "r") as f:
    data = json.load(f)

print(f"Before filtering: {len(data)} examples")

# Filtrage
filtered = []
stats = {
    "invalid_sql": 0,
    "too_complex": 0,
    "too_simple": 0,
    "vague_question": 0,
    "kept": 0
}

for ex in data:
    sql = ex["sql"]
    question = ex["question"]

    if not is_valid_sql(sql):
        stats["invalid_sql"] += 1
        continue

    if is_too_complex(sql):
        stats["too_complex"] += 1
        continue

    if is_too_simple(sql):
        stats["too_simple"] += 1
        continue

    if is_vague_question(question):
        stats["vague_question"] += 1
        continue

    filtered.append(ex)
    stats["kept"] += 1

# Results
print(f"\n=== FILTERING STATS ===")
print(f"Invalid SQL:      {stats['invalid_sql']}")
print(f"Too complex:      {stats['too_complex']}")
print(f"Too simple:       {stats['too_simple']}")
print(f"Vague question:   {stats['vague_question']}")
print(f"Kept:             {stats['kept']}")
print(f"Removed:          {len(data) - stats['kept']}")

# Sauvegardi
with open("data/processed/train_filtered.json", "w") as f:
    json.dump(filtered, f, indent=2)

print(f"\nSaved to data/processed/train_filtered.json")