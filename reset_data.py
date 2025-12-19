import mysql.connector
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

def reset_all_data():
    """
    Xóa tất cả dữ liệu đã được tạo bởi các script generate.
    Thứ tự xóa quan trọng do foreign key constraints.
    """
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(buffered=True)
        print("-> Kết nối Database thành công!")
        
        # Tắt kiểm tra foreign key
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        # === PERFORMANCE MODULE ===
        print("\n[1/4] Xóa dữ liệu Performance Management...")
        performance_tables = [
            'ohrm_reviewer_rating',
            'ohrm_performance_tracker_log',
            'ohrm_performance_track',
            'ohrm_reviewer',
            'ohrm_performance_review',
            'ohrm_kpi',
        ]
        for table in performance_tables:
            try:
                cursor.execute(f"DELETE FROM {table}")
                print(f"   ✓ Đã xóa {table}")
            except Exception as e:
                print(f"   ✗ Lỗi xóa {table}: {e}")
        
        # === TIME & ATTENDANCE MODULE ===
        print("\n[2/4] Xóa dữ liệu Time & Attendance...")
        time_tables = [
            'ohrm_attendance_record',
            'ohrm_timesheet_item',
            'ohrm_timesheet',
            'ohrm_project_activity',
            'ohrm_project_admin',
            'ohrm_project',
            'ohrm_customer',
        ]
        for table in time_tables:
            try:
                cursor.execute(f"DELETE FROM {table}")
                print(f"   ✓ Đã xóa {table}")
            except Exception as e:
                print(f"   ✗ Lỗi xóa {table}: {e}")
        
        # === LEAVE MODULE ===
        print("\n[3/6] Xóa dữ liệu Leave Management...")
        leave_tables = [
            'ohrm_leave_comment',
            'ohrm_leave_request_comment',
            'ohrm_leave',
            'ohrm_leave_request',
            'ohrm_leave_entitlement',
            'ohrm_leave_type',
            'ohrm_leave_period_history',
            'ohrm_leave_status',
        ]
        for table in leave_tables:
            try:
                cursor.execute(f"DELETE FROM {table}")
                print(f"   ✓ Đã xóa {table}")
            except Exception as e:
                print(f"   ✗ Lỗi xóa {table}: {e}")
        
        # === RECRUITMENT MODULE ===
        print("\n[4/6] Xóa dữ liệu Recruitment...")
        recruitment_tables = [
            'ohrm_job_interview_attachment',      
            'ohrm_job_interview_interviewer',     
            'ohrm_job_interview',                 
            'ohrm_job_candidate_history',         
            'ohrm_job_candidate_attachment',      
            'ohrm_job_candidate_vacancy',         
            'ohrm_job_candidate',                 
            'ohrm_job_vacancy_attachment',        
            'ohrm_job_vacancy',                   
        ]
        for table in recruitment_tables:
            try:
                cursor.execute(f"DELETE FROM {table}")
                print(f"   ✓ Đã xóa {table}")
            except Exception as e:
                print(f"   ✗ Lỗi xóa {table}: {e}")
        
        # === HR ADMIN MODULE ===
        print("\n[5/6] Xóa dữ liệu HR Administration...")
        hr_admin_tables = [
            # Employee assignments
            'hs_hr_emp_skill',
            'hs_hr_emp_language',
            'ohrm_emp_license',
            'ohrm_emp_education',
            'ohrm_employee_work_shift',
            'hs_hr_emp_reportto',
            # Master data
            'ohrm_work_shift',
            'ohrm_holiday',
            'ohrm_pay_grade_currency',
            'ohrm_pay_grade',
            'ohrm_skill',
            'ohrm_language',
            'ohrm_license',
            'ohrm_education',
            'ohrm_subunit',
            'ohrm_location',
            'ohrm_organization_gen_info',
        ]
        for table in hr_admin_tables:
            try:
                cursor.execute(f"DELETE FROM {table}")
                print(f"   ✓ Đã xóa {table}")
            except Exception as e:
                print(f"   ✗ Lỗi xóa {table}: {e}")
        
        # === PIM / EMPLOYEES ===
        print("\n[6/6] Xóa dữ liệu Employees...")
        employee_tables = [
            'ohrm_user',
            'hs_hr_employee',
            'ohrm_employment_status',
            'ohrm_job_title',
            'ohrm_emp_reporting_method',
        ]
        for table in employee_tables:
            try:
                cursor.execute(f"DELETE FROM {table}")
                print(f"   ✓ Đã xóa {table}")
            except Exception as e:
                print(f"   ✗ Lỗi xóa {table}: {e}")
        
        # Bật lại kiểm tra foreign key
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        conn.commit()
        print("\n" + "="*50)
        print("[THÀNH CÔNG] Đã xóa tất cả dữ liệu test!")
        print("="*50)
        
    except mysql.connector.Error as err:
        print(f"Lỗi MySQL: {err}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"Lỗi: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("-> Đã đóng kết nối Database")

if __name__ == "__main__":
    print("="*50)
    print("RESET ALL TEST DATA")
    print("="*50)
    
    confirm = input("\n⚠️  Bạn có chắc muốn XÓA TẤT CẢ dữ liệu test? (y/n): ")
    if confirm.lower() == 'y':
        reset_all_data()
    else:
        print("Đã hủy thao tác.")
