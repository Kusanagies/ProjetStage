import pandas as pd

# Load the CSV
df = pd.read_csv("mock_database_tables.csv")

# Group rows by the table name
tables = {name: group.drop(columns="__table__") for name, group in df.groupby("__table__")}

# Import the similarity function
from difflib import SequenceMatcher
import unicodedata
import re

def normalize_column_name(name):
    name = name.lower()
    name = unicodedata.normalize('NFD', name)
    name = name.encode('ascii', 'ignore').decode('utf-8')
    name = re.sub(r'\W+', ' ', name).strip()
    return name

def calculate_column_similarity(query_table: pd.DataFrame, candidate_table: pd.DataFrame) -> float:
    query_columns = set(normalize_column_name(col) for col in query_table.columns)
    candidate_columns = set(normalize_column_name(col) for col in candidate_table.columns)
    overlap = len(query_columns & candidate_columns)
    denominator = min(len(query_columns), len(candidate_columns))
    return overlap / denominator if denominator > 0 else 0.0

# Run pairwise similarity comparison
results = []
for t1_name, t1_df in tables.items():
    for t2_name, t2_df in tables.items():
        if t1_name != t2_name:
            sim = calculate_column_similarity(t1_df, t2_df)
            results.append((t1_name, t2_name, round(sim, 2)))

# Display results
results_df = pd.DataFrame(results, columns=["Table A", "Table B", "Similarity"])
print(results_df.sort_values(by="Similarity", ascending=False).head(10))
