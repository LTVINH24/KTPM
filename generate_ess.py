import os
import mysql.connector
from dotenv import load_dotenv
import sys
from datetime import datetime, timedelta
from faker import Faker
import random

load_dotenv()

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


def try_insert_leave(cursor, lr):
    # Best-effort insert into common leave table shape
    try:
        cursor.execute(
            "INSERT INTO ohrm_leave_request (emp_number, date_from, date_to, comments, status) VALUES (%s,%s,%s,%s,%s)",
            (lr['emp_number'], lr['date_from'], lr['date_to'], lr['comments'], lr['status'])
        )
        return True
    except Exception:
        return False


def run_ess(n_employees=50):
    employees = generate_employees(n_employees)
    leaves = generate_leave_requests(employees, pct=0.3)
    timesheets = generate_timesheets(employees, weeks=2)

    try:
        conn = connect_db()
        cursor = conn.cursor()
        print('Connected to DB — inserting ESS data')

        # Insert basic employee profiles
        for emp in employees:
            try:
                cursor.execute(
                    "INSERT IGNORE INTO hs_hr_employee (emp_number, employee_id, emp_lastname, emp_firstname, emp_middle_name, emp_work_email, joined_date) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (emp['emp_number'], emp['employee_id'], emp['last_name'], emp['first_name'], emp['middle_name'], emp['work_email'], emp['joined_date'])
                )
            except Exception:
                pass

        # Leave requests
        inserted = 0
        for lr in leaves:
            if try_insert_leave(cursor, lr):
                inserted += 1

        # Attendance/timesheet: try common table
        att_inserted = 0
        for ts in timesheets:
            try:
                cursor.execute(
                    "INSERT IGNORE INTO ohrm_attendance_record (employee_id, punch_in_user_time, punch_out_user_time, state) VALUES (%s,%s,%s,%s)",
                    (ts['emp_number'], ts['date'] + ' 09:00:00', ts['date'] + ' 17:00:00', 'PUNCHED OUT')
                )
                att_inserted += 1
            except Exception:
                pass

        conn.commit()
        cursor.close()
        conn.close()
        print(f'Inserted/updated employees: {len(employees)}, leaves: {inserted}, attendance records: {att_inserted}')

    except Exception as e:
        print('DB unavailable or insertion failed:', e)
        print('No file exports will be performed; exiting with failure.')
        sys.exit(1)


if __name__ == '__main__':
    print('='*50)
    print('GENERATE EMPLOYEE SELF-SERVICE (ESS) DATA')
    print('='*50)
    run_ess(50)
