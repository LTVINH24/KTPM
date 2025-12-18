# **Tài liệu Thiết kế Test Case cho Hệ thống CineBook (Chi tiết theo quy trình)**

Tài liệu này trình bày các trường hợp kiểm thử (Test Case) mẫu cho hệ thống CineBook, được thiết kế bằng cách áp dụng 5 kỹ thuật Black-box testing, bám sát các bước quy trình trong bài giảng.

## **1\. Kỹ thuật: Phân vùng Tương đương & Giá trị biên (Domain & Boundary Testing)**

*Áp dụng quy trình 5 bước (B1-B5) và các quy tắc chọn TC (từ slide 21-23).*

### **B1: Xác định biến (in/out)**

* **Đầu vào (Inputs):**  
  * Số lượng (qty)  
  * Email (email)  
  * Số điện thoại (SĐT)  
  * Nhóm tuổi (ageGroup)  
  * Ngày sinh (DOB)  
  * Điều kiện sinh viên (hasStudentID)  
* **Đầu ra (Outputs):**  
  * Chấp nhận (Success / Allow)  
  * Thông báo lỗi (Error Message)

### **B2: Xác định điều kiện (đk)**

* **Liên quan đến `qty` (Input):**  
  * **C1:** `1 <= qty <= 10`  
* **Liên quan đến `email` (Input):**  
  * **C2:** `email local part >= 3`  
  * **C3:** `email` phải chứa `@`  
  * **C4:** `email domain` phải chứa `.` (vd: .com, .vn)  
* **Liên quan đến `SĐT` (Input):**  
  * **C5:** `SĐT` phải theo format Việt Nam `^(03|05|07|08|09)\d{8}$`  
* **Liên quan đến `ageGroup`, `DOB` (Input):**  
  * **C6:** `ageGroup` phải khớp với tuổi tính từ `DOB`  
* **Liên quan đến `ageGroup`, `hasStudentID` (Input):**  
  * **C7:** NẾU `ageGroup` \= "Sinh viên" THÌ `hasStudentID` \= `true`  
* **Liên quan đến `Success Message` (Output):**  
  * **C8:** Tất cả các điều kiện (C1-C7) đều hợp lệ (Valid).  
* **Liên quan đến `Error Message` (Output):**  
  * **C9:** Bất kỳ điều kiện nào (C1-C7) không hợp lệ (Invalid).

### **B3: Xác định miền tương đương (EC)**

* **Từ C1 (qty):**  
  * EC1: qty \< 1 (Invalid, I)  
  * EC2: 1 \<= qty \<= 10 (Valid, V)  
  * EC3: qty \> 10 (Invalid, I)  
* **Từ C2-C4 (email):**  
  * EC4: local part \< 3 (Invalid, I)  
  * EC5: thiếu `@` (Invalid, I)  
  * EC6: domain thiếu `.` (Invalid, I)  
  * EC7: Hợp lệ (Valid, V)  
* **Từ C5 (SĐT):**  
  * EC8: Sai đầu số (Invalid, I)  
  * EC9: Sai độ dài (Invalid, I)  
  * EC10: Hợp lệ (Valid, V)  
* **Từ C6 (Logic tuổi):**  
  * EC11: `ageGroup` không khớp `DOB` (Invalid, I)  
  * EC12: `ageGroup` khớp `DOB` (Valid, V)  
* **Từ C7 (Logic SV):**  
  * EC13: `ageGroup`\="SV" VÀ `hasStudentID`\=false (Invalid, I)  
  * EC14: `ageGroup`\="SV" VÀ `hasStudentID`\=true (Valid, V)  
  * EC15: `ageGroup`\!="SV" (Valid, V)  
* **C8 (Output Success):**  
  * **EC16:** Thành công (V)  
* **C9 (Output Error):**  
  * **EC17:** Lỗi (I)

### **B4: Xác định Test Data (Bảng Phủ Lớp Tương đương)**

(Đây là bước tiền đề, xác định dữ liệu thô (raw data) để phủ *từng* EC. Các giá trị khác được giả định là Hợp lệ (Valid Default \- VD) để cô lập EC cần test).

| ID Dữ liệu | qty | email | SĐT | ageGroup | DOB | hasStudentID | EC được phủ (Mục tiêu) |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **D1 (Valid Set 1\)** | 5 | valid@domain.com | 0901234567 | "Người lớn" | 30 tuổi | false | EC2, EC7, EC10, EC12, EC15 |
| **D2 (Valid Set 2\)** | 1 | abc@domain.com | 0351234567 | "Sinh viên" | 20 tuổi | true | EC2, EC7, EC10, EC12, EC14 |
| **D3 (Valid Set 3\)** | 10 | valid@domain.com | 0901234567 | "Người lớn" | 30 tuổi | false | EC2 |
| **D4 (Invalid qty \<)** | **0** | valid@domain.com | 0901234567 | "Người lớn" | 30 tuổi | false | EC1 |
| **D5 (Invalid qty \>)** | **11** | valid@domain.com | 0901234567 | "Người lớn" | 30 tuổi | false | EC3 |
| **D6 (Invalid email \<3)** | 5 | **ab@domain.com** | 0901234567 | "Người lớn" | 30 tuổi | false | EC4 |
| **D7 (Invalid email no @)** | 5 | **invalid-email.com** | 0901234567 | "Người lớn" | 30 tuổi | false | EC5 |
| **D8 (Invalid email no .)** | 5 | **invalid@domain** | 0901234567 | "Người lớn" | 30 tuổi | false | EC6 |
| **D9 (Invalid SĐT prefix)** | 5 | valid@domain.com | **0123456789** | "Người lớn" | 30 tuổi | false | EC8 |
| **D10 (Invalid SĐT len)** | 5 | valid@domain.com | **090123456** | "Người lớn" | 30 tuổi | false | EC9 |
| **D11 (Invalid age logic)** | 5 | valid@domain.com | 0901234567 | "Sinh viên" | **30 tuổi** | true | EC11 |
| **D12 (Invalid SV card)** | 5 | valid@domain.com | 0901234567 | "Sinh viên" | 20 tuổi | **false** | EC13 |

### **B5: Xác định Test Cases Tối thiểu**

(Bảng này gom nhóm các Test Data (từ B4) lại theo quy tắc: 1 TC cho Valid (Happy Path) và 1 TC cho *mỗi* Invalid)

| TC ID | Mục đích (Tên TC) | Dữ liệu sử dụng (Từ B4) | Xử lý (Kết quả mong đợi) | Lớp Tương đương (EC) được kiểm tra |
| :---- | :---- | :---- | :---- | :---- |
| **TC1** | **Happy Path (Valid Case)** | **D1** | Thành công | **EC2, EC7, EC10, EC12, EC15** (Gộp nhiều Lớp Hợp lệ) |
| **TC2** | Happy Path (SV, Biên) | **D2** | Thành công | **EC2, EC7, EC10, EC12, EC14** (Gộp nhiều Lớp Hợp lệ \+ Biên) |
| **TC3** | Valid (Biên qty max) | **D3** | Thành công | **EC2** (Chỉ test biên còn lại) |
| **TC4** | Invalid (qty \< min) | **D4** | Lỗi: "Số lượng..." | **EC1** (Chỉ 1 Lớp Không Hợp lệ) |
| **TC5** | Invalid (qty \> max) | **D5** | Lỗi: "Số lượng..." | **EC3** (Chỉ 1 Lớp Không Hợp lệ) |
| **TC6** | Invalid (email local \< 3\) | **D6** | Lỗi: "Email..." | **EC4** (Chỉ 1 Lớp Không Hợp lệ) |
| **TC7** | Invalid (email thiếu @) | **D7** | Lỗi: "Email..." | **EC5** (Chỉ 1 Lớp Không Hợp lệ) |
| **TC8** | Invalid (email thiếu .tld) | **D8** | Lỗi: "Email..." | **EC6** (Chỉ 1 Lớp Không Hợp lệ) |
| **TC9** | Invalid (SĐT sai đầu số) | **D9** | Lỗi: "SĐT..." | **EC8** (Chỉ 1 Lớp Không Hợp lệ) |
| **TC10** | Invalid (SĐT sai độ dài) | **D10** | Lỗi: "SĐT..." | **EC9** (Chỉ 1 Lớp Không Hợp lệ) |
| **TC11** | Invalid (Tuổi không khớp) | **D11** | Lỗi: "Tuổi..." | **EC11** (Chỉ 1 Lớp Không Hợp lệ) |
| **TC12** | Invalid (SV thiếu thẻ) | **D12** | Lỗi: "Thiếu thẻ SV" | **EC13** (Chỉ 1 Lớp Không Hợp lệ) |

## **2\. Kỹ thuật: Bảng Quyết định (Decision Table Testing)**

*Áp dụng quy trình 4 bước từ slide "Decision Table Testing" (05\_Decision Table Testing.pdf) cho logic **Tính giá vé**.* *(Giả sử giá vé 2D Ngày thường Suất tối \= 100.000, Phụ thu IMAX \= 50.000)*

### **Bước 1: Xác định Nguyên nhân (Causes) & Kết quả (Effects)**

* **Nguyên nhân (Causes \- Dưới dạng câu hỏi T/F):**  
  * C1: ageGroup \= Trẻ em?  
  * C2: movieType \= IMAX?  
  * C3: qty \>= 4?  
  * C4: dayType \= Ngày lễ?  
  * C5: coupon \= Có?  
  * C6: memberTier \= Gold?  
  * C7: ageGroup \= Sinh viên?  
* **Kết quả (Effects \- Hành động sẽ thực thi):**  
  * E1: Áp dụng Giảm 30% (Trẻ em)  
  * E2: Áp dụng Giảm 10% (Số lượng)  
  * E3: Áp dụng Giảm 10% (Gold)  
  * E4: Áp dụng Giảm 15% (Sinh viên)  
  * E5: Áp dụng Giới hạn (Max 20% / Sàn 70%)  
  * E6: KHÔNG Giảm (Trẻ em \+ IMAX)  
  * E7: KHÔNG Giảm (Qty \+ Ngày lễ)  
  * E8: KHÔNG Giảm (Coupon \+ Ngày lễ)  
  * E\_Out: Tính toán & Hiển thị giá cuối

### **Bước 2: Tạo Bảng Quyết định (Đầy đủ \- Ví dụ)**

(Để minh họa Bước 2, chúng ta sẽ tạo một bảng đầy đủ cho 3 nguyên nhân **C1, C2, C4**. Bảng đầy đủ thực tế với 7+ nguyên nhân sẽ có $2^7=128$ cột, rất phức tạp và không khả thi để vẽ.)

| Nguyên nhân (Causes) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| C1: ageGroup \= Trẻ em? | T | T | T | T | F | F | F | F |
| C2: movieType \= IMAX? | T | T | F | F | T | T | F | F |
| C4: dayType \= Ngày lễ? | T | F | T | F | T | F | T | F |
| **Kết quả (Effects)** |  |  |  |  |  |  |  |  |
| E1: Giảm 30% (Trẻ em) | \- | \- | X | X | \- | \- | \- | \- |
| E6: KHÔNG Giảm (Trẻ em+IMAX) | X | X | \- | \- | \- | \- | \- | \- |
| E\_Out: (Tính giá...) | X | X | X | X | X | X | X | X |

(Bảng trên minh họa cách liệt kê tất cả $2^3 \= 8$ tổ hợp cho 3 điều kiện.)

### **Bước 3: Rút gọn Bảng Quyết định (Bảng Quy tắc)**

(Đây là bảng kết quả cuối cùng sau khi phân tích *tất cả* các quy tắc nghiệp vụ và rút gọn 128+ cột xuống còn các quy tắc chính yếu)

| Nguyên nhân (Causes) | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| C1: ageGroup \= Trẻ em? | **T** | **T** | F | F | F | F | F | **T** |
| C2: movieType \= IMAX? | **F** | **T** | F | F | F | F | F | **F** |
| C3: qty \>= 4? | F | F | **T** | **T** | F | F | F | F |
| C4: dayType \= Ngày lễ? | F | F | **F** | **T** | **T** | F | F | F |
| C5: coupon \= Có? | F | F | F | F | **T** | F | F | F |
| C6: memberTier \= Gold? | F | F | F | F | F | F | **T** | **T** |
| C7: ageGroup \= Sinh viên? | F | F | F | F | F | **T** | **T** | F |
| **Kết quả (Effects)** |  |  |  |  |  |  |  |  |
| E1: Giảm 30% (Trẻ em) | X | \- | \- | \- | \- | \- | \- | X |
| E2: Giảm 10% (Số lượng) | \- | \- | X | \- | \- | \- | \- | \- |
| E3: Giảm 10% (Gold) | \- | \- | \- | \- | \- | \- | X | X |
| E4: Giảm 15% (Sinh viên) | \- | \- | \- | \- | \- | X | X | \- |
| E5: Áp dụng Giới hạn (Max/Sàn) | \- | \- | \- | \- | \- | \- | X | X |
| E6: KHÔNG Giảm (Trẻ em+IMAX) | \- | X | \- | \- | \- | \- | \- | \- |
| E7: KHÔNG Giảm (Qty+Ngày Lễ) | \- | \- | \- | X | \- | \- | \- | \- |
| E8: KHÔNG Giảm (Coupon+Ngày Lễ) | \- | \- | \- | \- | X | \- | \- | \- |
| **Output (Giá dự kiến)** | **70k** | **150k** | **360k** | **400k** | **100k** | **85k** | **80k** | **70k** |

### **Bước 4: Chuyển Bảng Quyết định thành Test Case (Giống format Slide 8\)**

Mỗi Quy tắc (Rule) ở trên trở thành 1 Test Case.

| ID | Tương ứng (Rule) | Dữ liệu đầu vào (Input) | Kết quả mong đợi (Giá cuối cùng) |
| :---- | :---- | :---- | :---- |
| **TC-DT-01** | R1 | (Trẻ em, 2D, Qty=1, Ngày thường, Không Coupon, Không Member) | 70.000 |
| **TC-DT-02** | R2 | (Trẻ em, **IMAX**, Qty=1, Ngày thường, Không Coupon, Không Member) | 150.000 |
| **TC-DT-03** | R3 | (Người lớn, 2D, **Qty=4**, **Ngày thường**, Không Coupon, Không Member) | 360.000 (tổng 4 vé) |
| **TC-DT-04** | R4 | (Người lớn, 2D, **Qty=4**, **Ngày lễ**, Không Coupon, Không Member) | 400.000 (tổng 4 vé) |
| **TC-DT-05** | R5 | (Người lớn, 2D, Qty=1, **Ngày lễ**, **Có Coupon**, Không Member) | 100.000 |
| **TC-DT-06** | R6 | (Sinh viên, 2D, Qty=1, Ngày thường, Không Coupon, Không Member) | 85.000 |
| **TC-DT-07** | R7 | (Sinh viên, 2D, Qty=1, Ngày thường, Không Coupon, **Member Gold**) | 80.000 |
| **TC-DT-08** | R8 | (Trẻ em, 2D, Qty=1, Ngày thường, Không Coupon, **Member Gold**) | 70.000 |

## **3\. Kỹ thuật: Chuyển đổi trạng thái (State Transition Testing)**

*Áp dụng quy trình 3 bước từ slide "State Transition Testing" (06\_State Transition Testing.pdf) cho **Vòng đời đặt vé**.*

### **Bước 1: Mô tả hệ thống (Sơ đồ trạng thái)**

* **Các Trạng thái (States):**  
  * S0: (Null \- Chưa có)  
  * S1: Created (Đã tạo, giữ 15p)  
  * S2: Paid (Đã thanh toán)  
  * S3: CheckedIn (Đã check-in/Kết thúc)  
  * S4: Expired (Hết hạn 15p)  
  * S5: Cancelled (Khách hủy)  
  * S6: Refunded (Rạp hủy)  
* **Các Sự kiện (Events):**  
  * E1: Tạo đơn hàng  
  * E2: Thanh toán (hợp lệ)  
  * E3: Chờ quá 15 phút  
  * E4: Khách Hủy (còn \>= 120 phút)  
  * E5: Khách Hủy (còn \< 120 phút)  
  * E6: Rạp Hủy  
  * E7: Khách Check-in  
  * E8: Cố gắng Hủy/Check-in (khi đã ở trạng thái cuối)

### **Bước 2: Tạo Bảng Chuyển đổi Trạng thái (State Table)**

Bảng này mô tả trạng thái tiếp theo (Next State) khi có sự kiện (Event) xảy ra ở trạng thái hiện tại (Current State). "Lỗi" nghĩa là không có sự chuyển đổi.

| Trạng thái hiện tại | E1 (Tạo) | E2 (TT) | E3 (Hết 15p) | E4 (Hủy \<120p) | E5 (Hủy \>120p) | E6 (Rạp hủy) | E7 (Check-in) |
| :---- | :---- | :---- | :---- | :---- | :---- | :---- | :---- |
| **S0 (Mới)** | S1 | Lỗi | Lỗi | Lỗi | Lỗi | Lỗi | Lỗi |
| **S1 (Created)** | Lỗi | S2 | S4 | Lỗi | Lỗi | Lỗi | Lỗi |
| **S2 (Paid)** | Lỗi | Lỗi | Lỗi | S5 | Lỗi (S2) | S6 | S3 |
| **S3 (CheckedIn)** | Lỗi | Lỗi | Lỗi | Lỗi (S3) | Lỗi (S3) | Lỗi (S3) | Lỗi (S3) |
| **S4 (Expired)** | Lỗi | Lỗi | Lỗi | Lỗi (S4) | Lỗi (S4) | Lỗi (S4) | Lỗi (S4) |
| **S5 (Cancelled)** | Lỗi | Lỗi | Lỗi | Lỗi (S5) | Lỗi (S5) | Lỗi (S5) | Lỗi (S5) |
| **S6 (Refunded)** | Lỗi | Lỗi | Lỗi | Lỗi (S6) | Lỗi (S6) | Lỗi (S6) | Lỗi (S6) |

### **Bước 3: Dẫn xuất Test Case (Test các mũi tên chuyển đổi)**

Mỗi Test Case sẽ kiểm tra một ô hợp lệ (Valid) hoặc không hợp lệ (Invalid) trong bảng trên.

| ID | Trạng thái ban đầu | Hành động (Event) | Kết quả mong đợi (Trạng thái mới) | Ghi chú (Luồng hợp lệ/Không) |
| :---- | :---- | :---- | :---- | :---- |
| **TC-ST-01** | (Mới) | E1: Tạo đơn hàng | Created (S1) | (Hợp lệ) Happy path |
| **TC-ST-02** | Created (S1) | E2: Thanh toán (trong 15 phút) | Paid (S2) | (Hợp lệ) Happy path |
| **TC-ST-03** | Paid (S2) | E7: Khách hàng Check-in | CheckedIn (S3) | (Hợp lệ) Happy path |
| **TC-ST-04** | Created (S1) | E3: Chờ 16 phút (Không TT) | Expired (S4) | (Hợp lệ) Đơn hàng tự hủy |
| **TC-ST-05** | Paid (S2) | E4: Khách Hủy (trước 121 phút) | Cancelled (S5) | (Hợp lệ) Khách được hủy |
| **TC-ST-06** | Paid (S2) | E6: Rạp Hủy (báo sự cố) | Refunded (S6) | (Hợp lệ) Rạp hủy |
| **TC-ST-07** | Paid (S2) | E5: Khách Hủy (trước 119 phút) | Paid (Lỗi: "Đã quá hạn hủy vé") | (Không hợp lệ) |
| **TC-ST-08** | Expired (S4) | E7: Khách hàng Check-in | Expired (Lỗi: "Vé đã hết hạn") | (Không hợp lệ) |
| **TC-ST-09** | CheckedIn (S3) | E4: Khách Hủy | CheckedIn (Lỗi: "Vé đã sử dụng") | (Không hợp lệ) |

## **4\. Kỹ thuật: All-pairs Testing (Kiểm thử cặp đôi)**

*Áp dụng quy trình 2 bước từ slide "All-pairs Testing" (08\_All-pairs testing.pdf) cho chức năng **Tìm kiếm & Lọc**.*

### **Bước 1: Sắp xếp các biến và giá trị**

Chúng ta có 6 biến. Sắp xếp theo số lượng giá trị từ cao xuống thấp để tối ưu:

1. Rạp {C1, C2, C3, C4, C5} (5 giá trị)  
2. Phương thức TT {MoMo, VNPay, Visa, Tiền mặt} (4 giá trị)  
3. Thành phố {HCM, HN, DN} (3 giá trị)  
4. Thời điểm {Sáng, Chiều, Tối} (3 giá trị)  
5. Ngôn ngữ {Phụ đề, Lồng tiếng} (2 giá trị)  
6. Định dạng {2D, 3D} (2 giá trị) *Tổng tổ hợp đầy đủ \= 5 x 4 x 3 x 3 x 2 x 2 \= 720 TCs.*

### **Bước 2: Tạo bộ test (dùng tool PICT)**

Chúng ta sẽ dùng tool để sinh ra bộ test. Bộ test này đảm bảo mọi cặp (ví dụ: "Rạp C1" \+ "2D", "HN" \+ "MoMo") đều xuất hiện ít nhất 1 lần. *(Kết quả dưới đây là ví dụ đầu ra từ tool, giảm 720 TCs xuống chỉ còn khoảng 20-22 TCs. Lấy ví dụ 15 TCs cho 4 tham số đầu tiên để minh họa)*

| ID | City | Cinema | Ngôn ngữ | Định dạng | Kết quả mong đợi |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **TC-AP-01** | HCM | C1 | Phụ đề | 2D | Hiển thị kết quả lọc |
| **TC-AP-02** | HCM | C2 | Lồng tiếng | 3D | Hiển thị kết quả lọc |
| **TC-AP-03** | HCM | C3 | Phụ đề | 3D | Hiển thị kết quả lọc |
| **TC-AP-04** | HCM | C4 | Lồng tiếng | 2D | Hiển thị kết quả lọc |
| **TC-AP-05** | HCM | C5 | Phụ đề | 2D | Hiển thị kết quả lọc |
| **TC-AP-06** | HN | C1 | Lồng tiếng | 2D | Hiển thị kết quả lọc |
| **TC-AP-07** | HN | C2 | Phụ đề | 3D | Hiển thị kết quả lọc |
| **TC-AP-08** | HN | C3 | Lồng tiếng | 3D | Hiển thị kết quả lọc |
| **TC-AP-09** | HN | C4 | Phụ đề | 2D | Hiển thị kết quả lọc |
| **TC-AP-10** | HN | C5 | Lồng tiếng | 2D | Hiển thị kết quả lọc |
| **TC-AP-11** | DN | C1 | Phụ đề | 3D | Hiển thị kết quả lọc |
| **TC-AP-12** | DN | C2 | Lồng tiếng | 2D | Hiển thị kết quả lọc |
| **TC-AP-13** | DN | C3 | Phụ đề | 2D | Hiển thị kết quả lọc |
| **TC-AP-14** | DN | C4 | Lồng tiếng | 3D | Hiển thị kết quả lọc |
| **TC-AP-15** | DN | C5 | Phụ đề | 3D | Hiển thị kết quả lọc |

## **5\. Kỹ thuật: Use Case Testing (Kiểm thử Kịch bản)**

*Áp dụng quy trình 3 bước từ slide "Use Case Testing" (07\_Use Case Testing.pdf) cho quy trình **Chọn ghế**.*

### **Bước 1: Xác định Use Case (Luồng chính & Luồng phụ)**

* **Use Case:** Chọn ghế  
* **Luồng chính (Basic Flow):** Chọn 2 ghế liền kề hợp lệ $\\rightarrow$ Tiếp tục.  
* **Luồng phụ 1 (Alternate Flow):** Chọn 2 ghế nhưng để lại 1 ghế trống đơn lẻ (Orphan seat).  
* **Luồng phụ 2 (Alternate Flow):** Người không có nhu cầu, cố tình chọn ghế xe lăn.  
* **Luồng phụ 3 (Alternate Flow):** Người có nhu cầu, chọn ghế xe lăn.  
* **Luồng phụ 4 (Alternate Flow):** Chọn ghế sát lối đi (không bị tính là "mồ côi").

### **Bước 2: Dẫn xuất các Kịch bản (Scenarios)**

Từ các luồng trên, ta có các kịch bản:

* **Scenario 1 (Happy Path):** Luồng chính (Đặt 2 vé VIP liền kề thành công).  
* **Scenario 2 (Invalid):** Luồng chính $\\rightarrow$ Luồng phụ 1 (Cố tình chọn ghế "mồ côi").  
* **Scenario 3 (Valid):** Luồng chính $\\rightarrow$ Luồng phụ 4 (Chọn ghế sát lối đi).  
* **Scenario 4 (Invalid):** Luồng chính $\\rightarrow$ Luồng phụ 2 (Người thường chọn ghế xe lăn).  
* **Scenario 5 (Valid):** Luồng chính $\\rightarrow$ Luồng phụ 3 (Người cần hỗ trợ chọn ghế xe lăn).

### **Bước 3: Thiết kế Test Case chi tiết**

Mỗi kịch bản (Scenario) trở thành 1 Test Case.

| ID | Tên Kịch bản (Scenario) | Các bước thực hiện (Steps) | Kết quả mong đợi (Expected Result) |
| :---- | :---- | :---- | :---- |
| **TC-UC-01** | **(Scenario 1\)** Đặt 2 vé VIP liền kề thành công | 1\. Đăng nhập. 2\. Chọn phim A, suất 19:00. 3\. Chọn 2 ghế F5, F6 (VIP, liền kề). 4\. Nhấn "Tiếp tục". | (Hợp lệ) Chuyển sang trang thanh toán. |
| **TC-UC-02** | **(Scenario 2\)** Chọn ghế "mồ côi" (Orphan seat) | 1\. Chọn phim A, suất 19:00. 2\. Sơ đồ hàng F còn trống: F5, F6, F7. 3\. User chọn F5 và F7. 4\. Nhấn "Tiếp tục". | Lỗi: "Không được để trống 1 ghế đơn lẻ (F6)." Không cho phép tiếp tục. |
| **TC-UC-03** | **(Scenario 3\)** Chọn ghế sát lối đi | 1\. Chọn phim A, suất 19:00. 2\. Sơ đồ hàng F còn trống: F5, F6 (F6 là ghế lối đi). 3\. User chỉ chọn F5. 4\. Nhấn "Tiếp tục". | (Hợp lệ) Cho phép tiếp tục. (Ghế F6 không bị coi là "mồ côi"). |
| **TC-UC-04** | **(Scenario 4\)** Người thường chọn ghế xe lăn | 1\. User (mặc định needsAccessibility=false). 2\. Chọn ghế W1 (ghế xe lăn). | Lỗi: "Ghế W1 chỉ dành cho khách xe lăn." |
| **TC-UC-05** | **(Scenario 5\)** Người cần hỗ trợ chọn ghế xe lăn | 1\. User khai báo needsAccessibility=true. 2\. Chọn ghế W1 (ghế xe lăn). | (Hợp lệ) Cho phép chọn ghế. |

