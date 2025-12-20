# 📂 Improved File Organizer

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
- 📂 **Smart Categorization:** Sorts files into Images, Documents, Archives, Installers, Videos, and Music
- 🛡️ **Dry Run Mode:** Previews changes without moving files
- 📝 **Detailed Logging:** Keeps history in `file_organizer.log`
- ⚡ **Conflict Handling:** Auto-renames duplicates (e.g., `file (1).txt`)

#### 🚀 Getting Started
**Clone the repository:**
```bash
git clone https://github.com/Minx-nie/desktop-cleaner.git
```

**Configuration (in `cleaner.py`):**
```python
FOLDER_TO_CLEAN = os.path.join(os.path.expanduser("~"), "Downloads")
DRY_RUN = True  # Set to False to actually move files
```

**Run:**
```bash
python cleaner.py
```

#### 📄 License & Author
Distributed under the MIT License. See LICENSE for more information.  
Author: Minx-nie


---

<a id="vietnamese"></a>

## 🇻🇳 Tiếng Việt

### Giới thiệu
Thư mục Downloads của bạn quá bừa bộn? **File Organizer** sẽ giải quyết vấn đề này chỉ bằng một cú click. Tool sẽ tự động quét và di chuyển file vào các thư mục gọn gàng (Ảnh, Tài liệu, Nhạc, v.v.).

Điểm đặc biệt là chế độ **Dry Run** (Chạy thử) giúp bạn xem trước kết quả, đảm bảo an toàn tuyệt đối trước khi di chuyển file thật.

#### ✨ Tính năng chính
- 📂 **Phân loại thông minh:** Tự động đưa file vào nhóm Images, Documents, Archives, Installers, Videos, và Music
- 🛡️ **Chế độ Dry Run:** Xem trước những gì sẽ xảy ra mà không làm mất file
- 📝 **Ghi Log:** Lưu lại lịch sử di chuyển file vào `file_organizer.log`
- ⚡ **Xử lý trùng tên:** Tự động đổi tên nếu file đã tồn tại (ví dụ: `tailieu (1).pdf`)

#### 🚀 Hướng dẫn sử dụng
**Tải về máy:**
```bash
git clone https://github.com/Minx-nie/desktop-cleaner.git
```

**Cấu hình (trong file `cleaner.py`):**
```python
# Mặc định là thư mục Downloads
FOLDER_TO_CLEAN = os.path.join(os.path.expanduser("~"), "Downloads")
# Đổi thành False để bắt đầu di chuyển file thật
DRY_RUN = True
```

**Chạy tool:**
```bash
python cleaner.py
```

#### 📄 Bản quyền & Tác giả
Phân phối theo giấy phép MIT. Xem file LICENSE để biết thêm chi tiết.  
Tác giả: Minx-nie 



