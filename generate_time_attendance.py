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

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def generate_attendance_role_based():
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor(buffered=True)
        print("-> Kết nối Database thành công!")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        # BƯỚC 1: LẤY NHÂN VIÊN KÈM CHỨC DANH
        print("-> Đang lấy danh sách nhân viên và chức danh...")
        sql_get_emp = """
            SELECT e.emp_number, j.job_title 
            FROM hs_hr_employee e 
            LEFT JOIN ohrm_job_title j ON e.job_title_code = j.id
        """
        cursor.execute(sql_get_emp)
        employees_data = cursor.fetchall()

        if not employees_data:
            print("[LỖI] Chưa có dữ liệu nhân viên. Hãy chạy file tạo PIM trước.")
            return

        # BƯỚC 2: TẠO PROJECT & ACTIVITY THEO PHÂN LOẠI
        print("-> Đang tạo Dự án & Hoạt động phân theo vai trò...")

        # A. KHÁCH HÀNG BÊN NGOÀI
        cursor.execute("INSERT IGNORE INTO ohrm_customer (name,description, is_deleted) VALUES ('Global Tech Corp', 'Global Technology Corporation', 0)")
        cursor.execute("SELECT customer_id FROM ohrm_customer WHERE name = 'Global Tech Corp'")
        ext_cust_id = cursor.fetchone()[0]

        ext_projects = ['Super App', 'E-Banking Web', 'HRM System']
        ext_proj_ids = []
        for p in ext_projects:
            cursor.execute("INSERT IGNORE INTO ohrm_project (customer_id, name, is_deleted) VALUES (%s, %s, 0)", (ext_cust_id, p))
            cursor.execute("SELECT project_id FROM ohrm_project WHERE name = %s", (p,))
            ext_proj_ids.append(cursor.fetchone()[0])

        # B. KHÁCH HÀNG NỘI BỘ
        cursor.execute("INSERT IGNORE INTO ohrm_customer (name,description, is_deleted) VALUES ('Internal Management', 'Internal Management Department', 0)")
        cursor.execute("SELECT customer_id FROM ohrm_customer WHERE name = 'Internal Management'")
        int_cust_id = cursor.fetchone()[0]

        cursor.execute("INSERT IGNORE INTO ohrm_project (customer_id, name, is_deleted) VALUES (%s, 'Executive Board', 0)", (int_cust_id,))
        cursor.execute("SELECT project_id FROM ohrm_project WHERE name = 'Executive Board'")
        int_proj_id = cursor.fetchone()[0]

        # C. TẠO ACTIVITY VÀ PHÂN NHÓM (MAPPING)
        role_activities = {'Director': [], 'Manager': [], 'Staff': []}

        # 1. Staff
        staff_acts = ['Coding Backend', 'Coding Frontend', 'Unit Testing', 'Bug Fixing']
        for pid in ext_proj_ids:
            for act in staff_acts:
                cursor.execute("INSERT IGNORE INTO ohrm_project_activity (project_id, name, is_deleted) VALUES (%s, %s, 0)", (pid, act))
                cursor.execute("SELECT activity_id FROM ohrm_project_activity WHERE project_id=%s AND name=%s", (pid, act))
                act_id = cursor.fetchone()[0]
                role_activities['Staff'].append((pid, act_id))

        # 2. Manager
        manager_acts = ['Project Planning', 'Code Review', 'Client Meeting']
        for pid in ext_proj_ids:
            for act in manager_acts:
                cursor.execute("INSERT IGNORE INTO ohrm_project_activity (project_id, name, is_deleted) VALUES (%s, %s, 0)", (pid, act))
                cursor.execute("SELECT activity_id FROM ohrm_project_activity WHERE project_id=%s AND name=%s", (pid, act))
                act_id = cursor.fetchone()[0]
                role_activities['Manager'].append((pid, act_id))
        
        # 3. Director
        director_acts = ['Strategic Planning', 'Financial Review', 'Board Meeting']
        for act in director_acts:
            cursor.execute("INSERT IGNORE INTO ohrm_project_activity (project_id, name, is_deleted) VALUES (%s, %s, 0)", (int_proj_id, act))
            cursor.execute("SELECT activity_id FROM ohrm_project_activity WHERE project_id=%s AND name=%s", (int_proj_id, act))
            act_id = cursor.fetchone()[0]
            role_activities['Director'].append((int_proj_id, act_id))

        # BƯỚC 3: TẠO TIMESHEET VÀ ACTION LOG
        print("-> Đang tạo Timesheet kèm Action Log...")
        
        sql_timesheet = "INSERT INTO ohrm_timesheet (employee_id, state, start_date, end_date) VALUES (%s, %s, %s, %s)"
        sql_item = "INSERT INTO ohrm_timesheet_item (timesheet_id, date, duration, comment, project_id, employee_id, activity_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        sql_log = "INSERT INTO ohrm_timesheet_action_log (timesheet_id, action, date_time, performed_by, comment) VALUES (%s, %s, %s, %s, %s)"

        today = datetime.now()
        start_weeks = [today - timedelta(days=today.weekday() + 7*k) for k in range(1, 5)]        
        # Dùng User 1000 (Director) đại diện cho người thực hiện hành động duyệt
        cursor.execute("SELECT id FROM ohrm_user WHERE emp_number = 1000")
        admin_user_id = cursor.fetchone()[0]

        for emp_id, job_title in employees_data:
            job_title = job_title if job_title else 'Director'  
            suitable_acts = role_activities.get(job_title, role_activities['Staff'])
            if not suitable_acts: continue

            for start_date in start_weeks:
                end_date = start_date + timedelta(days=6)
                
                state = 'APPROVED' if job_title in ['Director', 'Manager'] else random.choice(['SUBMITTED', 'APPROVED'])

                try:
                    # 1. Tạo Header Timesheet
                    cursor.execute(sql_timesheet, (emp_id, state, start_date.date(), end_date.date()))
                    ts_id = cursor.lastrowid

                    # 2. Tạo Items (Chi tiết 5 ngày làm việc)
                    for d in range(5):
                        work_date = start_date + timedelta(days=d)
                        proj_id, act_id = random.choice(suitable_acts)

                        if job_title == 'Staff':
                            cmt = random.choice(["Fixed login bug", "Developed API", "Tested module A"])
                        elif job_title == 'Manager':
                            cmt = random.choice(["Review sprint", "Meeting with client", "Plan next phase"])
                        else:
                            cmt = "General management"

                        cursor.execute(sql_item, (ts_id, work_date.date(), 28800, cmt, proj_id, emp_id, act_id))
                    
                    # 3.TẠO LOG LỊCH SỬ (ACTION LOG)
                    # Giả định nhân viên nộp vào chiều Thứ 6 lúc 17:00
                    submit_time = (start_date + timedelta(days=4)).replace(hour=17, minute=0, second=0)
                    # Lấy ID người nộp
                    cursor.execute("SELECT id FROM ohrm_user WHERE emp_number = %s", (emp_id,))
                    user_record = cursor.fetchone()
                    # Nếu nhân viên không có tài khoản, dùng Admin ID làm người nộp thay thế
                    submitter_user_id = user_record[0] if user_record else admin_user_id
                    # Luôn có log SUBMITTED
                    cursor.execute(sql_log, (ts_id, 'SUBMITTED', submit_time, submitter_user_id, "Submitted by System"))

                    # Nếu trạng thái là APPROVED thì thêm log APPROVED (duyệt vào sáng Thứ 2 tuần sau)
                    if state == 'APPROVED':
                        approve_time = submit_time + timedelta(days=3) # Thứ 6 + 3 ngày = Thứ 2
                        approve_time = approve_time.replace(hour=9, minute=0, second=0)
                        cursor.execute(sql_log, (ts_id, 'APPROVED', approve_time, admin_user_id, "Approved by Manager"))

                except mysql.connector.Error as err:
                    print(f"[LỖI DB] Emp {emp_id} - Tuần {start_date.date()}: {err}")
                except Exception as e:
                    print(f"[LỖI Code] {e}")
        # BƯỚC 4: TẠO ATTENDANCE
        print("-> Đang tạo dữ liệu chấm công (Punch In/Out)...")
        
        sql_att = """
            INSERT INTO ohrm_attendance_record 
            (employee_id, punch_in_utc_time, punch_in_time_offset, punch_in_user_time, 
             punch_out_utc_time, punch_out_time_offset, punch_out_user_time, state) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'PUNCHED OUT')
        """
        offset_value = '7' 
        for emp_id, _ in employees_data:
            for i in range(30):
                curr = today - timedelta(days=i)
                if curr.weekday() >= 5: continue 
                
                in_hour = 8; in_minute = random.randint(0, 45)
                p_in_local = curr.replace(hour=in_hour, minute=in_minute, second=0)
                p_in_utc = p_in_local - timedelta(hours=7)

                duration = timedelta(hours=9, minutes=random.randint(0, 30))
                p_out_local = p_in_local + duration
                p_out_utc = p_out_local - timedelta(hours=7)
                try: 
                    cursor.execute(sql_att, (
                        emp_id, 
                        p_in_utc.strftime('%Y-%m-%d %H:%M:%S'),    
                        offset_value,                             
                        p_in_local.strftime('%Y-%m-%d %H:%M:%S'),  
                        p_out_utc.strftime('%Y-%m-%d %H:%M:%S'),   
                        offset_value,                              
                        p_out_local.strftime('%Y-%m-%d %H:%M:%S')  
                    ))
                except mysql.connector.Error as err:
                    if err.errno != 1062:
                        print(f"[LỖI DB] Emp {emp_id}: {err}")

        conn.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print("\n[THÀNH CÔNG] Đã tạo dữ liệu Time & Attendance!")

    except mysql.connector.Error as err:
        print(f"Lỗi MySQL: {err}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    generate_attendance_role_based()