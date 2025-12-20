import os
import mysql.connector
from dotenv import load_dotenv
from faker import Faker
import random
import csv
from datetime import datetime

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

def generate_reporting_data():
    conn = connect_db()
    cursor = conn.cursor()
    print("="*50)
    print("GENERATE REPORTING & RECRUITMENT DATA")
    print("="*50)

    try:
        # BƯỚC PHỤ: Lấy danh sách ID nhân viên để làm Hiring Manager
        print("-> Đang lấy danh sách nhân viên làm Hiring Manager...")
        cursor.execute("SELECT emp_number FROM hs_hr_employee")
        emp_rows = cursor.fetchall()
        emp_ids = [r[0] for r in emp_rows]
        
        if not emp_ids:
            print("LỖI: Không tìm thấy nhân viên nào để làm Hiring Manager. Hãy chạy generate_dim.py trước.")
            return

        # 1. TẠO JOB VACANCY (VỊ TRÍ TUYỂN DỤNG)
        print("-> Đang kiểm tra Job Titles...")
        cursor.execute("SELECT id, job_title FROM ohrm_job_title WHERE is_deleted=0")
        titles = cursor.fetchall()
        
        vacancy_ids = []
        if titles:
            print(f"-> Tìm thấy {len(titles)} chức danh. Đang tạo Vacancy...")
            for t_id, t_name in titles:
                # Kiểm tra xem vacancy đã có chưa
                cursor.execute("SELECT id FROM ohrm_job_vacancy WHERE job_title_code=%s", (t_id,))
                res = cursor.fetchone()
                if res:
                    vacancy_ids.append(res[0])
                else:
                    # === FIX: Chọn Hiring Manager ngẫu nhiên ===
                    hiring_manager_id = random.choice(emp_ids)
                    
                    sql_vac = """
                        INSERT INTO ohrm_job_vacancy 
                        (job_title_code, name, status, description, defined_time, updated_time, hiring_manager_id)
                        VALUES (%s, %s, 1, %s, NOW(), NOW(), %s)
                    """
                    vac_name = f"Senior {t_name}"
                    cursor.execute(sql_vac, (t_id, vac_name, f"Looking for experienced {t_name}", hiring_manager_id))
                    vacancy_ids.append(cursor.lastrowid)
        else:
            print("Cảnh báo: Không có Job Title nào. Hãy chạy generate_dim.py trước.")

        # 2. TẠO CANDIDATES (ỨNG VIÊN)
        print("-> Đang tạo hồ sơ ứng viên (Candidates)...")
        candidates_data = []
        
        for _ in range(30): 
            first = fake.first_name()
            last = fake.last_name()
            email = f"{first.lower()}.{last.lower()}.{random.randint(10,99)}@example.com"
            phone = fake.phone_number()
            date_app = fake.date_between(start_date='-3m', end_date='today')
            
            # Status: 1=Active
            sql_cand = """
                INSERT INTO ohrm_job_candidate 
                (first_name, last_name, email, contact_number, date_of_application, status, comment, mode_of_application)
                VALUES (%s, %s, %s, %s, %s, 1, %s, 1)
            """
            cursor.execute(sql_cand, (first, last, email, phone, date_app, fake.sentence()))
            cand_id = cursor.lastrowid
            
            vac_name = "N/A"
            if vacancy_ids:
                vac_id = random.choice(vacancy_ids)
                # Gán ứng viên vào Vacancy
                try:
                    cursor.execute("INSERT INTO ohrm_job_candidate_vacancy (candidate_id, vacancy_id, status, applied_date) VALUES (%s, %s, 'APPLICATION INITIATED', %s)", 
                                   (cand_id, vac_id, date_app))
                    vac_name = str(vac_id)
                except:
                    pass

            candidates_data.append({
                'Candidate ID': cand_id,
                'Name': f"{first} {last}",
                'Email': email,
                'Applied Date': date_app,
                'Vacancy ID': vac_name
            })

        conn.commit()
        print(f"   Đã tạo {len(candidates_data)} ứng viên.")

        # 3. XUẤT BÁO CÁO CSV
        write_csv(candidates_data, "reporting_candidates.csv")
        
        # Lấy dữ liệu nhân viên để làm báo cáo
        cursor.execute("""
            SELECT e.emp_number, e.emp_lastname, e.emp_firstname, j.job_title, l.name as location
            FROM hs_hr_employee e
            LEFT JOIN ohrm_job_title j ON e.job_title_code = j.id
            LEFT JOIN hs_hr_emp_locations el ON e.emp_number = el.emp_number
            LEFT JOIN ohrm_location l ON el.location_id = l.id
        """)
        emp_rows = cursor.fetchall()
        emp_csv_data = [{'ID': r[0], 'Name': f"{r[1]} {r[2]}", 'Job': r[3], 'Location': r[4]} for r in emp_rows]
        write_csv(emp_csv_data, "reporting_existing_employees.csv")

    except mysql.connector.Error as err:
        print(f"Lỗi MySQL: {err}")
    finally:
        if conn: conn.close()

def write_csv(data_list, filename):
    if not data_list: return
    path = os.path.join(EXPORT_DIR, filename)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        keys = data_list[0].keys()
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data_list)
    print(f"-> Exported: {path}")

if __name__ == "__main__":
    generate_reporting_data()