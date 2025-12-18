# BÁO CÁO REQUIREMENT 3: FUNCTIONAL TESTING
## OrangeHRM - HR Administration & Performance Management

**Sinh viên:** Lê Hoàng Việt

**MSSV:** 22120430

**Ngày thực hiện:** 19/12/2024  

**Môn học:** Kiểm thử phần mềm

---

## GIỚI THIỆU

### Mục đích
Tài liệu này trình bày chi tiết quá trình thiết kế Test Case cho hệ thống OrangeHRM, áp dụng các kỹ thuật Black-box testing theo quy trình chuẩn:

- **Domain Testing**: Phân vùng tương đương và phân tích giá trị biên (B1-B5)
- **Decision Table Testing**: Bảng quyết định với điều kiện và hành động
- **Use Case Testing**: Kiểm thử dựa trên kịch bản sử dụng

### Phạm vi kiểm thử

| Module | Features | Số Test Cases |
|--------|----------|---------------|
| **HR Administration** | Locations, Job Titles, Skills, Education, Languages, Licenses | 29 |
| **Performance Management** | KPIs, Reviews, Trackers | 17 |
| **Tổng cộng** | | **46** |

---

## **1. Kỹ thuật: Domain Testing (Phân vùng Tương đương & Giá trị biên)**

*Áp dụng quy trình 5 bước (B1-B5) cho các chức năng quản lý HR Administration.*

### **1.1 Module: Locations (Quản lý Địa điểm)**

#### **B1: Xác định biến (Input/Output)**

* **Đầu vào (Inputs):**
  * Tên địa điểm (name)
  * Quốc gia (country)
  * Thành phố (city)
  * Địa chỉ (address)
  * Mã bưu điện (zipCode)
  * Số điện thoại (phone)
* **Đầu ra (Outputs):**
  * Thành công (Success Message)
  * Thông báo lỗi (Error Message)

#### **B2: Xác định điều kiện (Conditions)**

* **Liên quan đến `name` (Input):**
  * **C1:** `1 <= name.length <= 100`
  * **C2:** `name` không được trùng lặp
* **Liên quan đến `country` (Input):**
  * **C3:** `country` phải được chọn (required)
* **Liên quan đến `city` (Input):**
  * **C4:** `0 <= city.length <= 50` (optional)
* **Liên quan đến `phone` (Input):**
  * **C5:** `phone` theo format hợp lệ (chỉ số và dấu +, -, khoảng trắng)
* **Liên quan đến `zipCode` (Input):**
  * **C6:** `0 <= zipCode.length <= 10`

#### **B3: Xác định miền tương đương (Equivalence Classes)**

| Biến | EC ID | Miền | Hợp lệ/Không |
|------|-------|------|--------------|
| name | EC1 | name = "" (rỗng) | Invalid (I) |
| name | EC2 | 1 <= name.length <= 100 | Valid (V) |
| name | EC3 | name.length > 100 | Invalid (I) |
| name | EC4 | name đã tồn tại | Invalid (I) |
| country | EC5 | country không chọn | Invalid (I) |
| country | EC6 | country đã chọn | Valid (V) |
| city | EC7 | city = "" (rỗng) | Valid (V) - optional |
| city | EC8 | 1 <= city.length <= 50 | Valid (V) |
| phone | EC9 | phone format không hợp lệ | Invalid (I) |
| phone | EC10 | phone format hợp lệ | Valid (V) |

#### **B4: Xác định Test Data**

| ID Dữ liệu | name | country | city | phone | EC được phủ |
|------------|------|---------|------|-------|-------------|
| D1 (Valid) | "HCM Office" | Viet Nam | Ho Chi Minh | +84-28-1234567 | EC2, EC6, EC8, EC10 |
| D2 (Boundary Min) | "A" | Viet Nam | "" | "" | EC2, EC6, EC7 |
| D3 (Boundary Max) | "A" * 100 | Viet Nam | HN | "" | EC2, EC6, EC8 |
| D4 (Invalid Empty) | "" | Viet Nam | HCM | "" | EC1 |
| D5 (Invalid Length) | "A" * 101 | Viet Nam | HCM | "" | EC3 |
| D6 (Invalid Country) | "Office" | (không chọn) | HCM | "" | EC5 |
| D7 (Duplicate) | "HCM Office" | Viet Nam | HCM | "" | EC4 |

#### **B5: Test Cases từ Domain Testing - Locations**

| TC ID | Mục đích | Dữ liệu | Kết quả mong đợi | EC kiểm tra |
|-------|----------|---------|------------------|-------------|
| **TC_LOC_D01** | Happy Path - Thêm location hợp lệ | D1 | Thành công | EC2, EC6, EC8, EC10 |
| **TC_LOC_D02** | Biên dưới - Tên 1 ký tự | D2 | Thành công | EC2, EC6, EC7 |
| **TC_LOC_D03** | Biên trên - Tên 100 ký tự | D3 | Thành công | EC2, EC6, EC8 |
| **TC_LOC_D04** | Invalid - Tên rỗng | D4 | Lỗi: "Required" | EC1 |
| **TC_LOC_D05** | Invalid - Tên > 100 ký tự | D5 | Lỗi hoặc cắt bớt | EC3 |
| **TC_LOC_D06** | Invalid - Không chọn Country | D6 | Lỗi: "Required" | EC5 |
| **TC_LOC_D07** | Invalid - Tên trùng lặp | D7 | Lỗi: "Already exists" | EC4 |

---

### **1.2 Module: Job Titles (Quản lý Chức danh)**

#### **B1-B2: Biến và Điều kiện**

* **Inputs:** jobTitle, jobDescription, jobSpecification (file)
* **Conditions:**
  * C1: `1 <= jobTitle.length <= 100`
  * C2: `jobTitle` không trùng lặp
  * C3: `jobDescription.length <= 400` (optional)

#### **B3: Miền tương đương**

| Biến | EC ID | Miền | Hợp lệ |
|------|-------|------|--------|
| jobTitle | EC1 | "" (rỗng) | Invalid |
| jobTitle | EC2 | 1-100 chars | Valid |
| jobTitle | EC3 | > 100 chars | Invalid |
| jobTitle | EC4 | Đã tồn tại | Invalid |
| description | EC5 | <= 400 chars | Valid |
| description | EC6 | > 400 chars | Invalid |

#### **B5: Test Cases - Job Titles**

| TC ID | Mục đích | Test Data | Kết quả mong đợi | EC |
|-------|----------|-----------|------------------|-----|
| **TC_JOB_D01** | Thêm job title hợp lệ | Title: "Senior Developer" | Thành công | EC2, EC5 |
| **TC_JOB_D02** | Title rỗng | Title: "" | Lỗi: Required | EC1 |
| **TC_JOB_D03** | Title trùng lặp | Title: "Staff" (đã có) | Lỗi: Already exists | EC4 |
| **TC_JOB_D04** | Title biên 100 chars | Title: "A" * 100 | Thành công | EC2 |
| **TC_JOB_D05** | Description quá dài | Desc: "A" * 401 | Lỗi hoặc cắt | EC6 |

---

### **1.3 Module: KPIs (Performance Management)**

#### **B1-B2: Biến và Điều kiện**

* **Inputs:** indicator, jobTitle, minRating, maxRating
* **Conditions:**
  * C1: `indicator` không rỗng
  * C2: `jobTitle` phải được chọn
  * C3: `0 <= minRating <= 100`
  * C4: `0 <= maxRating <= 100`
  * C5: `minRating <= maxRating`

#### **B3: Miền tương đương**

| Biến | EC ID | Miền | Hợp lệ |
|------|-------|------|--------|
| indicator | EC1 | "" (rỗng) | Invalid |
| indicator | EC2 | Có giá trị | Valid |
| jobTitle | EC3 | Không chọn | Invalid |
| jobTitle | EC4 | Đã chọn | Valid |
| minRating | EC5 | < 0 | Invalid |
| minRating | EC6 | 0-100 | Valid |
| maxRating | EC7 | < minRating | Invalid |
| maxRating | EC8 | >= minRating | Valid |

#### **B5: Test Cases - KPIs**

| TC ID | Mục đích | Test Data | Kết quả mong đợi | EC |
|-------|----------|-----------|------------------|-----|
| **TC_KPI_D01** | Thêm KPI hợp lệ | Indicator: "Sales Target", Job: "Sales Rep", Min: 0, Max: 100 | Thành công | EC2, EC4, EC6, EC8 |
| **TC_KPI_D02** | Indicator rỗng | Indicator: "" | Lỗi: Required | EC1 |
| **TC_KPI_D03** | Không chọn Job Title | JobTitle: null | Lỗi: Required | EC3 |
| **TC_KPI_D04** | Min > Max | Min: 80, Max: 50 | Lỗi: Invalid range | EC7 |
| **TC_KPI_D05** | Min = Max (biên) | Min: 50, Max: 50 | Thành công | EC6, EC8 |
| **TC_KPI_D06** | Min âm | Min: -10 | Lỗi: Invalid | EC5 |

---

## **2. Kỹ thuật: Decision Table Testing (Bảng Quyết định)**

*Áp dụng quy trình 4 bước cho các logic nghiệp vụ phức tạp.*

### **2.1 Decision Table: Thêm Location**

#### **Bước 1: Xác định Causes & Effects**

* **Causes (Điều kiện):**
  * C1: Name có giá trị?
  * C2: Country đã chọn?
  * C3: Name không trùng?
* **Effects (Kết quả):**
  * E1: Thêm location thành công
  * E2: Hiển thị lỗi "Name required"
  * E3: Hiển thị lỗi "Country required"
  * E4: Hiển thị lỗi "Name exists"

#### **Bước 2-3: Tạo và Rút gọn Bảng Quyết định**

| Conditions | R1 | R2 | R3 | R4 | R5 |
|------------|----|----|----|----|-----|
| C1: Name có giá trị? | T | F | T | T | F |
| C2: Country đã chọn? | T | T | F | T | F |
| C3: Name không trùng? | T | T | T | F | T |
| **Effects** | | | | | |
| E1: Thành công | X | - | - | - | - |
| E2: Lỗi Name required | - | X | - | - | X |
| E3: Lỗi Country required | - | - | X | - | X |
| E4: Lỗi Name exists | - | - | - | X | - |

#### **Bước 4: Test Cases từ Decision Table**

| TC ID | Rule | Input | Expected |
|-------|------|-------|----------|
| **TC_LOC_DT01** | R1 | Name: "Office A", Country: VN, Unique | Thành công |
| **TC_LOC_DT02** | R2 | Name: "", Country: VN | Lỗi: Name required |
| **TC_LOC_DT03** | R3 | Name: "Office B", Country: (không chọn) | Lỗi: Country required |
| **TC_LOC_DT04** | R4 | Name: "Office A" (đã có), Country: VN | Lỗi: Already exists |
| **TC_LOC_DT05** | R5 | Name: "", Country: (không chọn) | Lỗi: Required fields |

---

### **2.2 Decision Table: Thêm KPI**

#### **Bước 1: Causes & Effects**

* **Causes:**
  * C1: Indicator có giá trị?
  * C2: Job Title đã chọn?
  * C3: Min <= Max?
* **Effects:**
  * E1: Thêm KPI thành công
  * E2: Lỗi "Indicator required"
  * E3: Lỗi "Job Title required"
  * E4: Lỗi "Invalid rating range"

#### **Bước 2-3: Bảng Quyết định**

| Conditions | R1 | R2 | R3 | R4 |
|------------|----|----|----|----|
| C1: Indicator có giá trị? | T | F | T | T |
| C2: Job Title đã chọn? | T | T | F | T |
| C3: Min <= Max? | T | T | T | F |
| **Effects** | | | | |
| E1: Thành công | X | - | - | - |
| E2: Lỗi Indicator | - | X | - | - |
| E3: Lỗi Job Title | - | - | X | - |
| E4: Lỗi Range | - | - | - | X |

#### **Bước 4: Test Cases**

| TC ID | Rule | Input | Expected |
|-------|------|-------|----------|
| **TC_KPI_DT01** | R1 | Indicator: "KPI1", Job: "Dev", Min: 0, Max: 100 | Thành công |
| **TC_KPI_DT02** | R2 | Indicator: "", Job: "Dev" | Lỗi: Required |
| **TC_KPI_DT03** | R3 | Indicator: "KPI", Job: (không chọn) | Lỗi: Required |
| **TC_KPI_DT04** | R4 | Indicator: "KPI", Job: "Dev", Min: 100, Max: 50 | Lỗi: Invalid range |

---

### **2.3 Decision Table: Quản lý Performance Review**

#### **Causes & Effects**

* **Causes:**
  * C1: Employee đã chọn?
  * C2: Supervisor đã chọn?
  * C3: Start Date hợp lệ?
  * C4: End Date >= Start Date?
* **Effects:**
  * E1: Tạo review thành công
  * E2-E5: Các lỗi tương ứng

#### **Bảng Quyết định**

| Conditions | R1 | R2 | R3 | R4 | R5 |
|------------|----|----|----|----|-----|
| C1: Employee chọn? | T | F | T | T | T |
| C2: Supervisor chọn? | T | T | F | T | T |
| C3: Start Date OK? | T | T | T | F | T |
| C4: End >= Start? | T | T | T | T | F |
| **Effects** | | | | | |
| E1: Thành công | X | - | - | - | - |
| E2: Lỗi Employee | - | X | - | - | - |
| E3: Lỗi Supervisor | - | - | X | - | - |
| E4: Lỗi Start Date | - | - | - | X | - |
| E5: Lỗi Date Range | - | - | - | - | X |

#### **Test Cases**

| TC ID | Rule | Input | Expected |
|-------|------|-------|----------|
| **TC_REV_DT01** | R1 | Employee: John, Supervisor: Admin, Start: 2025-01-01, End: 2025-12-31 | Thành công |
| **TC_REV_DT02** | R2 | Employee: (không chọn) | Lỗi: Required |
| **TC_REV_DT03** | R3 | Supervisor: (không chọn) | Lỗi: Required |
| **TC_REV_DT04** | R4 | Start Date: invalid | Lỗi: Invalid date |
| **TC_REV_DT05** | R5 | Start: 2025-12-31, End: 2025-01-01 | Lỗi: Invalid range |

---

## **3. Kỹ thuật: Use Case Testing (Kiểm thử Kịch bản)**

*Áp dụng quy trình 3 bước cho các Use Case chính.*

### **3.1 Use Case: Quản lý Locations**

#### **Bước 1: Xác định Use Case**

* **Use Case:** Quản lý địa điểm làm việc
* **Actor:** HR Admin
* **Luồng chính (Basic Flow):** Thêm location mới với đầy đủ thông tin
* **Luồng phụ 1:** Chỉ điền các trường bắt buộc
* **Luồng phụ 2:** Tìm kiếm location
* **Luồng phụ 3:** Xóa location
* **Luồng ngoại lệ 1:** Thiếu thông tin bắt buộc
* **Luồng ngoại lệ 2:** Location đã tồn tại

#### **Bước 2: Dẫn xuất Scenarios**

| Scenario | Mô tả |
|----------|-------|
| S1 | Happy Path - Thêm location đầy đủ thông tin |
| S2 | Thêm location chỉ với fields bắt buộc |
| S3 | Tìm kiếm location theo tên |
| S4 | Tìm kiếm không có kết quả |
| S5 | Xóa location thành công |
| S6 | Xóa location đang được sử dụng |
| S7 | Thêm location thiếu Name |
| S8 | Thêm location thiếu Country |

#### **Bước 3: Test Cases từ Use Case**

| TC ID | Scenario | Steps | Expected |
|-------|----------|-------|----------|
| **TC_LOC_UC01** | S1 | 1. Login as Admin<br>2. Go to Admin > Organization > Locations<br>3. Click Add<br>4. Fill Name, Country, City, Address<br>5. Click Save | Location thêm thành công |
| **TC_LOC_UC02** | S2 | 1. Click Add<br>2. Fill Name, Country only<br>3. Click Save | Location thêm thành công |
| **TC_LOC_UC03** | S3 | 1. Go to Locations<br>2. Enter search term<br>3. Click Search | Hiển thị kết quả phù hợp |
| **TC_LOC_UC04** | S4 | 1. Search với tên không tồn tại | "No Records Found" |
| **TC_LOC_UC05** | S5 | 1. Select location<br>2. Click Delete<br>3. Confirm | Location bị xóa |
| **TC_LOC_UC06** | S7 | 1. Click Add<br>2. Leave Name empty<br>3. Click Save | Lỗi validation |

---

### **3.2 Use Case: Quản lý Job Titles**

#### **Scenarios**

| Scenario | Mô tả |
|----------|-------|
| S1 | Thêm job title mới |
| S2 | Thêm job title với description |
| S3 | Thêm job title với file specification |
| S4 | Xem danh sách job titles |
| S5 | Xóa job title |
| S6 | Xóa job title đang được gán cho employee |

#### **Test Cases**

| TC ID | Scenario | Steps | Expected |
|-------|----------|-------|----------|
| **TC_JOB_UC01** | S1 | 1. Go to Admin > Job > Job Titles<br>2. Click Add<br>3. Enter Title<br>4. Save | Thành công |
| **TC_JOB_UC02** | S2 | 1. Add Title + Description<br>2. Save | Thành công |
| **TC_JOB_UC03** | S4 | 1. Navigate to Job Titles | Hiển thị danh sách |
| **TC_JOB_UC04** | S5 | 1. Select job title<br>2. Delete | Xóa thành công |

---

### **3.3 Use Case: Quản lý KPIs**

#### **Scenarios**

| Scenario | Mô tả |
|----------|-------|
| S1 | Thêm KPI với đầy đủ thông tin |
| S2 | Xem danh sách KPIs |
| S3 | Tìm kiếm KPI theo Job Title |
| S4 | Xóa KPI |
| S5 | Sửa KPI |

#### **Test Cases**

| TC ID | Scenario | Steps | Expected |
|-------|----------|-------|----------|
| **TC_KPI_UC01** | S1 | 1. Go to Performance > Configure > KPIs<br>2. Click Add<br>3. Fill Indicator, Job Title, Min, Max<br>4. Save | KPI thêm thành công |
| **TC_KPI_UC02** | S2 | 1. Navigate to KPIs page | Hiển thị danh sách |
| **TC_KPI_UC03** | S3 | 1. Select Job Title filter<br>2. Search | Hiển thị KPIs của job đó |
| **TC_KPI_UC04** | S4 | 1. Select KPI<br>2. Delete | Xóa thành công |

---

### **3.4 Use Case: Quản lý Performance Reviews**

#### **Scenarios**

| Scenario | Mô tả |
|----------|-------|
| S1 | Tạo review mới cho employee |
| S2 | Xem danh sách reviews |
| S3 | Tìm kiếm review theo employee |
| S4 | Tìm kiếm review theo status |
| S5 | Activate review |

#### **Test Cases**

| TC ID | Scenario | Steps | Expected |
|-------|----------|-------|----------|
| **TC_REV_UC01** | S1 | 1. Go to Performance > Manage Reviews<br>2. Click Add<br>3. Fill Employee, Supervisor, Dates<br>4. Save | Review tạo thành công |
| **TC_REV_UC02** | S2 | 1. Navigate to Manage Reviews | Hiển thị danh sách |
| **TC_REV_UC03** | S3 | 1. Enter employee name<br>2. Search | Hiển thị reviews của employee |
| **TC_REV_UC04** | S4 | 1. Select status filter<br>2. Search | Hiển thị reviews theo status |

---

### **3.5 Use Case: Quản lý Skills**

#### **Scenarios & Test Cases**

| TC ID | Scenario | Steps | Expected |
|-------|----------|-------|----------|
| **TC_SKL_UC01** | Thêm skill mới | 1. Go to Admin > Qualifications > Skills<br>2. Add skill<br>3. Save | Thành công |
| **TC_SKL_UC02** | Xem danh sách | 1. Navigate to Skills | Hiển thị list |
| **TC_SKL_UC03** | Xóa skill | 1. Select<br>2. Delete | Xóa thành công |

---

### **3.6 Use Case: Quản lý Education Levels**

| TC ID | Scenario | Steps | Expected |
|-------|----------|-------|----------|
| **TC_EDU_UC01** | Thêm education level | 1. Go to Education<br>2. Add<br>3. Save | Thành công |
| **TC_EDU_UC02** | Xem danh sách | 1. Navigate | Hiển thị list |

---

### **3.7 Use Case: Quản lý Languages**

| TC ID | Scenario | Steps | Expected |
|-------|----------|-------|----------|
| **TC_LNG_UC01** | Thêm language | 1. Go to Languages<br>2. Add<br>3. Save | Thành công |
| **TC_LNG_UC02** | Xem danh sách | 1. Navigate | Hiển thị list |

---

### **3.8 Use Case: Quản lý Licenses**

| TC ID | Scenario | Steps | Expected |
|-------|----------|-------|----------|
| **TC_LIC_UC01** | Thêm license | 1. Go to Licenses<br>2. Add<br>3. Save | Thành công |
| **TC_LIC_UC02** | Xem danh sách | 1. Navigate | Hiển thị list |

---

### **3.9 Use Case: My Trackers & Employee Trackers**

| TC ID | Scenario | Steps | Expected |
|-------|----------|-------|----------|
| **TC_TRK_UC01** | Xem My Trackers | 1. Go to Performance > My Trackers | Hiển thị trackers của user |
| **TC_TRK_UC02** | Xem Employee Trackers | 1. Go to Performance > Employee Trackers | Hiển thị danh sách |
| **TC_TRK_UC03** | Tìm kiếm tracker | 1. Enter employee name<br>2. Search | Hiển thị kết quả |

---

## **4. Tổng hợp Test Cases (45 Test Cases)**

### **4.1 Phân bố theo Kỹ thuật**

| Kỹ thuật | Số lượng | Tỷ lệ |
|----------|----------|-------|
| Domain Testing | 18 | 40% |
| Decision Table | 14 | 31% |
| Use Case Testing | 13 | 29% |
| **Tổng** | **45** | 100% |

### **4.2 Phân bố theo Module**

| Module | Số lượng |
|--------|----------|
| HR Administration - Locations | 12 |
| HR Administration - Job Titles | 9 |
| HR Administration - Skills/Education/Languages/Licenses | 8 |
| Performance Management - KPIs | 10 |
| Performance Management - Reviews | 9 |
| Performance Management - Trackers | 3 |
| **Tổng** | **45** |

### **4.3 Danh sách Test Cases đầy đủ**

| # | TC ID | Module | Technique | Test Case |
|---|-------|--------|-----------|-----------|
| 1 | TC_LOC_D01 | Locations | Domain | Add location - valid data |
| 2 | TC_LOC_D02 | Locations | Domain | Add location - min name (1 char) |
| 3 | TC_LOC_D03 | Locations | Domain | Add location - max name (100 chars) |
| 4 | TC_LOC_D04 | Locations | Domain | Add location - empty name |
| 5 | TC_LOC_D05 | Locations | Domain | Add location - name > 100 chars |
| 6 | TC_LOC_D06 | Locations | Domain | Add location - no country |
| 7 | TC_LOC_D07 | Locations | Domain | Add location - duplicate name |
| 8 | TC_LOC_DT01 | Locations | Decision Table | Rule 1 - All valid |
| 9 | TC_LOC_DT02 | Locations | Decision Table | Rule 2 - Name empty |
| 10 | TC_LOC_DT03 | Locations | Decision Table | Rule 3 - Country not selected |
| 11 | TC_LOC_UC01 | Locations | Use Case | Add location full info |
| 12 | TC_LOC_UC02 | Locations | Use Case | Search location |
| 13 | TC_JOB_D01 | Job Titles | Domain | Add job title - valid |
| 14 | TC_JOB_D02 | Job Titles | Domain | Add job title - empty |
| 15 | TC_JOB_D03 | Job Titles | Domain | Add job title - duplicate |
| 16 | TC_JOB_D04 | Job Titles | Domain | Add job title - max length |
| 17 | TC_JOB_DT01 | Job Titles | Decision Table | All conditions valid |
| 18 | TC_JOB_DT02 | Job Titles | Decision Table | Title empty |
| 19 | TC_JOB_UC01 | Job Titles | Use Case | Add job title |
| 20 | TC_JOB_UC02 | Job Titles | Use Case | View job titles list |
| 21 | TC_JOB_UC03 | Job Titles | Use Case | Delete job title |
| 22 | TC_SKL_UC01 | Skills | Use Case | Add skill |
| 23 | TC_SKL_UC02 | Skills | Use Case | View skills |
| 24 | TC_SKL_D01 | Skills | Domain | Add skill - empty name |
| 25 | TC_EDU_UC01 | Education | Use Case | Add education |
| 26 | TC_EDU_D01 | Education | Domain | Add education - empty |
| 27 | TC_LNG_UC01 | Languages | Use Case | Add language |
| 28 | TC_LNG_D01 | Languages | Domain | Add language - empty |
| 29 | TC_LIC_UC01 | Licenses | Use Case | Add license |
| 30 | TC_KPI_D01 | KPIs | Domain | Add KPI - valid |
| 31 | TC_KPI_D02 | KPIs | Domain | Add KPI - empty indicator |
| 32 | TC_KPI_D03 | KPIs | Domain | Add KPI - no job title |
| 33 | TC_KPI_D04 | KPIs | Domain | Add KPI - min > max |
| 34 | TC_KPI_D05 | KPIs | Domain | Add KPI - min = max |
| 35 | TC_KPI_DT01 | KPIs | Decision Table | All valid |
| 36 | TC_KPI_DT02 | KPIs | Decision Table | Indicator empty |
| 37 | TC_KPI_DT03 | KPIs | Decision Table | Job Title not selected |
| 38 | TC_KPI_UC01 | KPIs | Use Case | Add KPI |
| 39 | TC_KPI_UC02 | KPIs | Use Case | View KPIs |
| 40 | TC_REV_DT01 | Reviews | Decision Table | Create review - valid |
| 41 | TC_REV_DT02 | Reviews | Decision Table | No employee selected |
| 42 | TC_REV_DT03 | Reviews | Decision Table | Invalid date range |
| 43 | TC_REV_UC01 | Reviews | Use Case | Create review |
| 44 | TC_REV_UC02 | Reviews | Use Case | Search reviews |
| 45 | TC_TRK_UC01 | Trackers | Use Case | View trackers |

---

## **5. Kết luận**

Tài liệu này đã thiết kế **45 Test Cases** cho hệ thống OrangeHRM sử dụng 3 kỹ thuật Black-box testing chính:

1. **Domain Testing (40%)**: Kiểm tra các giá trị biên và phân vùng tương đương
2. **Decision Table (31%)**: Kiểm tra các tổ hợp điều kiện logic
3. **Use Case Testing (29%)**: Kiểm tra các luồng nghiệp vụ thực tế

Các test cases được thiết kế theo quy trình chuẩn, đảm bảo coverage đầy đủ cho các module HR Administration và Performance Management.
