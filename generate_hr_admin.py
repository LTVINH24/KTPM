import mysql.connector
import random
import os
from dotenv import load_dotenv
from faker import Faker
from datetime import datetime, timedelta

load_dotenv()
fake = Faker('vi_VN')

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'orangehrm'),
    'password': os.getenv('DB_PASSWORD', 'orangehrm'),
    'database': os.getenv('DB_NAME', 'orangehrm'),
    'port': int(os.getenv('DB_PORT', 3306))
}

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def generate_hr_admin_data():
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor(buffered=True) # QUAN TRỌNG: buffered=True
        print("="*50)
        print("GENERATE FULL HR ADMIN & QUALIFICATIONS")
        print("="*50)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # --- 1. SETUP MASTER DATA (Dữ liệu danh mục) ---
        
        # A. Locations
        print("-> (1/8) Master Data: Locations...")
        locs = [('Head Office HCM', 'VN', 'HCM'), ('Hanoi Branch', 'VN', 'Hanoi'), ('Da Nang Tech Hub', 'VN', 'Da Nang')]
        loc_ids = []
        for l in locs:
            cursor.execute("INSERT IGNORE INTO ohrm_location (name, country_code, city) VALUES (%s,%s,%s)", l)
            # Lấy ID (nếu insert ignore không trả về id thì query lại)
            cursor.execute("SELECT id FROM ohrm_location WHERE name=%s", (l[0],))
            loc_ids.append(cursor.fetchone()[0])

        # B. Skills
        print("-> (2/8) Master Data: Skills...")
        skills = ['Java', 'Python', 'Testing', 'Selenium', 'Project Management', 'Communication']
        skill_ids = []
        for s in skills:
            cursor.execute("INSERT IGNORE INTO ohrm_skill (name, description) VALUES (%s, 'Tech Skill')", (s,))
            cursor.execute("SELECT id FROM ohrm_skill WHERE name=%s", (s,))
            skill_ids.append(cursor.fetchone()[0])

        # C. Education
        print("-> (3/8) Master Data: Education...")
        edus = ['Bachelor of IT', 'Master of CS', 'High School', 'PhD']
        edu_ids = []
        for e in edus:
            cursor.execute("INSERT IGNORE INTO ohrm_education (name) VALUES (%s)", (e,))
            cursor.execute("SELECT id FROM ohrm_education WHERE name=%s", (e,))
            edu_ids.append(cursor.fetchone()[0])

        # D. Licenses
        print("-> (4/8) Master Data: Licenses...")
        licenses = ['AWS Certified', 'PMP', 'ISTQB Foundation', 'Scrum Master', 'Driver License B2']
        lic_ids = []
        for l in licenses:
            cursor.execute("INSERT IGNORE INTO ohrm_license (name) VALUES (%s)", (l,))
            cursor.execute("SELECT id FROM ohrm_license WHERE name=%s", (l,))
            lic_ids.append(cursor.fetchone()[0])

        # E. Languages
        print("-> (5/8) Master Data: Languages...")
        langs = ['English', 'Vietnamese', 'Japanese', 'Korean']
        lang_ids = []
        for l in langs:
            cursor.execute("INSERT IGNORE INTO ohrm_language (name) VALUES (%s)", (l,))
            cursor.execute("SELECT id FROM ohrm_language WHERE name=%s", (l,))
            lang_ids.append(cursor.fetchone()[0])

        # F. Pay Grades (Lương)
        print("-> (6/8) Master Data: Pay Grades...")
        grades = ['Grade 1 - Fresher', 'Grade 2 - Junior', 'Grade 3 - Senior', 'Grade 4 - Manager']
        grade_ids = []
        for g in grades:
            cursor.execute("INSERT IGNORE INTO ohrm_pay_grade (name) VALUES (%s)", (g,))
            cursor.execute("SELECT id FROM ohrm_pay_grade WHERE name=%s", (g,))
            gid = cursor.fetchone()[0]
            grade_ids.append(gid)
            # Thêm currency VND cho grade này
            cursor.execute("INSERT IGNORE INTO ohrm_pay_grade_currency (pay_grade_id, currency_id, min_salary, max_salary) VALUES (%s, 'VND', 10000000, 100000000)", (gid,))

        # --- 2. ASSIGN DATA TO EMPLOYEES (Gán dữ liệu cho nhân viên) ---
        print("-> (7/8) Đang lấy danh sách nhân viên...")
        cursor.execute("SELECT emp_number FROM hs_hr_employee")
        employees = cursor.fetchall()

        print(f"-> (8/8) Đang cập nhật Qualifications cho {len(employees)} nhân viên...")
        count = 0
        for (emp_id,) in employees:
            # 1. Location
            if loc_ids:
                cursor.execute("INSERT IGNORE INTO hs_hr_emp_locations (emp_number, location_id) VALUES (%s, %s)", (emp_id, random.choice(loc_ids)))
            
            # 2. Skill (Random 1-2 skills)
            if skill_ids:
                for _ in range(random.randint(1, 2)):
                    try: cursor.execute("INSERT IGNORE INTO hs_hr_emp_skill (emp_number, skill_id, years_of_exp) VALUES (%s, %s, %s)", (emp_id, random.choice(skill_ids), random.randint(1,5)))
                    except: pass

            # 3. Education
            if edu_ids:
                try: cursor.execute("INSERT IGNORE INTO ohrm_emp_education (emp_number, education_id, major, year) VALUES (%s, %s, 'IT', 2020)", (emp_id, random.choice(edu_ids)))
                except: pass

            # 4. License
            if lic_ids and random.choice([True, False]): # 50% nhân viên có bằng cấp
                try: 
                    l_id = random.choice(lic_ids)
                    exp_date = fake.date_between(start_date='today', end_date='+2y')
                    cursor.execute("INSERT IGNORE INTO ohrm_emp_license (emp_number, license_id, license_expiry_date) VALUES (%s, %s, %s)", (emp_id, l_id, exp_date))
                except: pass

            # 5. Language
            if lang_ids:
                try: 
                    # fluency: 1=Writing, 2=Speaking, 3=Reading (Type). competency: 1=Poor, 2=Basic, 3=Good, 4=Mother Tongue
                    cursor.execute("INSERT IGNORE INTO hs_hr_emp_language (emp_number, lang_id, fluency, competency) VALUES (%s, %s, 1, 3)", (emp_id, random.choice(lang_ids)))
                except: pass

            # 6. Work Experience (Quan trọng: User báo thiếu)
            if random.choice([True, True, False]): # 66% có kinh nghiệm cũ
                try:
                    from_date = fake.date_between(start_date='-5y', end_date='-2y')
                    to_date = fake.date_between(start_date='-2y', end_date='-1y')
                    cursor.execute("""
                        INSERT IGNORE INTO hs_hr_emp_work_experience 
                        (emp_number, employer, jobtitle, from_date, to_date, comments) 
                        VALUES (%s, %s, %s, %s, %s, 'Previous Job')
                    """, (emp_id, fake.company(), 'Developer', from_date, to_date))
                except: pass
            
            # 7. Salary (Quan trọng cho Report)
            if grade_ids:
                try:
                    g_id = random.choice(grade_ids)
                    salary = random.randint(15000000, 50000000)
                    cursor.execute("""
                        INSERT IGNORE INTO hs_hr_emp_basicsalary 
                        (emp_number, sal_grd_code, currency_id, ebsal_basic_salary, payperiod_code) 
                        VALUES (%s, %s, 'VND', %s, 'Monthly')
                    """, (emp_id, g_id, salary))
                except: pass

            count += 1

        conn.commit()
        print(f"[THÀNH CÔNG] Đã cập nhật đầy đủ Profile (Skill, Edu, Lic, Lang, WorkExp, Salary) cho {count} nhân viên.")

    except mysql.connector.Error as err:
        print(f"Lỗi MySQL: {err}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    generate_hr_admin_data()