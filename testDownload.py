import requests
import os

API_URL = "https://www.data.gouv.fr/api/1/datasets/"
OUTPUT_DIR = "downloaded_csvs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

params = {
    'page_size': 100
}

response = requests.get(API_URL, params=params)
data = response.json()

downloaded = 0
max_downloads = 200

for idx, dataset in enumerate(data['data']):
    title = dataset['title']

    for resource in dataset['resources']:
        file_url = resource.get('url')
        format_type = resource.get('format', '').lower()

        if not file_url:
            continue

        if not (file_url.endswith('.csv') or format_type == 'csv'):
            continue

        safe_title = "".join(c for c in resource.get('title', 'resource') if c.isalnum() or c in (' ', '_', '-')).rstrip()
        filename = f"dataset_{downloaded+1}_{safe_title}.csv"
        filepath = os.path.join(OUTPUT_DIR, filename)

        try:
            r = requests.get(file_url)
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                f.write(r.content)
            print(f"✅ {filename} téléchargé depuis {file_url}")
            downloaded += 1
        except Exception as e:
            print(f"❌ Erreur pour {file_url}: {e}")

        if downloaded >= max_downloads:
            break
    if downloaded >= max_downloads:
        break
