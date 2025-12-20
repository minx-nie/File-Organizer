"""
Project: Dọn dẹp máy tính (File Organizer)
Author: Minx-nie
"""

import os
import shutil
import logging
import argparse
import json

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

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Recursive file organizer with dry-run, config and summary report"
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

def load_categories(config_path=CONFIG_FILE):
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logging.warning(f"Invalid config file: {e}")
    return DEFAULT_CATEGORIES

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

def print_summary(summary, dry_run):
    print("\n" + "=" * 40)
    print("📊 SUMMARY REPORT")
    print("=" * 40)
    print(f"Mode        : {'DRY RUN' if dry_run else 'REAL RUN'}")
    print(f"Total files : {summary['total']}")
    print(f"Moved files : {summary['moved']}")
    print(f"Renamed     : {summary['renamed']}")
    print("\nBy category:")
    for category, count in summary["by_category"].items():
        print(f"  - {category}: {count}")
    print("=" * 40)

def clean_folder(folder_to_clean, dry_run):
    if not os.path.isdir(folder_to_clean):
        print(f"❌ Folder not found: {folder_to_clean}")
        return

    categories = load_categories()

    summary = {
        "total": 0,
        "moved": 0,
        "renamed": 0,
        "by_category": {}
    }

    if dry_run:
        print("=" * 60)
        print("⚠️  DRY RUN MODE ENABLED - NO FILES WILL BE MOVED")
        print("=" * 60)

    for root, _, files in os.walk(folder_to_clean):
        relative_path = os.path.relpath(root, folder_to_clean)
        if relative_path.split(os.sep)[0] in categories:
            continue

        for filename in files:
            if filename.startswith("."):
                continue

            original_path = os.path.join(root, filename)
            if filename in [os.path.basename(__file__), LOG_FILE]:
                continue

            _, extension = os.path.splitext(filename)
            extension = extension.lower()

            category = get_category(extension, categories)
            summary["total"] += 1
            summary["by_category"].setdefault(category, 0)
            summary["by_category"][category] += 1

            target_folder = os.path.join(folder_to_clean, category)
            if not os.path.exists(target_folder) and not dry_run:
                os.makedirs(target_folder)

            new_filename = (
                get_unique_filename(target_folder, filename)
                if os.path.exists(target_folder)
                else filename
            )

            if new_filename != filename:
                summary["renamed"] += 1

            destination_path = os.path.join(target_folder, new_filename)

            if dry_run:
                print(f"[DRY RUN] {original_path} -> {category}/{new_filename}")
            else:
                shutil.move(original_path, destination_path)
                summary["moved"] += 1

    print_summary(summary, dry_run)

if __name__ == "__main__":
    args = parse_arguments()
    clean_folder(args.path, args.dry_run)
