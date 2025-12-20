"""
Project: Dọn dẹp máy tính (File Organizer)
Author: Minx-nie
"""

import os
import shutil
import logging
import argparse
import json

# ================= CONSTANTS =================

LOG_FILE = "file_organizer.log"
CONFIG_FILE = "categories.json"

DEFAULT_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Installers": [".exe", ".msi", ".dmg", ".iso"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Music": [".mp3", ".wav", ".flac"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".java", ".json", ".xml"]
}

# ================= LOGGING =================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# ================= ARGUMENT PARSER =================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Recursive file organizer with dry-run and JSON config support"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=os.path.join(os.path.expanduser("~"), "Downloads"),
        help="Folder to clean (default: ~/Downloads)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate actions without moving files"
    )
    return parser.parse_args()

# ================= CONFIG =================

def load_categories(config_path=CONFIG_FILE):
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                categories = json.load(f)
            print(f"✔ Loaded categories from {config_path}")
            return categories
        except Exception as e:
            print(f"⚠️ Failed to load {config_path}, using defaults: {e}")
            logging.warning(f"Invalid config file: {e}")

    print("ℹ️ Using default file categories")
    return DEFAULT_CATEGORIES

# ================= HELPERS =================

def get_unique_filename(folder, filename):
    name, ext = os.path.splitext(filename)
    counter = 1
    new_name = filename
    while os.path.exists(os.path.join(folder, new_name)):
        new_name = f"{name} ({counter}){ext}"
        counter += 1
    return new_name

def get_category(extension, categories):
    for category, extensions in categories.items():
        if extension in extensions:
            return category
    return "Others"

# ================= MAIN LOGIC =================

def clean_folder(folder_to_clean, dry_run):
    if not os.path.isdir(folder_to_clean):
        print(f"❌ Folder not found: {folder_to_clean}")
        logging.error(f"Folder not found: {folder_to_clean}")
        return

    categories = load_categories()

    print(f"\n--- Cleaning folder (recursive): {folder_to_clean} ---")
    if dry_run:
        print("=" * 60)
        print("⚠️  DRY RUN MODE ENABLED - NO FILES WILL BE MOVED")
        print("=" * 60)

    moved_count = 0

    for root, _, files in os.walk(folder_to_clean):
        # Skip category folders to avoid infinite loop
        relative_path = os.path.relpath(root, folder_to_clean)
        if relative_path.split(os.sep)[0] in categories:
            continue

        for filename in files:
            try:
                if filename.startswith("."):
                    continue

                original_path = os.path.join(root, filename)

                if filename in [os.path.basename(__file__), LOG_FILE]:
                    continue

                _, extension = os.path.splitext(filename)
                extension = extension.lower()

                category = get_category(extension, categories)
                target_folder = os.path.join(folder_to_clean, category)

                if not os.path.exists(target_folder) and not dry_run:
                    os.makedirs(target_folder)

                new_filename = (
                    get_unique_filename(target_folder, filename)
                    if os.path.exists(target_folder)
                    else filename
                )

                destination_path = os.path.join(target_folder, new_filename)

                if dry_run:
                    print(f"[DRY RUN] {original_path} -> {category}/{new_filename}")
                    logging.info(f"[DRY RUN] {original_path} -> {destination_path}")
                else:
                    shutil.move(original_path, destination_path)
                    print(f"✔ Moved: {original_path} -> {category}/{new_filename}")
                    logging.info(f"Moved: {original_path} -> {destination_path}")
                    moved_count += 1

            except Exception as e:
                print(f"⚠️ Error processing {filename}: {e}")
                logging.error(f"Error processing {filename}: {e}")

    print(f"\n--- Done! {moved_count} files processed. ---")

# ================= ENTRY POINT =================

if __name__ == "__main__":
    args = parse_arguments()
    clean_folder(args.path, args.dry_run)
