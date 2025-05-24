import pandas as pd
import os

def calculate_column_similarity(query_table, candidate_table):
    query_columns = set(query_table.columns)
    candidate_columns = set(candidate_table.columns)
    
    overlap = len(query_columns.intersection(candidate_columns))
    denominator = min(len(query_columns), len(candidate_columns))
    
    if denominator == 0:
        return 0
    return overlap / denominator

def compare_all_csvs(query_path, folder_path):
    query_table = pd.read_csv(query_path)
    results = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".csv") and filename != os.path.basename(query_path):
            filepath = os.path.join(folder_path, filename)
            try:
                candidate_table = pd.read_csv(filepath)
                similarity = calculate_column_similarity(query_table, candidate_table)
                results.append((filename, similarity))
            except Exception as e:
                results.append((filename, f"Error: {e}"))

    # Sort by highest similarity
    results.sort(key=lambda x: (x[1] if isinstance(x[1], float) else -1), reverse=True)

    return pd.DataFrame(results, columns=["File", "Similarity"])

# === USAGE EXAMPLE ===
query_file = "base/1.csv"     # your reference CSV
folder = "benchmark"                                 # the folder to scan
similarities_df = compare_all_csvs(query_file, folder)

print(similarities_df)
