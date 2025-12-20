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
    cursor.execute("SELECT emp_number, emp_lastname, emp_firstname FROM hs_hr_employee WHERE emp_number >= 1000")
    return cursor.fetchall()

def ensure_leave_types(cursor):
    types = ['Annual Leave', 'Casual Leave', 'Sick Leave', 'Maternity Leave']
    type_ids = {} 
    cursor.execute("SELECT id, name FROM ohrm_leave_type WHERE deleted = 0")
    existing = {row[1]: row[0] for row in cursor.fetchall()}
    for t_name in types:
        if t_name in existing:
            type_ids[t_name] = existing[t_name]
        else:
            try:
                cursor.execute("INSERT INTO ohrm_leave_type (name, deleted) VALUES (%s, 0)", (t_name,))
                type_ids[t_name] = cursor.lastrowid
            except: 
                pass
    return type_ids

def ensure_project_and_activity(cursor):
    # 1. Customer
    cursor.execute("SELECT customer_id FROM ohrm_customer WHERE name='Internal'")
    res = cursor.fetchone()
    cust_id = res[0] if res else None
    if not cust_id:
        cursor.execute("INSERT INTO ohrm_customer (name, description, is_deleted) VALUES ('Internal', 'Internal Projects', 0)")
        cust_id = cursor.lastrowid

    # 2. Project
    cursor.execute("SELECT project_id FROM ohrm_project WHERE name='General Work'")
    res = cursor.fetchone()
    proj_id = res[0] if res else None
    if not proj_id:
        cursor.execute("INSERT INTO ohrm_project (customer_id, name, description, is_deleted) VALUES (%s, 'General Work', 'Daily Tasks', 0)", (cust_id,))
        proj_id = cursor.lastrowid

    # 3. Activity
    cursor.execute("SELECT activity_id FROM ohrm_project_activity WHERE name='Development'")
    res = cursor.fetchone()
    act_id = res[0] if res else None
    if not act_id:
        cursor.execute("INSERT INTO ohrm_project_activity (project_id, name, is_deleted) VALUES (%s, 'Development', 0)", (proj_id,))
        act_id = cursor.lastrowid
    return proj_id, act_id

def assign_admin_as_supervisor(cursor, employees):
    """Gán Admin làm Supervisor để thấy Timesheet ở mục 'Pending Action'."""
    print("-> Đang gán Admin làm Supervisor...")
    cursor.execute("SELECT emp_number FROM hs_hr_employee ORDER BY emp_number ASC LIMIT 1")
    res = cursor.fetchone()
    if not res: 
        return
    admin_id = res[0]

    count = 0
    sql_assign = "INSERT IGNORE INTO hs_hr_emp_reportto (erep_sup_emp_number, erep_sub_emp_number, erep_reporting_mode) VALUES (%s, %s, 1)"
    
    for emp in employees:
        if count >= 10: 
            break
        if emp[0] != admin_id:
            cursor.execute(sql_assign, (admin_id, emp[0]))
            count += 1
    print(f"   Đã gán Admin (ID {admin_id}) làm sếp của {count} nhân viên.")

def generate_ess_data():
    conn = connect_db()
    cursor = conn.cursor()
    print("="*50)
    print("GENERATE ESS DATA (FIXED - SCHEMA COMPLIANT)")
    print("="*50)

    try:
        employees = get_employees(cursor)
        if not employees:
            print("LỖI: Không tìm thấy nhân viên.")
            return

        print(f"-> Tìm thấy {len(employees)} nhân viên. Đang xử lý...")
        
        leave_types_map = ensure_leave_types(cursor)
        leave_type_ids = list(leave_types_map.values())
        
        proj_id, act_id = ensure_project_and_activity(cursor)
        
        # ===== 1. LEAVE ENTITLEMENT & REQUESTS (FIXED) =====
        print("-> (1/4) Tạo Quỹ phép & Đơn nghỉ...")
        entitlement_count = 0
        leave_count = 0
        current_year = datetime.now().year
        
        # Tạo entitlement cho TẤT CẢ leave types với entitlement_type
        for emp in employees:
            emp_number = emp[0]
            for lt_name, lt_id in leave_types_map.items():
                cursor.execute(
                    "SELECT id FROM ohrm_leave_entitlement WHERE emp_number=%s AND leave_type_id=%s AND deleted=0",
                    (emp_number, lt_id)
                )
                if not cursor.fetchone():
                    try:
                        days = 12.0 if lt_name == 'Annual Leave' else 10.0
                        # CRITICAL: Thêm entitlement_type (1 = Added, 2 = Brought Forward)
                        sql_ent = """
                            INSERT INTO ohrm_leave_entitlement 
                            (emp_number, no_of_days, days_used, leave_type_id, from_date, to_date, 
                             credited_date, entitlement_type, deleted, created_by_id)
                            VALUES (%s, %s, 0.0000, %s, %s, %s, NOW(), 1, 0, 1)
                        """
                        cursor.execute(sql_ent, (
                            emp_number, 
                            days, 
                            lt_id, 
                            f"{current_year}-01-01 00:00:00", 
                            f"{current_year}-12-31 23:59:59"
                        ))
                        entitlement_count += 1
                    except mysql.connector.Error as e:
                        print(f"   Warning: Không thể tạo entitlement cho emp {emp_number}: {e}")
                        pass

        conn.commit()  # Commit entitlement trước
        print(f"   ✓ Đã tạo {entitlement_count} entitlements")

        # Tạo leave requests với đầy đủ thông tin
        for emp in employees:
            if random.random() < 0.4:  # 40% nhân viên có đơn nghỉ
                emp_number = emp[0]
                
                # Random ngày trong 2 tháng qua hoặc 1 tháng tới
                start_date = fake.date_between(start_date='-60d', end_date='+30d')
                l_type = random.choice(leave_type_ids)
                
                # Status: -1=Rejected, 0=Cancelled, 1=Pending, 2=Scheduled, 3=Taken
                status = random.choices([1, 2, 3], weights=[0.3, 0.4, 0.3])[0]
                
                # Kiểm tra có entitlement không
                cursor.execute("""
                    SELECT id, no_of_days, days_used 
                    FROM ohrm_leave_entitlement 
                    WHERE emp_number=%s AND leave_type_id=%s 
                    AND from_date <= %s AND to_date >= %s
                    AND deleted=0
                """, (emp_number, l_type, start_date, start_date))
                ent = cursor.fetchone()
                
                if not ent:
                    continue  # Bỏ qua nếu không có entitlement
                
                ent_id, total_days, used_days = ent
                remaining = float(total_days) - float(used_days)
                
                if remaining < 1.0:
                    continue  # Bỏ qua nếu hết phép
                
                try:
                    # 1. Tạo leave request
                    cursor.execute("""
                        INSERT INTO ohrm_leave_request 
                        (leave_type_id, date_applied, emp_number)
                        VALUES (%s, %s, %s)
                    """, (l_type, start_date, emp_number))
                    req_id = cursor.lastrowid
                    
                    # 2. Tạo leave record với đầy đủ thông tin
                    cursor.execute("""
                        INSERT INTO ohrm_leave 
                        (date, length_days, length_hours, status, leave_request_id, 
                         leave_type_id, emp_number, start_time, end_time, duration_type)
                        VALUES (%s, 1.0000, 8.00, %s, %s, %s, %s, '00:00:00', '00:00:00', 1)
                    """, (start_date, status, req_id, l_type, emp_number))
                    
                    # 3. Cập nhật days_used nếu status = Taken (3)
                    if status == 3:
                        cursor.execute("""
                            UPDATE ohrm_leave_entitlement 
                            SET days_used = days_used + 1.0000
                            WHERE id = %s
                        """, (ent_id,))
                    
                    leave_count += 1
                    
                except mysql.connector.Error as e:
                    print(f"   Warning: Không thể tạo leave cho emp {emp_number}: {e}")
                    continue

        conn.commit()
        print(f"   ✓ Đã tạo {leave_count} leave requests")

        # ===== 2. TIMESHEETS (Current Week - Pending) =====
        print("-> (2/4) Tạo Timesheet tuần này (SUBMITTED)...")
        ts_count = 0
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        
        for emp in employees[:15]: 
            emp_number = emp[0]
            cursor.execute("DELETE FROM ohrm_timesheet WHERE employee_id=%s AND start_date=%s", 
                          (emp_number, start_of_week))
            
            cursor.execute("""
                INSERT INTO ohrm_timesheet (state, start_date, end_date, employee_id) 
                VALUES ('SUBMITTED', %s, %s, %s)
            """, (start_of_week, start_of_week + timedelta(days=6), emp_number))
            ts_id = cursor.lastrowid
            
            for i in range(5): 
                work_date = start_of_week + timedelta(days=i)
                cursor.execute("""
                    INSERT INTO ohrm_timesheet_item 
                    (timesheet_id, date, duration, project_id, employee_id, activity_id, comment) 
                    VALUES (%s, %s, 28800, %s, %s, %s, 'Daily development work')
                """, (ts_id, work_date, proj_id, emp_number, act_id))
            ts_count += 1

        # ===== 3. TIMESHEETS (Past - Approved) =====
        print("-> (3/4) Tạo Timesheet quá khứ (APPROVED)...")
        for week_ago in range(1, 3): 
            past_date = today - timedelta(weeks=week_ago)
            start_week_past = past_date - timedelta(days=past_date.weekday())
            for emp in employees[:10]:
                cursor.execute("""
                    SELECT timesheet_id FROM ohrm_timesheet 
                    WHERE employee_id=%s AND start_date=%s
                """, (emp[0], start_week_past))
                if cursor.fetchone(): 
                    continue
                    
                cursor.execute("""
                    INSERT INTO ohrm_timesheet (state, start_date, end_date, employee_id) 
                    VALUES ('APPROVED', %s, %s, %s)
                """, (start_week_past, start_week_past+timedelta(6), emp[0]))
                ts_id_past = cursor.lastrowid
                
                for i in range(5):
                    cursor.execute("""
                        INSERT INTO ohrm_timesheet_item 
                        (timesheet_id, date, duration, project_id, employee_id, activity_id) 
                        VALUES (%s, %s, 28800, %s, %s, %s)
                    """, (ts_id_past, start_week_past+timedelta(i), proj_id, emp[0], act_id))

        # ===== 4. ATTENDANCE =====
        print("-> (4/4) Tạo Attendance Records...")
        att_count = 0
        for emp in employees:
            for i in range(5):
                w_date = today - timedelta(days=random.randint(1, 14))
                if w_date.weekday() < 5:
                    in_t = datetime.combine(w_date, datetime.strptime("08:00:00", "%H:%M:%S").time())
                    out_t = datetime.combine(w_date, datetime.strptime("17:00:00", "%H:%M:%S").time())
                    cursor.execute("""
                        INSERT IGNORE INTO ohrm_attendance_record 
                        (employee_id, punch_in_user_time, punch_out_user_time, state) 
                        VALUES (%s, %s, %s, 'PUNCHED_OUT')
                    """, (emp[0], in_t, out_t))
                    att_count += 1

        assign_admin_as_supervisor(cursor, employees)

        conn.commit()
        
        print("="*50)
        print("[THÀNH CÔNG] Tóm tắt:")
        print(f"  • {entitlement_count} Leave Entitlements")
        print(f"  • {leave_count} Leave Requests")
        print(f"  • {ts_count} Timesheets (SUBMITTED)")
        print(f"  • {att_count} Attendance Records")
        print("="*50)
        print("\nKiểm tra tại:")
        print("  → Leave > Leave List (chọn 'All' để thấy tất cả)")
        print("  → Time > Timesheets > Employee Timesheets")
        print("  → Time > Attendance > Employee Records")
        
        # Export summary
        data = [
            {'Category': 'Leave Entitlements', 'Count': entitlement_count},
            {'Category': 'Leave Requests', 'Count': leave_count},
            {'Category': 'Timesheets', 'Count': ts_count},
            {'Category': 'Attendance', 'Count': att_count}
        ]
        path = os.path.join(EXPORT_DIR, 'ess_generation_summary.csv')
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Category', 'Count'])
            writer.writeheader()
            writer.writerows(data)
        print(f"\nBáo cáo đã xuất: {path}")

    except mysql.connector.Error as err:
        print(f"Lỗi MySQL: {err}")
        conn.rollback()
    finally:
        if conn: 
            conn.close()

if __name__ == "__main__":
    generate_ess_data()