# 📂 File Organizer

<div align="center">
🇬🇧 [English](#english) | 🇻🇳 [Tiếng Việt](#vietnamese)
</div>

---

<a id="english"></a>

## 🇬🇧 English

### About The Project
Tired of a messy Downloads folder? **File Organizer** scans your target directory and intelligently moves files into categorized folders (Images, Documents, Music, etc.).

Unlike basic cleaners, this tool features a **Dry Run** mode (simulation) to ensure safety before moving any files.

#### ✨ Key Features
- 📂 **Smart Categorization:** Sorts files into Images, Documents, Archives, Installers, Videos, Music, and Code
- 🛡️ **Dry Run Mode:** Previews changes without moving files
- 📝 **Detailed Logging:** Keeps history in `file_organizer.log`
- ⚡ **Conflict Handling:** Auto-renames duplicates (e.g., `file (1).txt`)
- 💻 **Cross-platform & CLI:** Specify folder to clean and dry-run option via command line

#### 🚀 Getting Started
**Clone the repository:**
```bash
git clone https://github.com/Minx-nie/desktop-cleaner.git
````

**Run the tool:**

* **Default run (Downloads folder, moves files for real):**

```bash
python cleaner.py
```

* **Specify a custom folder:**

```bash
python cleaner.py "D:\MyFolder"
```

* **Dry Run (preview changes without moving files):**

```bash
python cleaner.py --dry-run
```

* **Custom folder + Dry Run:**

```bash
python cleaner.py "D:\MyFolder" --dry-run
```

> The tool will automatically create category folders if they do not exist.

#### 📄 License & Author

Distributed under the MIT License. See LICENSE for more information.
Author: Minx-nie

---

<a id="vietnamese"></a>

## 🇻🇳 Tiếng Việt

### Giới thiệu

Thư mục Downloads của bạn quá bừa bộn? **File Organizer** sẽ giải quyết vấn đề này chỉ bằng một cú click. Tool sẽ tự động quét và di chuyển file vào các thư mục gọn gàng (Ảnh, Tài liệu, Nhạc, v.v.).

Điểm đặc biệt là **chế độ Dry Run** (Chạy thử) giúp bạn xem trước kết quả, đảm bảo an toàn trước khi di chuyển file thật.

#### ✨ Tính năng chính

* 📂 **Phân loại thông minh:** Tự động đưa file vào nhóm Images, Documents, Archives, Installers, Videos, Music và Code
* 🛡️ **Chế độ Dry Run:** Xem trước những gì sẽ xảy ra mà không di chuyển file
* 📝 **Ghi Log chi tiết:** Lưu lịch sử di chuyển file vào `file_organizer.log`
* ⚡ **Xử lý trùng tên:** Tự động đổi tên nếu file đã tồn tại (ví dụ: `tailieu (1).pdf`)
* 💻 **Chạy đa nền tảng & CLI:** Chọn thư mục muốn dọn và chế độ dry-run qua command line

#### 🚀 Hướng dẫn sử dụng

**Tải về máy:**

```bash
git clone https://github.com/Minx-nie/desktop-cleaner.git
```

**Chạy tool:**

* **Mặc định (thư mục Downloads, di chuyển file thật):**

```bash
python cleaner.py
```

* **Chọn thư mục khác:**

```bash
python cleaner.py "D:\MyFolder"
```

* **Chạy thử (không di chuyển file):**

```bash
python cleaner.py --dry-run
```

* **Chọn thư mục + chạy thử:**

```bash
python cleaner.py "D:\MyFolder" --dry-run
```

> Tool sẽ tự động tạo các thư mục theo category nếu chưa có.

#### 📄 Bản quyền & Tác giả

Phân phối theo giấy phép MIT. Xem file LICENSE để biết thêm chi tiết.
Tác giả: Minx-nie

```
