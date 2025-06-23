import os
import requests
import zipfile
import shutil
from datetime import datetime

# Execute this file in order to update the folders for ipl, psl, and mens international matches using data directly from cricheet.org
# Downloads a .zip file and unpacks it, following up by deleting the old folder
# Also updates registry data in names.csv and people.csv
# Creates log entry with recent most date on which data was synced with cricsheet.org



# === URLs ===
urls = {
    "tests": "https://cricsheet.org/downloads/tests_json.zip",
    "odis": "https://cricsheet.org/downloads/odis_json.zip",
    "t20s": "https://cricsheet.org/downloads/t20s_json.zip",
    "ipl": "https://cricsheet.org/downloads/ipl_json.zip",
    "psl": "https://cricsheet.org/downloads/psl_male_json.zip",
}

# === CSV Files ===
registry = {
    "names.csv": "https://cricsheet.org/register/names.csv",
    "people.csv": "https://cricsheet.org/register/people.csv"
}

# === Subfolder for CSVs and README ===
meta_folder = "metadata"
os.makedirs(meta_folder, exist_ok=True)

# === Process each competition ===
for name, url in urls.items():
    zip_name = f"{name}.zip"
    extract_folder = f"{name}_data"

    # Remove old extracted folder
    if os.path.exists(extract_folder):
        print(f"Removing old data folder: {extract_folder}")
        shutil.rmtree(extract_folder)

    # Download new zip
    print(f"Downloading {name} from {url} ...")
    response = requests.get(url)
    with open(zip_name, "wb") as f:
        f.write(response.content)
    print(f"Saved as {zip_name}")

    # Extract new zip
    with zipfile.ZipFile(zip_name, 'r') as zip_ref:
        zip_ref.extractall(extract_folder)
    print(f"Extracted to '{extract_folder}' ✅\n")

    # Delete zip after extraction
    os.remove(zip_name)
    print(f"Deleted zip: {zip_name}\n")

print("Match Data Updated")

print("\nUpdating player data...")

for name, url in registry.items():
    file_path = os.path.join(meta_folder, name)
    print(f"Downloading {name} from. {url}...")
    response = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(response.content)
    print(f"Saved {name} ✅")

print("\nAll matches and registry data up to data.")
print("\n=========================================")


# === Create/Update README ===
readme_file = os.path.join(meta_folder, "README.md")
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_line = f"- Data updated on: {now}\n"

# If README exists, append to it; otherwise, create it with a heading
if os.path.exists(readme_file):
    with open(readme_file, "a") as f:
        f.write(log_line)
else:
    with open(readme_file, "w") as f:
        f.write("# Cricsheet Data Update Log\n\n")
        f.write(log_line)

print(f"\nLogged update to {readme_file} ✅")