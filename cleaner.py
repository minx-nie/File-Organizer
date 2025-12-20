"""
Project: Dọn dẹp máy tính (File Organizer)
Author: Minx-nie
"""

import os
import shutil
import logging
import argparse
import json
import mimetypes
from datetime import datetime

# ================= CONSTANTS =================

LOG_FILE = "file_organizer.log"
CONFIG_FILE = "categories.json"
HISTORY_FILE = "move_history.json"

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

# ================= ARGUMENTS =================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Recursive file organizer with dry-run, config, summary, and rollback"
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
    parser.add_argument(
        "--rollback",
        metavar="TIMESTAMP",
        help="Rollback last run or a specific timestamp"
    )
    return parser.parse_args()


# ================= CONFIG =================

def load_categories(config_path=CONFIG_FILE):
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to load {config_path}, using defaults: {e}")
            logging.warning(f"Invalid config file: {e}")
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

def get_category(extension, categories, filepath=None):
    extension = extension.lower()
    for category, exts in categories.items():
        if extension in exts:
            return category

    if filepath:
        mime_type, _ = mimetypes.guess_type(filepath)
        if mime_type:
            if mime_type.startswith("image/"):
                return "Images"
            elif mime_type.startswith("video/"):
                return "Videos"
            elif mime_type.startswith("audio/"):
                return "Music"
            elif mime_type in ("application/pdf", "application/msword",
                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                               "application/vnd.ms-excel",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                               "text/plain"):
                return "Documents"
            elif mime_type in ("application/zip", "application/x-rar-compressed",
                               "application/x-7z-compressed", "application/gzip"):
                return "Archives"
            elif mime_type in ("application/x-msdownload", "application/x-ms-installer"):
                return "Installers"
            elif mime_type.startswith("text/"):
                return "Code"
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

# ================= HISTORY =================

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_history_entry(moves):
    history = load_history()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    history.append({"timestamp": timestamp, "moves": moves})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

# ================= ROLLBACK =================

def rollback(timestamp=None):
    history = load_history()
    if not history:
        print("⚠️ No history available for rollback.")
        return

    if timestamp:
        entry = next((h for h in history if h["timestamp"] == timestamp), None)
        if not entry:
            print(f"⚠️ No rollback entry found for timestamp: {timestamp}")
            return
        moves_to_rollback = entry["moves"]
    else:
        moves_to_rollback = history[-1]["moves"]

    restored = 0
    for move in reversed(moves_to_rollback):
        dst = move["dst"]
        src = move["src"]
        if os.path.exists(dst):
            os.makedirs(os.path.dirname(src), exist_ok=True)
            shutil.move(dst, src)
            restored += 1

    print(f"✔ Rollback complete. {restored} files restored.")

    if timestamp:
        history = [h for h in history if h["timestamp"] != timestamp]
    else:
        history.pop()

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

# ================= MAIN LOGIC =================

def clean_folder(folder_to_clean, dry_run):
    if not os.path.isdir(folder_to_clean):
        print(f"❌ Folder not found: {folder_to_clean}")
        return

    categories = load_categories()
    history = []

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
            if filename in [os.path.basename(__file__), LOG_FILE, HISTORY_FILE]:
                continue

            _, extension = os.path.splitext(filename)

            category = get_category(extension, categories, filepath=original_path)
            summary["total"] += 1
            summary["by_category"].setdefault(category, 0)
            summary["by_category"][category] += 1

            target_folder = os.path.join(folder_to_clean, category)
            if not os.path.exists(target_folder) and not dry_run:
                os.makedirs(target_folder)

            new_filename = (
                get_unique_filename(target_folder, filename)
                if os.path.exists(os.path.join(target_folder, filename))
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
                history.append({"src": original_path, "dst": destination_path})

    if not dry_run and history:
        save_history_entry(history)

    print_summary(summary, dry_run)

# ================= ENTRY POINT =================

if __name__ == "__main__":
    args = parse_arguments()
    if args.rollback:
        rollback()
    else:
        clean_folder(args.path, args.dry_run)
