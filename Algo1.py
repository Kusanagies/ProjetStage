import pandas as pd
import os
import time  # ⏱️ for measuring execution time

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

    results.sort(key=lambda x: (x[1] if isinstance(x[1], float) else -1), reverse=True)
    return pd.DataFrame(results, columns=["File", "Similarity"])

# === USER INPUT ===
query_file = input("📥 Enter the path to your input CSV file: ").strip()
folder = input("📁 Enter the path to the folder containing benchmark CSVs: ").strip()

# === TIMED EXECUTION ===
if os.path.isfile(query_file) and os.path.isdir(folder):
    start_time = time.time()
    similarities_df = compare_all_csvs(query_file, folder)
    end_time = time.time()
    duration = end_time - start_time

    print("\n🔍 Similarity Results:\n")
    print(similarities_df)
    print(f"\n⏱️ Comparison completed in {duration:.2f} seconds.")
else:
    print("❌ Invalid file or folder path. Please check your input.")
