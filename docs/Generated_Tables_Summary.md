# 📊 Danh sách các bảng được tạo dữ liệu bởi các Script Python

## Tổng quan

| Script | Module | Số bảng |
|--------|--------|---------|
| `generate_dim.py` | PIM, Admin | 5 bảng |
| `generate_hr_admin.py` | HR Administration | 12 bảng |
| `generate_time_attendance.py` | Time & Attendance | 7 bảng |
| `generate_performance.py` | Performance Management | 4 bảng |
| **Tổng cộng** | | **28 bảng** |

---

## 1️⃣ generate_dim.py

> **Chức năng**: Tạo dữ liệu nền tảng (Nhân viên, User, Cấu trúc tổ chức)  
> **Phải chạy TRƯỚC các script khác**

| Bảng | Mô tả | Số lượng |
|------|-------|----------|
| `ohrm_job_title` | Chức danh công việc | 3 (Director, Manager, Staff) |
| `ohrm_employment_status` | Trạng thái hợp đồng | 2 (Full-Time Permanent, Contract) |
| `hs_hr_employee` | Thông tin nhân viên | 50 nhân viên |
| `ohrm_user` | Tài khoản đăng nhập | 50 users |
| `ohrm_emp_reporting_method` | Phương thức báo cáo | 1 (Direct) |
| `hs_hr_emp_reportto` | Cấu trúc báo cáo (ai báo cáo ai) | ~49 records |

### Dữ liệu mẫu - hs_hr_employee:
```
emp_number, employee_id, emp_firstname, emp_lastname, emp_birthday, 
emp_gender, job_title_code, emp_status, joined_date, city_code, 
emp_work_email, emp_work_telephone
```

---

## 2️⃣ generate_hr_admin.py

> **Chức năng**: Tạo dữ liệu cấu hình HR Administration  
> **Yêu cầu**: Đã chạy `generate_dim.py`

| Bảng | Mô tả | Số lượng |
|------|-------|----------|
| `ohrm_organization_gen_info` | Thông tin tổ chức | 1 công ty |
| `ohrm_location` | Địa điểm/Văn phòng | 5 locations |
| `ohrm_pay_grade` | Bậc lương | 5 grades (A-E) |
| `ohrm_pay_grade_currency` | Bậc lương theo tiền tệ | 5 (VND) |
| `ohrm_education` | Trình độ học vấn | 6 levels |
| `ohrm_language` | Danh sách ngôn ngữ | 7 ngôn ngữ |
| `ohrm_skill` | Danh sách kỹ năng | 10 skills |
| `ohrm_license` | Danh sách chứng chỉ | 7 licenses |
| `ohrm_work_shift` | Ca làm việc | 4 shifts |
| `hs_hr_emp_skill` | Kỹ năng của nhân viên | ~150 records |
| `hs_hr_emp_language` | Ngôn ngữ của nhân viên | ~75 records |
| `hs_hr_emp_education` | Học vấn của nhân viên | ~50 records |

### Dữ liệu mẫu - ohrm_location:
```
- Head Office - HCMC (123 Nguyen Hue, District 1)
- Branch Office - Hanoi (456 Lang Ha, Dong Da)
- Branch Office - Da Nang (789 Bach Dang, Hai Chau)
- R&D Center (321 Vo Van Kiet, District 5)
- Training Center (654 Le Loi, District 1)
```

### Dữ liệu mẫu - ohrm_pay_grade:
```
- Grade A - Executive: 50,000,000 - 100,000,000 VND
- Grade B - Senior: 30,000,000 - 50,000,000 VND
- Grade C - Mid-Level: 15,000,000 - 30,000,000 VND
- Grade D - Junior: 8,000,000 - 15,000,000 VND
- Grade E - Entry: 5,000,000 - 8,000,000 VND
```

---

## 3️⃣ generate_time_attendance.py

> **Chức năng**: Tạo dữ liệu Time & Attendance  
> **Yêu cầu**: Đã chạy `generate_dim.py`

| Bảng | Mô tả | Số lượng |
|------|-------|----------|
| `ohrm_customer` | Khách hàng | 2 (External, Internal) |
| `ohrm_project` | Dự án | 4 projects |
| `ohrm_project_activity` | Hoạt động dự án | ~24 activities |
| `ohrm_timesheet` | Bảng chấm công header | ~200 (50 NV x 4 tuần) |
| `ohrm_timesheet_item` | Chi tiết timesheet | ~1000 items |
| `ohrm_timesheet_action_log` | Lịch sử Submit/Approve | ~300 logs |
| `ohrm_attendance_record` | Punch In/Out | ~1000 records |

### Dữ liệu mẫu - ohrm_customer:
```
- Global Tech Corp (External)
- Internal Management (Internal)
```

### Dữ liệu mẫu - ohrm_project:
```
External Projects:
- Super App
- E-Banking Web
- HRM System

Internal Project:
- Executive Board
```

### Dữ liệu mẫu - ohrm_project_activity (theo vai trò):
```
Staff:
- Coding Backend, Coding Frontend, Unit Testing, Bug Fixing

Manager:
- Project Planning, Code Review, Client Meeting

Director:
- Strategic Planning, Financial Review, Board Meeting
```

---

## 4️⃣ generate_performance.py

> **Chức năng**: Tạo dữ liệu Performance Management  
> **Yêu cầu**: Đã chạy `generate_dim.py`

| Bảng | Mô tả | Số lượng |
|------|-------|----------|
| `ohrm_performance_tracker` | Performance Tracker | ~45 trackers |
| `ohrm_performance_tracker_log` | Log theo dõi KPIs | ~135 logs |
| `ohrm_reviewer` | Người đánh giá | ~45 reviewers |
| `ohrm_performance_review` | Đánh giá hiệu suất | ~20 reviews |

### Dữ liệu mẫu - Performance Tracker Templates:
```
1. Sales Performance Q4 2024
   - Monthly Revenue Target
   - Customer Acquisition
   - Client Retention Rate

2. Project Delivery Metrics
   - On-time Delivery
   - Code Quality Score
   - Bug Fix Rate

3. Customer Service Excellence
   - Customer Satisfaction Score
   - Response Time
   - Issue Resolution Rate
```

### Dữ liệu mẫu - Performance Review Status:
```
1 = Activated
2 = In Progress
3 = Completed
4 = Approved
```

---

## 📌 Thứ tự chạy bắt buộc

```
┌─────────────────────────────────────────────────────────┐
│  1. python generate_dim.py          ← BẮT BUỘC TRƯỚC   │
│     └── Tạo: hs_hr_employee, ohrm_user, ohrm_job_title │
├─────────────────────────────────────────────────────────┤
│  2. python generate_hr_admin.py     ← Sau bước 1       │
│     └── Cần: emp_number từ hs_hr_employee              │
├─────────────────────────────────────────────────────────┤
│  3. python generate_time_attendance.py ← Sau bước 1    │
│     └── Cần: emp_number + job_title                    │
├─────────────────────────────────────────────────────────┤
│  4. python generate_performance.py  ← Sau bước 1       │
│     └── Cần: emp_number + user_id                      │
└─────────────────────────────────────────────────────────┘
```

Hoặc chạy tất cả bằng 1 lệnh:
```bash
python run_all.py
```

---

## 📊 Tổng kết các bảng theo Module

### HR Administration (12 bảng)
- `ohrm_organization_gen_info`
- `ohrm_location`
- `ohrm_job_title`
- `ohrm_employment_status`
- `ohrm_pay_grade`
- `ohrm_pay_grade_currency`
- `ohrm_education`
- `ohrm_language`
- `ohrm_skill`
- `ohrm_license`
- `ohrm_work_shift`
- `ohrm_emp_reporting_method`

### Performance Management (4 bảng)
- `ohrm_performance_tracker`
- `ohrm_performance_tracker_log`
- `ohrm_reviewer`
- `ohrm_performance_review`

### PIM - Employee Data (6 bảng)
- `hs_hr_employee`
- `hs_hr_emp_reportto`
- `hs_hr_emp_skill`
- `hs_hr_emp_language`
- `hs_hr_emp_education`
- `ohrm_user`

### Time & Attendance (7 bảng)
- `ohrm_customer`
- `ohrm_project`
- `ohrm_project_activity`
- `ohrm_timesheet`
- `ohrm_timesheet_item`
- `ohrm_timesheet_action_log`
- `ohrm_attendance_record`
