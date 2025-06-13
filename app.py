from flask import Flask, request, render_template
import os
import time
from Algo1 import compare_all_csvs
from Algo2 import compare_value_similarity_all_csvs

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
BENCHMARK_FOLDER = 'benchmark'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/about-algorithms')
def about_algorithms():
    return "<h2> À propos des algorithmes</h2><p>Algo1 compare les noms de colonnes, Algo2 compare les valeurs textuelles à l'intérieur des colonnes.</p>"

@app.route('/about-benchmark')
def about_benchmark():
    return render_template('about_benchmark.html')

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_csv():
    file = request.files.get('file')
    algorithm = request.form.get('algorithm')
    limit = request.form.get('limit', 200)

    # Sécurité : conversion avec fallback
    try:
        limit = int(limit)
        limit = max(1, min(limit, 1530))  # Clamp entre 1 et 1530
    except ValueError:
        limit = 200

    if not file or not file.filename.endswith('.csv'):
        return " Seulement les fichiers .csv sont autorisés", 400

    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # === Exécuter l'algorithme choisi
    start_time = time.time()

    if algorithm == 'algo2':
        df = compare_value_similarity_all_csvs(filepath, BENCHMARK_FOLDER, sample_size=100, limit=limit)
        results = df.values.tolist()
        algo_name = "Algorithme de similarité par valeur des colonnes"
    else:
        results = compare_all_csvs(filepath, BENCHMARK_FOLDER, limit=limit)
        algo_name = "Algorithme de similarité par nom de colonne"

    duration = round(time.time() - start_time, 2)

    return render_template(
        'result.html',
        filename=filename,
        results=results,
        duration=duration,
        algorithm=algo_name
    )

if __name__ == '__main__':
    app.run(debug=True)
