import mysql.connector
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from faker import Faker

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

def generate_hr_admin_data():
    """
    Tạo dữ liệu cho module HR Administration:
    - Organization Info
    - Locations
    - Pay Grades
    - Education Levels
    - Languages
    - Skills
    - Licenses
    - Nationalities
    """
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        print("-> Kết nối Database thành công!")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # BƯỚC 1: TẠO ORGANIZATION INFO
        print("-> Đang tạo Organization Info...")
        
        cursor.execute("""
            INSERT INTO ohrm_organization_gen_info 
            (name, tax_id, registration_number, phone, fax, email, 
             country, province, city, zip_code, street1, street2, note)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE name = VALUES(name)
        """, (
            'OrangeHRM Vietnam Co., Ltd',
            'VN1234567890',
            'BIZ-2024-001',
            '+84-28-1234-5678',
            '+84-28-1234-5679',
            'hr@orangehrm.com.vn',
            'VN',
            'Ho Chi Minh',
            'Ho Chi Minh City',
            '700000',
            '123 Nguyen Hue Boulevard',
            'District 1',
            'Leading HR Solutions Provider in Vietnam'
        ))
        print("   Đã tạo Organization Info")

        # BƯỚC 2: TẠO LOCATIONS
        print("-> Đang tạo Locations...")
        
        locations = [
            ('Head Office - HCMC', 'VN', 'Ho Chi Minh', '123 Nguyen Hue, District 1', '700000', '+84-28-1234-5678'),
            ('Branch Office - Hanoi', 'VN', 'Ha Noi', '456 Lang Ha, Dong Da', '100000', '+84-24-1234-5678'),
            ('Branch Office - Da Nang', 'VN', 'Da Nang', '789 Bach Dang, Hai Chau', '550000', '+84-236-123-4567'),
            ('R&D Center', 'VN', 'Ho Chi Minh', '321 Vo Van Kiet, District 5', '700000', '+84-28-9876-5432'),
            ('Training Center', 'VN', 'Ho Chi Minh', '654 Le Loi, District 1', '700000', '+84-28-5555-6666'),
        ]

        location_ids = []
        for loc in locations:
            cursor.execute("""
                INSERT IGNORE INTO ohrm_location 
                (name, country_code, city, address, zip_code, phone)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, loc)
            cursor.execute("SELECT id FROM ohrm_location WHERE name = %s", (loc[0],))
            result = cursor.fetchone()
            if result:
                location_ids.append(result[0])
        
        print(f"   Đã tạo {len(locations)} Locations")

        # BƯỚC 3: TẠO PAY GRADES
        print("-> Đang tạo Pay Grades...")
        
        pay_grades = [
            ('Grade A - Executive', 50000000, 100000000),
            ('Grade B - Senior', 30000000, 50000000),
            ('Grade C - Mid-Level', 15000000, 30000000),
            ('Grade D - Junior', 8000000, 15000000),
            ('Grade E - Entry', 5000000, 8000000),
        ]

        for grade_name, min_sal, max_sal in pay_grades:
            cursor.execute("""
                INSERT IGNORE INTO ohrm_pay_grade (name) VALUES (%s)
            """, (grade_name,))
            cursor.execute("SELECT id FROM ohrm_pay_grade WHERE name = %s", (grade_name,))
            grade_id = cursor.fetchone()
            if grade_id:
                cursor.execute("""
                    INSERT IGNORE INTO ohrm_pay_grade_currency 
                    (pay_grade_id, currency_id, min_salary, max_salary)
                    VALUES (%s, 'VND', %s, %s)
                """, (grade_id[0], min_sal, max_sal))
        
        print(f"   Đã tạo {len(pay_grades)} Pay Grades")

        # BƯỚC 4: TẠO EDUCATION LEVELS
        print("-> Đang tạo Education Levels...")
        
        education_levels = [
            'High School',
            'Vocational Certificate',
            'Associate Degree',
            'Bachelor\'s Degree',
            'Master\'s Degree',
            'Doctorate (PhD)',
        ]

        for edu in education_levels:
            cursor.execute("""
                INSERT IGNORE INTO ohrm_education (name) VALUES (%s)
            """, (edu,))
        
        print(f"   Đã tạo {len(education_levels)} Education Levels")

        # BƯỚC 5: TẠO LANGUAGES
        print("-> Đang tạo Languages...")
        
        languages = [
            'Vietnamese',
            'English',
            'Japanese',
            'Korean',
            'Chinese (Mandarin)',
            'French',
            'German',
        ]

        for lang in languages:
            cursor.execute("""
                INSERT IGNORE INTO ohrm_language (name) VALUES (%s)
            """, (lang,))
        
        print(f"   Đã tạo {len(languages)} Languages")

        # BƯỚC 6: TẠO SKILLS
        print("-> Đang tạo Skills...")
        
        skills = [
            ('Programming - Python', 'Python programming and data analysis'),
            ('Programming - Java', 'Java/Spring development'),
            ('Programming - JavaScript', 'Frontend and Node.js development'),
            ('Database Management', 'MySQL, PostgreSQL, MongoDB'),
            ('Cloud Computing', 'AWS, Azure, GCP'),
            ('Project Management', 'Agile, Scrum, PMP'),
            ('Communication', 'Presentation and negotiation skills'),
            ('Leadership', 'Team management and mentoring'),
            ('Data Analysis', 'Excel, Power BI, Tableau'),
            ('Testing & QA', 'Manual and automation testing'),
        ]

        for skill_name, desc in skills:
            cursor.execute("""
                INSERT IGNORE INTO ohrm_skill (name, description) VALUES (%s, %s)
            """, (skill_name, desc))
        
        print(f"   Đã tạo {len(skills)} Skills")

        # BƯỚC 7: TẠO LICENSES
        print("-> Đang tạo Licenses...")
        
        licenses = [
            'Driver License Class B2',
            'AWS Certified Solutions Architect',
            'PMP Certification',
            'IELTS Certificate',
            'JLPT N2',
            'Scrum Master Certification',
            'ISTQB Foundation',
        ]

        for lic in licenses:
            cursor.execute("""
                INSERT IGNORE INTO ohrm_license (name) VALUES (%s)
            """, (lic,))
        
        print(f"   Đã tạo {len(licenses)} Licenses")

        # BƯỚC 8: GÁN SKILLS/LANGUAGES CHO NHÂN VIÊN
        print("-> Đang gán Skills và Languages cho nhân viên...")
        
        cursor.execute("SELECT emp_number FROM hs_hr_employee LIMIT 50")
        employees = cursor.fetchall()

        cursor.execute("SELECT id FROM ohrm_skill")
        skill_ids = [s[0] for s in cursor.fetchall()]

        cursor.execute("SELECT id FROM ohrm_language")
        lang_ids = [l[0] for l in cursor.fetchall()]

        cursor.execute("SELECT id FROM ohrm_education")
        edu_ids = [e[0] for e in cursor.fetchall()]

        skill_count = 0
        lang_count = 0
        edu_count = 0

        for (emp_number,) in employees:
            # Gán 2-4 skills ngẫu nhiên
            for skill_id in random.sample(skill_ids, min(random.randint(2, 4), len(skill_ids))):
                years = random.randint(1, 10)
                try:
                    cursor.execute("""
                        INSERT IGNORE INTO hs_hr_emp_skill 
                        (emp_number, skill_id, years_of_exp, comments)
                        VALUES (%s, %s, %s, %s)
                    """, (emp_number, skill_id, years, f'{years} years of experience'))
                    skill_count += 1
                except:
                    pass

            # Gán 1-2 languages
            for lang_id in random.sample(lang_ids, min(random.randint(1, 2), len(lang_ids))):
                fluency = random.choice([1, 2, 3])  # Basic, Intermediate, Advanced
                competency = random.choice([1, 2, 3, 4])  # Reading, Writing, Speaking, All
                try:
                    cursor.execute("""
                        INSERT IGNORE INTO hs_hr_emp_language 
                        (emp_number, lang_id, fluency, competency, comments)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (emp_number, lang_id, fluency, competency, 'Work proficiency'))
                    lang_count += 1
                except:
                    pass

            # Gán 1 education
            if edu_ids:
                edu_id = random.choice(edu_ids)
                try:
                    cursor.execute("""
                        INSERT IGNORE INTO ohrm_emp_education 
                        (emp_number, education_id, institute, major, year, score, start_date, end_date)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        emp_number, 
                        edu_id, 
                        random.choice(['HCMUS', 'HCMUT', 'UEH', 'FPT University', 'RMIT Vietnam']),
                        random.choice(['Computer Science', 'Business Administration', 'Engineering', 'IT']),
                        random.randint(2010, 2023),
                        round(random.uniform(2.5, 4.0), 2),
                        f'{random.randint(2006, 2019)}-09-01',
                        f'{random.randint(2010, 2023)}-06-30'
                    ))
                    edu_count += 1
                except:
                    pass

        print(f"   Đã gán {skill_count} Skills, {lang_count} Languages, {edu_count} Education records")

        # BƯỚC 9: TẠO WORK SHIFTS
        print("-> Đang tạo Work Shifts...")
        
        work_shifts = [
            ('Morning Shift', '08:00:00', '17:00:00'),
            ('Evening Shift', '14:00:00', '23:00:00'),
            ('Night Shift', '22:00:00', '07:00:00'),
            ('Flexible Hours', '09:00:00', '18:00:00'),
        ]

        for shift_name, start_time, end_time in work_shifts:
            cursor.execute("""
                INSERT IGNORE INTO ohrm_work_shift 
                (name, hours_per_day, start_time, end_time)
                VALUES (%s, 8, %s, %s)
            """, (shift_name, start_time, end_time))
        
        print(f"   Đã tạo {len(work_shifts)} Work Shifts")

        # BƯỚC 10: TẠO SUBUNITS (Phòng ban)
        print("-> Đang tạo Subunits (Phòng ban)...")
        
        subunits = [
            (2, 'Engineering', 1, 1, 2),
            (3, 'Human Resources', 1, 3, 4),
            (4, 'Finance', 1, 5, 6),
            (5, 'Marketing', 1, 7, 8),
            (6, 'Sales', 1, 9, 10),
        ]
        
        for unit_id, name, level, lft, rgt in subunits:
            cursor.execute("""
                INSERT IGNORE INTO ohrm_subunit (id, name, unit_id, level, lft, rgt)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (unit_id, name, unit_id, level, lft, rgt))
        
        print(f"   Đã tạo {len(subunits)} Subunits")

        # BƯỚC 11: TẠO HOLIDAYS
        print("-> Đang tạo Holidays (Ngày lễ)...")
        
        holidays = [
            ('New Year', '2025-01-01', 1, 0),
            ('Lunar New Year Eve', '2025-01-28', 1, 0),
            ('Lunar New Year Day 1', '2025-01-29', 1, 0),
            ('Lunar New Year Day 2', '2025-01-30', 1, 0),
            ('Lunar New Year Day 3', '2025-01-31', 1, 0),
            ('Hung Kings Day', '2025-04-07', 1, 0),
            ('Reunification Day', '2025-04-30', 1, 0),
            ('Labour Day', '2025-05-01', 1, 0),
            ('National Day', '2025-09-02', 1, 0),
        ]
        
        for name, date, length, recurring in holidays:
            cursor.execute("""
                INSERT IGNORE INTO ohrm_holiday (description, date, length, recurring, operational_country_id)
                VALUES (%s, %s, %s, %s, NULL)
            """, (name, date, length, recurring))
        
        print(f"   Đã tạo {len(holidays)} Holidays")

        # BƯỚC 12: GÁN SALARY, LICENSE, WORK SHIFT, LOCATION CHO NHÂN VIÊN
        print("-> Đang gán Salary, License, Work Shift, Location cho nhân viên...")
        
        cursor.execute("SELECT id FROM ohrm_pay_grade")
        pay_grade_ids = [p[0] for p in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM ohrm_license")
        license_ids = [l[0] for l in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM ohrm_work_shift")
        shift_ids = [s[0] for s in cursor.fetchall()]
        
        cursor.execute("SELECT id FROM ohrm_location")
        loc_ids = [l[0] for l in cursor.fetchall()]
        
        salary_count = 0
        license_count = 0
        shift_count = 0
        location_count = 0
        
        for (emp_number,) in employees:
            # Gán salary
            if pay_grade_ids:
                pay_grade_id = random.choice(pay_grade_ids)
                salary = random.randint(8000000, 50000000)
                try:
                    cursor.execute("""
                        INSERT IGNORE INTO hs_hr_emp_basicsalary 
                        (emp_number, sal_grd_code, currency_id, ebsal_basic_salary, payperiod_code, salary_component, comments)
                        VALUES (%s, %s, 'VND', %s, 5, 'Basic Salary', 'Monthly salary')
                    """, (emp_number, pay_grade_id, salary))
                    salary_count += 1
                except:
                    pass
            
            # Gán license (1-2 licenses)
            if license_ids:
                for lic_id in random.sample(license_ids, min(random.randint(1, 2), len(license_ids))):
                    try:
                        cursor.execute("""
                            INSERT IGNORE INTO ohrm_emp_license 
                            (emp_number, license_id, license_no, license_issued_date, license_expiry_date)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (
                            emp_number, 
                            lic_id, 
                            f'LIC-{emp_number}-{lic_id}',
                            f'{random.randint(2020, 2023)}-{random.randint(1,12):02d}-01',
                            f'{random.randint(2025, 2028)}-{random.randint(1,12):02d}-01'
                        ))
                        license_count += 1
                    except:
                        pass
            
            # Gán work shift
            if shift_ids:
                shift_id = random.choice(shift_ids)
                try:
                    cursor.execute("""
                        INSERT IGNORE INTO ohrm_employee_work_shift (work_shift_id, emp_number)
                        VALUES (%s, %s)
                    """, (shift_id, emp_number))
                    shift_count += 1
                except:
                    pass
            
            # Gán location
            if loc_ids:
                loc_id = random.choice(loc_ids)
                try:
                    cursor.execute("""
                        INSERT IGNORE INTO hs_hr_emp_locations (emp_number, location_id)
                        VALUES (%s, %s)
                    """, (emp_number, loc_id))
                    location_count += 1
                except:
                    pass
        
        print(f"   Đã gán {salary_count} Salaries, {license_count} Licenses, {shift_count} Work Shifts, {location_count} Locations")

        # COMMIT
        conn.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        print("\n" + "="*50)
        print("[THÀNH CÔNG] Đã tạo dữ liệu HR Administration!")
        print("="*50)
        print(f"  - Organization Info: 1")
        print(f"  - Locations: {len(locations)}")
        print(f"  - Pay Grades: {len(pay_grades)}")
        print(f"  - Education Levels: {len(education_levels)}")
        print(f"  - Languages: {len(languages)}")
        print(f"  - Skills: {len(skills)}")
        print(f"  - Licenses: {len(licenses)}")
        print(f"  - Work Shifts: {len(work_shifts)}")
        print(f"  - Subunits: {len(subunits)}")
        print(f"  - Holidays: {len(holidays)}")
        print(f"  - Employee Skills: {skill_count}")
        print(f"  - Employee Languages: {lang_count}")
        print(f"  - Employee Education: {edu_count}")
        print(f"  - Employee Salaries: {salary_count}")
        print(f"  - Employee Licenses: {license_count}")
        print(f"  - Employee Work Shifts: {shift_count}")
        print(f"  - Employee Locations: {location_count}")

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
    print("GENERATE HR ADMINISTRATION DATA")
    print("="*50)
    generate_hr_admin_data()
