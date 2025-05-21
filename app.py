from flask import Flask, request, render_template, send_file
import pandas as pd
from io import StringIO

app = Flask(__name__)

def merge_multiple_csvs(files):
    merged_df = pd.DataFrame()

    for file in files:
        try:
            df = pd.read_csv(file)
            df['source_file'] = file.filename  # Track origin
            merged_df = pd.concat([merged_df, df], ignore_index=True)
        except Exception as e:
            raise ValueError(f"Error reading {file.filename}: {str(e)}")

    return merged_df

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge_files():
    files = request.files.getlist('files')

    if not files or any(file.filename == '' for file in files):
        return "No files selected.", 400

    # Validate file extensions
    for file in files:
        if not file.filename.lower().endswith('.csv'):
            return f"Invalid file type: {file.filename}. Only .csv files are allowed.", 400

    try:
        df = merge_multiple_csvs(files)
    except ValueError as ve:
        return str(ve), 400

    output = StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    # Option 1: return HTML preview
    return f"<pre>{df.to_string()}</pre>"

    # Option 2: return downloadable CSV
    # return send_file(
    #     output,
    #     mimetype='text/csv',
    #     download_name='merged.csv',
    #     as_attachment=True
    # )

if __name__ == '__main__':
    app.run(debug=True)
