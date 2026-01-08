# BÁO CÁO REQUIREMENT 4: GUI TESTING

## Thông tin cá nhân

| **Thông tin** | **Chi tiết** |
| :--- | :--- |
| **Môn học** | Kiểm thử phần mềm (Software Testing) |
| **Đồ án** | OrangeHRM Case Study |
| **Sinh viên** | Trương Lê Anh Vũ |
| **MSSV** | 22120443 |
| **Nhóm** | 13 |

---

## Thông tin nhóm

| MSSV     | Họ và Tên        | Module                                                      | Feature / Work                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| -------- | ---------------- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 22120376 | Nguyễn Đức Toàn  | Leave Management; Recruitment - Applicant Tracking          | GUI Testing: Xây dựng và kiểm tra checklist (98 items) cho module Leave Management và Recruitment với 2 GUI (Leave List, Candidates); thực hiện Cross-Browser trên 3 trình duyệt (Chrome, Firefox, Edge) sử dụng BrowserStack. <br> Automation Testing: Automation Testing: Xây dựng kịch bản kiểm thử tự động bằng Selenium WebDriver (Python) cho 49 test cases thuộc 2 module Leave Management và Recruitment (Gửi yêu cầu nghỉ phép , cấu hình loại nghỉ phép, quản lý số lượng ngày phép, Quy trình tuyển dụng từ lúc nộp hồ sơ, phỏng vấn đến khi được tuyển dụng), áp dụng kỹ thuật Data-Driven, Assertion, thực thi trên 3 trình duyệt (Chrome, Firefox, Edge) |
| 22120430 | Lê Hoàng Việt    | HR Administration; Performance Management                   | GUI Testing: Xây dựng và kiểm tra checklist (124 items) cho module Locations và KPIs; thực hiện Cross-Browser Testing trên 3 nền tảng (Windows, macOS, Android) sử dụng BrowserStack. <br> Automation Testing: Xây dựng kịch bản kiểm thử tự động bằng Selenium WebDriver (Python) cho 47 test cases (Locations, Job Titles, Skills, KPIs, Reviews...), áp dụng kỹ thuật Data-Driven, Assertion và thực thi song song trên 3 trình duyệt (Chrome, Firefox, Edge).                                                                                                                                                                                                      |
| 22120434 | Lê Thành Vinh    | PIM - Personnel Information Management; Time and Attendance | GUI Testing: Xây dựng và kiểm tra checklist (172 items) cho module PIM và Time and Attendance với 3 GUI (Add Employee, Employee Timesheets, My Timesheets); thực hiện Cross-Browser trên 3 trình duyệt (Chrome, Firefox, Edge). <br> Automation Testing: Xây dựng và thực thi kiểm thử tự động sử dụng Pytest kết hợp Selenium cho 57 test case (Thêm mới nhân viên và tài khoản, quản lý quy trình timesheet: tạo mới, gửi, duyệt, từ chối), áp dụng kỹ thuật Data-Driven, Assertion, thực thi trên 3 trình duyệt (Chrome, Firefox, Edge).                                                                                                                            |
| 22120443 | Trương Lê Anh Vũ | Reporting and Analytics; ESS - Employee Self-Service        | GUI Testing: Xây dựng checklist (108 items) và thực hiện kiểm thử giao diện (thực hiện Cross-Browser) cho chức năng Báo cáo nhân sự và Thông tin cá nhân (OrangeHRM) trên 3 môi trường trình duyệt khác nhau (Chrome, Firefox, Edge). <br> Automation Testing: Xây dựng và thực thi kiểm thử tự động sử dụng Java (TestNG) kết hợp Selenium cho 49 test case (Phân hệ Báo cáo & Phân tích: lọc và xuất dữ liệu; Phân hệ ESS: quản lý hồ sơ cá nhân, quy trình nghỉ phép: đăng ký, kiểm tra số dư), áp dụng kỹ thuật Data-Driven, Assertion, thực thi trên 3 trình duyệt (Chrome, Firefox, Edge).                                                                                   |

---

## Chi tiết chức năng và màn hình được phân công:
1.  **Reporting & Analytics** (GUI: Employee Reports)
2.  **Employee Self-Service (ESS)** (GUI: My Info - Personal Details)

---

## 1. Giới thiệu (Introduction)
Báo cáo này ghi lại quy trình Kiểm thử Giao diện (GUI Testing) được thực hiện trên hệ thống OrangeHRM nhằm đảm bảo tính nhất quán (Consistency), tính tiện dụng (Usability) và khả năng hiển thị đáp ứng (Responsiveness) của giao diện người dùng trên đa nền tảng.

Checklist được sử dụng cho quá trình kiểm thử bao gồm 31 tiêu chí, bao quát các khía cạnh về: Bố cục (Layout), Phông chữ (Fonts), Điều hướng (Navigation), Màu sắc (Color Scheme) và các thành phần Form/Table.

## 2. Thiết lập môi trường kiểm thử (Testing Environment Setup)

Để đảm bảo kết quả kiểm thử khách quan và chính xác trên các hệ điều hành khác nhau, em đã sử dụng **BrowserStack** - nền tảng kiểm thử thực tế trên đám mây.

### 2.1. Công cụ & Cấu hình
* **Công cụ kiểm thử:** BrowserStack (Live Testing).
* **Phương thức kết nối:** Sử dụng **BrowserStack Local** để thiết lập đường hầm bảo mật (tunnel) kết nối từ Cloud Server về máy localhost (`http://localhost:8080`).
* **Cấu hình hiển thị:** Độ phân giải mặc định của thiết bị, Zoom 100%.

### 2.2. Các môi trường được chọn
Em đã lựa chọn 3 môi trường tiêu biểu đại diện cho các hệ điều hành phổ biến nhất hiện nay:

1.  **Desktop (Windows):** Windows 11 - Google Chrome 143 (Phiên bản mới nhất).
2.  **Desktop (macOS):** macOS Sonoma - Safari 17.3 (Đại diện cho WebKit Engine).
3.  **Mobile (Android):** Samsung Galaxy S23 - Chrome Mobile (Kiểm tra Responsive).

## 3. Quy trình thực hiện (Testing Process)
Với mỗi chức năng được phân công (Reporting & ESS), quy trình kiểm thử diễn ra như sau:
1.  Khởi tạo phiên làm việc (Session) trên BrowserStack với từng môi trường.
2.  Truy cập vào màn hình đích (`PIM > Reports` và `My Info`).
3.  Đối chiếu từng thành phần giao diện với checklist.
4.  Thực hiện các thao tác tương tác (Search, Hover, Input) để phát hiện lỗi tiềm ẩn.
5.  Thực hiện thao tác resize (trên Desktop) hoặc xoay màn hình (trên Mobile) để kiểm tra độ co giãn.
6.  Chụp ảnh minh chứng và ghi nhận lỗi.

---

## 4. Kết quả kiểm thử & Hình ảnh (Test Results & Screenshots)

### 4.1. GUI 1: Reporting - Employee Reports
Màn hình danh sách báo cáo, bao gồm thanh tìm kiếm và bảng dữ liệu (Data Grid).

**Hình ảnh minh chứng Cross-Browser:**

| Môi trường | Hình ảnh |
| :--- | :--- |
| **Windows 11 (Chrome)** | ![Windows 11 Report](../images/win11-report.png) |
| **macOS Sonoma (Safari)** | ![macOS Sonoma Report](../images/macos-sonoma-report.png) |
| **Samsung S23 (Mobile)** | ![Android S23 Report](../images/android-s23-chrome-report.png) |

**Quan sát & Đánh giá:**

* **Hiển thị trên Desktop (Windows & macOS):**
    * Bố cục đồng nhất giữa Chrome và Safari.
    * **Vấn đề (Issue):** Khi hover chuột vào các icon tác vụ (Sửa/Xóa) ở cột *Actions*, hệ thống không hiển thị Tooltip hướng dẫn, gây khó hiểu cho người dùng mới.
    * **Vấn đề (Issue):** Kích thước font chữ mặc định (12px) khá nhỏ, khó đọc trên màn hình độ phân giải cao.

* **Hiển thị trên Mobile (Samsung S23):**
    * **Responsive Tốt:** Cột `Report Name` tự động xuống dòng (Text Wrap) khi tên dài, không bị lỗi tràn màn hình.
    * Form tìm kiếm xếp chồng (Stacking) hợp lý.

---

### 4.2. GUI 2: ESS - My Info (Personal Details)
Màn hình thông tin cá nhân, bao gồm nhiều Form nhập liệu, Datepicker và Avatar.

**Hình ảnh minh chứng Cross-Browser:**

| Môi trường | Hình ảnh |
| :--- | :--- |
| **Windows 11 (Chrome)** | ![Windows 11 My Info](../images/win11-myinfo.png) |
| **macOS Sonoma (Safari)** | ![macOS Sonoma My Info](../images/macos-sonoma-myinfo.png) |
| **Samsung S23 (Mobile)** | ![Android S23 My Info](../images/android-s23-chrome-myinfo.png) |

**Quan sát & Đánh giá:**

* **Hiển thị trên Desktop (Windows & macOS):**
    * Giao diện hiển thị tốt, pixel-perfect giữa hai nền tảng.
    * Các cạnh Input field và Button trên Safari được render sắc nét, bo góc đúng thiết kế.

* **Hiển thị trên Mobile (Samsung S23):**
    * **Responsive Tốt:** Các trường thông tin chuyển về bố cục 1 cột (Single column), menu bên trái thu gọn thành Hamburger icon.
    * **Vấn đề thao tác (Usability):** Các icon lịch (Datepicker) hiển thị khá nhỏ và nằm sát mép input, gây khó khăn khi thao tác chạm (Touch) chính xác.

---

## 5. Kết luận & Đề xuất (Conclusion & Recommendations)

Quá trình kiểm thử cho thấy hệ thống OrangeHRM có mức độ tương thích trình duyệt (Cross-browser compatibility) tốt và khả năng Responsive ổn định. Tuy nhiên, tồn tại một số vấn đề ảnh hưởng đến Trải nghiệm người dùng (UX) và Tính tiện dụng (Usability) cần được khắc phục:

**Các vấn đề tìm thấy (Defects Found):**

1.  **Vấn đề hiển thị (Visual & Layout):**
    * Kích thước phông chữ mặc định (`0.75rem` ~ 12px) quá nhỏ so với tiêu chuẩn web hiện đại, gây khó đọc.
    * Hệ thống thiếu chế độ tối (Dark Mode), gây mỏi mắt trong điều kiện thiếu sáng.

2.  **Vấn đề tương tác (Interaction & Usability):**
    * **Thiếu Tooltip:** Các icon hành động (Edit/Delete) không hiện văn bản hướng dẫn khi hover.
    * **Xử lý Input:** Hệ thống không tự động loại bỏ khoảng trắng thừa (trim whitespace) trong ô tìm kiếm, dẫn đến kết quả sai lệch.
    * **Touch Targets:** Trên Mobile, các icon Datepicker có vùng chạm quá nhỏ, khó thao tác.
3.  **Vấn đề tính nhất quán dữ liệu (Data Consistency & Feedback):**
    * **Lỗi cập nhật trạng thái:** Tại màn hình *Personal Details*, sau khi nhấn *Save* và nhận thông báo thành công, dữ liệu trên giao diện không tự động thay đổi (refresh). Người dùng bắt buộc phải tải lại trang thủ công để thấy thông tin mới cập nhật (Bug ID: B006).

**Đề xuất cải tiến (Recommendations):**
* Tăng kích thước phông chữ cơ sở lên tối thiểu **14px**.
* Bổ sung thuộc tính `title` hoặc Tooltip component cho các nút icon.
* Thực hiện `trim()` dữ liệu đầu vào tại các ô tìm kiếm.
* Tăng padding cho các nút bấm/icon trên giao diện Mobile để tối ưu hóa cho thao tác cảm ứng.
* Cải thiện cơ chế AJAX để tự động render lại dữ liệu form sau khi nhận response thành công từ server.