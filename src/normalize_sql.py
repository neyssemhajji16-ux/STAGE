import json
import sqlparse
from sqlparse import tokens as T
from sqlparse.sql import Statement

def normalize_sql(sql):
    """
    Normalise el SQL query:
    - Keywords UPPERCASE
    - Identifiers lowercase  
    - Espaces propres
    - Supprime espaces doubles
    """
    try:
        # Parse
        parsed = sqlparse.parse(sql.strip())[0]
        
        normalized_tokens = []
        for token in parsed.flatten():
            val = token.value
            # Keywords → UPPERCASE
            if token.ttype in (T.Keyword, T.Keyword.DML, 
                               T.Keyword.DDL, T.Wildcard,
                               T.Comparison):
                normalized_tokens.append(val.upper())
            # Identifiers, Names → lowercase
            elif token.ttype in (T.Name, T.Literal.String.Single):
                normalized_tokens.append(val.lower())
            # Numbers → garder as-is
            elif token.ttype in (T.Number.Integer, T.Number.Float):
                normalized_tokens.append(val)
            # Punctuation → garder as-is
            else:
                normalized_tokens.append(val)
        
        # Join w clean espaces
        result = " ".join(normalized_tokens)
        # Supprime espaces doubles
        while "  " in result:
            result = result.replace("  ", " ")
        return result.strip()
    
    except Exception as e:
        return sql  # Si erreur, garder el original

# Load filtered data
print("Loading filtered data...")
with open("data/processed/train_filtered.json", "r") as f:
    data = json.load(f)

print(f"Examples to normalize: {len(data)}")

# Normalize
normalized = []
for ex in data:
    ex["sql"] = normalize_sql(ex["sql"])
    normalized.append(ex)

# Shuf avant/après
print("\n=== BEFORE / AFTER EXAMPLES ===")
for i in [0, 1, 2]:
    original_sql = data[i]["sql"]
    normalized_sql = normalized[i]["sql"]
    print(f"\nExample {i+1}:")
    print(f"  Question:   {data[i]['question']}")
    print(f"  Normalized: {normalized_sql}")

# Sauvegardi
with open("data/processed/train_normalized.json", "w") as f:
    json.dump(normalized, f, indent=2)

print(f"\nSaved to data/processed/train_normalized.json")
print(f"Total: {len(normalized)} examples")