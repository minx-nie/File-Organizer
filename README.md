# 📂 File Organizer

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License MIT">
  <img src="https://img.shields.io/badge/Status-Stable-brightgreen" alt="Status Stable">
</div>

---

<div align="center">
🇬🇧 [English](#english) | 🇻🇳 [Tiếng Việt](#vietnamese)
</div>

---

<a id="english"></a>

## 🇬🇧 English

### 📌 About

**File Organizer** is a Python CLI tool that automatically sorts files in cluttered folders into categorized directories.

**Key highlights:**

* Safety first — Dry Run mode to preview changes
* Rollback last run using `move_history.json`
* Summary report with processed, moved, and renamed files
* Configurable categories via `categories.json`

---

### ✨ Features

* 📂 Automatic file categorization by extension
* 🛡️ Dry Run mode (preview without moving files)
* ↩️ Rollback / Undo last run
* 🧾 CLI with clear summary report
* 📝 Logging in `file_organizer.log`
* ⚡ Safe handling of duplicate filenames
* ⚙️ Configurable file categories via JSON

---

### 🧰 Requirements

* Python **3.8+**
* No third-party libraries

---

### 🚀 Installation

```bash
git clone https://github.com/Minx-nie/desktop-cleaner.git
cd desktop-cleaner
```

---

### ▶️ Usage

| Command                                     | Description                                  |
| ------------------------------------------- | -------------------------------------------- |
| `python cleaner.py`                         | Default run (real move)                      |
| `python cleaner.py --dry-run`               | Preview changes without moving files         |
| `python cleaner.py "D:\MyFolder"`           | Clean a custom folder                        |
| `python cleaner.py "D:\MyFolder" --dry-run` | Dry run on custom folder                     |
| `python cleaner.py --rollback`              | Undo last real-run using `move_history.json` |

---

### 📁 File Categories

Files are sorted into:
**Images, Documents, Archives, Installers, Videos, Music, Code, Others**

### ⚙️ Custom Categories

Edit `categories.json` to change file groups. If missing/invalid, defaults are used.

---

### 📊 Summary Report

After running, terminal displays:

* Total files processed
* Files moved
* Files renamed
* Breakdown by category
* Mode (Dry Run / Real Run)

---

### ⚠️ Notes

* Category folders auto-created if missing
* Hidden files and directories ignored
* Files never overwritten — duplicates renamed automatically
* Recursively scans subfolders while preserving structure
* Logs (`file_organizer.log`) and move history (`move_history.json`) created locally
* Add these files to `.gitignore` to avoid pushing to GitHub

---

### 📄 License

MIT License
Author: **Minx-nie**

---

<a id="vietnamese"></a>

## 🇻🇳 Tiếng Việt

### 📌 Giới thiệu

**File Organizer** là công cụ Python CLI giúp tự động phân loại file trong các thư mục lộn xộn.

**Điểm nổi bật:**

* An toàn — Dry Run xem trước thay đổi
* Hoàn tác lần chạy gần nhất bằng `move_history.json`
* Báo cáo tổng kết file đã xử lý, di chuyển và đổi tên
* Cấu hình nhóm file qua `categories.json`

---

### ✨ Tính năng

* 📂 Tự động phân loại file theo đuôi
* 🛡️ Chạy thử (Dry Run) mà không di chuyển file
* ↩️ Hoàn tác / Rollback lần chạy gần nhất
* 🧾 CLI với báo cáo tổng kết chi tiết
* 📝 Ghi log vào `file_organizer.log`
* ⚡ Xử lý file trùng tên an toàn
* ⚙️ Tuỳ chỉnh nhóm file bằng JSON

---

### 🧰 Yêu cầu

* Python **3.8+**
* Không cần thư viện ngoài

---

### 🚀 Cài đặt

```bash
git clone https://github.com/Minx-nie/desktop-cleaner.git
cd desktop-cleaner
```

---

### ▶️ Cách sử dụng

| Lệnh                                        | Mô tả                                     |
| ------------------------------------------- | ----------------------------------------- |
| `python cleaner.py`                         | Chạy thật trên Downloads                  |
| `python cleaner.py --dry-run`               | Xem trước kết quả mà không di chuyển file |
| `python cleaner.py "D:\MyFolder"`           | Dọn thư mục khác                          |
| `python cleaner.py "D:\MyFolder" --dry-run` | Chạy thử thư mục khác                     |
| `python cleaner.py --rollback`              | Hoàn tác lần chạy gần nhất                |

---

### 📁 Các nhóm file

**Images, Documents, Archives, Installers, Videos, Music, Code, Others**

### ⚙️ Tuỳ chỉnh phân loại

Sửa `categories.json` để thay đổi nhóm file. Nếu không hợp lệ, tool dùng mặc định.

---

### 📊 Báo cáo tổng kết

Hiển thị:

* Tổng số file đã xử lý
* File đã di chuyển
* File đổi tên
* Thống kê theo nhóm
* Chế độ chạy (Dry Run / Real Run)

---

### ⚠️ Lưu ý

* Tự tạo thư mục nếu chưa có
* Bỏ qua file/ thư mục ẩn
* File trùng tên tự đổi tên, không ghi đè
* Quét toàn bộ thư mục con, giữ cấu trúc
* Logs và history tạo tại thư mục hiện tại
* Nên thêm `.gitignore` để không push log/history

---

### 📄 Bản quyền

MIT License
Tác giả: **Minx-nie**

