"""File Organizer CLI with dry-run, rollback, and rich summary output."""

from __future__ import annotations

import argparse
import json
import logging
import mimetypes
import os
import shutil
import sys
from dataclasses import dataclass, field
from datetime import datetime
from fnmatch import fnmatch
from pathlib import Path
from typing import Dict, Iterable, List, Optional

# ================= CONSTANTS =================

LOG_FILE = "file_organizer.log"
CONFIG_FILE = "categories.json"
HISTORY_FILE = "move_history.json"
AUTHOR_NAME = "Thanh Nguyen"
AUTHOR_EMAIL = "thanhnguyentuan2007@gmail.com"

IGNORED_DIRS = {'.git', '.idea', '.vscode', '__pycache__', 'node_modules', 'venv', 'env', '.svn', 'AppData'}

DEFAULT_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".md"],
    "Installers": [".exe", ".msi", ".dmg", ".iso"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Music": [".mp3", ".wav", ".flac"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".cpp", ".java", ".json", ".xml"]
}


@dataclass
class OrganizerSettings:
    root: Path
    dry_run: bool
    confirm: bool
    mode: str = "move"  # move | copy
    destination: Optional[Path] = None
    cleanup_empty: bool = True
    config_path: Path = Path(CONFIG_FILE)
    exclude_patterns: set[str] = field(default_factory=set)
    history_path: Path = Path(HISTORY_FILE)
    log_path: Path = Path(LOG_FILE)
    merge_defaults: bool = False
    include_hidden: bool = False
    max_depth: Optional[int] = None
    console_log: bool = False
    report_path: Optional[Path] = None


@dataclass
class RunSummary:
    total_scanned: int = 0
    moved: int = 0
    copied: int = 0
    renamed: int = 0
    skipped: int = 0
    by_category: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, object]:
        return {
            "total_scanned": self.total_scanned,
            "moved": self.moved,
            "copied": self.copied,
            "renamed": self.renamed,
            "skipped": self.skipped,
            "by_category": self.by_category,
        }

# ================= LOGGING =================

def configure_logging(log_path: Path, console: bool = False) -> None:
    handlers: List[logging.Handler] = [logging.FileHandler(log_path, encoding="utf-8")]
    if console:
        handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        handlers=handlers,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
        force=True,
    )

# ================= ARGUMENTS =================

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Recursive file organizer with dry-run, config, summary, and rollback"
    )
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path(os.path.expanduser("~")) / "Downloads",
        help="Folder to clean (default: ~/Downloads)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without moving files")
    parser.add_argument(
        "--rollback",
        nargs="?",
        const="LATEST",
        default=None,
        help="Undo a previous file organization (default: latest). Provide timestamp to rollback specific entry.",
    )
    parser.add_argument("--confirm", action="store_true", help="Confirm before executing the move")
    parser.add_argument("--list-history", action="store_true", help="List available rollback history")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path(CONFIG_FILE),
        help="Path to a custom categories config (JSON)",
    )
    parser.add_argument(
        "--destination",
        type=Path,
        help="Optional destination root for categorized folders (defaults to the source folder)",
    )
    parser.add_argument(
        "--merge-defaults",
        action="store_true",
        help="Merge custom config with built-in defaults instead of replacing them",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Glob pattern to exclude (can be provided multiple times)",
    )
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Skip removing empty folders after organizing",
    )
    parser.add_argument(
        "--mode",
        choices=["move", "copy"],
        default="move",
        help="Choose to move (default) or copy files into categories",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden files (dotfiles) during organization",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        help="Limit recursion depth when scanning (0 processes only the root folder)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Write summary report to the given JSON file",
    )
    parser.add_argument(
        "--console-log",
        action="store_true",
        help="Stream log output to console as well as the log file",
    )
    return parser.parse_args()


# ================= CONFIG =================

def validate_categories(categories: Dict[str, List[str]]) -> Dict[str, List[str]]:
    valid: Dict[str, List[str]] = {}
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


def merge_categories(base: Dict[str, List[str]], override: Dict[str, List[str]]) -> Dict[str, List[str]]:
    merged = {cat: exts[:] for cat, exts in base.items()}
    for cat, exts in override.items():
        merged.setdefault(cat, [])
        for ext in exts:
            if ext not in merged[cat]:
                merged[cat].append(ext)
    return merged


def load_categories(config_path: Path = Path(CONFIG_FILE), merge_defaults: bool = False) -> Dict[str, List[str]]:
    if config_path.exists():
        try:
            with config_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict) or not all(isinstance(v, list) for v in data.values()):
                raise ValueError("Invalid structure, should be a dict of lists.")
            custom = validate_categories(data)
            return merge_categories(DEFAULT_CATEGORIES, custom) if merge_defaults else custom
        except Exception as e:  # pylint: disable=broad-except
            print(f"[!] Failed to load {config_path}, using defaults: {e}")
            logging.warning(f"Invalid config file: {e}")
    return DEFAULT_CATEGORIES


# ================= HELPERS =================

def get_unique_filename(folder: Path, filename: str, max_attempts: int = 1000) -> str:
    name, ext = os.path.splitext(filename)
    counter = 1
    new_name = filename
    while (folder / new_name).exists() and counter <= max_attempts:
        new_name = f"{name} ({counter}){ext}"
        counter += 1
    if counter > max_attempts:
        raise RuntimeError(f"[!] Cannot create unique filename for {filename} in {folder}")
    return new_name


def get_category(extension: str, categories: Dict[str, List[str]], filepath: Optional[Path] = None) -> str:
    extension = extension.lower()
    for category, exts in categories.items():
        if extension in exts:
            return category

    if filepath:
        mime_type, _ = mimetypes.guess_type(str(filepath))
        if mime_type:
            if mime_type.startswith("image/"):
                return "Images"
            if mime_type.startswith("video/"):
                return "Videos"
            if mime_type.startswith("audio/"):
                return "Music"
            if mime_type in (
                "application/pdf",
                "application/msword",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "application/vnd.ms-excel",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "text/plain",
            ):
                return "Documents"
            if mime_type in (
                "application/zip",
                "application/x-rar-compressed",
                "application/x-7z-compressed",
                "application/gzip",
            ):
                return "Archives"
            if mime_type in ("application/x-msdownload", "application/x-ms-installer"):
                return "Installers"
            if mime_type.startswith("text/"):
                return "Code"
    return "Others"


def matches_exclude(path: Path, patterns: Iterable[str]) -> bool:
    return any(fnmatch(path.name, pattern) or fnmatch(str(path), pattern) for pattern in patterns)


def remove_empty_folders(path: Path, dry_run: bool = False) -> None:
    if not path.is_dir():
        return
    for root, dirs, files in os.walk(path, topdown=False):
        if Path(root) == path:
            continue
        if Path(root).name in IGNORED_DIRS:
            continue

        try:
            if not os.listdir(root):
                if dry_run:
                    print(f"[DRY RUN] Would remove empty folder: {root}")
                    logging.info(f"[DRY RUN] Would remove empty folder: {root}")
                else:
                    os.rmdir(root)
                    logging.info(f"Removed empty folder: {root}")
        except Exception as e:  # pylint: disable=broad-except
            logging.warning(f"Cannot remove folder {root}: {e}")


def print_summary(
    summary: RunSummary,
    dry_run: bool,
    report_path: Optional[Path] = None,
    meta: Optional[Dict[str, str]] = None,
) -> None:
    print("\n" + "=" * 40)
    print("📊 SUMMARY REPORT")
    print("=" * 40)
    if meta:
        for key, value in meta.items():
            print(f"{key:<12}: {value}")
    print(f"Mode        : {'DRY RUN' if dry_run else 'REAL RUN'}")
    print(f"Total files : {summary.total_scanned}")
    print(f"Moved files : {summary.moved}")
    print(f"Copied      : {summary.copied}")
    print(f"Renamed     : {summary.renamed}")
    print(f"Skipped     : {summary.skipped}")
    print("\nBy category:")
    for category, count in summary.by_category.items():
        print(f"  - {category}: {count}")
    print("=" * 40)

    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report = summary.to_dict()
        report.update({"mode": "dry-run" if dry_run else "real", "meta": meta or {}})
        with report_path.open("w", encoding="utf-8") as report_file:
            json.dump(report, report_file, indent=2)
        print(f"Report written to {report_path}")


# ================= HISTORY =================

def load_history(history_path: Path) -> List[dict]:
    if history_path.exists():
        with history_path.open("r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


def save_history_entry(root_folder: Path, moves: List[dict], history_path: Path, destination: Path) -> None:
    history = load_history(history_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    history.append(
        {
            "timestamp": timestamp,
            "root": str(root_folder),
            "destination": str(destination),
            "moves": moves,
        }
    )
    with history_path.open("w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def list_history(history_path: Path) -> None:
    history = load_history(history_path)
    if not history:
        print("[!] No history available.")
        return

    print("\n Available rollback history:")
    print("-" * 40)
    for entry in history:
        ts = entry.get("timestamp")
        count = len(entry.get("moves", []))
        destination = entry.get("destination")
        dest_hint = f" -> {destination}" if destination else ""
        print(f" - {ts} ({count} files){dest_hint}")
    print("-" * 40)


# ================= ROLLBACK =================

def rollback(history_path: Path, timestamp: Optional[str] = None) -> None:
    history = load_history(history_path)
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
        dst = Path(move["dst"])
        src = Path(move["src"])
        if dst.exists():
            src.parent.mkdir(parents=True, exist_ok=True)
            final_src = src
            if src.exists():
                new_src = get_unique_filename(src.parent, src.name)
                msg = f"[!] Rollback rename: {src.name} -> {new_src}"
                print(msg)
                logging.warning(msg)
                final_src = src.parent / new_src
            try:
                shutil.move(str(dst), str(final_src))
                restored += 1
            except Exception as e:  # pylint: disable=broad-except
                print(f"[X] Failed to restore {dst}: {e}")

    print(f"✔ Rollback complete. {restored} files restored.")

    if timestamp:
        history = [h for h in history if h["timestamp"] != timestamp]
    else:
        history.pop()

    with history_path.open("w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


# ================= MAIN LOGIC =================

def clean_folder(settings: OrganizerSettings) -> None:
    abs_path = settings.root.resolve()
    destination_root = (settings.destination or settings.root).resolve()
    root_paths = {Path(os.path.abspath(os.sep))}
    if os.name == 'nt':
        root_paths.add(Path("C:/").resolve())

    if abs_path in root_paths:
        print(f"[X] REFUSING to run on system root directory: {abs_path}")
        print(" Please choose a specific folder (e.g., Downloads)")
        return

    if destination_root in root_paths:
        print(f"[X] REFUSING to write into system root directory: {destination_root}")
        print(" Please choose a destination folder instead of the filesystem root.")
        return

    if not abs_path.is_dir():
        print(f"[X] Folder not found: {abs_path}")
        return
    if not settings.dry_run and not settings.confirm:
        print("[!] Real run detected. Use --confirm to proceed.")
        return

    categories = load_categories(settings.config_path, merge_defaults=settings.merge_defaults)
    history: List[dict] = []
    summary = RunSummary()

    if settings.dry_run:
        print("=" * 60)
        print("[!]  DRY RUN MODE ENABLED - NO FILES WILL BE MOVED")
        print("=" * 60)

    current_script = Path(sys.argv[0]).name
    target_category_folders = {destination_root / c for c in categories}

    # Avoid re-processing destination when it lives inside the source tree.
    skip_paths = set()
    try:
        destination_root.relative_to(abs_path)
        skip_paths.add(destination_root)
    except ValueError:
        pass

    for root, dirs, files in os.walk(abs_path):
        root_path = Path(root)
        depth = len(root_path.relative_to(abs_path).parts)
        if settings.max_depth is not None and depth >= settings.max_depth:
            dirs[:] = []

        dirs[:] = [
            d
            for d in dirs
            if d not in IGNORED_DIRS
            and (settings.include_hidden or not d.startswith("."))
            and not matches_exclude(root_path / d, settings.exclude_patterns)
            and (root_path / d) not in target_category_folders
            and (root_path / d) not in skip_paths
        ]

        for filename in files:
            file_path = root_path / filename
            if not settings.include_hidden and filename.startswith("."):
                summary.skipped += 1
                continue

            if filename in {current_script, LOG_FILE, HISTORY_FILE, CONFIG_FILE}:
                summary.skipped += 1
                continue

            if matches_exclude(file_path, settings.exclude_patterns):
                summary.skipped += 1
                continue

            summary.total_scanned += 1

            _, extension = os.path.splitext(filename)
            category = get_category(extension, categories, filepath=file_path)
            target_folder = destination_root / category

            if file_path.parent == target_folder:
                summary.skipped += 1
                continue

            summary.by_category[category] = summary.by_category.get(category, 0) + 1

            if not target_folder.exists() and not settings.dry_run:
                target_folder.mkdir(parents=True)

            if (target_folder / filename).exists():
                new_filename = get_unique_filename(target_folder, filename)
                if settings.dry_run:
                    msg = f"[DRY RUN] Rename conflict: {filename} -> {new_filename}"
                    print(msg)
                    logging.warning(msg)
            else:
                new_filename = filename

            if new_filename != filename and not settings.dry_run:
                summary.renamed += 1
                logging.warning(f"Renamed {filename} -> {new_filename}")

            destination_path = target_folder / new_filename

            if settings.dry_run:
                logging.info(f"[DRY RUN] {file_path} -> {destination_path}")
            else:
                try:
                    if settings.mode == "copy":
                        shutil.copy2(str(file_path), str(destination_path))
                        summary.copied += 1
                        logging.info(f"Copied {file_path} -> {destination_path}")
                    else:
                        shutil.move(str(file_path), str(destination_path))
                        summary.moved += 1
                        history.append({"src": str(file_path), "dst": str(destination_path)})
                        logging.info(f"Moved {file_path} -> {destination_path}")
                except Exception as e:  # pylint: disable=broad-except
                    logging.error(f"Failed to move {file_path}: {e}")

    if not settings.dry_run:
        if history and settings.mode == "move":
            save_history_entry(abs_path, history, settings.history_path, destination_root)
        if settings.cleanup_empty:
            print("Cleaning up empty folders...")
            remove_empty_folders(abs_path)

    meta = {
        "Source": str(abs_path),
        "Destination": str(destination_root),
        "Mode": settings.mode,
        "Author": f"{AUTHOR_NAME} <{AUTHOR_EMAIL}>",
    }
    print_summary(summary, settings.dry_run, report_path=settings.report_path, meta=meta)


# ================= ENTRY POINT =================

if __name__ == "__main__":
    args = parse_arguments()

    settings = OrganizerSettings(
        root=args.path,
        dry_run=args.dry_run,
        confirm=args.confirm,
        mode=args.mode,
        destination=args.destination,
        cleanup_empty=not args.no_cleanup,
        config_path=args.config,
        exclude_patterns=set(args.exclude or []),
        history_path=Path(HISTORY_FILE),
        log_path=Path(LOG_FILE),
        merge_defaults=args.merge_defaults,
        include_hidden=args.include_hidden,
        max_depth=args.max_depth,
        console_log=args.console_log,
        report_path=args.report,
    )

    configure_logging(settings.log_path, console=settings.console_log)

    if args.list_history:
        list_history(settings.history_path)
    elif args.rollback is not None:
        rollback(settings.history_path, args.rollback)
    else:
        clean_folder(settings)
