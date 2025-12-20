# 📂 File Organizer

<div align="center">
🇬🇧 [English](#english) | 🇻🇳 [Tiếng Việt](#vietnamese)
</div>

---

<a id="english"></a>

## 🇬🇧 English

### About The Project
**File Organizer** is a simple CLI tool that helps you clean up cluttered folders by automatically organizing files into categorized directories.

⚠️ **Important:**  
This tool now uses **command-line arguments** instead of hard-coded configuration inside the script.

#### ✨ Key Features
- 📂 **Smart Categorization** by file extension
- 🛡️ **Dry Run Mode (default-safe):** Preview actions before moving files
- 🧾 **Command Line Interface (CLI):** No need to edit the source code
- 📝 **Detailed Logging:** All actions are recorded in `file_organizer.log`
- ⚡ **Duplicate Handling:** Automatically renames files to avoid overwrite

---

### 🚀 Usage

#### Default run (real move)
```bash
python cleaner.py
````

✔ Cleans your **Downloads** folder and moves files for real.

---

#### Dry Run (recommended first)

```bash
python cleaner.py --dry-run
```

✔ Shows what would happen
❌ Does NOT move any files
⚠️ A warning banner will be displayed

---

#### Custom folder

```bash
python cleaner.py "D:\MyFolder"
```

---

#### Custom folder + Dry Run

```bash
python cleaner.py "D:\MyFolder" --dry-run
```

---

### 📌 Notes

* Category folders will be created automatically.
* Files with duplicate names will be auto-renamed.
* Hidden files and folders are ignored.

---

#### 📄 License & Author

MIT License
Author: Minx-nie

---

<a id="vietnamese"></a>

## 🇻🇳 Tiếng Việt

### Giới thiệu

**File Organizer** là một tool dòng lệnh (CLI) giúp bạn dọn dẹp thư mục lộn xộn bằng cách tự động phân loại file theo đuôi mở rộng.

⚠️ **Lưu ý quan trọng:**
Tool **không còn chỉnh sửa cấu hình trong code**. Mọi thao tác đều thực hiện qua **command line**.

#### ✨ Tính năng chính

* 📂 **Phân loại thông minh** theo loại file
* 🛡️ **Dry Run (khuyến nghị chạy trước):** Xem trước kết quả mà không di chuyển file
* 🧾 **CLI thân thiện:** Không cần mở file `.py` để chỉnh sửa
* 📝 **Ghi log chi tiết:** Lưu toàn bộ lịch sử vào `file_organizer.log`
* ⚡ **Tự xử lý trùng tên file**

---

### 🚀 Cách sử dụng

#### Chạy thật (mặc định)

```bash
python cleaner.py
```

✔ Dọn thư mục **Downloads**
⚠️ File sẽ được di chuyển thật

---

#### Chạy thử (an toàn)

```bash
python cleaner.py --dry-run
```

✔ Chỉ hiển thị kết quả
❌ Không di chuyển file
⚠️ Có banner cảnh báo DRY RUN

---

#### Chọn thư mục khác

```bash
python cleaner.py "D:\MyFolder"
```

---

#### Chọn thư mục + chạy thử

```bash
python cleaner.py "D:\MyFolder" --dry-run
```

---

### 📌 Ghi chú

* Tool sẽ tự tạo thư mục phân loại nếu chưa tồn tại
* File trùng tên sẽ được tự động đổi tên
* Bỏ qua file ẩn và thư mục con

---

#### 📄 Bản quyền & Tác giả

MIT License
Tác giả: Minx-nie

