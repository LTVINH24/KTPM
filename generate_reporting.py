import os
import mysql.connector
from dotenv import load_dotenv
import sys
from datetime import datetime, timedelta
from faker import Faker
import random

# Inline generator functions (previously in tools/data_generator.py)
fake = Faker('vi_VN')


def generate_employees(n=50, start_emp=1000):
    rows = []
    for i in range(n):
        emp_number = start_emp + i
        gender = random.choice(['Male', 'Female'])
        if gender == 'Male':
            firstname = fake.first_name_male()
            middle = random.choice(['Văn', 'Hữu', 'Đức'])
        else:
            firstname = fake.first_name_female()
            middle = random.choice(['Thị', 'Ngọc', 'Thu'])
        lastname = fake.last_name()
        username = f"{fake.user_name()}{random.randint(10,99)}"
        email = f"{username}@orangehrm.com"
        job_title = random.choice(['Director','Manager','Staff'])
        joined = fake.date_between(start_date='-5y', end_date='today')
        salary = random.randint(5000000, 100000000)

        rows.append({
            'emp_number': emp_number,
            'employee_id': f'EMP{emp_number:04d}',
            'last_name': lastname,
            'first_name': firstname,
            'middle_name': middle,
            'gender': gender,
            'job_title': job_title,
            'joined_date': str(joined),
            'work_email': email,
            'username': username,
            'salary_vnd': salary
        })
    return rows


def generate_leave_requests(employees, pct=0.2):
    rows = []
    leave_types = ['Annual', 'Sick', 'Unpaid', 'Maternity']
    for emp in random.sample(employees, max(1, int(len(employees)*pct))):
        num = random.randint(1, 4)
        for _ in range(num):
            start = fake.date_between(start_date='-1y', end_date='today')
            length = random.randint(1, 14)
            end = (datetime.strptime(str(start), '%Y-%m-%d') + timedelta(days=length-1)).date()
            status = random.choice(['Pending','Approved','Rejected'])
            rows.append({
                'emp_number': emp['emp_number'],
                'leave_type': random.choice(leave_types),
                'date_from': str(start),
                'date_to': str(end),
                'days': length,
                'status': status,
                'comments': fake.sentence(nb_words=6)
            })
    return rows


def generate_timesheets(employees, weeks=4):
    rows = []
    today = datetime.now().date()
    for emp in employees:
        for w in range(weeks):
            start = today - timedelta(days=today.weekday() + 7*(w+1))
            for d in range(5):
                work_date = start + timedelta(days=d)
                duration_hours = random.choice([8,8.5,9])
                rows.append({
                    'emp_number': emp['emp_number'],
                    'date': str(work_date),
                    'duration_hours': duration_hours,
                    'project': random.choice(['Super App','E-Banking Web','HRM System','Internal'])
                })
    return rows


def generate_recruitment_candidates(n=20):
    rows = []
    positions = ['Software Engineer','QA Engineer','Product Manager','Business Analyst']
    for i in range(n):
        app_date = fake.date_between(start_date='-6M', end_date='today')
        rows.append({
            'candidate_name': fake.name(),
            'email': fake.email(),
            'applied_for': random.choice(positions),
            'applied_date': str(app_date),
            'status': random.choice(['New','Phone Screen','Interview','Hired','Rejected'])
        })
    return rows


def generate_all(n_employees=50):
    employees = generate_employees(n_employees)
    leaves = generate_leave_requests(employees)
    timesheets = generate_timesheets(employees)
    candidates = generate_recruitment_candidates(n=20)
    return {
        'employees': employees,
        'leaves': leaves,
        'timesheets': timesheets,
        'candidates': candidates
    }

# Load env
load_dotenv()
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'orangehrm'),
    'password': os.getenv('DB_PASSWORD', 'orangehrm'),
    'database': os.getenv('DB_NAME', 'orangehrm'),
    'port': int(os.getenv('DB_PORT', 3306))
}


def connect_db():
    return mysql.connector.connect(**DB_CONFIG)


def insert_employees(cursor, employees):
    sql = (
        "INSERT IGNORE INTO hs_hr_employee "
        "(emp_number, employee_id, emp_lastname, emp_firstname, emp_middle_name, emp_work_email, joined_date) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s)"
    )
    for e in employees:
        try:
            cursor.execute(sql, (
                e['emp_number'], e['employee_id'], e['last_name'], e['first_name'], e['middle_name'], e['work_email'], e['joined_date']
            ))
        except Exception:
            pass


def insert_leaves(cursor, leaves):
    sql = (
        "INSERT IGNORE INTO ohrm_leave_request (emp_number, date_from, date_to, comments, status) VALUES (%s,%s,%s,%s,%s)"
    )
    for l in leaves:
        try:
            cursor.execute(sql, (l['emp_number'], l['date_from'], l['date_to'], l['comments'], l['status']))
        except Exception:
            pass


def insert_attendance(cursor, timesheets):
    sql = (
        "INSERT IGNORE INTO ohrm_attendance_record (employee_id, punch_in_user_time, punch_out_user_time, state) VALUES (%s,%s,%s,%s)"
    )
    for t in timesheets:
        try:
            cursor.execute(sql, (t['emp_number'], t['date'] + ' 09:00:00', t['date'] + ' 17:00:00', 'PUNCHED OUT'))
        except Exception:
            pass


def insert_candidates(cursor, candidates):
    sql = (
        "INSERT IGNORE INTO ohrm_job_candidate (name, email, applied_for, applied_date, status) VALUES (%s,%s,%s,%s,%s)"
    )
    for c in candidates:
        try:
            cursor.execute(sql, (c['candidate_name'], c['email'], c['applied_for'], c['applied_date'], c['status']))
        except Exception:
            pass


def run_reports(seed_n=50):
    # Create sample data and insert into DB (fail if DB not available)
    data = generate_all(seed_n)
    try:
        conn = connect_db()
        cursor = conn.cursor()
        print('Connected to DB — inserting reporting sample data')

        insert_employees(cursor, data['employees'])
        insert_leaves(cursor, data['leaves'])
        insert_attendance(cursor, data['timesheets'])
        insert_candidates(cursor, data['candidates'])

        conn.commit()
        cursor.close()
        conn.close()
        print('Inserted reporting sample data into DB')
    except Exception as e:
        print('DB unavailable or error while inserting reporting data:', e)
        sys.exit(1)


if __name__ == '__main__':
    print('='*50)
    print('GENERATE REPORTING & ANALYTICS DATA (DB only)')
    print('='*50)
    run_reports(50)
