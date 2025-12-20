import os
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime, timedelta
from faker import Faker
import random
import csv

# --- CẤU HÌNH ---
load_dotenv()
fake = Faker('vi_VN')
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'orangehrm'),
    'password': os.getenv('DB_PASSWORD', 'orangehrm'),
    'database': os.getenv('DB_NAME', 'orangehrm'),
    'port': int(os.getenv('DB_PORT', 3306))
}

EXPORT_DIR = os.path.join(os.path.dirname(__file__), 'exports')
os.makedirs(EXPORT_DIR, exist_ok=True)

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def get_employees(cursor):
    cursor.execute("SELECT emp_number, emp_lastname, emp_firstname FROM hs_hr_employee")
    return cursor.fetchall()

def ensure_leave_types(cursor):
    types = ['Annual Leave', 'Casual Leave', 'Sick Leave', 'Maternity Leave']
    type_ids = {} # Đổi thành dict để lưu tên và ID
    
    # Lấy các loại đã có
    cursor.execute("SELECT id, name FROM ohrm_leave_type WHERE deleted = 0")
    existing = {row[1]: row[0] for row in cursor.fetchall()}
    
    for t_name in types:
        if t_name in existing:
            type_ids[t_name] = existing[t_name]
        else:
            try:
                cursor.execute("INSERT INTO ohrm_leave_type (name, exclude_in_reports_if_no_entitlement, deleted) VALUES (%s, 0, 0)", (t_name,))
                type_ids[t_name] = cursor.lastrowid
            except:
                pass
    return type_ids

def generate_ess_data():
    conn = connect_db()
    cursor = conn.cursor()
    print("="*50)
    print("GENERATE ESS DATA (LEAVE & ATTENDANCE)")
    print("="*50)

    try:
        employees = get_employees(cursor)
        if not employees:
            print("LỖI: Không tìm thấy nhân viên. Hãy chạy generate_dim.py trước.")
            return

        print(f"-> Tìm thấy {len(employees)} nhân viên. Đang xử lý...")
        leave_types_map = ensure_leave_types(cursor)
        leave_type_ids = list(leave_types_map.values())
        
        # --- 1. CẤP QUỸ PHÉP (LEAVE ENTITLEMENTS) - MỚI BỔ SUNG ---
        print("-> Đang cấp quỹ phép (Entitlements)...")
        entitlement_count = 0
        current_year = datetime.now().year
        start_year = f"{current_year}-01-01 00:00:00"
        end_year = f"{current_year}-12-31 23:59:59"

        # Lấy ID của Annual Leave để cấp phép
        annual_id = leave_types_map.get('Annual Leave')
        
        if annual_id:
            for emp in employees:
                emp_number = emp[0]
                # Kiểm tra xem đã có entitlement chưa
                cursor.execute("""
                    SELECT id FROM ohrm_leave_entitlement 
                    WHERE emp_number=%s AND leave_type_id=%s AND from_date >= %s
                """, (emp_number, annual_id, f"{current_year}-01-01"))
                
                if not cursor.fetchone():
                    days = 12.0 # Mặc định 12 ngày phép
                    try:
                        # Insert vào bảng ohrm_leave_entitlement
                        sql_ent = """
                            INSERT INTO ohrm_leave_entitlement 
                            (emp_number, no_of_days, days_used, leave_type_id, from_date, to_date, credited_date, created_by_id)
                            VALUES (%s, %s, 0, %s, %s, %s, NOW(), 1)
                        """
                        cursor.execute(sql_ent, (emp_number, days, annual_id, start_year, end_year))
                        entitlement_count += 1
                    except Exception as e:
                        pass # Bỏ qua nếu lỗi duplicate
        
        print(f"   Đã cấp quỹ phép năm (12 ngày) cho {entitlement_count} nhân viên.")

        # --- 2. TẠO DỮ LIỆU NGHỈ PHÉP (LEAVE REQUESTS) ---
        print("-> Đang tạo dữ liệu Leave Requests...")
        leave_count = 0
        
        for emp in employees:
            emp_number = emp[0]
            for _ in range(random.randint(0, 3)):
                start_date = fake.date_between(start_date='-6m', end_date='today')
                days = random.randint(1, 5)
                
                status = random.choice([3, 2, 1]) 
                l_type = random.choice(leave_type_ids)
                
                sql_req = "INSERT INTO ohrm_leave_request (leave_type_id, date_applied, emp_number) VALUES (%s, %s, %s)"
                cursor.execute(sql_req, (l_type, start_date, emp_number))
                request_id = cursor.lastrowid
                
                current_date = start_date
                for i in range(days):
                    sql_leave = """
                        INSERT INTO ohrm_leave 
                        (date, length_days, length_hours, status, leave_request_id, leave_type_id, emp_number, duration_type)
                        VALUES (%s, 1.00, 8.00, %s, %s, %s, %s, 0)
                    """
                    cursor.execute(sql_leave, (current_date, status, request_id, l_type, emp_number))
                    current_date += timedelta(days=1)
                
                leave_count += 1

        print(f"   Đã tạo {leave_count} đơn nghỉ phép.")

        # --- 3. TẠO DỮ LIỆU CHẤM CÔNG (ATTENDANCE) ---
        print("-> Đang tạo dữ liệu Attendance (Chấm công)...")
        att_count = 0
        
        for emp in employees:
            emp_number = emp[0]
            today = datetime.now().date()
            for i in range(14):
                work_date = today - timedelta(days=i)
                if work_date.weekday() >= 5: continue 
                
                in_time = datetime.combine(work_date, datetime.strptime("08:00:00", "%H:%M:%S").time()) + timedelta(minutes=random.randint(-15, 30))
                out_time = datetime.combine(work_date, datetime.strptime("17:30:00", "%H:%M:%S").time()) + timedelta(minutes=random.randint(-15, 30))
                
                sql_att = """
                    INSERT INTO ohrm_attendance_record 
                    (employee_id, punch_in_user_time, punch_out_user_time, punch_in_note, punch_out_note, state)
                    VALUES (%s, %s, %s, 'Normal check-in', 'Normal check-out', 'PUNCHED_OUT')
                """
                cursor.execute(sql_att, (emp_number, in_time, out_time))
                att_count += 1
                
        print(f"   Đã tạo {att_count} bản ghi chấm công.")
        
        conn.commit()
        print("[THÀNH CÔNG] Dữ liệu ESS đã được tạo xong!")
        
        # Xuất file báo cáo
        export_ess_report(entitlement_count, leave_count, att_count)

    except mysql.connector.Error as err:
        print(f"Lỗi MySQL: {err}")
    finally:
        if conn: conn.close()

def export_ess_report(e_count, l_count, a_count):
    data = [
        {'Category': 'Leave Entitlements', 'Total Generated': e_count, 'Tables Affected': 'ohrm_leave_entitlement'},
        {'Category': 'Leave Requests', 'Total Generated': l_count, 'Tables Affected': 'ohrm_leave_request, ohrm_leave'},
        {'Category': 'Attendance Records', 'Total Generated': a_count, 'Tables Affected': 'ohrm_attendance_record'}
    ]
    path = os.path.join(EXPORT_DIR, 'ess_generation_summary.csv')
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Category', 'Total Generated', 'Tables Affected'])
        writer.writeheader()
        writer.writerows(data)
    print(f"-> File báo cáo đã xuất tại: {path}")

if __name__ == "__main__":
    generate_ess_data()