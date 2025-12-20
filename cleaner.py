"""
Project: Dọn dẹp máy tính (Improved File Organizer)
Author: Minx-nie
"""

import os
import shutil
import logging

# ================= CẤU HÌNH =================

FOLDER_TO_CLEAN = r"C:\Users\TenUserCuaBan\Downloads"

DRY_RUN = True 

LOG_FILE = "file_organizer.log"

FILE_CATEGORIES = {
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

# ================= HÀM HỖ TRỢ =================

def get_unique_filename(folder, filename):
    name, ext = os.path.splitext(filename)
    counter = 1
    new_name = filename
    while os.path.exists(os.path.join(folder, new_name)):
        new_name = f"{name} ({counter}){ext}"
        counter += 1
    return new_name

def get_category(extension):
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"

# ================= CHƯƠNG TRÌNH CHÍNH =================

def clean_folder():
    if not os.path.isdir(FOLDER_TO_CLEAN):
        print(f"Lỗi: Thư mục không tồn tại: {FOLDER_TO_CLEAN}")
        logging.error(f"Folder not found: {FOLDER_TO_CLEAN}")
        return

    print(f"--- Bắt đầu dọn dẹp: {FOLDER_TO_CLEAN} ---")
    print(f"--- Chế độ: {'DRY RUN (Chạy thử)' if DRY_RUN else 'REAL RUN (Chạy thật)'} ---")

    files = os.listdir(FOLDER_TO_CLEAN)
    moved_count = 0

    for filename in files:
        try:
            original_path = os.path.join(FOLDER_TO_CLEAN, filename)

            if os.path.isdir(original_path) or filename.startswith('.'):
                continue
            if filename in [os.path.basename(__file__), LOG_FILE]:
                continue

            _, extension = os.path.splitext(filename)
            extension = extension.lower()

            category = get_category(extension)
            target_folder = os.path.join(FOLDER_TO_CLEAN, category)

            if not os.path.exists(target_folder) and not DRY_RUN:
                os.makedirs(target_folder)
            
            if os.path.exists(target_folder):
                new_filename = get_unique_filename(target_folder, filename)
            else:
                new_filename = filename

            destination_path = os.path.join(target_folder, new_filename)

            if DRY_RUN:
                print(f"[Thử nghiệm] {filename} -> {category}/{new_filename}")
            else:
                shutil.move(original_path, destination_path)
                print(f"✅ Đã chuyển: {filename} -> {category}/{new_filename}")
                logging.info(f"Moved: {filename} -> {category}/{new_filename}")
                moved_count += 1

        except Exception as e:
            print(f"⚠️ Lỗi xử lý file {filename}: {e}")
            logging.error(f"Error processing {filename}: {e}")

    print(f"--- Hoàn tất! Đã xử lý {moved_count} files. ---")

if __name__ == "__main__":
    clean_folder()