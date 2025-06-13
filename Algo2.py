import pandas as pd
import os

def calculate_value_similarity(query_table, candidate_table, sample_size=100):
    query_values = set()
    for column in query_table.select_dtypes(include=['object']).columns:
        values = query_table[column].dropna().unique()
        query_values.update(values[:sample_size])

    candidate_values = set()
    for column in candidate_table.select_dtypes(include=['object']).columns:
        values = candidate_table[column].dropna().unique()
        candidate_values.update(values[:sample_size])

    overlap = len(query_values.intersection(candidate_values))
    denominator = min(len(query_values), len(candidate_values))

    if denominator == 0:
        return 0
    return overlap / denominator

def compare_value_similarity_all_csvs(query_path, folder_path, sample_size=100, limit=200):
    query_table = pd.read_csv(query_path)
    results = []

    all_csvs = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    for filename in all_csvs[:limit]:
        filepath = os.path.join(folder_path, filename)
        try:
            candidate_table = pd.read_csv(filepath)
            similarity = calculate_value_similarity(query_table, candidate_table, sample_size)
            results.append((filename, similarity))
        except Exception as e:
            results.append((filename, f"Error: {e}"))

    results.sort(key=lambda x: (x[1] if isinstance(x[1], float) else -1), reverse=True)
    return pd.DataFrame(results, columns=["File", "Value Similarity"])
