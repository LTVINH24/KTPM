# KTPM - Công cụ tạo dữ liệu test cho OrangeHRM

Bộ công cụ Python tự động tạo dữ liệu test cho hệ thống **OrangeHRM**, phục vụ kiểm thử 2 module:
- **HR Administration**
- **Performance Management**

---

## 🛠️ Cài đặt

**Nếu sử dụng venv**


```bash
# Bước 1: Tạo
python -m venv venv
# Bước 2: Chạy
.\venv\Scripts\activate
```

```bash
# 1. Clone repo
git clone https://github.com/LTVINH24/KTPM.git
cd KTPM

# 2. Cài đặt dependencies
pip install -r requirements.txt

# 3. Cấu hình database
cp .env.example .env
# Chỉnh sửa .env theo cấu hình của bạn
```

---

## 🚀 Chạy Generate Data

### Cách 1: Chạy tất cả (khuyến nghị)

```bash
python main.py
```

### Cách 2: Chạy từng script

```bash
# Bước 1: Tạo nhân viên (BẮT BUỘC chạy trước)
python generate_dim.py

# Bước 2-4: Chạy theo thứ tự bất kỳ
python generate_hr_admin.py
python generate_time_attendance.py
python generate_performance.py
```

### Sửa lỗi Authentication (nếu cần)

```bash
docker exec -it orangehrm-mysql mysql -uroot -proot -e "ALTER USER 'orangehrm'@'%' IDENTIFIED WITH caching_sha2_password BY 'orangehrm'; FLUSH PRIVILEGES;"
```

---

## 📁 Cấu trúc

| File | Mô tả |
|------|-------|
| `main.py` | Chạy tất cả scripts |
| `generate_dim.py` | Tạo nhân viên, users |
| `generate_hr_admin.py` | Tạo HR Admin data |
| `generate_time_attendance.py` | Tạo Time & Attendance |
| `generate_performance.py` | Tạo Performance data |

---

## 📖 Tài liệu chi tiết

- [Database_Tables_Reference.md](docs/Database_Tables_Reference.md) - Phân loại bảng theo module
- [Generated_Tables_Summary.md](docs/Generated_Tables_Summary.md) - Tóm tắt dữ liệu được tạo

---

## 🔐 Thông tin mặc định

| Thông tin | Giá trị |
|-----------|---------|
| Mật khẩu user | `OrangeHRM@111` |
| phpMyAdmin | http://localhost:8080 (`root`/`root`) |
| OrangeHRM | http://localhost |

---

## 👥 Tác giả

**LTVINH24** - [GitHub](https://github.com/LTVINH24)
