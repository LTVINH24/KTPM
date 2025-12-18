# Functional Testing - OrangeHRM

## 🚀 Cách chạy

### Tạo file Excel template (chưa có kết quả)
```bash
python run_functional_tests.py
```

### Tạo file Excel với mock data (có đầy đủ kết quả)
```bash
python run_functional_tests.py --mock
```

### Chạy automation test thực tế với Selenium
```bash
python run_functional_tests.py --auto --url http://localhost:8080
```

### Chạy automation ở chế độ headless
```bash
python run_functional_tests.py --auto --headless
```

---

## 📁 Output

| File | Mô tả |
|------|-------|
| `reports/Test_cases.xlsx` | Danh sách 46 test cases với kết quả |
| `reports/Bug_reports.xlsx` | Danh sách bugs phát hiện |

---

## 📊 Thống kê Test Cases

| Module | Số lượng |
|--------|----------|
| HR Administration | 29 |
| Performance Management | 17 |
| **Tổng** | **46** |

| Kỹ thuật | Số lượng |
|----------|----------|
| Domain Testing | 20 (43.5%) |
| Decision Table | 11 (23.9%) |
| Use Case Testing | 15 (32.6%) |

---

## 📋 Tài liệu

- [Test_Design_Report.md](../docs/Test_Design_Report.md) - Chi tiết thiết kế test cases
