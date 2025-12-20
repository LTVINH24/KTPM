import os
import mysql.connector
from dotenv import load_dotenv
from faker import Faker
import random
import csv
from datetime import datetime

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
        # Lấy nhân viên làm Hiring Manager
        print("-> Đang lấy danh sách Hiring Manager...")
        cursor.execute("SELECT emp_number FROM hs_hr_employee")
        emp_rows = cursor.fetchall()
        emp_ids = [r[0] for r in emp_rows]
        
        if not emp_ids:
            print("LỖI: Chưa có nhân viên (generate_dim).")
            return

        # 1. VACANCIES (Vị trí tuyển dụng)
        print("-> (1/3) Tạo Vacancies...")
        cursor.execute("SELECT id, job_title FROM ohrm_job_title WHERE is_deleted=0")
        titles = cursor.fetchall()
        
        vacancy_ids = []
        if titles:
            for t_id, t_name in titles:
                cursor.execute("SELECT id FROM ohrm_job_vacancy WHERE job_title_code=%s", (t_id,))
                res = cursor.fetchone()
                if res:
                    vacancy_ids.append(res[0])
                else:
                    hiring_manager_id = random.choice(emp_ids)
                    sql_vac = """
                        INSERT INTO ohrm_job_vacancy 
                        (job_title_code, name, status, description, defined_time, updated_time, hiring_manager_id)
                        VALUES (%s, %s, 1, %s, NOW(), NOW(), %s)
                    """
                    cursor.execute(sql_vac, (t_id, f"Senior {t_name}", f"Looking for {t_name}", hiring_manager_id))
                    vacancy_ids.append(cursor.lastrowid)

        # 2. CANDIDATES (Ứng viên) - Nâng cấp: Đa dạng trạng thái
        print("-> (2/3) Tạo Candidates với nhiều trạng thái (để test Filter)...")
        candidates_data = []
        
        # Danh sách trạng thái để test filtering
        # Lưu ý: Các string này cần khớp với config của OHRM, nếu không dùng ID mặc định 'APPLICATION INITIATED'
        # Ở đây ta giả lập bằng cách gán vào cột comment hoặc tạo nhiều bản ghi
        
        for _ in range(30): 
            first = fake.first_name()
            last = fake.last_name()
            email = f"{first.lower()}.{last.lower()}.{random.randint(10,99)}@example.com"
            phone = fake.phone_number()
            date_app = fake.date_between(start_date='-3m', end_date='today')
            
            # Insert Candidate Profile
            sql_cand = """
                INSERT INTO ohrm_job_candidate 
                (first_name, last_name, email, contact_number, date_of_application, status, comment, mode_of_application)
                VALUES (%s, %s, %s, %s, %s, 1, %s, 1)
            """
            cursor.execute(sql_cand, (first, last, email, phone, date_app, "Generated for Testing"))
            cand_id = cursor.lastrowid
            
            vac_name = "N/A"
            status_text = "APPLICATION INITIATED"
            
            if vacancy_ids:
                vac_id = random.choice(vacancy_ids)
                # Random trạng thái quy trình tuyển dụng
                # Các status phổ biến: APPLICATION INITIATED, SHORTLISTED, SCHEDULED INTERVIEW, HIRED, REJECTED
                status_text = random.choice(['APPLICATION INITIATED', 'SHORTLISTED', 'HIRED', 'REJECTED'])
                
                try:
                    cursor.execute("INSERT INTO ohrm_job_candidate_vacancy (candidate_id, vacancy_id, status, applied_date) VALUES (%s, %s, %s, %s)", 
                                   (cand_id, vac_id, status_text, date_app))
                    vac_name = str(vac_id)
                except: pass

            candidates_data.append({
                'ID': cand_id,
                'Name': f"{first} {last}",
                'Status': status_text, # Quan trọng cho báo cáo
                'Vacancy ID': vac_name
            })

        conn.commit()
        print(f"   => Đã tạo {len(candidates_data)} ứng viên.")

        # 3. EXPORT EVIDENCE
        print("-> (3/3) Xuất dữ liệu chứng minh...")
        path = os.path.join(EXPORT_DIR, "reporting_candidates.csv")
        with open(path, 'w', newline='', encoding='utf-8') as f:
            keys = candidates_data[0].keys()
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(candidates_data)
        
        # Xuất thêm danh sách nhân viên để test Employee Report
        cursor.execute("SELECT emp_number, emp_lastname, emp_firstname FROM hs_hr_employee LIMIT 20")
        emp_rows = cursor.fetchall()
        with open(os.path.join(EXPORT_DIR, "reporting_employees.csv"), 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name'])
            for r in emp_rows:
                writer.writerow([r[0], f"{r[1]} {r[2]}"])
                
        print(f"-> File báo cáo: {path}")

    except mysql.connector.Error as err:
        print(f"Lỗi MySQL: {err}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    generate_reporting_data()