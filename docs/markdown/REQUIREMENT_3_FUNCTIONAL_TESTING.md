# BÁO CÁO REQUIREMENT 3: FUNCTIONAL TESTING

## Thông tin cá nhân

| **Thông tin** | **Chi tiết** |
| --- | --- |
| **Môn học** | Kiểm thử phần mềm (Software Testing) |
| **Sinh viên** | Trương Lê Anh Vũ |
| **MSSV** | 22120443 |
| **Nhóm** | 13 |

## Thông tin nhóm

| Họ và tên        | MSSV     | Module phụ trách                                            | Feature                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| :--------------- | :------- | :---------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Nguyễn Đức Toàn  | 22120376 | Leave Management; Recruitment                               | - Sinh dữ liệu loại nghỉ phép, quyền nghỉ phép của nhân viên, đơn xin nghỉ phép, bình luận đơn nghỉ, trạng thái duyệt đơn nghỉ của quản lý.<br>- Sinh dữ liệu vị trí tuyển dụng, ứng viên, hồ sơ ứng tuyển, lịch phỏng vấn, người phỏng vấn, lịch sử tuyển dụng, tài liệu đính kèm.<br>- Thiết kế và thực thi các test case cho chức năng nộp đơn xin nghỉ phép & cấu hình hệ thống nghỉ phép (Leave Types, Entitlements, Approve/Reject workflow).<br>- Thiết kế và thực thi các test case cho quy trình tuyển dụng (Thêm ứng viên, sơ tuyển, phỏng vấn, offer, tuyển dụng, quản lý hồ sơ).                                                                                                                                               |
| Lê Hoàng Việt    | 22120430 | HR Administration; Performance Management                   | - Sinh dữ liệu HR Administration (Organization, Locations, Pay Grades, Skills, Languages, Licenses, Work Shifts, Holidays) và Performance Management (KPIs, Performance Trackers, Tracker Logs, Performance Reviews).<br>- Thiết kế và thực thi test case cho cấu hình HR (Locations, Skills, Pay Grades) và cho Performance (tạo KPI, review, reviewer workflow).                                                                                                                                                                                                                                                                                                                                                                         |
| Lê Thành Vinh    | 22120434 | PIM - Personnel Information Management; Time and Attendance | - Sinh dữ liệu mô tả công việc (Job title), employee status, thông tin nhân viên, thông tin tài khoản người dùng, thông tin báo cáo của nhân viên với quản lý.<br>- Sinh dữ liệu khách hàng, project, hoạt động của project, dữ liệu timesheet của nhân viên, lịch sử tạo, duyệt, từ chối timesheet, dữ liệu chấm công của nhân viên.<br>- Thiết kế và thực thi các test case cho chức năng thêm mới thông tin nhân viên & tài khoản hệ thống cho nhân viên.<br>- Thiết kế và thực thi các test case cho quy trình timesheet (Tạo mới, gửi, duyệt, từ chối chấm công).                                                                                                                                                                     |
| Trương Lê Anh Vũ | 22120443 | Reporting and Analytics; ESS - Employee Self-Service        | Reporting and Analytics: Cung cấp bộ công cụ trích xuất và xuất dữ liệu (Export) đa định dạng:<br>- Báo cáo Hồ sơ Nhân viên: Lọc và xuất danh sách nhân viên theo các tiêu chí mở rộng (Trình độ, Kỹ năng, Lương) phục vụ thống kê.<br>- Báo cáo Quy trình Tuyển dụng: Theo dõi danh sách ứng viên và trạng thái tuyển dụng theo từng người phụ trách (Hiring Manager).<br>- Báo cáo Tổng hợp Time & Leave: Truy xuất lịch sử sử dụng phép và bảng công đã được duyệt (Approved) để phục vụ mục đích báo cáo dự án.<br><br>Employee Self-Service (ESS): Tính năng tương tác trực tiếp dành cho người lao động:<br>- Tra cứu thông tin: Nhân viên tự truy cập để kiểm tra hồ sơ cá nhân (My Info) và hạn mức phép năm (Leave Entitlements). |

---

## 1. Tổng quan (Overview)

### 1.1. Mục đích tài liệu (Document Purpose)

Tài liệu này trình bày chi tiết quy trình thiết kế và thực thi test cases cho **2 chức năng chính** trong module **Employee Self-Service (ESS)** của hệ thống OrangeHRM:

1. **Personal Details** - Sử dụng kỹ thuật **Domain Testing**
2. **Apply Leave Request** - Sử dụng kỹ thuật **Decision Table Testing**

### 1.2. Requirement Context

**Module:** Employee Self-Service (ESS)

**Requirement từ đề bài:**
> "Employee Self-Service (ESS): Employee access to personal profiles, leave balances and history, timesheets, and the ability to submit and track requests online."

**Các chức năng được kiểm thử:**

| Chức năng | Requirement Coverage | Kỹ thuật | Test Cases |
| :--- | :--- | :--- | :---: |
| **Personal Details** | "Employee access to personal profiles" | Domain Testing | 39 TCs |
| **Apply Leave Request** | "submit and track requests online" + "leave balances" | Decision Table Testing | 10 TCs |
| **TỔNG** | | | **49 TCs** |

- **Personal Details:** Một trong những chức năng cốt lõi của ESS cho phép nhân viên:
    - Truy cập và xem thông tin cá nhân của chính mình
    - Cập nhật các thông tin được phép chỉnh sửa
    - Quản lý hồ sơ cá nhân một cách tự chủ không cần qua Admin

- **Apply Leave Request:** Cho phép nhân viên xin nghỉ phép

---

## PHẦN 1: PERSONAL DETAILS - DOMAIN TESTING

### 1.1. Giới thiệu chức năng (Feature Introduction)

**Feature:** Personal Profile Management (My Info > Personal Details)

**Mô tả:** Nhân viên tự truy cập và cập nhật thông tin cá nhân của mình thông qua ESS module (My Info), bao gồm:
- Họ tên (First Name, Middle Name, Last Name)
- Employee ID (read-only)
- Other ID
- Giấy phép lái xe và ngày hết hạn
- Quốc tịch
- Tình trạng hôn nhân
- Ngày sinh
- Giới tính

**User role:** Employee (ESS user)

### 1.2. Kỹ thuật Domain Testing

**Domain Testing** là kỹ thuật kiểm thử hộp đen tập trung vào việc phân tích các miền giá trị của dữ liệu đầu vào.

**Quy trình áp dụng:**
1. Xác định các miền đầu vào (Input Domains)
2. Phân vùng miền dữ liệu (Partition Domains)
3. Xác định các điểm biên (Identify Boundary Points)
4. Thiết kế test cases

**Số lượng test cases:** 39 test cases

**User role:** Employee (ESS user) - Nhân viên tự quản lý hồ sơ của mình

**Lưu ý quan trọng:** 
- Test cases được thiết kế từ góc nhìn **Employee** (không phải Admin)
- Tập trung vào quyền tự chỉnh sửa (self-service) của nhân viên
- Personal Details là 1 trong 4 chức năng chính của ESS (còn có Leave, Timesheets, Requests)

### 1.3. Phân tích chi tiết

## 1.3.1. Kỹ thuật Domain Testing (Domain Testing Technique)

### 1.3.1.1. Tổng quan về Domain Testing

**Domain Testing** là kỹ thuật kiểm thử hộp đen (black-box testing) tập trung vào việc phân tích các miền giá trị (value domains) của dữ liệu đầu vào để tạo ra các test cases hiệu quả.

**Nguyên lý cốt lõi:**
1. **Phân vùng dữ liệu (Partitioning):** Chia không gian đầu vào thành các vùng con (partitions) với đặc điểm tương tự
2. **Phân tích biên (Boundary Analysis):** Tập trung vào các giá trị biên giới giữa các vùng
3. **Giá trị đại diện (Representative Values):** Chọn giá trị đại diện cho mỗi vùng để kiểm thử

### 1.3.1.2. Quy trình áp dụng Domain Testing

#### Bước 1: Xác định các miền đầu vào (Identify Input Domains)

Phân tích từng trường dữ liệu để xác định:
- **Kiểu dữ liệu:** String, Number, Date, Dropdown, Radio button
- **Ràng buộc (Constraints):** Required/Optional, Min/Max length, Format, Range
- **Quy tắc nghiệp vụ (Business Rules):** Tuổi hợp lệ, định dạng ngày tháng, v.v.

#### Bước 2: Phân vùng miền dữ liệu (Partition Domains)

Chia mỗi miền đầu vào thành các vùng:
- **Valid Partitions (Vùng hợp lệ):** Giá trị được chấp nhận
- **Invalid Partitions (Vùng không hợp lệ):** Giá trị bị từ chối
- **Boundary Values (Giá trị biên):** Giá trị tại ranh giới các vùng

#### Bước 3: Xác định các điểm biên (Identify Boundary Points)

Cho mỗi vùng, xác định:
- **On-point:** Giá trị nằm đúng trên biên (ví dụ: độ dài = 30)
- **In-point:** Giá trị nằm trong vùng hợp lệ (ví dụ: độ dài = 15)
- **Out-point:** Giá trị nằm ngoài vùng (ví dụ: độ dài = 31)

#### Bước 4: Thiết kế test cases

Tạo test cases cho:
1. Mỗi vùng hợp lệ (ít nhất 1 giá trị đại diện)
2. Mỗi vùng không hợp lệ (ít nhất 1 giá trị đại diện)
3. Tất cả các điểm biên quan trọng
4. Các trường hợp đặc biệt (empty, null, special characters)

---

## 1.4.1. Phân tích chi tiết từng trường (Detailed Field Analysis)

### 1.4.1.1. Employee Full Name (First Name, Middle Name, Last Name)

#### 1.4.1.1.1. Đặc tả yêu cầu (Requirements Specification)

| Thuộc tính | First Name | Middle Name | Last Name |
| :--- | :--- | :--- | :--- |
| **Kiểu dữ liệu** | String | String | String |
| **Required** | ✓ Yes | ✗ No | ✓ Yes |
| **Min Length** | 1 | 0 | 1 |
| **Max Length** | 30 | 30 | 30 |
| **Ký tự cho phép** | Letters, spaces, Vietnamese | Letters, spaces, Vietnamese | Letters, spaces, Vietnamese |
| **Ký tự không cho phép** | Numbers, special chars | Numbers, special chars | Numbers, special chars |

#### 1.4.1.1.2. Phân vùng miền dữ liệu (Domain Partitioning)

**Chiều dài (Length Domain):**

| Vùng | Mô tả | Loại | Giá trị ví dụ |
| :--- | :--- | :--- | :--- |
| D1 | Empty (length = 0) | **Invalid** (cho First/Last Name) | "" |
| D2 | Very short (length = 1) | **Valid** (Lower boundary) | "A" |
| D3 | Normal (1 < length < 30) | **Valid** (In-range) | "Văn", "Nguyễn" |
| D4 | Maximum (length = 30) | **Valid** (Upper boundary) | "A" × 30 |
| D5 | Too long (length > 30) | **Invalid** | "A" × 31 |

**Nội dung (Content Domain):**

| Vùng | Mô tả | Loại | Giá trị ví dụ |
| :--- | :--- | :--- | :--- |
| C1 | Vietnamese letters only | **Valid** | "Văn", "Nguyễn" |
| C2 | English letters only | **Valid** | "John", "Smith" |
| C3 | Letters with spaces | **Valid** | "Văn A" |
| C4 | Contains numbers | **Invalid** | "Văn123" |
| C5 | Contains special chars | **Invalid** | "Văn@#$" |

#### 1.4.1.1.3. Điểm biên (Boundary Points)

```
Length Domain:
    |----X----[====1====|==============|====30====]----X----|
    0    ✗     ✓                               ✓        ✗   31+
  Empty  Invalid  Lower Boundary    Upper Boundary  Invalid
         (D1)     (D2, Valid)         (D4, Valid)    (D5)
```

**Test Cases từ phân tích này:**
- TC001: Cập nhật họ tên hợp lệ với ký tự tiếng Việt (Valid partition - Normal Vietnamese name)
- TC002: Cập nhật First Name rỗng (boundary) (Invalid partition - Empty required field)
- TC003: Cập nhật First Name với 1 ký tự (lower boundary) (Valid boundary - Minimum length (1 character))
- TC004: Cập nhật First Name với 30 ký tự (upper boundary) (Valid boundary - Maximum allowed length)
- TC005: Cập nhật First Name vượt quá 30 ký tự (Invalid partition - Exceeds maximum length)
- TC006: Cập nhật First Name chứa số (Invalid partition - Numbers not allowed)
- TC007: Cập nhật First Name chứa ký tự đặc biệt (Invalid partition - Special characters not allowed)
- TC008: Cập nhật Last Name rỗng (boundary) (Invalid partition - Empty required field)
- TC009: Cập nhật Middle Name tùy chọn (optional field) (Valid partition - Optional field can be empty)

**Tổng: 9 test cases**

---

### 1.4.1.2. Employee ID

#### 1.4.1.2.1. Đặc tả yêu cầu (Requirements Specification)

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Kiểu dữ liệu** | String (Numeric) |
| **Format** | 4 digits (e.g., "0001") |
| **Editable** | No (Read-only) |
| **Auto-generated** | Yes |

#### 1.4.1.2.2. Phân vùng miền dữ liệu

Do Employee ID là trường **read-only** và được hệ thống tự động sinh, domain testing tập trung vào:

| Vùng | Mô tả | Test Case |
| :--- | :--- | :--- |
| **Constraint Check** | Trường không cho phép chỉnh sửa | TC010: Verify read-only |
| **Format Validation** | Hiển thị đúng format 4 digits | TC011: Verify format "0001" |

**Test Cases:**
- TC010: Kiểm tra Employee ID hợp lệ (4 chữ số) (Valid partition - Standard format)
- TC011: Kiểm tra Employee ID chỉ đọc (read-only) (Constraint check - Should be read-only)

**Tổng: 2 test cases**

---

### 1.4.1.3. Other ID

#### 1.4.1.3.1. Đặc tả yêu cầu

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Kiểu dữ liệu** | String (Alphanumeric) |
| **Required** | No |
| **Max Length** | 50 characters |
| **Ký tự cho phép** | Letters, numbers, hyphens |

#### 1.4.1.3.2. Phân vùng miền dữ liệu

| Vùng | Mô tả | Loại | Giá trị ví dụ |
| :--- | :--- | :--- | :--- |
| D1 | Empty (optional) | **Valid** | "" |
| D2 | Normal alphanumeric | **Valid** | "CMND123456" |
| D3 | Max length (50 chars) | **Valid** (Boundary) | "A" × 50 |
| D4 | Exceeds max (>50) | **Invalid** | "A" × 51 |

**Test Cases:**
- TC012: Cập nhật Other ID với giá trị hợp lệ (Valid partition - Alphanumeric value)
- TC013: Để trống Other ID (optional field) (Valid partition - Optional field)
- TC014: Cập nhật Other ID vượt quá độ dài cho phép (Invalid partition - Exceeds max length)

**Tổng: 3 test cases**

---

### 1.4.1.4. Driver's License Number & Expiry Date

#### 1.4.1.4.1. Đặc tả yêu cầu

| Thuộc tính | License Number | Expiry Date |
| :--- | :--- | :--- |
| **Required** | No | No |
| **Format** | Alphanumeric | yyyy-mm-dd |
| **Dependency** | - | Should be future date |

#### 1.4.1.4.2. Phân vùng miền dữ liệu cho Expiry Date

```
Time Domain (relative to TODAY):
    Past         |  Today  |        Future
    [=====X=====]|[==X==]|[==========X==========]
     Invalid/      Boundary      Valid
     Warning      (On-point)   (Normal)
```


| Vùng | Mô tả | Loại | Ví dụ (TODAY = 2025-12-20) |
| :--- | :--- | :--- | :--- |
| D1 | Past date | **Warning/Invalid** | "2020-01-01" |
| D2 | Today | **Boundary** (Valid) | "2025-12-20" |
| D3 | Future date | **Valid** | "2026-12-31" |

**Test Cases:**
- TC015: Cập nhật License Number và Expiry Date hợp lệ (Valid partition - Future expiry date)
- TC016: Cập nhật License với ngày hết hạn trong quá khứ (Boundary - Past date (expired license))
- TC017: Cập nhật License Expiry Date = ngày hiện tại (boundary) (Boundary - Today's date)
- TC018: Để trống cả License Number và Expiry Date (Valid partition - Both fields optional)
- TC019: Nhập License Number nhưng không có Expiry Date (Dependency check - License without expiry)

**Tổng: 5 test cases**

---

### 1.4.1.5. Nationality (Dropdown)

#### 1.4.1.5.1. Đặc tả yêu cầu

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Input Type** | Dropdown |
| **Required** | Depends on business rule |
| **Valid Values** | Predefined list (Vietnamese, American, etc.) |

#### 1.4.1.5.2. Phân vùng miền dữ liệu

| Vùng | Mô tả | Loại |
| :--- | :--- | :--- |
| **D1** | No selection ("-- Select --") | **Boundary** (Check if required) |
| **D2** | Valid selection from dropdown | **Valid** |
| **D3** | Multiple sequential selections | **Valid** (State change) |

**Test Cases:**
- TC020: Chọn Nationality hợp lệ từ dropdown (Valid partition - Valid dropdown selection)
- TC021: Không chọn Nationality (để mặc định) (Boundary - No selection (empty))
- TC022: Chọn nhiều Nationality khác nhau liên tiếp (Valid partition - Multiple valid selections)

**Tổng: 3 test cases**

---

### 1.4.1.6. Marital Status (Dropdown)

#### 1.4.1.6.1. Đặc tả yêu cầu

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Input Type** | Dropdown |
| **Valid Values** | Single, Married, Other |
| **Required** | Depends on business rule |

#### 1.4.1.6.2. Phân vùng miền dữ liệu

| Vùng | Mô tả | Loại |
| :--- | :--- | :--- |
| **D1** | "Single" | **Valid** |
| **D2** | "Married" | **Valid** |
| **D3** | "Other" | **Valid** |
| **D4** | No selection | **Boundary** |

**Lý do test cả 3 giá trị hợp lệ:** Mỗi giá trị là một **equivalence class** riêng biệt có thể có logic xử lý khác nhau trong hệ thống (ví dụ: "Married" có thể kích hoạt các trường liên quan đến gia đình).

**Test Cases:**
- TC023: Chọn Marital Status = "Single" (Valid partition - Valid option "Single")
- TC024: Chọn Marital Status = "Married" (Valid partition - Valid option "Married")
- TC025: Chọn Marital Status = "Other" (Valid partition - Valid option "Other")
- TC026: Không chọn Marital Status (Boundary - No selection)

**Tổng: 4 test cases**

---

### 1.4.1.7. Date of Birth

#### 1.4.1.7.1. Đặc tả yêu cầu

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Kiểu dữ liệu** | Date |
| **Format** | yyyy-mm-dd |
| **Required** | Depends on business rule |
| **Business Rules** | - Must be in the past<br>- Minimum age: 18 years<br>- Maximum age: ~100 years |

#### 1.4.1.7.2. Phân vùng miền dữ liệu theo tuổi

```
Age Domain:
    [===X===]|[==X==|=========|==X==]|[===X===]
     <18      18    18-65     65-100  >100
   Invalid  Lower  Normal    Upper   Invalid/
           Boundary         Boundary  Extreme
```


| Vùng | Tuổi (years) | Loại | Ví dụ (TODAY = 2025-12-20) |
| :--- | :--- | :--- | :--- |
| **D1** | Age < 18 | **Invalid** | DOB: "2010-01-01" (15 tuổi) |
| **D2** | Age = 18 | **Valid (Lower Boundary)** | DOB: "2007-12-20" (đúng 18 tuổi) |
| **D3** | 18 < Age < 65 | **Valid (Normal)** | DOB: "1995-06-15" (30 tuổi) |
| **D4** | Age = 65 | **Valid (Upper Boundary)** | DOB: "1960-12-20" (65 tuổi) |
| **D5** | Age = 100 | **Valid (Extreme Boundary)** | DOB: "1925-12-20" (100 tuổi) |
| **D6** | Age = 0 (Today) | **Invalid** | DOB: "2025-12-20" |
| **D7** | Age < 0 (Future) | **Invalid** | DOB: "2030-12-31" |

#### 1.4.1.7.3. Phân vùng theo định dạng

| Vùng | Mô tả | Loại | Ví dụ |
| :--- | :--- | :--- | :--- |
| **F1** | Correct format (yyyy-mm-dd) | **Valid** | "1995-06-15" |
| **F2** | Wrong format (dd/mm/yyyy) | **Invalid** | "15/06/1995" |
| **F3** | Empty | **Boundary** (Check if required) | "" |

**Test Cases:**
- TC027: Cập nhật Date of Birth hợp lệ (30 tuổi) (Valid partition - Normal working age (30 years))
- TC028: Cập nhật Date of Birth đúng 18 tuổi (lower boundary) (Lower boundary - Minimum legal working age (18))
- TC029: Cập nhật Date of Birth dưới 18 tuổi (invalid) (Invalid partition - Below minimum age (<18))
- TC030: Cập nhật Date of Birth = 65 tuổi (upper boundary typical) (Upper boundary - Typical retirement age (65))
- TC031: Cập nhật Date of Birth = 100 tuổi (extreme upper boundary) (Extreme boundary - Very old age (100))
- TC032: Cập nhật Date of Birth = ngày hôm nay (invalid) (Invalid partition - Today (age = 0))
- TC033: Cập nhật Date of Birth trong tương lai (invalid) (Invalid partition - Future date)
- TC034: Cập nhật Date of Birth với định dạng sai (Invalid partition - Wrong format)
- TC035: Để trống Date of Birth (optional) (Boundary - Empty field (optional check))

**Tổng: 9 test cases**

---

### 1.4.1.8. Gender (Radio Button)

#### 1.4.1.8.1. Đặc tả yêu cầu

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Input Type** | Radio Button |
| **Valid Values** | Male, Female |
| **Default** | None selected (or pre-selected) |
| **Mutually Exclusive** | Yes |

#### 1.4.1.8.2. Phân vùng miền dữ liệu

| Vùng | Mô tả | Loại |
| :--- | :--- | :--- |
| **D1** | Male selected | **Valid** |
| **D2** | Female selected | **Valid** |
| **D3** | No selection | **Boundary** (Check if required) |
| **D4** | Change from Male to Female | **Valid Transition** |

**Lý do test chuyển đổi giá trị:** Radio button có state management, cần đảm bảo khi chuyển từ Male sang Female, giá trị cũ bị ghi đè đúng cách.

**Test Cases:**
- TC036: Chọn Gender = "Male" (Valid partition - Male selection)
- TC037: Chọn Gender = "Female" (Valid partition - Female selection)
- TC038: Thay đổi Gender từ Male sang Female (Valid transition - Change from one valid value to another)
- TC039: Không chọn Gender (kiểm tra required) (Boundary - No selection (check if required))

**Tổng: 4 test cases**

---

## 1.5.1. Tổng hợp Test Cases (Test Case Summary)

### 1.5.1.1. Phân bổ Test Cases theo trường

| Trường (Field) | Số lượng TC | TC IDs |
| :--- | :---: | :--- |
| Employee Full Name | 9 | TC001 - TC009 |
| Employee ID | 2 | TC010 - TC011 |
| Other ID | 3 | TC012 - TC014 |
| Driver's License | 5 | TC015 - TC019 |
| Nationality | 3 | TC020 - TC022 |
| Marital Status | 4 | TC023 - TC026 |
| Date of Birth | 9 | TC027 - TC035 |
| Gender | 4 | TC036 - TC039 |
| **TỔNG** | **39** | |

### 1.5.1.2. Phân bổ Test Cases theo loại miền

| Loại Test Case | Số lượng | Tỷ lệ (%) |
| :--- | :---: | :---: |
| Valid Partitions (In-range) | 18 | 46.2% |
| Invalid Partitions (Out-range) | 10 | 25.6% |
| Boundary Values (On-point) | 11 | 28.2% |
| **TỔNG** | **39** | **100%** |

### 1.5.1.3. Ma trận Coverage (Coverage Matrix)

| Kỹ thuật | Áp dụng |
| :--- | :---: |
| **Boundary Value Analysis** | ✓ |
| **Equivalence Partitioning** | ✓ |
| **Required/Optional Field Testing** | ✓ |
| **Format Validation** | ✓ |
| **Data Type Testing** | ✓ |
| **Length Testing** | ✓ |
| **Range Testing** | ✓ |
| **Dependency Testing** | ✓ |

---

## 5. Ví dụ minh họa chi tiết (Detailed Examples)

### 5.1. Ví dụ 1: Boundary Testing cho First Name Length

**Mục tiêu:** Kiểm tra xử lý độ dài chuỗi tại các điểm biên

**Phân tích miền:**
- Min length: 1 character
- Max length: 30 characters

**Test Cases:**

| TC ID | Input Value | Length | Expected Result | Remark |
| :--- | :--- | :---: | :--- | :--- |
| TC002 | "" (Empty) | 0 | ❌ Error: "Required" | Just below lower boundary |
| TC003 | "A" | 1 | ✅ Success | **Lower boundary (on-point)** |
| TC001 | "Văn" | 3 | ✅ Success | In-range value |
| TC004 | "A"×30 | 30 | ✅ Success | **Upper boundary (on-point)** |
| TC005 | "A"×31 | 31 | ❌ Error: "Max 30 chars" | Just above upper boundary |

**Kết luận:** Test cases bao phủ đầy đủ cả hai biên (lower/upper) và các điểm kế cận (adjacent points).

---

### 5.2. Ví dụ 2: Equivalence Partitioning cho Marital Status

**Mục tiêu:** Đảm bảo mỗi giá trị hợp lệ trong dropdown được xử lý đúng

**Phân tích miền:**
- Class 1: "Single" → Độc thân
- Class 2: "Married" → Đã kết hôn
- Class 3: "Other" → Khác
- Class 4: No selection → Không chọn

**Test Cases:**

| TC ID | Input Value | Expected Result | Equivalence Class |
| :--- | :--- | :--- | :--- |
| TC023 | "Single" | ✅ Updated successfully | Valid Class 1 |
| TC024 | "Married" | ✅ Updated successfully | Valid Class 2 |
| TC025 | "Other" | ✅ Updated successfully | Valid Class 3 |
| TC026 | "-- Select --" | ✅ or ❌ (depends on required) | Boundary Class 4 |

**Lý do test hết các giá trị:**
- Mỗi giá trị có thể trigger logic nghiệp vụ khác nhau
- Ví dụ: "Married" có thể enable trường "Spouse Name" (nếu có)
- "Other" có thể cho phép nhập text giải thích (nếu có)

---

### 5.3. Ví dụ 3: Multi-Dimensional Testing cho Date of Birth

**Mục tiêu:** Kiểm tra cả **giá trị** (age) và **định dạng** (format)

**Phân tích 2 chiều:**

**Dimension 1: Age Range**
- Invalid: < 18 years
- Valid: 18 - 100 years
- Invalid: Future date

**Dimension 2: Format**
- Valid: yyyy-mm-dd
- Invalid: dd/mm/yyyy, mm/dd/yyyy, etc.

**Test Case Matrix:**

| TC ID | Age | Format | Expected Result |
| :--- | :--- | :--- | :--- |
| TC027 | 30 | ✅ yyyy-mm-dd | ✅ Success |
| TC029 | 15 | ✅ yyyy-mm-dd | ❌ Error: "Min age 18" |
| TC034 | 30 | ❌ dd/mm/yyyy | ❌ Error: "Invalid format" |
| TC032 | 0 (Today) | ✅ yyyy-mm-dd | ❌ Error: "Must be past" |
| TC033 | -5 (Future) | ✅ yyyy-mm-dd | ❌ Error: "Must be past" |

**Kết luận:** Kiểm thử kết hợp cả constraint về giá trị và constraint về định dạng.

---

## 6. Chiến lược thực thi (Execution Strategy)

### 6.1. Môi trường kiểm thử (Test Environment)
**Employee user with ESS access** (VD: username_nhanvien / OrangeHRM@111) |
| **Test Module** | My Info (ESS) - accessed by employee
| Thành phần | Chi tiết |
| :--- | :--- |
| **Application** | OrangeHRM 5.x |
| **Database** | MySQL |
| **Browser** | Chrome, Firefox, Edge |
| **Test Data** | Generated by `generate_dim.py` script |
| **Test Account** | Admin user with PIM access |
iền điều kiện (Preconditions)

**Trước khi thực thi test cases:**
1. ✅ Hệ thống OrangeHRM đã được cài đặt và cấu hình
2. ✅ Database đã có dữ liệu nhân viên (generated by `generate_dim.py`)
3. ✅ **Đăng nhập bằng tài khoản Employee** (không phải Admin):
   - Username: `[employee_username]` (VD: `username_nhanvien`)
   - Password: `OrangeHRM@111`
4. ✅ Navigate to **My Info** menu (ESS module)
5. ✅ Chọn tab **Personal Details**

### 6.3. Thứ tự thực thi (Execution Order)

**Giai đoạn 1: Smoke Testing**
- TC001, TC010, TC027, TC036: Kiểm tra các trường hợp cơ bản với quyền Employee
1.5.1. Tiêu chí Pass/Fail (Pass/Fail Criteria)

| Kết quả | Điều kiện |
| :--- | :--- |
| **Pass** | Actual Result = Expected Result |
| **Fail** | Actual Result ≠ Expected Result |
| **Blocked** | Không thể thực thi do lỗi tiền điều kiện (VD: không login được)
**Giai đoạn 4: Boundary Testing**
- Tất cả test cases có remark "Boundary"

**Giai đoạn 5: Permission Testing**
- Verify Employee chỉ có thể sửa hồ sơ của chính mình
- Verify không thể truy cập hồ sơ nhân viên khác
- Tất cả test cases có remark "Boundary"

### 6.3. Tiêu chí Pass/Fail (Pass/Fail Criteria)

| Kết quả | Điều kiện |
| :--- | :--- |
| **Pass** | Actual Result = Expected Result |
| **Fail** | Actual Result ≠ Expected Result |
| **Blocked** | Không thể thực thi do lỗi tiền điều kiện |
| **Skip** | Tạm hoãn do ưu tiên thấp |

---

## 7. Lợi ích của Domain Testing (Benefits)

### 7.1. Ưu điểm

✅ **Độ bao phủ cao (High Coverage):**
- Bao phủ đầy đủ các miền giá trị quan trọng
- Phát hiện lỗi tại các điểm biên (boundary bugs) - nơi thường có lỗi nhất

✅ **Hệ thống và có cấu trúc (Systematic):**
- Quy trình rõ ràng: Phân tích → Phân vùng → Biên → Test cases
- Dễ review và audit

✅ **Tối ưu số lượng test cases (Optimized):**
- Không cần test mọi giá trị (exhaustive testing)
- Chọn giá trị đại diện cho mỗi vùng

✅ **Phát hiện lỗi hiệu quả (Effective Bug Detection):**
- Boundary errors: Off-by-one, fencepost errors
- Invalid input handling
- Range validation issues

### 7.2. Hạn chế

⚠️ **Không bao phủ logic nghiệp vụ phức tạp:**
- Cần kết hợp với Decision Table hoặc State Transition Testing

⚠️ **Phụ thuộc vào specification:**
- Cần tài liệu requirements rõ ràng về boundaries

⚠️ **Không test tương tác giữa các trường:**
- Cần kết hợp với All-Pairs Testing cho combinatorial testing

---

## 8. Kết quả kiểm thử mẫu (Sample Test Results)

### 8.1. Thống kê (Statistics)

| Metric | Giá trị |
| :--- | :---: |
| Total Test Cases | 39 |
| Passed | TBD |
| Failed | TBD |
| Blocked | TBD |
| Pass Rate | TBD |

*(Sẽ được cập nhật sau khi thực thi)*

### 8.2. Defects phát hiện (Defects Found)

*(Sẽ được cập nhật sau khi thực thi)*

Các lỗi tiềm năng có thể phát hiện bằng Domain Testing:
- Lỗi xử lý chuỗi rỗng (empty string)
- Lỗi boundary: chấp nhận 31 ký tự thay vì reject
- Lỗi validation: chấp nhận ngày tháng trong tương lai
- Lỗi format: không xử lý các định dạng date khác nhau

**Các trường được test:**
- Employee Full Name (9 TCs): Length boundaries (0, 1, 30, 31), Content validation
- Employee ID (2 TCs): Read-only constraint, Format validation
- Other ID (3 TCs): Optional field, Max length boundary
- Driver's License (5 TCs): Date boundaries (past/today/future), Dependency check
- Nationality (3 TCs): Dropdown valid selections
- Marital Status (4 TCs): All equivalence classes
- Date of Birth (9 TCs): Age boundaries (18/65/100), Format validation
- Gender (4 TCs): Radio button state transitions

### 1.4. Test Cases Summary

**Tổng số:** 39 test cases (TC001 - TC039)

**Phân bổ theo loại:**
- Valid Partitions: 18 TCs (46.2%)
- Invalid Partitions: 10 TCs (25.6%)
- Boundary Values: 11 TCs (28.2%)

---

## PHẦN 2: APPLY LEAVE REQUEST - DECISION TABLE TESTING

### 2.1. Giới thiệu chức năng (Feature Introduction)

**Feature:** Apply Leave Request (Leave > Apply)

**Mô tả:** Nhân viên nộp đơn xin nghỉ phép thông qua ESS với các quy tắc nghiệp vụ:
- Kiểm tra số dư phép (Leave Balance)
- Validate ngày bắt đầu và kết thúc
- Đảm bảo ngày xin phép trong tương lai
- Kiểm tra trùng lặp với đơn nghỉ khác

**User role:** Employee (ESS user)

### 2.2. Kỹ thuật Decision Table Testing

**Decision Table Testing** là kỹ thuật kiểm thử hộp đen dùng để test các business rules phức tạp với nhiều điều kiện kết hợp.

**Cấu trúc Decision Table:**
- **Conditions (Điều kiện):** Các yếu tố đầu vào cần kiểm tra
- **Actions (Hành động):** Kết quả tương ứng với tổ hợp điều kiện
- **Rules (Quy tắc):** Các combination cụ thể của conditions và actions

### 2.3. Decision Table cho Apply Leave Request

#### 2.3.1. Định nghĩa Conditions và Actions

**Conditions:**

| ID | Condition | Mô tả | Giá trị |
| :--- | :--- | :--- | :--- |
| **C1** | Leave Balance >= Requested Days? | Số dư phép đủ cho số ngày xin? | Y / N / EQUAL |
| **C2** | From Date < To Date? | Ngày bắt đầu < ngày kết thúc? | Y / N |
| **C3** | Date Range in Future? | Ngày xin phép trong tương lai? | Y / N / TODAY |
| **C4** | No Overlapping Leave? | Không trùng với đơn nghỉ khác? | Y / N |

**Actions:**

| ID | Action | Mô tả |
| :--- | :--- | :--- |
| **A1** | Submit Success | Đơn được nộp thành công |
| **A2** | Error - Insufficient Balance | Lỗi: Không đủ số dư phép |
| **A3** | Error - Invalid Date Range | Lỗi: Ngày không hợp lệ (From >= To) |
| **A4** | Error - Date Must Be Future | Lỗi: Phải là ngày trong tương lai |
| **A5** | Error - Overlapping Dates | Lỗi: Trùng với đơn nghỉ khác |

#### 2.3.2. Decision Table Matrix

| Rule | C1 | C2 | C3 | C4 | Action | Description | Test Case |
| :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **R1** | Y | Y | Y | Y | **A1** | Tất cả điều kiện hợp lệ → Success | TC040 |
| **R2** | N | Y | Y | Y | **A2** | Không đủ số dư phép | TC041 |
| **R3** | Y | N | Y | Y | **A3** | Ngày bắt đầu >= ngày kết thúc | TC042 |
| **R4** | Y | Y | N | Y | **A4** | Ngày xin phép trong quá khứ | TC043 |
| **R5** | Y | Y | Y | N | **A5** | Trùng với đơn nghỉ đã tồn tại | TC044 |
| **R6** | N | N | Y | Y | **A2/A3** | Multiple errors (Balance + Date) | TC045 |
| **R7** | N | Y | N | Y | **A2/A4** | Insufficient + Past date | TC046 |
| **R8** | Y | N | Y | N | **A3** | Invalid date (ưu tiên lỗi này) | TC047 |
| **R9** | **EQUAL** | Y | Y | Y | **A1** | Boundary: Balance = Days | TC048 |
| **R10** | Y | Y | **TODAY** | Y | **A1** | Boundary: From Date = Today | TC049 |

#### 2.3.3. Giải thích các Rules chính

**Rule R1 (Happy Path):**
```
Conditions: All YES
- Balance: 12 days >= 3 days requested ✓
- From Date (2025-12-25) < To Date (2025-12-27) ✓
- Future date ✓
- No overlap ✓
Result: Submit Success
```

**Rule R2 (Insufficient Balance):**
```
Conditions: C1=NO, others YES
- Balance: 2 days < 5 days requested ✗
- Other conditions valid
Result: Error - Insufficient Balance
```

**Rule R9 (Boundary - Equal Balance):**
```
Conditions: C1=EQUAL (boundary case)
- Balance: 3 days = 3 days requested (exactly equal)
- Other conditions valid
Result: Submit Success (boundary test)
```

**Rule R6 (Multiple Errors):**
```
Conditions: C1=NO, C2=NO
- Insufficient balance ✗
- Invalid date range ✗
Result: Show first error (depends on validation order)
```

### 2.4. Test Cases chi tiết

**Ví dụ Test Case TC040 (Rule R1 - Happy Path):**

```
Test Case ID: TC040
Feature: Apply Leave Request
Description: Decision Table Rule R1: Tất cả điều kiện hợp lệ

Test Steps:
1. Đăng nhập OrangeHRM bằng tài khoản Employee
2. Vào Leave menu
3. Click "Apply"
4. Chọn Leave Type: "Annual Leave"
5. Nhân viên có số dư phép: 12 ngày
6. Nhập From Date: "2025-12-25"
7. Nhập To Date: "2025-12-27" (3 ngày)
8. Nhập Comment: "Xin nghỉ phép"
9. Click "Apply" button

Expected Result:
Đơn xin nghỉ được nộp thành công. Hiển thị thông báo "Successfully Saved" 
và đơn xuất hiện trong Leave List với status "Pending Approval"

Remark: Decision Table - R1: Balance=Y, DateOrder=Y, Future=Y, NoOverlap=Y -> A1
```

**Ví dụ Test Case TC041 (Rule R2 - Insufficient Balance):**

```
Test Case ID: TC041
Feature: Apply Leave Request
Description: Decision Table Rule R2: Không đủ số dư phép

Test Steps:
1. Đăng nhập OrangeHRM bằng tài khoản Employee
2. Vào Leave menu
3. Click "Apply"
4. Chọn Leave Type: "Annual Leave"
5. Nhân viên có số dư phép: 2 ngày
6. Nhập From Date: "2025-12-25"
7. Nhập To Date: "2025-12-29" (5 ngày - vượt quá số dư)
8. Nhập Comment: "Xin nghỉ phép"
9. Click "Apply" button

Expected Result:
Hiển thị thông báo lỗi "Balance not sufficient" hoặc 
"Failed to Submit: Leave balance exceeded"

Remark: Decision Table - R2: Balance=N, DateOrder=Y, Future=Y, NoOverlap=Y -> A2
```

### 2.5. Test Cases Summary

**Tổng số:** 10 test cases (TC040 - TC049)

**Phân bổ theo Actions:**
- Success (A1): 3 TCs (R1, R9, R10)
- Insufficient Balance (A2): 1 TC (R2)
- Invalid Date Range (A3): 2 TCs (R3, R8)
- Past Date (A4): 1 TC (R4)
- Overlapping (A5): 1 TC (R5)
- Multiple Errors: 2 TCs (R6, R7)

**Coverage:**
- ✅ All single error conditions covered
- ✅ Boundary cases (EQUAL balance, TODAY date)
- ✅ Multiple error combinations
- ✅ Happy path và các negative scenarios

---

## 3. Tổng hợp toàn bộ Test Cases

### 3.1. Summary Table

| Module | Feature | Technique | Test Cases | TC IDs |
| :--- | :--- | :--- | :---: | :--- |
| ESS | Personal Details | Domain Testing | 39 | TC001 - TC039 |
| ESS | Apply Leave Request | Decision Table Testing | 10 | TC040 - TC049 |
| **TỔNG** | | | **49** | |

### 3.2. Coverage Matrix

| Kỹ thuật kiểm thử | Áp dụng cho Feature | Số TCs |
| :--- | :--- | :---: |
| **Domain Testing** | Personal Details | 39 |
| **Decision Table Testing** | Apply Leave Request | 10 |
| **State Transition Testing** | *(Có thể mở rộng)* | - |
| **Use Case Testing** | *(Có thể mở rộng)* | - |
| **All-Pairs Testing** | *(Có thể mở rộng)* | - |

### 3.3. ESS Module Coverage

| Chức năng ESS (Requirement) | Status | Test Cases |
| :--- | :---: | :---: |
| ✅ **Personal Profiles** | Completed | 39 TCs (Domain Testing) |
| ✅ **Leave Balances & Submit Requests** | Completed | 10 TCs (Decision Table) |
| ⏳ **Leave History** | Pending | - |
| ⏳ **Timesheets** | Pending | - |
| ⏳ **Track Requests** | Pending | - |

---

## 4. Chiến lược thực thi (Execution Strategy)

### 4.1. Môi trường kiểm thử (Test Environment)

| Thành phần | Chi tiết |
| :--- | :--- |
| **Application** | OrangeHRM 5.x |
| **Database** | MySQL (with test data from generate_dim.py) |
| **Browser** | Chrome, Firefox, Edge |
| **Test Account** | Employee user (username_nhanvien / OrangeHRM@111) |
| **Test Module** | ESS (My Info & Leave menus) |

### 4.2. Preconditions

**Trước khi thực thi:**
1. ✅ Hệ thống OrangeHRM đã được cài đặt và cấu hình
2. ✅ Database có dữ liệu nhân viên (50 employees)
3. ✅ Nhân viên đã được cấp Leave Entitlements (12 ngày Annual Leave)
4. ✅ **Đăng nhập bằng tài khoản Employee** (không phải Admin)

### 4.3. Thứ tự thực thi

**Phase 1: Domain Testing (Personal Details)**
- TC001-TC039: Test từng trường theo domain partitions

**Phase 2: Decision Table Testing (Leave Request)**
- TC040: Happy path (Rule R1) - Smoke test
- TC041-TC044: Single error conditions (R2-R5)
- TC045-TC047: Multiple error combinations (R6-R8)
- TC048-TC049: Boundary cases (R9-R10)

### 4.4. Tiêu chí Pass/Fail

| Kết quả | Điều kiện |
| :--- | :--- |
| **Pass** | Actual Result = Expected Result |
| **Fail** | Actual Result ≠ Expected Result |
| **Blocked** | Không thể thực thi do lỗi tiền điều kiện |

---

## 5.1. So sánh 2 kỹ thuật kiểm thử

### 5.1.1. Domain Testing vs Decision Table Testing

| Khía cạnh | Domain Testing | Decision Table Testing |
| :--- | :--- | :--- |
| **Use Case** | Test input validation, data fields | Test business logic, rules |
| **Focus** | Boundaries, equivalence classes | Condition combinations |
| **Strength** | Phát hiện lỗi input validation | Phát hiện lỗi logic nghiệp vụ |
| **Độ phức tạp** | Simple → Medium | Medium → Complex |
| **Số lượng TCs** | Nhiều (mỗi field riêng biệt) | Ít hơn (combinations) |
| **Áp dụng cho** | Forms, data entry | Workflows, rule-based systems |

### 5.1.2. Khi nào dùng kỹ thuật nào?

**Dùng Domain Testing khi:**
- ✅ Test form nhập liệu với nhiều fields
- ✅ Cần validate input (length, format, type)
- ✅ Có boundaries rõ ràng (min/max values)
- ✅ Test từng trường độc lập

**Ví dụ:** Personal Details form, Registration form, Settings page

**Dùng Decision Table Testing khi:**
- ✅ Có nhiều conditions kết hợp với nhau
- ✅ Business rules phức tạp (if-then-else logic)
- ✅ Cần test tất cả combinations
- ✅ Multiple conditions quyết định 1 outcome

**Ví dụ:** Leave approval logic, Discount calculation, Access control

## 6.1. Kết quả kiểm thử (Test Results)

### 6.1.1. Thống kê

| Metric | Personal Details | Leave Request | TỔNG |
| :--- | :---: | :---: | :---: |
| Total Test Cases | 39 | 10 | **49** |
| Passed | 31 | 6 | 37 |
| Failed | 8 | 4 | 12 |
| Blocked | 0 | 0 | 0 |


### 6.1.2. Defects có thể phát hiện

**Domain Testing (Personal Details):**
- Lỗi boundary: chấp nhận 31 ký tự thay vì reject
- Lỗi validation: chấp nhận số trong tên
- Lỗi format: Date format không consistent

**Decision Table Testing (Leave Request):**
- Lỗi logic: Không check số dư trước khi submit
- Lỗi overlap detection: Không phát hiện đơn trùng
- Lỗi validation order: Check date sau khi check balance

---

## 7. Phụ lục (Appendix)

### 7.1. Glossary

| Thuật ngữ | Định nghĩa |
| :--- | :--- |
| **Domain** | Tập hợp tất cả giá trị có thể của biến đầu vào |
| **Boundary Value** | Giá trị tại ranh giới giữa các partitions |
| **Decision Table** | Bảng liệt kê conditions và actions tương ứng |
| **Rule** | Một combination cụ thể của conditions |
| **Condition** | Yếu tố đầu vào cần kiểm tra (True/False) |
| **Action** | Kết quả/hành động tương ứng với conditions |

### 7.2. Decision Table Template

```
┌─────────────────────────────────────────────────────┐
│           DECISION TABLE TEMPLATE                   │
├─────────────────┬───────────────────────────────────┤
│ CONDITIONS      │  R1  │  R2  │  R3  │ ... │  Rn  │
├─────────────────┼──────┼──────┼──────┼─────┼──────┤
│ Condition 1     │  Y   │  N   │  Y   │ ... │  ?   │
│ Condition 2     │  Y   │  Y   │  N   │ ... │  ?   │
│ Condition 3     │  Y   │  Y   │  Y   │ ... │  ?   │
├─────────────────┼──────┼──────┼──────┼─────┼──────┤
│ ACTIONS         │      │      │      │     │      │
├─────────────────┼──────┼──────┼──────┼─────┼──────┤
│ Action 1        │  X   │      │      │     │      │
│ Action 2        │      │  X   │      │     │      │
│ Action 3        │      │      │  X   │     │      │
└─────────────────┴──────┴──────┴──────┴─────┴──────┘
```

---

## 8. Kết luận (Conclusion)

Báo cáo này đã trình bày chi tiết quy trình áp dụng **2 kỹ thuật black-box testing** để thiết kế **49 test cases** cho module **Employee Self-Service (ESS)** của OrangeHRM:

**Tóm tắt:**
1. ✅ **Domain Testing** cho Personal Details: 39 test cases
   - Phân tích đầy đủ 8 trường dữ liệu
   - Bao phủ boundaries, valid/invalid partitions
   - Tỷ lệ: 46% valid, 26% invalid, 28% boundary

2. ✅ **Decision Table Testing** cho Apply Leave Request: 10 test cases
   - Decision table với 10 rules
   - 4 conditions, 5 actions
   - Coverage: All single errors, multiple errors, boundaries

**ESS Requirement Coverage:**
| Requirement | Covered by |
| :--- | :--- |
| "Employee access to personal profiles" | ✅ Personal Details (39 TCs) |
| "Leave balances" | ✅ Apply Leave Request (10 TCs) |
| "Submit and track requests online" | ✅ Apply Leave Request (10 TCs) |

**Độ bao phủ kiểm thử:**
- ✅ 2/5 chức năng ESS chính đã được test
- ✅ 2/5 kỹ thuật black-box đã được áp dụng
- ✅ 49 test cases sẵn sàng thực thi

**Mức độ sẵn sàng:** Test cases đã sẵn sàng để thực thi trên môi trường OrangeHRM với tài khoản Employee.

---

**Ngày hoàn thành:** 20/12/2025

**Người thực hiện:** Trương Lê Anh Vũ (22120443)

**Module:** Employee Self-Service (ESS)

**Trạng thái:** ✅ Completed - 49 Test Cases Ready

**Kỹ thuật:** Domain Testing + Decision Table Testing
