import os
import requests
from tqdm import tqdm
import pandas as pd

# Download folder
RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

# Metadata file
META_URL = "https://raw.githubusercontent.com/subpic/koniq10k-dataset/master/koniq10k_scores_and_distributions.csv"
META_FILE = "data/raw/koniq_meta.csv"

os.makedirs("data/raw", exist_ok=True)

if not os.path.exists(META_FILE):
    r = requests.get(META_URL)
    if r.status_code == 200:
        with open(META_FILE, "wb") as f:
            f.write(r.content)
        print(f"Downloaded metadata to {META_FILE}")
    else:
        raise ValueError(f"Failed to download metadata. Status code: {r.status_code}")

df = pd.read_csv(META_FILE)
print(df.head())

# Load metadata and choose subset
subset_df = df.sample(50, random_state=42)  # select 50 random images

BASE_URL = "http://database.mmsp-kn.de/koniq10k/1024x768/"
for img_name in tqdm(subset_df['image_name'], desc="Downloading images"):
    img_url = BASE_URL + img_name
    img_path = os.path.join(RAW_DIR, img_name)
    if not os.path.exists(img_path):
        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            with open(img_path, 'wb') as f:
                f.write(r.content)
