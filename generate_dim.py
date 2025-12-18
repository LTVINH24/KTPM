import mysql.connector
from faker import Faker
import random
import bcrypt
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

NUM_EMPLOYEES = 50 
START_EMP_ID = 1000 
fake = Faker('vi_VN') 

hashed_bytes = bcrypt.hashpw('OrangeHRM@111'.encode('utf-8'), bcrypt.gensalt(rounds=12))
DEFAULT_PASSWORD_HASH = hashed_bytes.decode('utf-8')

vn_cities = ["Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Cần Thơ", "Hải Phòng", "Nha Trang", "Vũng Tàu", "Biên Hòa"]
vn_streets = [
    "Nguyễn Huệ", "Lê Lợi", "Trần Hưng Đạo", "Hai Bà Trưng", "Lý Thường Kiệt", 
    "Điện Biên Phủ", "Nam Kỳ Khởi Nghĩa", "Pasteur", "Võ Văn Kiệt", "Phạm Văn Đồng",
    "Hoàng Diệu", "Phan Đình Phùng", "Nguyễn Trãi", "Lê Duẩn", "Trường Chinh"
]

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def generate_pim_data():
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor(buffered=True)
        print("-> Kết nối Database thành công!")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # BƯỚC 1: TẠO DỮ LIỆU JOB TITLES
        print("-> Đang tạo Job Titles...")

        job_titles = ['Director', 'Manager', 'Staff']
        job_map = {}
        for title in job_titles:
            cursor.execute("INSERT IGNORE INTO ohrm_job_title (job_title, is_deleted) VALUES (%s, 0)", (title,))
            cursor.execute("SELECT id FROM ohrm_job_title WHERE job_title = %s", (title,))
            job_map[title] = cursor.fetchone()[0]

        # BƯỚC 2: TẠO DỮ LIỆU EMPLOYMENT STATUS
        print("-> Đang tạo Employment Status...")

        statuses = ['Full-Time Permanent', 'Full-Time Contract']
        status_map = {}
        for s in statuses:
            cursor.execute("INSERT IGNORE INTO ohrm_employment_status (name) VALUES (%s)", (s,))
            cursor.execute("SELECT id FROM ohrm_employment_status WHERE name = %s", (s,))
            status_map[s] = cursor.fetchone()[0]

        # BƯỚC 3:  TẠO DỮ LIỆU NHÂN VIÊN & USER
        print(f"-> Đang tạo {NUM_EMPLOYEES} nhân viên và tài khoản...")
        
        director_id = None
        manager_ids = []
        staff_ids = []

        sql_employee = (
            "INSERT INTO hs_hr_employee "
            "(emp_number, employee_id, emp_lastname, emp_firstname, emp_middle_name, "
            "emp_birthday, emp_gender, emp_marital_status, job_title_code, emp_status, "
            "joined_date, emp_street1, city_code, coun_code, emp_zipcode, "
            "emp_hm_telephone, emp_work_telephone, emp_work_email) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )

        # Tạo tài khoản User

        sql_user = (
            "INSERT INTO ohrm_user (user_role_id, emp_number, user_name, user_password, status, deleted) "
            "VALUES (%s, %s, %s, %s, 1, 0)"
        )

        for i in range(NUM_EMPLOYEES):
            emp_number = START_EMP_ID + i
            
            # 1. TÊN & GIỚI TÍNH
            gender = random.choice([1, 2])
            lastname = fake.last_name()
            if gender == 1:
                firstname = fake.first_name_male()
                middle_name = random.choice(["Văn", "Hữu", "Đức", "Công", "Quang", "Minh"])
            else:
                firstname = fake.first_name_female()
                middle_name = random.choice(["Thị", "Ngọc", "Thu", "Mai", "Phương", "Diệu"])

            # 2. PHÂN CẤP CHỨC DANH (SẾP vs NHÂN VIÊN)
            user_role_id = 2 

            if i == 0: 
                # Giám Đốc
                job_code = job_map['Director']
                status_code = status_map['Full-Time Permanent']
                dob = fake.date_of_birth(minimum_age=40, maximum_age=55)
                director_id = emp_number
                user_role_id = 1 
            elif i < 5: 
                # Quản Lý
                job_code = job_map['Manager']
                status_code = status_map['Full-Time Permanent']
                dob = fake.date_of_birth(minimum_age=30, maximum_age=50)
                manager_ids.append(emp_number)
            else: 
                # Nhân viên
                job_code = job_map['Staff']
                status_code = status_map['Full-Time Contract']
                dob = fake.date_of_birth(minimum_age=22, maximum_age=35)
                staff_ids.append(emp_number)

            # 3. DỮ LIỆU KHÁC
            emp_id_str = f"EMP{emp_number:04d}"
            marital = random.choice(['Single', 'Married'])
            joined_date = fake.date_between(start_date='-5y', end_date='today')
            street1 = f"{random.randint(1, 999)} {random.choice(vn_streets)}"
            city_code = random.choice(vn_cities)
            coun_code = 'VN'
            zipcode = fake.postcode()
            hm_telephone = f"02{random.randint(10000000, 99999999)}"
            work_telephone = f"09{random.randint(10000000, 99999999)}"
            
            # [CẬP NHẬT NHỎ] Tạo username trước để dùng chung cho Email và Login
            username = fake.user_name()
            # Thêm số ngẫu nhiên để tránh trùng lặp username
            username = f"{username}{random.randint(10,99)}" 
            work_email = f"{username}@orangehrm.com"

            val = (
                emp_number, emp_id_str, lastname, firstname, middle_name,
                dob, gender, marital, job_code, status_code,
                joined_date, street1, city_code, coun_code, zipcode,
                hm_telephone, work_telephone, work_email
            )
            try: 
                cursor.execute(sql_employee, val)
                cursor.execute(sql_user, (user_role_id, emp_number, username, DEFAULT_PASSWORD_HASH))
                
            except mysql.connector.Error as err: 
                print(f"Lỗi {emp_number}: {err}")

        # BƯỚC 4:TẠO DỮ LIỆU REPORTING
        print("-> Đang tạo dữ liệu báo cáo...")
        cursor.execute("INSERT IGNORE INTO ohrm_emp_reporting_method (reporting_method_id, reporting_method_name) VALUES (1, 'Direct')")
        sql_report = "INSERT INTO hs_hr_emp_reportto (erep_sup_emp_number, erep_sub_emp_number, erep_reporting_mode) VALUES (%s, %s, 1)"

        # 1. Staff báo cáo cho Manager
        for s_id in staff_ids:
            if manager_ids:
                try: cursor.execute(sql_report, (random.choice(manager_ids), s_id))
                except: pass
        
        # 2. Manager báo cáo cho Director
        for m_id in manager_ids:
            if director_id:
                try: cursor.execute(sql_report, (director_id, m_id))
                except: pass

        conn.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print(f"\n[THÀNH CÔNG] Đã tạo {NUM_EMPLOYEES} nhân viên và tài khoản.")
        
    except mysql.connector.Error as err:
        print(f"Lỗi MySQL: {err}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    generate_pim_data()