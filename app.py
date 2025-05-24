from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'benchmark'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_csv():
    file = request.files.get('file')
    if not file or not file.filename.endswith('.csv'):
        return "❌ Only CSV files are allowed.", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return f"✅ File '{file.filename}' uploaded to /{UPLOAD_FOLDER}/"

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, render_template, redirect
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
BENCHMARK_FOLDER = 'benchmark'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def calculate_column_similarity(query_table, candidate_table):
    query_columns = set(query_table.columns)
    candidate_columns = set(candidate_table.columns)
    overlap = len(query_columns.intersection(candidate_columns))
    denominator = min(len(query_columns), len(candidate_columns))
    if denominator == 0:
        return 0
    return overlap / denominator

def compare_with_benchmark(uploaded_file_path):
    query_table = pd.read_csv(uploaded_file_path)
    results = []

    for filename in os.listdir(BENCHMARK_FOLDER):
        if filename.endswith(".csv"):
            try:
                benchmark_path = os.path.join(BENCHMARK_FOLDER, filename)
                candidate_table = pd.read_csv(benchmark_path)
                similarity = calculate_column_similarity(query_table, candidate_table)
                results.append((filename, similarity))
            except Exception as e:
                results.append((filename, f"Error: {e}"))

    # Sort descending by similarity
    results.sort(key=lambda x: (x[1] if isinstance(x[1], float) else -1), reverse=True)
    return results

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_csv():
    file = request.files.get('file')
    if not file or not file.filename.endswith('.csv'):
        return "❌ Only CSV files are allowed.", 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Run comparison
    results = compare_with_benchmark(filepath)

    # Display results
    html = f"<h2>✅ File '{file.filename}' uploaded and compared.</h2><table border='1'><tr><th>Benchmark File</th><th>Similarity</th></tr>"
    for filename, score in results:
        html += f"<tr><td>{filename}</td><td>{score}</td></tr>"
    html += "</table><br><a href='/'>🔙 Upload another file</a>"

    return html

if __name__ == '__main__':
    app.run(debug=True)
