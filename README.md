# KTPM - Công cụ tạo dữ liệu test cho OrangeHRM

## 🛠️ Cài đặt

```bash
# 1. Clone repo hoặc mở thư mục source code
git clone https://github.com/LTVINH24/KTPM.git

# 2 Tạo venv
python -m venv venv
.\venv\Scripts\activate

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Cấu hình database
cp .env.example .env
# Chỉnh sửa .env theo cấu hình của bạn
```
---

## 🚀 Chạy Generate Data

### Cách 1: Chạy tất cả

```bash
python main.py
```

### Cách 2: Chạy từng script

```bash
# Bước 1: Tạo nhân viên (Bắt buộc chạy trước)
python generate_dim.py

# Bước 2: Tạo dữ liệu time and attendance
python generate_time_attendance.py
```
## 🚀 Reset Data
```bash
py reset_data.py
```
## 🔐 Thông tin mặc định

| Thông tin | Giá trị |
|-----------|---------|
| Mật khẩu user | `OrangeHRM@111` |
 |
| OrangeHRM | http://localhost:8080 |
