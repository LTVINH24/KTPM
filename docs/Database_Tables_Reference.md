# 📊 OrangeHRM Database Tables - Phân loại theo Module

## Tổng quan
Database OrangeHRM chứa **~150 bảng**, được phân chia theo các module chức năng.

---

## 🔴 HR ADMINISTRATION (Chức năng của bạn)

### Organization Info
| Bảng | Mô tả |
|------|-------|
| `ohrm_organization_gen_info` | Thông tin tổ chức (tên, địa chỉ, tax ID...) |
| `ohrm_subunit` | Cơ cấu tổ chức (phòng ban, đơn vị) |
| `ohrm_operational_country` | Quốc gia hoạt động |

### Locations
| Bảng | Mô tả |
|------|-------|
| `ohrm_location` | Danh sách địa điểm/văn phòng |
| `hs_hr_emp_locations` | Nhân viên - Địa điểm làm việc |

### Job Administration
| Bảng | Mô tả |
|------|-------|
| `ohrm_job_title` | Chức danh công việc |
| `ohrm_job_category` | Danh mục công việc |
| `ohrm_job_specification_attachment` | Tài liệu mô tả công việc |
| `ohrm_employment_status` | Trạng thái hợp đồng |
| `hs_hr_jobtit_empstat` | Liên kết Job Title - Employment Status |

### Pay & Compensation
| Bảng | Mô tả |
|------|-------|
| `ohrm_pay_grade` | Bậc lương |
| `ohrm_pay_grade_currency` | Bậc lương theo tiền tệ (min/max) |
| `hs_hr_emp_basicsalary` | Lương cơ bản nhân viên |
| `hs_hr_emp_directdebit` | Thông tin chuyển khoản lương |
| `hs_hr_payperiod` | Kỳ trả lương |
| `hs_hr_pay_period` | Cấu hình kỳ lương |

### Qualifications (Skills, Education, Languages)
| Bảng | Mô tả |
|------|-------|
| `ohrm_skill` | Danh sách kỹ năng |
| `hs_hr_emp_skill` | Kỹ năng của nhân viên |
| `ohrm_education` | Trình độ học vấn |
| `ohrm_emp_education` / `hs_hr_emp_education` | Học vấn của nhân viên |
| `ohrm_language` | Danh sách ngôn ngữ |
| `hs_hr_emp_language` | Ngôn ngữ của nhân viên |
| `ohrm_license` | Danh sách chứng chỉ/bằng cấp |
| `ohrm_emp_license` | Chứng chỉ của nhân viên |
| `ohrm_membership` | Hội viên/Tổ chức |

### Work Schedule
| Bảng | Mô tả |
|------|-------|
| `ohrm_work_shift` | Ca làm việc |
| `ohrm_employee_work_shift` | Ca làm việc của nhân viên |
| `ohrm_work_week` | Cấu hình tuần làm việc |
| `ohrm_holiday` | Ngày lễ |

### User & Security
| Bảng | Mô tả |
|------|-------|
| `ohrm_user` | Tài khoản người dùng |
| `ohrm_user_role` | Vai trò người dùng (Admin, ESS, Supervisor) |
| `ohrm_user_role_screen` | Quyền truy cập màn hình |
| `ohrm_user_role_data_group` | Quyền truy cập dữ liệu |
| `ohrm_login` | Lịch sử đăng nhập |
| `ohrm_reset_password` | Reset mật khẩu |
| `ohrm_enforce_password` | Chính sách mật khẩu |

### Termination
| Bảng | Mô tả |
|------|-------|
| `ohrm_emp_termination` | Thông tin nghỉ việc |
| `ohrm_emp_termination_reason` | Lý do nghỉ việc |

---

## 🟡 PERFORMANCE MANAGEMENT (Chức năng của bạn)

| Bảng | Mô tả |
|------|-------|
| `ohrm_kpi` | Key Performance Indicators (Chỉ số KPI) |
| `ohrm_performance_track` | Performance Tracker |
| `ohrm_performance_tracker_log` | Log theo dõi hiệu suất |
| `ohrm_performance_tracker_reviewer` | Người đánh giá tracker |
| `ohrm_performance_review` | Đánh giá hiệu suất |
| `ohrm_reviewer` | Người đánh giá |
| `ohrm_reviewer_group` | Nhóm người đánh giá |
| `ohrm_reviewer_rating` | Điểm đánh giá |

---

## 🟢 PIM (Personal Information Management)

### Employee Core
| Bảng | Mô tả |
|------|-------|
| `hs_hr_employee` | **Thông tin nhân viên chính** |
| `hs_hr_emp_picture` | Ảnh nhân viên |
| `hs_hr_emp_attachment` | Tài liệu đính kèm |
| `hs_hr_unique_id` | ID duy nhất |

### Personal Details
| Bảng | Mô tả |
|------|-------|
| `hs_hr_emp_passport` | Hộ chiếu/CMND |
| `hs_hr_emp_dependents` | Người phụ thuộc |
| `hs_hr_emp_children` | Con cái |
| `hs_hr_emp_emergency_contacts` | Liên hệ khẩn cấp |
| `hs_hr_emp_us_tax` | Thông tin thuế (US) |

### Work Experience
| Bảng | Mô tả |
|------|-------|
| `hs_hr_emp_work_experience` | Kinh nghiệm làm việc |
| `hs_hr_emp_history_of_ealier_pos` | Lịch sử vị trí trước đó |
| `hs_hr_emp_contract_extend` | Gia hạn hợp đồng |
| `hs_hr_emp_member_detail` | Chi tiết hội viên |

### Reporting Structure
| Bảng | Mô tả |
|------|-------|
| `hs_hr_emp_reportto` | Cấu trúc báo cáo (Supervisor) |
| `ohrm_emp_reporting_method` | Phương thức báo cáo |

### Custom Fields
| Bảng | Mô tả |
|------|-------|
| `hs_hr_custom_fields` | Trường tùy chỉnh |

---

## 🔵 TIME & ATTENDANCE

### Attendance
| Bảng | Mô tả |
|------|-------|
| `ohrm_attendance_record` | Bản ghi chấm công (Punch In/Out) |

### Timesheet
| Bảng | Mô tả |
|------|-------|
| `ohrm_timesheet` | Bảng chấm công theo tuần |
| `ohrm_timesheet_item` | Chi tiết từng mục timesheet |
| `ohrm_timesheet_action_log` | Lịch sử hành động (Submit/Approve) |

### Projects
| Bảng | Mô tả |
|------|-------|
| `ohrm_customer` | Khách hàng |
| `ohrm_project` | Dự án |
| `ohrm_project_activity` | Hoạt động dự án |
| `ohrm_project_admin` | Admin dự án |

---

## 🟣 LEAVE MANAGEMENT

| Bảng | Mô tả |
|------|-------|
| `ohrm_leave_type` | Loại nghỉ phép |
| `ohrm_leave` | Ngày nghỉ phép |
| `ohrm_leave_request` | Yêu cầu nghỉ phép |
| `ohrm_leave_request_comment` | Bình luận yêu cầu |
| `ohrm_leave_comment` | Bình luận nghỉ phép |
| `ohrm_leave_entitlement` | Quyền nghỉ phép |
| `ohrm_leave_entitlement_type` | Loại quyền nghỉ phép |
| `ohrm_leave_leave_entitlement` | Liên kết nghỉ phép - quyền |
| `ohrm_leave_status` | Trạng thái nghỉ phép |
| `ohrm_leave_period_history` | Lịch sử kỳ nghỉ phép |

---

## 🟠 RECRUITMENT

| Bảng | Mô tả |
|------|-------|
| `ohrm_job_vacancy` | Vị trí tuyển dụng |
| `ohrm_job_vacancy_attachment` | Tài liệu tuyển dụng |
| `ohrm_job_candidate` | Ứng viên |
| `ohrm_job_candidate_vacancy` | Ứng viên - Vị trí |
| `ohrm_job_candidate_attachment` | Tài liệu ứng viên |
| `ohrm_job_candidate_history` | Lịch sử ứng viên |
| `ohrm_job_interview` | Phỏng vấn |
| `ohrm_job_interview_interviewer` | Người phỏng vấn |
| `ohrm_job_interview_attachment` | Tài liệu phỏng vấn |

---

## ⚪ CLAIM / EXPENSE

| Bảng | Mô tả |
|------|-------|
| `ohrm_claim_event` | Sự kiện claim |
| `ohrm_claim_request` | Yêu cầu claim |
| `ohrm_claim_attachment` | Tài liệu claim |
| `ohrm_expense` | Chi phí |
| `ohrm_expense_type` | Loại chi phí |

---

## 🔘 SYSTEM / CONFIG

### Email
| Bảng | Mô tả |
|------|-------|
| `ohrm_email` | Email |
| `ohrm_email_configuration` | Cấu hình email |
| `ohrm_email_notification` | Thông báo email |
| `ohrm_email_template` | Template email |
| `ohrm_email_subscriber` | Người đăng ký |
| `ohrm_email_processor` | Xử lý email |
| `ohrm_mail_queue` | Hàng đợi email |

### Localization
| Bảng | Mô tả |
|------|-------|
| `hs_hr_country` | Danh sách quốc gia |
| `hs_hr_province` | Tỉnh/Thành phố |
| `hs_hr_district` | Quận/Huyện |
| `hs_hr_currency_type` | Loại tiền tệ |
| `ohrm_nationality` | Quốc tịch |
| `ohrm_i18n_*` | Đa ngôn ngữ |

### Reports
| Bảng | Mô tả |
|------|-------|
| `ohrm_report` | Báo cáo |
| `ohrm_report_group` | Nhóm báo cáo |
| `ohrm_display_field*` | Cấu hình hiển thị |
| `ohrm_filter_field` | Bộ lọc |
| `ohrm_group_field` | Nhóm trường |

### OAuth / API
| Bảng | Mô tả |
|------|-------|
| `ohrm_oauth*` | OAuth tokens |
| `ohrm_oauth2_*` | OAuth 2.0 |
| `ohrm_api_permission` | Quyền API |
| `ohrm_rest_api_usage` | Sử dụng API |

### System
| Bảng | Mô tả |
|------|-------|
| `hs_hr_config` | Cấu hình hệ thống |
| `ohrm_module` | Module |
| `ohrm_screen` | Màn hình |
| `ohrm_menu_item` | Menu |
| `ohrm_home_page` | Trang chủ |
| `ohrm_plugin` | Plugin |
| `ohrm_theme` | Giao diện |
| `ohrm_migration_log` | Log migration |
| `ohrm_upgrade_history` | Lịch sử nâng cấp |

---

## 📌 Tóm tắt cho 2 chức năng của bạn

### HR Administration (12+ bảng chính)
```
ohrm_organization_gen_info, ohrm_location, ohrm_subunit,
ohrm_job_title, ohrm_job_category, ohrm_employment_status,
ohrm_pay_grade, ohrm_pay_grade_currency,
ohrm_skill, ohrm_education, ohrm_language, ohrm_license,
ohrm_work_shift, ohrm_work_week, ohrm_holiday,
ohrm_user, ohrm_user_role
```

### Performance Management (8 bảng)
```
ohrm_kpi, ohrm_performance_track, ohrm_performance_tracker_log,
ohrm_performance_tracker_reviewer, ohrm_performance_review,
ohrm_reviewer, ohrm_reviewer_group, ohrm_reviewer_rating
```
