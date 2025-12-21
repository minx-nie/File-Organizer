# 📂 File Organizer

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License MIT">
  <img src="https://img.shields.io/badge/Status-Stable-brightgreen" alt="Status Stable">
  <img src="https://img.shields.io/badge/Type-CLI%20Tool-orange" alt="CLI Tool">
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

### ⚠️ Safety Notice

> * Always run with `--dry-run` before using `--confirm`
> * Rollback is **best-effort** and may rename files if name conflicts occur
> * **Do NOT run this tool on system root directories** (e.g. `/`, `C:\`)
> * Back up important data before organizing large folders

---

### ✨ Features

* 📂 Automatic file categorization by extension & MIME
* 🛡️ Dry Run mode (preview without moving files)
* ✅ Confirm before real run (`--confirm`)
* ↩️ Rollback / Undo last run or specific timestamp
* 🧾 CLI with clear summary report
* 📝 Logging in `file_organizer.log`
* ⚡ Safe handling of duplicate filenames
* ⚙️ Configurable file categories via JSON
* 🧹 Optional cleanup of empty folders

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

---

### ⚙️ Custom Categories

Edit `categories.json` to change file groups.
If the file is missing or invalid, default categories are used automatically.

---

### 🚫 Ignored Directories

To avoid breaking projects, the following directories are automatically skipped:

`.git`, `.idea`, `.vscode`, `node_modules`, `venv`, `env`, `__pycache__`, `.svn`

---

### ↩️ Rollback Behavior

Rollback restores files based on recorded move history.

If the original file path already exists, the restored file will be **renamed automatically** to avoid overwriting existing files.

---

### ❌ Limitations

* Does not analyze file contents (extension & MIME-based only)
* Does not merge folders or flatten directory structure
* Does not delete files (except empty folders after organizing)

---

🎨 Visual Examples

<div align="center">

Messy Folder <img src="sample_images/messy_folder.png" alt="Messy folder" width="400"/>

Cleaned Folder <img src="sample_images/cleaned_folder.png" alt="Cleaned folder" width="400"/>

Workflow Diagram <img src="sample_images/workflow.png" alt="Workflow" width="600"/>

</div>

---

### 📊 Summary Report

After running, the terminal displays:

* Total files processed
* Files moved
* Files renamed
* Breakdown by category
* Execution mode (Dry Run / Real Run)

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
* Hoàn tác lần chạy gần nhất hoặc theo timestamp
* Báo cáo tổng kết chi tiết
* Tuỳ chỉnh nhóm file qua `categories.json`

---

### ⚠️ Cảnh báo an toàn

> * Luôn chạy `--dry-run` trước khi dùng `--confirm`
> * Rollback **không đảm bảo tuyệt đối** nếu file đã bị thay đổi sau khi chạy
> * **Không chạy tool ở thư mục gốc hệ thống** (`/`, `C:\`)
> * Nên sao lưu dữ liệu quan trọng trước khi dọn dẹp

---

### ✨ Tính năng

* 📂 Tự động phân loại file theo đuôi & MIME
* 🛡️ Chạy thử (Dry Run)
* ✅ Xác nhận trước khi chạy thật
* ↩️ Hoàn tác / Rollback an toàn
* 🧾 Báo cáo tổng kết rõ ràng
* 📝 Ghi log chi tiết
* ⚡ Xử lý file trùng tên
* ⚙️ Tuỳ chỉnh nhóm file bằng JSON
* 🧹 Dọn thư mục trống sau khi sắp xếp

---

### 🚫 Thư mục bị bỏ qua

Tool tự động bỏ qua các thư mục sau để tránh làm hỏng project:

`.git`, `.idea`, `.vscode`, `node_modules`, `venv`, `env`, `__pycache__`, `.svn`

---

### ↩️ Cơ chế Rollback

Rollback hoàn tác dựa trên lịch sử đã ghi.

Nếu file gốc đã tồn tại, file được hoàn tác sẽ được **đổi tên tự động** để tránh ghi đè.

---

### ❌ Giới hạn

* Không phân tích nội dung file
* Không gộp hoặc làm phẳng thư mục
* Không xoá file (chỉ xoá thư mục trống)

---

### 📄 Bản quyền

MIT License
Tác giả: **Minx-nie**

