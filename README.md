# 📂 File Organizer

<div align="center">
🇬🇧 [English](#english) | 🇻🇳 [Tiếng Việt](#vietnamese)
</div>

---

<a id="english"></a>

## 🇬🇧 English

### 📌 About

**File Organizer** is a simple Python CLI tool that helps you clean up cluttered folders by automatically sorting files into categorized directories.

This project focuses on **safety**, **simplicity**, and **ease of use** — no configuration inside the code is required.

---

### ✨ Features

* 📂 Automatic file categorization by extension
* 🛡️ Dry Run mode (preview before moving files)
* 🧾 Command Line Interface (CLI)
* 📝 Action logging to `file_organizer.log`
* ⚡ Safe handling of duplicate filenames


### 🧰 Requirements

* Python **3.8+**
* No third-party libraries required


### 📊 Summary Report

After the tool finishes running, a summary report will be displayed in the terminal. This helps you quickly verify what the tool has done without checking logs manually.


### 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/Minx-nie/desktop-cleaner.git
cd desktop-cleaner
```

---

### ▶️ Usage

#### 1️⃣ Default run (real move)

Cleans the **Downloads** folder and moves files for real:

```bash
python cleaner.py
```

#### 2️⃣ Dry Run (recommended first)

Preview all changes **without moving files**:

```bash
python cleaner.py --dry-run
```

A warning banner will be displayed to indicate Dry Run mode.

#### 3️⃣ Clean a custom folder

```bash
python cleaner.py "D:\MyFolder"
```

#### 4️⃣ Custom folder + Dry Run

```bash
python cleaner.py "D:\MyFolder" --dry-run
```

---

### 📁 File Categories

Files are organized based on their extensions into folders such as:

* Images
* Documents
* Archives
* Installers
* Videos
* Music
* Code
* Others

---

### ⚙️ Custom Categories (Optional)

You can customize file categories by editing `categories.json`.
No code changes are required.

If the file is missing or invalid, the tool will use default categories.

---

### ⚠️ Notes

* Category folders are created automatically if they do not exist
* Hidden files and directories are ignored
* Files are never overwritten — duplicates are auto-renamed
* The tool scans subfolders recursively but keeps the folder structure intact.


---

### 📄 License

MIT License

Author: **Minx-nie**

---

<a id="vietnamese"></a>

## 🇻🇳 Tiếng Việt

### 📌 Giới thiệu

**File Organizer** là một công cụ Python chạy bằng dòng lệnh (CLI) giúp bạn dọn dẹp thư mục lộn xộn bằng cách tự động phân loại file theo đuôi mở rộng.

Tool được thiết kế với tiêu chí **an toàn**, **đơn giản** và **dễ sử dụng** — không cần chỉnh sửa code.

---

### ✨ Tính năng

* 📂 Tự động phân loại file
* 🛡️ Chế độ Dry Run (xem trước kết quả)
* 🧾 Chạy bằng dòng lệnh (CLI)
* 📝 Ghi log chi tiết vào `file_organizer.log`
* ⚡ Tự xử lý file trùng tên


### 🧰 Yêu cầu

* Python **3.8 trở lên**
* Không cần cài thêm thư viện


### 📊 Báo cáo tổng kết

Sau khi tool chạy xong, một báo cáo tổng kết sẽ được in ra terminal. Phần này giúp bạn kiểm tra nhanh kết quả mà không cần mở file log.


### 🚀 Cài đặt

Clone project về máy:

```bash
git clone https://github.com/Minx-nie/desktop-cleaner.git
cd desktop-cleaner
```

---

### ▶️ Cách sử dụng

#### 1️⃣ Chạy thật (mặc định)

Dọn thư mục **Downloads** và di chuyển file thật:

```bash
python cleaner.py
```

#### 2️⃣ Chạy thử (khuyến nghị)

Xem trước những gì sẽ xảy ra **mà không di chuyển file**:

```bash
python cleaner.py --dry-run
```

Sẽ có banner cảnh báo đang ở chế độ Dry Run.

#### 3️⃣ Dọn thư mục khác

```bash
python cleaner.py "D:\MyFolder"
```

#### 4️⃣ Thư mục khác + chạy thử

```bash
python cleaner.py "D:\MyFolder" --dry-run
```

---

### 📁 Các nhóm file

File sẽ được đưa vào các thư mục:
Images, Documents, Archives, Installers, Videos, Music, Code và Others.

---

### ⚙️ Tuỳ chỉnh phân loại (Không bắt buộc)

Bạn có thể tuỳ chỉnh các nhóm file bằng cách sửa file `categories.json`
mà không cần chỉnh sửa code.

Nếu file không tồn tại hoặc bị lỗi, tool sẽ dùng cấu hình mặc định.

---

### ⚠️ Lưu ý

* Tool tự tạo thư mục phân loại nếu chưa tồn tại
* Không ghi đè file — file trùng tên sẽ được đổi tên tự động
* Bỏ qua file ẩn và thư mục con
* Tool quét toàn bộ thư mục con nhưng không xóa cấu trúc thư mục.


---

### 📄 Bản quyền

Giấy phép MIT
Tác giả: **Minx-nie**
