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
import sys

# ================= CONSTANTS =================

LOG_FILE = "file_organizer.log"
CONFIG_FILE = "categories.json"
HISTORY_FILE = "move_history.json"

IGNORED_DIRS = {'.git', '.idea', '.vscode', '__pycache__', 'node_modules', 'venv', 'env', '.svn', 'AppData'}

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
    parser.add_argument("path", nargs="?", default=os.path.join(os.path.expanduser("~"), "Downloads"),
                        help="Folder to clean (default: ~/Downloads)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without moving files")
    parser.add_argument("--rollback", nargs="?", const="LATEST", default=None,
                        help="Undo a previous file organization (default: latest). Provide timestamp to rollback specific entry.")
    parser.add_argument("--confirm", action="store_true", help="Confirm before executing the move")
    parser.add_argument("--list-history", action="store_true", help="List available rollback history")
    return parser.parse_args()


# ================= CONFIG =================

def validate_categories(categories):
    valid = {}
    for cat, exts in categories.items():
        if not isinstance(cat, str) or not cat.strip():
            logging.warning(f"Invalid category name: {cat}")
            continue
        valid_exts = []
        if isinstance(exts, list):
            for ext in exts:
                if isinstance(ext, str) and ext.startswith("."):
                    valid_exts.append(ext.lower())
                else:
                    logging.warning(f"Invalid extension '{ext}' in category '{cat}'")
        if valid_exts:
            valid[cat] = valid_exts
        else:
            logging.warning(f"No valid extensions for category '{cat}', skipping")
    return valid if valid else DEFAULT_CATEGORIES

def load_categories(config_path=CONFIG_FILE):
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict) or not all(isinstance(v, list) for v in data.values()):
                raise ValueError("Invalid structure, should be a dict of lists.")
            return validate_categories(data)
        except Exception as e:
            print(f"[!] Failed to load {config_path}, using defaults: {e}")
            logging.warning(f"Invalid config file: {e}")
    return DEFAULT_CATEGORIES


# ================= HELPERS =================

def get_unique_filename(folder, filename,max_attempts=1000):
    name, ext = os.path.splitext(filename)
    counter = 1
    new_name = filename
    while os.path.exists(os.path.join(folder, new_name)) and counter <= max_attempts:
        new_name = f"{name} ({counter}){ext}"
        counter += 1
    if counter > max_attempts:
        raise Exception(f"[!] Cannot create unique filename for {filename} in {folder}")
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

def remove_empty_folders(path, dry_run=False):
    if not os.path.isdir(path):
        return
    for root, dirs, files in os.walk(path, topdown=False):
        if root == path: continue
        if os.path.basename(root) in IGNORED_DIRS:
            continue

        try:
            if not os.listdir(root):
                if dry_run:
                    print(f"[DRY RUN] Would remove empty folder: {root}")
                    logging.info(f"[DRY RUN] Would remove empty folder: {root}")
                else:
                    os.rmdir(root)
                    logging.info(f"Removed empty folder: {root}")
        except Exception as e:
            logging.warning(f"Cannot remove folder {root}: {e}")

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


def save_history_entry(root_folder, moves):
    history = load_history()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    history.append({
        "timestamp": timestamp,
        "root": root_folder,
        "moves": moves})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def list_history():
    history = load_history()
    if not history:
        print("[!] No history available.")
        return
    
    print("\n Available rollback history:")
    print("-" * 40)
    for entry in history:
        ts = entry.get("timestamp")
        count = len(entry.get("moves", []))
        print(f" - {ts} ({count} files)")
    print("-" * 40)


# ================= ROLLBACK =================

def rollback(timestamp=None):
    history = load_history()
    if not history:
        print("[!] No history available for rollback.")
        return

    if timestamp and timestamp != "LATEST":
        entry = next((h for h in history if h["timestamp"] == timestamp), None)
        if not entry:
            print(f"[!] No rollback entry found for timestamp: {timestamp}")
            return
        moves_to_rollback = entry["moves"]
    else:
        entry = history[-1]
        timestamp = entry["timestamp"]
        print(f"[*] Rolling back latest session: {timestamp}")
        moves_to_rollback = entry["moves"]

    restored = 0
    for move in reversed(moves_to_rollback):
        dst = move["dst"]
        src = move["src"]
        if os.path.exists(dst):
            os.makedirs(os.path.dirname(src), exist_ok=True)
            if os.path.exists(src):
                new_src = get_unique_filename(os.path.dirname(src), os.path.basename(src))
                msg = f"[!] Rollback rename: {os.path.basename(src)} -> {os.path.basename(new_src)}"
                print(msg)
                logging.warning(msg)
                src = new_src
            try:    
                shutil.move(dst, src)
                restored += 1
            except Exception as e:
                print(f"[X] Failed to restore {dst}: {e}")

    print(f"✔ Rollback complete. {restored} files restored.")

    if timestamp:
        history = [h for h in history if h["timestamp"] != timestamp]
    else:
        history.pop()

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


# ================= MAIN LOGIC =================

def clean_folder(folder_to_clean, dry_run, confirm):
    abs_path = os.path.abspath(folder_to_clean)
    root_paths = {os.path.abspath(os.sep)}
    if os.name == 'nt':
        root_paths.add(os.path.abspath("C:\\"))
        root_paths.add(os.path.abspath("C:/"))

    if abs_path in root_paths:
        print(f"[X] REFUSING to run on system root directory: {abs_path}")
        print(" Please choose a specific folder (e.g., Downloads)")
        return
    
    if not os.path.isdir(folder_to_clean):
        print(f"[X] Folder not found: {folder_to_clean}")
        return
    if not dry_run and not confirm:
        print("[!] Real run detected. Use --confirm to proceed.")
        return
    
    categories = load_categories()
    history = []

    summary = {
        "total_scanned": 0,
        "moved": 0,
        "renamed": 0,
        "by_category": {}
    }

    if dry_run:
        print("=" * 60)
        print("[!]  DRY RUN MODE ENABLED - NO FILES WILL BE MOVED")
        print("=" * 60)

    current_script = os.path.basename(sys.argv[0])
    target_category_folders = {os.path.join(folder_to_clean, c) for c in categories}

    for root, dirs, files in os.walk(folder_to_clean):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        if any(os.path.samefile(root, skip) for skip in target_category_folders if os.path.exists(skip)):
            continue
        
        for filename in files:
            if filename.startswith("."):  continue

            original_path = os.path.join(root, filename)
            if filename in [current_script, LOG_FILE, HISTORY_FILE, CONFIG_FILE]:
                continue

            summary["total_scanned"] += 1

            _, extension = os.path.splitext(filename)
            category = get_category(extension, categories, filepath=original_path)
            target_folder = os.path.join(folder_to_clean, category)
            
            if os.path.dirname(original_path) == target_folder:
                continue

            summary["by_category"].setdefault(category, 0)
            summary["by_category"][category] += 1

            target_folder = os.path.join(folder_to_clean, category)
           
            if not os.path.exists(target_folder) and not dry_run:
                os.makedirs(target_folder)

            if os.path.exists(os.path.join(target_folder, filename)):
                new_filename = get_unique_filename(target_folder, filename)
                if dry_run:
                    msg = f"[DRY RUN] Rename conflict: {filename} -> {new_filename}"
                    print(msg)
                    logging.warning(msg)
            else:
                new_filename = filename

            if new_filename != filename and not dry_run:
                summary["renamed"] += 1
                logging.warning(f"Renamed {filename} -> {new_filename}")

            destination_path = os.path.join(target_folder, new_filename)

            if dry_run:
                logging.info(f"[DRY RUN] {original_path} -> {destination_path}")
            else:
                try:
                    shutil.move(original_path, destination_path)
                    summary["moved"] += 1
                    history.append({"src": original_path, "dst": destination_path})
                    logging.info(f"Moved {original_path} -> {destination_path}")
                except Exception as e:
                    logging.error(f"Failed to move {original_path}: {e}")

    if not dry_run:
        if history:
            save_history_entry(folder_to_clean, history)
        print("Cleaning up empty folders...")
        remove_empty_folders(folder_to_clean)

    print_summary(summary, dry_run)


# ================= ENTRY POINT =================

if __name__ == "__main__":
    args = parse_arguments()

    if args.list_history:
        list_history()
    elif args.rollback is not None:
        rollback(args.rollback)
    else:
        clean_folder(args.path, args.dry_run, args.confirm)
