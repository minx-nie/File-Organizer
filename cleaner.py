"""
Project: Dọn dẹp máy tính (File Organizer)
Author: Minx-nie

"""

import os
import shutil
import logging

# ================= CẤU HÌNH =================

FOLDER_TO_CLEAN = os.path.join(os.path.expanduser("~"), "Downloads")

DRY_RUN = True # Change to False to perform actual moves

LOG_FILE = "file_organizer.log"

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Installers": [".exe", ".msi"],
    "Archives": [".zip", ".rar", ".7z"],
    "Videos": [".mp4", ".avi"],
    "Music": [".mp3", ".wav"]
}

# ================= LOGGING =================

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
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
        print("Lỗi: Thư mục không tồn tại.")
        logging.error("Folder not found: %s", FOLDER_TO_CLEAN)
        return

    print("--- Bắt đầu dọn dẹp ---")
    print("Chế độ:", "DRY RUN " if DRY_RUN else "THỰC THI")

    try:
        for filename in os.listdir(FOLDER_TO_CLEAN):
            original_path = os.path.join(FOLDER_TO_CLEAN, filename)

            if os.path.isdir(original_path):
                continue

            _, extension = os.path.splitext(filename)
            extension = extension.lower()

            category = get_category(extension)
            target_folder = os.path.join(FOLDER_TO_CLEAN, category)

            # Kiểm tra xung đột
            if os.path.exists(target_folder) and not os.path.isdir(target_folder):
                logging.warning("Xung đột: %s tồn tại nhưng không phải thư mục", target_folder)
                continue

            if not os.path.exists(target_folder):
                if not DRY_RUN:
                    os.makedirs(target_folder)
                logging.info("Tạo thư mục: %s", category)

            new_filename = get_unique_filename(target_folder, filename)
            destination_path = os.path.join(target_folder, new_filename)

            if DRY_RUN:
                print(f"[DRY RUN] {filename} → {category}/{new_filename}")
            else:
                shutil.move(original_path, destination_path)
                print(f"Đã chuyển: {filename} → {category}/{new_filename}")
                logging.info("Moved %s → %s", filename, category)

    except Exception as e:
        print("Lỗi nghiêm trọng:", e)
        logging.exception("Unhandled error")

    print("--- Hoàn tất ---")

# ================= ENTRY POINT =================

if __name__ == "__main__":
    clean_folder()
