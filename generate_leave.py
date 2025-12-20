import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# --- CẤU HÌNH DATABASE TỪ .ENV ---
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'orangehrm'),
    'password': os.getenv('DB_PASSWORD', 'orangehrm'),
    'database': os.getenv('DB_NAME', 'orangehrm'),
    'port': int(os.getenv('DB_PORT', 3306))
}

fake = Faker('vi_VN')

# --- CẤU HÌNH NGHIỆP VỤ LEAVE ---
LEAVE_TYPES_CONFIG = [
    {
        'name': 'Annual Leave',
        'days_per_year': 12,
        'max_consecutive_days': 10,
        'requires_approval': True,
        'advance_notice_days': 3
    },
    {
        'name': 'Sick Leave',
        'days_per_year': 30,
        'max_consecutive_days': 14,
        'requires_approval': True,
        'advance_notice_days': 0
    },
    {
        'name': 'Casual Leave',
        'days_per_year': 6,
        'max_consecutive_days': 3,
        'requires_approval': True,
        'advance_notice_days': 1
    },
    {
        'name': 'Maternity Leave',
        'days_per_year': 180,
        'max_consecutive_days': 180,
        'requires_approval': True,
        'advance_notice_days': 30
    },
    {
        'name': 'Paternity Leave',
        'days_per_year': 5,
        'max_consecutive_days': 5,
        'requires_approval': True,
        'advance_notice_days': 7
    },
    {
        'name': 'Bereavement Leave',
        'days_per_year': 3,
        'max_consecutive_days': 3,
        'requires_approval': False,
        'advance_notice_days': 0
    },
    {
        'name': 'Unpaid Leave',
        'days_per_year': 30,
        'max_consecutive_days': 30,
        'requires_approval': True,
        'advance_notice_days': 7
    },
    {
        'name': 'Compensatory Leave',
        'days_per_year': 10,
        'max_consecutive_days': 5,
        'requires_approval': True,
        'advance_notice_days': 1
    },
]

LEAVE_STATUSES = {
    1: 'REJECTED',
    2: 'CANCELLED',
    3: 'PENDING APPROVAL',
    4: 'SCHEDULED',
    5: 'TAKEN'
}

# Nội dung bình luận cho từng loại nghỉ phép
LEAVE_COMMENTS = {
    'Annual Leave': [
        'Planning family vacation to Da Lat',
        'Need to visit family in hometown',
        'Taking time off to rest after busy work period',
        'Family trip to Nha Trang',
        'Attending relative wedding ceremony'
    ],
    'Sick Leave': [
        'Having high fever and headache, need rest',
        'Doctor advised rest due to severe flu',
        'Experiencing stomach pain, need medical attention',
        'Not feeling well, require treatment time',
        'Suffering from sore throat and fever'
    ],
    'Casual Leave': [
        'Need to handle personal matters at bank',
        'Taking child for vaccination tomorrow morning',
        'Home repair scheduled',
        'Need to accompany parents to hospital',
        'Processing personal documents'
    ],
    'Maternity Leave': [
        'Preparing for childbirth, maternity leave request',
        'Doctor recommended rest before delivery',
        'Due date approaching, need time for baby care',
        'Maternity leave as per regulations'
    ],
    'Paternity Leave': [
        'Wife just gave birth, need time for care',
        'Need time to take care of wife and newborn',
        'New baby in family, supporting wife',
        'Paternity leave as per policy'
    ],
    'Bereavement Leave': [
        'Family bereavement, need to attend funeral',
        'Grandfather passed away, need to attend services',
        'Family member passed away, funeral arrangements',
        'Attending relative funeral in hometown'
    ],
    'Unpaid Leave': [
        'Personal matters requiring extended time',
        'Need time for professional development',
        'Important family obligations',
        'Pursuing additional education'
    ],
    'Compensatory Leave': [
        'Worked overtime last weekend, requesting comp leave',
        'Accumulated OT hours, requesting time off',
        'Worked extra hours on project, taking comp leave',
        'Compensatory leave for weekend work'
    ]
}

# Lý do từ chối nghỉ phép
REJECTION_REASONS = [
    'Insufficient leave balance',
    'Peak season - cannot approve at this time',
    'Requires more advance notice for this leave type',
    'Team member already on leave during this period',
    'Please reschedule to next month',
    'Project requires full team presence',
    'Need additional documentation for leave request',
    'Does not meet advance notice requirements'
]

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def get_current_leave_period():
    """Lấy hoặc tạo kỳ nghỉ phép hiện tại (năm hiện tại)"""
    current_year = datetime.now().year
    start_date = datetime(current_year, 1, 1)
    end_date = datetime(current_year, 12, 31)
    return start_date, end_date

def generate_leave_data():
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor(buffered=True)
        print("=" * 70)
        print("ORANGEHRM - LEAVE MANAGEMENT DATA GENERATOR")
        print("=" * 70)
        print("-> Kết nối Database thành công!")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # ===== BƯỚC 1: LẤY DANH SÁCH NHÂN VIÊN =====
        print("\n[BƯỚC 1] Đang lấy danh sách nhân viên...")
        cursor.execute("""
            SELECT e.emp_number, e.emp_gender, e.joined_date, j.job_title
            FROM hs_hr_employee e
            LEFT JOIN ohrm_job_title j ON e.job_title_code = j.id
        """)
        employees = cursor.fetchall()
        
        if not employees:
            print("CẢNH BÁO: Chưa có dữ liệu nhân viên! Hãy chạy generate_dim.py trước.")
            return
        
        print(f"   Tìm thấy {len(employees)} nhân viên")

        # ===== BƯỚC 2: TẠO LEAVE TYPES =====
        print("\n[BƯỚC 2] Đang tạo Leave Types...")
        
        leave_type_map = {}
        for lt_config in LEAVE_TYPES_CONFIG:
            cursor.execute("""
                INSERT INTO ohrm_leave_type (name, deleted, operational_country_id, exclude_in_reports_if_no_entitlement)
                VALUES (%s, 0, NULL, 0)
                ON DUPLICATE KEY UPDATE name = VALUES(name)
            """, (lt_config['name'],))
            
            cursor.execute("SELECT id FROM ohrm_leave_type WHERE name = %s", (lt_config['name'],))
            result = cursor.fetchone()
            if result:
                leave_type_map[lt_config['name']] = {
                    'id': result[0],
                    'config': lt_config
                }
        
        print(f"   Đã tạo {len(leave_type_map)} Leave Types")
        for lt_name in leave_type_map.keys():
            print(f"     - {lt_name}")

        # ===== BƯỚC 3: TẠO LEAVE PERIOD =====
        print("\n[BƯỚC 3] Đang tạo Leave Period...")
        
        start_date, end_date = get_current_leave_period()
        
        cursor.execute("""
            INSERT INTO ohrm_leave_period_history (leave_period_start_month, leave_period_start_day, created_at)
            VALUES (1, 1, NOW())
            ON DUPLICATE KEY UPDATE leave_period_start_month = VALUES(leave_period_start_month)
        """)
        
        print(f"   Kỳ nghỉ phép: {start_date.strftime('%Y-%m-%d')} đến {end_date.strftime('%Y-%m-%d')}")

        # ===== BƯỚC 4: TẠO LEAVE ENTITLEMENTS =====
        print("\n[BƯỚC 4] Đang tạo Leave Entitlements...")
        
        entitlement_count = 0
        for emp_number, emp_gender, joined_date, job_title in employees:
            for lt_name, lt_data in leave_type_map.items():
                lt_id = lt_data['id']
                lt_config = lt_data['config']
                
                # Logic phân quyền nghỉ phép
                days_entitled = lt_config['days_per_year']
                
                # Nữ mới được nghỉ thai sản
                if lt_name == 'Maternity Leave':
                    if emp_gender != 2:  # Không phải nữ
                        continue
                
                # Nam mới được nghỉ chăm con
                if lt_name == 'Paternity Leave':
                    if emp_gender != 1:  # Không phải nam
                        continue
                
                # Tính số ngày dựa vào thời gian làm việc
                # Nếu nhân viên vào cuối năm, giảm số ngày tương ứng
                if joined_date:
                    months_worked = (datetime.now().year - joined_date.year) * 12 + (datetime.now().month - joined_date.month)
                    if months_worked < 12:
                        days_entitled = int(days_entitled * months_worked / 12)
                
                if days_entitled > 0:
                    # Tạo entitlement
                    cursor.execute("""
                        INSERT INTO ohrm_leave_entitlement 
                        (emp_number, leave_type_id, from_date, to_date, 
                         credited_date, no_of_days, days_used, entitlement_type, deleted, note, created_by_id)
                        VALUES (%s, %s, %s, %s, %s, %s, 0, 1, 0, %s, 1)
                    """, (
                        emp_number,
                        lt_id,
                        start_date.date(),
                        end_date.date(),
                        start_date.date(),
                        days_entitled,
                        f"{lt_config['name']} {datetime.now().year}"
                    ))
                    entitlement_count += 1
        
        print(f"   Đã tạo {entitlement_count} Leave Entitlements")

        # ===== BƯỚC 5: TẠO LEAVE REQUESTS & LEAVES =====
        print("\n[BƯỚC 5] Đang tạo Leave Requests & Leaves...")
        
        leave_request_count = 0
        leave_day_count = 0
        comment_count = 0
        
        # Lấy danh sách supervisor để làm người duyệt
        cursor.execute("""
            SELECT DISTINCT erep_sup_emp_number 
            FROM hs_hr_emp_reportto
        """)
        supervisors = [row[0] for row in cursor.fetchall()]
        
        for emp_number, emp_gender, joined_date, job_title in employees:
            # Lấy entitlements của nhân viên này
            cursor.execute("""
                SELECT e.id, e.leave_type_id, e.no_of_days, lt.name
                FROM ohrm_leave_entitlement e
                JOIN ohrm_leave_type lt ON e.leave_type_id = lt.id
                WHERE e.emp_number = %s AND e.deleted = 0
            """, (emp_number,))
            
            emp_entitlements = cursor.fetchall()
            
            if not emp_entitlements:
                continue
            
            # Tạo 2-5 yêu cầu nghỉ phép cho mỗi nhân viên
            num_requests = random.randint(2, 5)
            
            for _ in range(num_requests):
                # Chọn ngẫu nhiên một loại nghỉ phép từ danh sách quyền nghỉ của nhân viên
                entitlement_id, leave_type_id, entitled_days, leave_type_name = random.choice(emp_entitlements)
                lt_config = leave_type_map[leave_type_name]['config']
                
                # Tính số ngày xin nghỉ (từ 1 đến số ngày tối đa được phép)
                days_requested = random.randint(1, min(lt_config['max_consecutive_days'], int(entitled_days)))
                
                # Tạo ngày bắt đầu nghỉ (từ 60 ngày trước đến 30 ngày sau)
                date_applied = datetime.now() - timedelta(days=random.randint(0, 60))
                leave_start_date = date_applied + timedelta(days=random.randint(lt_config['advance_notice_days'], 30))
                
                # Đảm bảo không nghỉ quá năm hiện tại
                if leave_start_date.year > datetime.now().year:
                    leave_start_date = datetime(datetime.now().year, 12, random.randint(1, 20))
                
                # Đảm bảo leave_start_date là ngày làm việc (thứ 2-6), không phải cuối tuần
                while leave_start_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
                    leave_start_date += timedelta(days=1)
                
                leave_end_date = leave_start_date + timedelta(days=days_requested - 1)
                
                # Xác định trạng thái dựa vào ngày
                if leave_start_date > datetime.now():
                    status = random.choice([3, 4])  # PENDING hoặc SCHEDULED
                elif leave_end_date < datetime.now():
                    status = random.choice([2, 5])  # CANCELLED hoặc TAKEN
                else:
                    status = 5  # TAKEN (đang nghỉ)
                
                # Thêm khả năng bị từ chối
                if random.random() < 0.1:  # 10% bị từ chối
                    status = 1
                
                # Tạo Leave Request
                cursor.execute("""
                    INSERT INTO ohrm_leave_request 
                    (leave_type_id, date_applied, emp_number)
                    VALUES (%s, %s, %s)
                """, (
                    leave_type_id,
                    date_applied.date(),
                    emp_number
                ))
                
                leave_request_id = cursor.lastrowid
                leave_request_count += 1
                
                # Tạo các ngày nghỉ cụ thể cho từng ngày trong khoảng thời gian
                current_date = leave_start_date
                while current_date <= leave_end_date:
                    # Chỉ tạo nghỉ cho các ngày làm việc (bỏ qua thứ 7, chủ nhật)
                    if current_date.weekday() < 5:  # 0-4 là thứ 2-6
                        # Thời lượng nghỉ: ngày đầy đủ = 8 giờ, nửa ngày = 4 giờ
                        leave_length = random.choice([8.0, 4.0]) if leave_type_name == 'Casual Leave' else 8.0
                        
                        cursor.execute("""
                            INSERT INTO ohrm_leave 
                            (date, length_hours, length_days, status, leave_request_id, leave_type_id, emp_number, start_time, end_time, duration_type)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            current_date.date(),
                            leave_length,
                            leave_length / 8.0,  # chuyển đổi giờ sang ngày
                            status,
                            leave_request_id,
                            leave_type_id,
                            emp_number,
                            '00:00:00' if leave_length == 8.0 else '08:00:00',
                            '00:00:00' if leave_length == 8.0 else '12:00:00',
                            1 if leave_length == 8.0 else 2  # 1=ngày đầy đủ, 2=nửa ngày
                        ))
                        
                        leave_id = cursor.lastrowid
                        leave_day_count += 1
                        
                        # Tạo bình luận cho các đơn bị từ chối (70% các đơn từ chối có comment)
                        if status == 1 and random.random() > 0.3:
                            # Lấy thông tin user_id của người quản lý (supervisor)
                            supervisor_emp = random.choice(supervisors) if supervisors else 1000
                            cursor.execute("SELECT id FROM ohrm_user WHERE emp_number = %s LIMIT 1", (supervisor_emp,))
                            supervisor_user = cursor.fetchone()
                            supervisor_user_id = supervisor_user[0] if supervisor_user else 1
                            
                            cursor.execute("""
                                INSERT INTO ohrm_leave_comment 
                                (leave_id, created, created_by_id, created_by_emp_number, comments)
                                VALUES (%s, %s, %s, %s, %s)
                            """, (
                                leave_id,
                                current_date,
                                supervisor_user_id,
                                supervisor_emp,
                                random.choice(REJECTION_REASONS)
                            ))
                            comment_count += 1
                        
                    current_date += timedelta(days=1)
                
                # Tạo bình luận lý do cho yêu cầu nghỉ phép (50% các yêu cầu có lý do)
                if random.random() > 0.5:
                    # Lấy thông tin user_id của nhân viên nộp đơn
                    cursor.execute("SELECT id FROM ohrm_user WHERE emp_number = %s LIMIT 1", (emp_number,))
                    emp_user = cursor.fetchone()
                    emp_user_id = emp_user[0] if emp_user else 1
                    
                    # Chọn bình luận phù hợp với loại nghỉ phép được chọn
                    leave_comment = random.choice(LEAVE_COMMENTS.get(leave_type_name, ['Xin nghỉ phép']))
                    
                    cursor.execute("""
                        INSERT INTO ohrm_leave_request_comment
                        (leave_request_id, created, created_by_id, created_by_emp_number, comments)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        leave_request_id,
                        date_applied,
                        emp_user_id,
                        emp_number,
                        leave_comment
                    ))
                    comment_count += 1
        
        print(f"   Đã tạo {leave_request_count} Leave Requests")
        print(f"   Đã tạo {leave_day_count} Leave Days")
        print(f"   Đã tạo {comment_count} Comments")

        # ===== BƯỚC 6: CẬP NHẬT DAYS_USED =====
        print("\n[BƯỚC 6] Đang cập nhật days_used trong entitlements...")
        
        cursor.execute("""
            UPDATE ohrm_leave_entitlement e
            SET e.days_used = (
                SELECT COALESCE(SUM(l.length_days), 0)
                FROM ohrm_leave l
                WHERE l.emp_number = e.emp_number 
                AND l.leave_type_id = e.leave_type_id
                AND l.status IN (4, 5)  -- SCHEDULED hoặc TAKEN
                AND l.date BETWEEN e.from_date AND e.to_date
            )
        """)
        
        print(f"   Đã cập nhật days_used")

        # ===== BƯỚC 7: TẠO LEAVE STATUS RECORDS =====
        print("\n[BƯỚC 7] Đang tạo Leave Status records...")
        
        # Đảm bảo tất cả các mã trạng thái nghỉ phép đều tồn tại trong database
        for status_id, status_name in LEAVE_STATUSES.items():
            cursor.execute("""
                INSERT IGNORE INTO ohrm_leave_status (id, status, name)
                VALUES (%s, %s, %s)
            """, (status_id, status_id, status_name))
        
        print(f"   Đã tạo {len(LEAVE_STATUSES)} Leave Status records")

        # ===== LƯU DỮ LIỆU VÀ TỔNG KẾT =====
        conn.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        print("\n" + "=" * 50)
        print("HOÀN THÀNH TẠO DỮ LIỆU LEAVE MANAGEMENT")
        print("=" * 50)
        print(f"THỐNG KÊ:")
        print(f"   • Leave Types: {len(leave_type_map)}")
        print(f"   • Employees Processed: {len(employees)}")
        print(f"   • Leave Entitlements: {entitlement_count}")
        print(f"   • Leave Requests: {leave_request_count}")
        print(f"   • Leave Days: {leave_day_count}")
        print(f"   • Comments: {comment_count}")
        print("=" * 50)
        
        # Hiển thị dữ liệu mẫu từ database
        print("\nMẪU DỮ LIỆU:")
        cursor.execute("""
            SELECT e.employee_id, 
                   CONCAT(e.emp_firstname, ' ', e.emp_lastname) as name,
                   lt.name as leave_type,
                   le.no_of_days as entitled,
                   le.days_used as used,
                   (le.no_of_days - le.days_used) as balance
            FROM ohrm_leave_entitlement le
            JOIN hs_hr_employee e ON le.emp_number = e.emp_number
            JOIN ohrm_leave_type lt ON le.leave_type_id = lt.id
            LIMIT 10
        """)
        
        print("\n" + "-" * 50)
        print(f"{'EMP ID':<10} {'Name':<20} {'Leave Type':<20} {'Entitled':>10} {'Used':>8} {'Balance':>10}")
        print("-" * 50)
        for row in cursor.fetchall():
            print(f"{row[0]:<10} {row[1]:<20} {row[2]:<20} {row[3]:>10.1f} {row[4]:>8.1f} {row[5]:>10.1f}")
        print("-" * 50)
        
    except mysql.connector.Error as err:
        print(f"\nLỖI MySQL: {err}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"\nLỖI: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("\n-> Đã đóng kết nối Database")

if __name__ == "__main__":
    print("="*50)
    print("GENERATE LEAVE DATA")
    print("="*50)
    generate_leave_data()
