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
* Confirm before executing real moves to prevent accidental file moves
* Rollback last run using `move_history.json`
* Summary report with processed, moved, and renamed files
* Configurable categories via `categories.json`

---

### ✨ Features

* 📂 Automatic file categorization by extension
* 🛡️ Dry Run mode (preview without moving files)
* ✅ Confirm before real run (`--confirm`)
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

| Command                                        | Description                              |
| ---------------------------------------------- | ---------------------------------------- |
| `python cleaner.py --dry-run`                  | Preview changes without moving files     |
| `python cleaner.py --confirm`                  | Execute real move (Downloads by default) |
| `python cleaner.py "D:\MyFolder" --dry-run`    | Dry run on custom folder                 |
| `python cleaner.py "D:\MyFolder" --confirm`    | Real run on custom folder                |
| `python cleaner.py --rollback`                 | Undo last run                            |
| `python cleaner.py --rollback 20251221_153045` | Undo specific timestamp run              |
| `python cleaner.py --list-history`             | List available rollback history          |

---

### 📁 File Categories

Files are sorted into:

**Images, Documents, Archives, Installers, Videos, Music, Code, Others**

### ⚙️ Custom Categories

Edit `categories.json` to change file groups. If missing/invalid, defaults are used.

---

🎨 Visual Examples
<div align="center">

Messy Folder
<img src="sample_images/messy_folder.png" alt="Messy folder" width="400"/>

Cleaned Folder
<img src="sample_images/cleaned_folder.png" alt="Cleaned folder" width="400"/>

Workflow Diagram
<img src="sample_images/workflow.png" alt="Workflow" width="600"/>

</div>

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


---

### 📝 Examples

#### Dry Run

```bash
python cleaner.py --dry-run
python cleaner.py "D:\MyFolder" --dry-run
```

#### Real Run (Confirm)

```bash
python cleaner.py --confirm
python cleaner.py "D:\MyFolder" --confirm
```

#### Rollback

```bash
python cleaner.py --rollback
python cleaner.py --rollback 20251221_153045
```

#### List History

```bash
python cleaner.py --list-history
```

#### Visual Example

| File Name   | Original Folder | Category Folder | Action |
| ----------- | --------------- | --------------- | ------ |
| photo.jpg   | Downloads       | Images          | Move   |
| report.docx | Downloads       | Documents       | Move   |
| song.mp3    | Downloads       | Music           | Move   |
| archive.zip | Downloads       | Archives        | Move   |
| setup.exe   | Downloads       | Installers      | Move   |
| script.py   | Downloads       | Code            | Move   |
| unknown.xyz | Downloads       | Others          | Move   |

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
* Xác nhận trước khi chạy thật (`--confirm`)
* Hoàn tác lần chạy gần nhất bằng `move_history.json`
* Báo cáo tổng kết file đã xử lý, di chuyển và đổi tên
* Cấu hình nhóm file qua `categories.json`

---

### ✨ Tính năng

* 📂 Tự động phân loại file theo đuôi
* 🛡️ Chạy thử (Dry Run) mà không di chuyển file
* ✅ Xác nhận trước khi chạy thật
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

| Lệnh                                           | Mô tả                                     |
| ---------------------------------------------- | ----------------------------------------- |
| `python cleaner.py --dry-run`                  | Xem trước kết quả mà không di chuyển file |
| `python cleaner.py --confirm`                  | Chạy thật trên Downloads                  |
| `python cleaner.py "D:\MyFolder" --dry-run`    | Chạy thử thư mục khác                     |
| `python cleaner.py "D:\MyFolder" --confirm`    | Chạy thật thư mục khác                    |
| `python cleaner.py --rollback`                 | Hoàn tác lần chạy gần nhất                |
| `python cleaner.py --rollback 20251221_153045` | Hoàn tác theo timestamp cụ thể            |
| `python cleaner.py --list-history`             | Liệt kê lịch sử các lần chạy              |

---

### 📁 Các nhóm file

**Images, Documents, Archives, Installers, Videos, Music, Code, Others**

### ⚙️ Tuỳ chỉnh phân loại

Sửa `categories.json` để thay đổi nhóm file. Nếu không hợp lệ, tool dùng mặc định.

---

🎨 Ví dụ trực quan
<div align="center">

Thư mục lộn xộn
<img src="sample_images/messy_folder.png" alt="Messy folder" width="400"/>

Thư mục đã sắp xếp
<img src="sample_images/cleaned_folder.png" alt="Cleaned folder" width="400"/>

Sơ đồ Workflow
<img src="sample_images/workflow.png" alt="Workflow" width="600"/>

</div>

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

---

### 📝 Ví dụ minh họa

| Tên File    | Thư mục gốc | Thư mục phân loại | Hành động |
| ----------- | ----------- | ----------------- | --------- |
| photo.jpg   | Downloads   | Images            | Di chuyển |
| report.docx | Downloads   | Documents         | Di chuyển |
| song.mp3    | Downloads   | Music             | Di chuyển |
| archive.zip | Downloads   | Archives          | Di chuyển |
| setup.exe   | Downloads   | Installers        | Di chuyển |
| script.py   | Downloads   | Code              | Di chuyển |
| unknown.xyz | Downloads   | Others            | Di chuyển |

---

### 📄 Bản quyền

MIT License
Tác giả: **Minx-nie**

