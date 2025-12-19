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

# --- CẤU HÌNH RECRUITMENT ---

# Trạng thái ứng viên (Candidate Status)
CANDIDATE_STATUS = {
    1: 'APPLICATION INITIATED',  # Đơn mới nộp
    2: 'SHORTLISTED',           # Đã sơ tuyển
    3: 'REJECTED',              # Bị từ chối
    4: 'INTERVIEW SCHEDULED',   # Đã hẹn phỏng vấn
    5: 'INTERVIEW PASSED',      # Pass phỏng vấn
    6: 'INTERVIEW FAILED',      # Fail phỏng vấn
    7: 'JOB OFFERED',           # Đã offer
    8: 'OFFER DECLINED',        # Từ chối offer
    9: 'HIRED'                  # Đã tuyển
}

# Phân bổ trạng thái (tổng = 100%)
STATUS_DISTRIBUTION = {
    1: 30,  # 30% đơn mới
    2: 20,  # 20% sơ tuyển
    3: 20,  # 20% từ chối
    4: 15,  # 15% hẹn PV
    5: 8,   # 8% pass PV
    6: 4,   # 4% fail PV
    7: 2,   # 2% đã offer
    8: 0,   # 0% từ chối offer (rare)
    9: 1    # 1% đã tuyển
}

# Tên vị trí tuyển dụng (Job Vacancy Names)
JOB_VACANCY_NAMES = [
    'Senior Software Engineer - Ho Chi Minh City',
    'Frontend Developer (ReactJS) - Hanoi',
    'Backend Developer (Node.js/Python)',
    'Full Stack Developer - Remote',
    'DevOps Engineer',
    'QA/Test Engineer - Automation',
    'Business Analyst',
    'Product Manager',
    'Project Manager (IT)',
    'Scrum Master',
    'Marketing Manager',
    'Digital Marketing Specialist',
    'Content Creator',
    'Graphic Designer',
    'UI/UX Designer',
    'HR Manager',
    'HR Specialist - Talent Acquisition',
    'Accountant',
    'Financial Analyst',
    'Sales Executive - B2B',
    'Customer Service Representative',
    'Data Analyst',
    'Data Engineer',
    'Mobile Developer (Flutter/React Native)',
    'System Administrator'
]

# Mô tả công việc (Job Descriptions)
JOB_DESCRIPTIONS = {
    'Software Engineer': 'Develop and maintain web/mobile applications. Work with modern technologies like React, Node.js, MongoDB. Opportunities to learn and grow in a dynamic environment.',
    'Marketing': 'Plan and execute marketing campaigns. Manage social media and content marketing. Analyze effectiveness and optimize ROI.',
    'HR': 'Recruit high-quality personnel. Manage onboarding and training processes. Build positive corporate culture.',
    'Accountant': 'Manage accounting books. Prepare periodic financial reports. Ensure compliance with tax laws.',
    'Sales': 'Develop new customers. Maintain relationships with existing customers. Achieve and exceed sales targets.',
    'Designer': 'Design beautiful and user-friendly interfaces. Work with team to realize product ideas.'
}

# Tên vòng phỏng vấn (Interview Round Names)
INTERVIEW_ROUNDS = [
    'Phone Screening',
    'Technical Interview Round 1',
    'Technical Interview Round 2',
    'System Design Interview',
    'Coding Test',
    'HR Interview',
    'Manager Interview',
    'Team Culture Fit Interview',
    'Final Interview with Director'
]

# Bình luận tích cực về ứng viên
POSITIVE_COMMENTS = [
    'Strong technical skills with React and Node.js',
    'Excellent problem-solving skills',
    'Great cultural fit for the company',
    'Clear and professional communication',
    'Impressive portfolio with practical projects',
    'Enthusiastic and eager to learn',
    'Relevant work experience matches requirements',
    'Strong teamwork abilities',
    'Positive and proactive attitude',
    'Good presentation skills'
]

# Lý do từ chối ứng viên
REJECTION_REASONS = [
    'Lacks experience with required technologies',
    'Communication skills need improvement',
    'Salary expectations exceed budget',
    'Not available to start immediately',
    'Position has already been filled',
    'Candidate withdrew application',
    'Does not meet technical requirements',
    'Lacks necessary certifications',
    'English proficiency below required standard',
    'Does not fit company culture'
]

# Ghi chú phỏng vấn
INTERVIEW_NOTES = [
    'Focus on evaluating React and Node.js skills',
    'Test problem-solving abilities',
    'Assess company culture fit',
    'Interview via video call - Google Meet',
    'In-person interview at office',
    'Complete 60-minute coding test',
    'Discuss project experience',
    'Evaluate teamwork skills'
]

# Danh sách tên đệm tiếng Việt (mở rộng)
VIETNAMESE_MALE_MIDDLE_NAMES = [
    "Văn", "Hữu", "Đức", "Công", "Quang", "Minh", 
    "Xuân", "Duy", "Tuấn", "Hoàng", "Anh", "Bảo",
    "Thành", "Thanh", "Trung", "Ngọc", "Đình", "Việt"
]

VIETNAMESE_FEMALE_MIDDLE_NAMES = [
    "Thị", "Ngọc", "Thu", "Mai", "Phương", "Diệu",
    "Thùy", "Thanh", "Kim", "Hồng", "Lan", "Linh",
    "Như", "Bích", "Hương", "Ánh", "Uyển", "Khánh"
]

def connect_db():
    """Kết nối đến database"""
    return mysql.connector.connect(**DB_CONFIG)

def get_random_status_with_distribution():
    """Lấy trạng thái ngẫu nhiên theo tỉ lệ phân bổ"""
    statuses = list(STATUS_DISTRIBUTION.keys())
    weights = list(STATUS_DISTRIBUTION.values())
    return random.choices(statuses, weights=weights)[0]

def generate_recruitment_data():
    """Hàm chính để sinh dữ liệu recruitment"""
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor(buffered=True)
        
        print("=" * 70)
        print("ORANGEHRM - RECRUITMENT DATA GENERATOR")
        print("=" * 70)
        print("-> Kết nối Database thành công!")
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        # ===== BƯỚC 1: LẤY DỮ LIỆU PHỤ THUỘC =====
        print("\n[BƯỚC 1] Đang lấy dữ liệu phụ thuộc...")
        
        # Lấy danh sách Job Titles
        cursor.execute("SELECT id, job_title FROM ohrm_job_title")
        job_titles = cursor.fetchall()
        if not job_titles:
            print("CẢNH BÁO: Chưa có Job Titles! Hãy chạy generate_dim.py trước.")
            return
        print(f"   Tìm thấy {len(job_titles)} Job Titles")
        
        # Lấy danh sách Employees (để làm Hiring Manager và Interviewer)
        cursor.execute("""
            SELECT emp_number, CONCAT(emp_firstname, ' ', emp_lastname) as name, job_title_code
            FROM hs_hr_employee
        """)
        employees = cursor.fetchall()
        if not employees:
            print("CẢNH BÁO: Chưa có Employees!")
            return
        print(f"   Tìm thấy {len(employees)} Employees")
        
        # Lấy danh sách Managers (để làm Hiring Manager)
        cursor.execute("""
            SELECT DISTINCT e.emp_number
            FROM hs_hr_employee e
            JOIN ohrm_job_title j ON e.job_title_code = j.id
            WHERE j.job_title LIKE '%Manager%' OR j.job_title LIKE '%Director%'
        """)
        managers = [row[0] for row in cursor.fetchall()]
        if not managers:
            managers = [emp[0] for emp in employees[:5]]  # Fallback: lấy 5 người đầu
        print(f"   Tìm thấy {len(managers)} Managers")
        
        # ===== BƯỚC 2: TẠO JOB VACANCIES =====
        print("\n[BƯỚC 2] Đang tạo Job Vacancies...")
        
        vacancies = []
        num_vacancies = min(10, len(JOB_VACANCY_NAMES))
        
        for i in range(num_vacancies):
            vacancy_name = JOB_VACANCY_NAMES[i]
            
            # Xác định loại công việc để lấy description phù hợp
            if 'Software' in vacancy_name or 'Developer' in vacancy_name or 'Engineer' in vacancy_name:
                description = JOB_DESCRIPTIONS['Software Engineer']
            elif 'Marketing' in vacancy_name:
                description = JOB_DESCRIPTIONS['Marketing']
            elif 'HR' in vacancy_name:
                description = JOB_DESCRIPTIONS['HR']
            elif 'Account' in vacancy_name or 'Financial' in vacancy_name:
                description = JOB_DESCRIPTIONS['Accountant']
            elif 'Sales' in vacancy_name:
                description = JOB_DESCRIPTIONS['Sales']
            elif 'Designer' in vacancy_name:
                description = JOB_DESCRIPTIONS['Designer']
            else:
                description = "Mô tả công việc chi tiết. Yêu cầu ứng viên có kinh nghiệm và kỹ năng phù hợp. Môi trường làm việc chuyên nghiệp và năng động."
            
            # 70% Active, 30% Closed
            status = 1 if random.random() < 0.7 else 2
            
            # Chọn random job title và hiring manager
            job_title_id = random.choice(job_titles)[0]
            hiring_manager = random.choice(managers)
            
            # Số lượng cần tuyển: 1-5
            no_of_positions = random.randint(1, 5)
            
            # Thời gian tạo: từ 6 tháng trước đến nay
            days_ago = random.randint(0, 180)
            defined_time = datetime.now() - timedelta(days=days_ago)
            
            # Published in feed: 80% có publish
            published_in_feed = 1 if random.random() < 0.8 else 0
            
            # Thêm vacancy vào database
            cursor.execute("""
                INSERT INTO ohrm_job_vacancy 
                (job_title_code, hiring_manager_id, name, description, no_of_positions, 
                 status, published_in_feed, defined_time, updated_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                job_title_id,
                hiring_manager,
                vacancy_name,
                description,
                no_of_positions,
                status,
                published_in_feed,
                defined_time,
                defined_time
            ))
            
            vacancy_id = cursor.lastrowid
            vacancies.append({
                'id': vacancy_id,
                'name': vacancy_name,
                'status': status,
                'no_of_positions': no_of_positions,
                'defined_time': defined_time,
                'job_title_id': job_title_id,
                'hiring_manager': hiring_manager
            })
        
        vacancy_count = len(vacancies)
        print(f"   Đã tạo {vacancy_count} Job Vacancies")
        
        # ===== BƯỚC 3: TẠO CANDIDATES =====
        print("\n[BƯỚC 3] Đang tạo Candidates...")
        
        candidates = []
        num_candidates = 60
        used_emails = set()  # Để đảm bảo email unique
        
        for _ in range(num_candidates):
            # Tạo tên tiếng Việt 100%
            gender = random.choice([1, 2])  # 1=nam, 2=nữ
            last_name = fake.last_name()
            
            if gender == 1:  # Nam
                first_name = fake.first_name_male()
                middle_name = random.choice(VIETNAMESE_MALE_MIDDLE_NAMES)
            else:  # Nữ
                first_name = fake.first_name_female()
                middle_name = random.choice(VIETNAMESE_FEMALE_MIDDLE_NAMES)
            
            # Tạo email unique (giống generate_dim.py - dùng fake.user_name())
            username = fake.user_name()
            # Thêm số ngẫu nhiên để tránh trùng lặp
            username = f"{username}{random.randint(10,99)}"
            email_domain = random.choice(['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com'])
            email = f"{username}@{email_domain}"
            
            # Nếu email trùng, thêm số
            counter = 1
            while email in used_emails:
                email = f"{username}{counter}@{email_domain}"
                counter += 1
            used_emails.add(email)
            
            # Số điện thoại Việt Nam
            phone_prefix = random.choice(['03', '07', '08', '09'])
            phone = f"0{phone_prefix[1]}{random.randint(1,9)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
            
            # Trạng thái theo distribution
            status = get_random_status_with_distribution()
            
            # Ngày nộp đơn: từ 6 tháng trước đến nay
            days_ago = random.randint(0, 180)
            date_of_application = datetime.now() - timedelta(days=days_ago)
            
            # Mode: 80% Online, 20% Manual
            mode_of_application = 1 if random.random() < 0.2 else 2  # 1=Manual, 2=Online
            
            # Comment cho rejected hoặc các trường hợp đặc biệt
            comment = None
            if status == 3:  # REJECTED
                comment = random.choice(REJECTION_REASONS)
            elif status >= 5:  # INTERVIEW PASSED trở lên
                comment = random.choice(POSITIVE_COMMENTS)
            
            # Keywords cho tìm kiếm
            keywords = f"{first_name} {last_name} {email}"
            
            # Người thêm: chọn ngẫu nhiên từ nhân viên HR
            added_person = random.choice([emp[0] for emp in employees[:10]])
            
            # Thêm ứng viên vào database
            cursor.execute("""
                INSERT INTO ohrm_job_candidate
                (first_name, middle_name, last_name, email, contact_number, status,
                 comment, mode_of_application, date_of_application, keywords, 
                 added_person, consent_to_keep_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
            """, (
                first_name,
                middle_name,
                last_name,
                email,
                phone,
                status,
                comment,
                mode_of_application,
                date_of_application.date(),
                keywords,
                added_person
            ))
            
            candidate_id = cursor.lastrowid
            candidates.append({
                'id': candidate_id,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'status': status,
                'date_of_application': date_of_application,
                'comment': comment
            })
        
        candidate_count = len(candidates)
        print(f"   Đã tạo {candidate_count} Candidates")
        
        # ===== BƯỚC 4: LIÊN KẾT ỨNG VIÊN VỚI VỊ TRÍ TUYỂN DỤNG =====
        print("\n[BƯỚC 4] Đang link Candidates to Vacancies...")
        
        applications = []
        application_count = 0
        
        # Mỗi candidate apply 1-2 vacancies
        for candidate in candidates:
            num_applications = random.randint(1, 2)
            selected_vacancies = random.sample(vacancies, min(num_applications, len(vacancies)))
            
            for vacancy in selected_vacancies:
                # Status text theo candidate status
                status_text = CANDIDATE_STATUS[candidate['status']]
                
                # Ngày nộp đơn
                applied_date = candidate['date_of_application'].date()
                
                cursor.execute("""
                    INSERT INTO ohrm_job_candidate_vacancy
                    (candidate_id, vacancy_id, status, applied_date)
                    VALUES (%s, %s, %s, %s)
                """, (
                    candidate['id'],
                    vacancy['id'],
                    status_text,
                    applied_date
                ))
                
                application_id = cursor.lastrowid
                applications.append({
                    'id': application_id,
                    'candidate_id': candidate['id'],
                    'vacancy_id': vacancy['id'],
                    'candidate': candidate,
                    'vacancy': vacancy,
                    'status_text': status_text,
                    'applied_date': applied_date
                })
                application_count += 1
        
        print(f"   Đã tạo {application_count} Applications")
        
        # ===== BƯỚC 5: TẠO TỆP ĐÍNH KÈM CỦA ỨNG VIÊN =====
        print("\n[BƯỚC 5] Đang tạo Candidate Attachments (CV)...")
        
        attachment_count = 0
        
        for candidate in candidates:
            # Tạo attachment 
            file_name = f"CV_{candidate['last_name']}_{candidate['first_name']}_2025.pdf"
            file_type = "application/pdf"
            file_size = random.randint(100, 500)  # KB
            
            cursor.execute("""
                INSERT INTO ohrm_job_candidate_attachment
                (candidate_id, file_name, file_type, file_size, attachment_type)
                VALUES (%s, %s, %s, %s, 1)
            """, (
                candidate['id'],
                file_name,
                file_type,
                file_size
            ))
            attachment_count += 1
        
        print(f"   Đã tạo {attachment_count} Attachments")
        
        # ===== BƯỚC 6: TẠO LỊCH PHỎNG VẤN =====
        print("\n[BƯỚC 6] Đang tạo Interviews...")
        
        interviews = []
        interview_count = 0
        
        # Chỉ tạo interview cho candidates có status >= 4 (INTERVIEW SCHEDULED)
        for application in applications:
            candidate = application['candidate']
            
            if candidate['status'] >= 4:  # INTERVIEW SCHEDULED trở lên
                # Số vòng phỏng vấn: 1-3 vòng
                num_rounds = random.randint(1, 3)
                
                for round_num in range(num_rounds):
                    # Chọn tên vòng phỏng vấn
                    if num_rounds == 1:
                        interview_name = random.choice(INTERVIEW_ROUNDS[:6])  # Một vòng duy nhất
                    else:
                        # Nhiều vòng: Kỹ thuật → Quản lý → Nhân sự
                        if round_num == 0:
                            interview_name = random.choice(['Phone Screening', 'Technical Interview Round 1'])
                        elif round_num == 1:
                            interview_name = random.choice(['Technical Interview Round 2', 'Manager Interview'])
                        else:
                            interview_name = random.choice(['HR Interview', 'Final Interview with Director'])
                    
                    # Ngày phỏng vấn: sau ngày nộp đơn 7-30 ngày
                    days_after_apply = random.randint(7, 30) + (round_num * 7)  # Mỗi round cách nhau ~1 tuần
                    interview_date = application['applied_date'] + timedelta(days=days_after_apply)
                    
                    # Thời gian phỏng vấn: trong giờ hành chính
                    interview_time = random.choice(['08:00:00', '09:00:00', '10:00:00', '14:00:00', '15:00:00', '16:00:00'])
                    
                    # Ghi chú
                    note = random.choice(INTERVIEW_NOTES)
                    
                    cursor.execute("""
                        INSERT INTO ohrm_job_interview
                        (candidate_vacancy_id, candidate_id, interview_name, interview_date, interview_time, note)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        application['id'],
                        candidate['id'],
                        interview_name,
                        interview_date,
                        interview_time,
                        note
                    ))
                    
                    interview_id = cursor.lastrowid
                    interviews.append({
                        'id': interview_id,
                        'candidate_id': candidate['id'],
                        'candidate_vacancy_id': application['id'],
                        'interview_name': interview_name,
                        'interview_date': interview_date,
                        'vacancy': application['vacancy']
                    })
                    interview_count += 1
        
        print(f"   Đã tạo {interview_count} Interviews")
        
        # ===== BƯỚC 7: PHÂN CÔNG NGƯỜI PHỎNG VẤN =====
        print("\n[BƯỚC 7] Đang assign Interviewers...")
        
        interviewer_count = 0
        
        # Lấy danh sách potential interviewers (Managers, Leads, HR)
        cursor.execute("""
            SELECT e.emp_number
            FROM hs_hr_employee e
            JOIN ohrm_job_title j ON e.job_title_code = j.id
            WHERE j.job_title LIKE '%Manager%' 
               OR j.job_title LIKE '%Lead%' 
               OR j.job_title LIKE '%Director%'
               OR j.job_title LIKE '%HR%'
        """)
        interviewers_pool = [row[0] for row in cursor.fetchall()]
        
        if not interviewers_pool:
            interviewers_pool = [emp[0] for emp in employees[:20]]
        
        for interview in interviews:
            # Mỗi interview có 2-3 interviewers
            num_interviewers = random.randint(2, 3)
            selected_interviewers = random.sample(interviewers_pool, min(num_interviewers, len(interviewers_pool)))
            
            for interviewer_emp_num in selected_interviewers:
                cursor.execute("""
                    INSERT INTO ohrm_job_interview_interviewer
                    (interview_id, interviewer_id)
                    VALUES (%s, %s)
                """, (
                    interview['id'],
                    interviewer_emp_num
                ))
                interviewer_count += 1
        
        print(f"   Đã assign {interviewer_count} Interviewers")
        
        # ===== BƯỚC 8: TẠO LỊCH SỬ ỨNG VIÊN =====
        print("\n[BƯỚC 8] Đang tạo Candidate History (Audit Trail)...")
        
        history_count = 0
        
        for application in applications:
            candidate = application['candidate']
            vacancy = application['vacancy']
            status = candidate['status']
            applied_date = application['applied_date']
            
            # Hành động 1: NỘP ĐƠN (tất cả ứng viên đều có)
            cursor.execute("""
                INSERT INTO ohrm_job_candidate_history
                (candidate_id, vacancy_id, candidate_vacancy_name, action, 
                 performed_by, performed_date, note)
                VALUES (%s, %s, %s, 1, %s, %s, %s)
            """, (
                candidate['id'],
                vacancy['id'],
                vacancy['name'],
                vacancy['hiring_manager'],
                applied_date,
                f"Ứng viên nộp đơn cho vị trí {vacancy['name']}"
            ))
            history_count += 1
            
            # Hành động 2: SƠ TUYỂN (nếu status >= 2)
            if status >= 2:
                shortlist_date = applied_date + timedelta(days=random.randint(3, 7))
                cursor.execute("""
                    INSERT INTO ohrm_job_candidate_history
                    (candidate_id, vacancy_id, candidate_vacancy_name, action,
                     performed_by, performed_date, note)
                    VALUES (%s, %s, %s, 2, %s, %s, %s)
                """, (
                    candidate['id'],
                    vacancy['id'],
                    vacancy['name'],
                    vacancy['hiring_manager'],
                    shortlist_date,
                    "Ứng viên được chọn vào vòng trong"
                ))
                history_count += 1
            
            # Hành động 3: TỪ CHỐI (nếu status == 3)
            if status == 3:
                reject_date = applied_date + timedelta(days=random.randint(5, 15))
                cursor.execute("""
                    INSERT INTO ohrm_job_candidate_history
                    (candidate_id, vacancy_id, candidate_vacancy_name, action,
                     performed_by, performed_date, note)
                    VALUES (%s, %s, %s, 3, %s, %s, %s)
                """, (
                    candidate['id'],
                    vacancy['id'],
                    vacancy['name'],
                    vacancy['hiring_manager'],
                    reject_date,
                    candidate['comment'] or random.choice(REJECTION_REASONS)
                ))
                history_count += 1
            
            # Hành động 4: HẸN LỊCH PHỎNG VẤN (nếu status >= 4)
            if status >= 4:
                schedule_date = applied_date + timedelta(days=random.randint(7, 14))
                cursor.execute("""
                    INSERT INTO ohrm_job_candidate_history
                    (candidate_id, vacancy_id, candidate_vacancy_name, action,
                     performed_by, performed_date, note)
                    VALUES (%s, %s, %s, 4, %s, %s, %s)
                """, (
                    candidate['id'],
                    vacancy['id'],
                    vacancy['name'],
                    vacancy['hiring_manager'],
                    schedule_date,
                    "Đã hẹn lịch phỏng vấn"
                ))
                history_count += 1
            
            # Hành động 5: ĐẠT PHỎNG VẤN (nếu status == 5)
            if status == 5:
                pass_date = applied_date + timedelta(days=random.randint(15, 25))
                cursor.execute("""
                    INSERT INTO ohrm_job_candidate_history
                    (candidate_id, vacancy_id, candidate_vacancy_name, action,
                     performed_by, performed_date, note)
                    VALUES (%s, %s, %s, 5, %s, %s, %s)
                """, (
                    candidate['id'],
                    vacancy['id'],
                    vacancy['name'],
                    vacancy['hiring_manager'],
                    pass_date,
                    candidate['comment'] or random.choice(POSITIVE_COMMENTS)
                ))
                history_count += 1
            
            # Hành động 6: TRƯỢT PHỎNG VẤN (nếu status == 6)
            if status == 6:
                fail_date = applied_date + timedelta(days=random.randint(15, 25))
                cursor.execute("""
                    INSERT INTO ohrm_job_candidate_history
                    (candidate_id, vacancy_id, candidate_vacancy_name, action,
                     performed_by, performed_date, note)
                    VALUES (%s, %s, %s, 6, %s, %s, %s)
                """, (
                    candidate['id'],
                    vacancy['id'],
                    vacancy['name'],
                    vacancy['hiring_manager'],
                    fail_date,
                    "Không đạt yêu cầu kỹ thuật"
                ))
                history_count += 1
            
            # Hành động 7: GỬI THÔNG BÁO TUYỂN DỤNG (nếu status >= 7)
            if status >= 7:
                offer_date = applied_date + timedelta(days=random.randint(20, 35))
                cursor.execute("""
                    INSERT INTO ohrm_job_candidate_history
                    (candidate_id, vacancy_id, candidate_vacancy_name, action,
                     performed_by, performed_date, note)
                    VALUES (%s, %s, %s, 7, %s, %s, %s)
                """, (
                    candidate['id'],
                    vacancy['id'],
                    vacancy['name'],
                    vacancy['hiring_manager'],
                    offer_date,
                    "Đã gửi thư mời làm việc"
                ))
                history_count += 1
            
            # Hành động 9: TUYỂN DỤNG (nếu status == 9)
            if status == 9:
                hire_date = applied_date + timedelta(days=random.randint(30, 45))
                cursor.execute("""
                    INSERT INTO ohrm_job_candidate_history
                    (candidate_id, vacancy_id, candidate_vacancy_name, action,
                     performed_by, performed_date, note)
                    VALUES (%s, %s, %s, 9, %s, %s, %s)
                """, (
                    candidate['id'],
                    vacancy['id'],
                    vacancy['name'],
                    vacancy['hiring_manager'],
                    hire_date,
                    "Ứng viên đã nhận việc và bắt đầu làm việc"
                ))
                history_count += 1
        
        print(f"   Đã tạo {history_count} History Records")
        
        # ===== LƯU DỮ LIỆU VÀ TỔNG KẾT =====
        conn.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        print("\n" + "=" * 50)
        print("HOÀN THÀNH TẠO DỮ LIỆU RECRUITMENT")
        print("=" * 50)
        print(f"THỐNG KÊ:")
        print(f"   • Job Vacancies: {vacancy_count}")
        print(f"   • Candidates: {candidate_count}")
        print(f"   • Applications: {application_count}")
        print(f"   • Attachments: {attachment_count}")
        print(f"   • Interviews: {interview_count}")
        print(f"   • Interviewers: {interviewer_count}")
        print(f"   • History Records: {history_count}")
        print("=" * 50)
        
        # Thống kê phân bổ status
        print("\nPHÂN BỔ TRẠNG THÁI ỨNG VIÊN:")
        cursor.execute("""
            SELECT status, COUNT(*) as count,
                   ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ohrm_job_candidate), 1) as percentage
            FROM ohrm_job_candidate
            GROUP BY status
            ORDER BY status
        """)
        
        print("\n" + "-" * 50)
        print(f"{'Status':<5} {'Tên trạng thái':<25} {'Số lượng':>12} {'Tỷ lệ':>10}")
        print("-" * 50)
        for row in cursor.fetchall():
            status_id = row[0]
            status_name = CANDIDATE_STATUS.get(status_id, 'UNKNOWN')
            count = row[1]
            percentage = row[2]
            print(f"{status_id:<5} {status_name:<25} {count:>12} {percentage:>9}%")
        print("-" * 50)
        
        # In mẫu dữ liệu
        print("\nMẪU DỮ LIỆU:")
        cursor.execute("""
            SELECT c.first_name, c.last_name, c.email, v.name as vacancy, 
                   cv.status as application_status
            FROM ohrm_job_candidate c
            JOIN ohrm_job_candidate_vacancy cv ON c.id = cv.candidate_id
            JOIN ohrm_job_vacancy v ON cv.vacancy_id = v.id
            LIMIT 10
        """)
        
        print("\n" + "-" * 120)
        print(f"{'Tên':<25} {'Email':<35} {'Vị trí':<35} {'Trạng thái':<25}")
        print("-" * 120)
        for row in cursor.fetchall():
            full_name = f"{row[0]} {row[1]}"
            print(f"{full_name:<25} {row[2]:<35} {row[3]:<35} {row[4]:<25}")
        print("-" * 120)
        
    except mysql.connector.Error as err:
        print(f"\nLỖI MySQL: {err}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"\nLỖI: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("\n-> Đã đóng kết nối Database")

if __name__ == "__main__":
    print("=" * 50)
    print("GENERATE RECRUITMENT DATA")
    print("=" * 50)
    generate_recruitment_data()
