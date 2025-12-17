import mysql.connector
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

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def generate_performance_data():
    """
    Tạo dữ liệu cho module Performance Management:
    - Performance Trackers (KPIs)
    - Performance Reviews
    """
    conn = None
    try:
        conn = connect_db()
        cursor = conn.cursor()
        print("-> Kết nối Database thành công!")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        # BƯỚC 1: LẤY DANH SÁCH NHÂN VIÊN
        print("-> Đang lấy danh sách nhân viên...")
        cursor.execute("""
            SELECT e.emp_number, j.job_title, u.id as user_id
            FROM hs_hr_employee e 
            LEFT JOIN ohrm_job_title j ON e.job_title_code = j.id
            LEFT JOIN ohrm_user u ON e.emp_number = u.emp_number
            WHERE u.id IS NOT NULL
        """)
        employees = cursor.fetchall()

        if not employees:
            print("[LỖI] Chưa có dữ liệu nhân viên. Hãy chạy generate_dim.py trước.")
            return

        print(f"   Tìm thấy {len(employees)} nhân viên")

        # Lấy Director và Manager làm reviewer
        directors = [e for e in employees if e[1] == 'Director']
        managers = [e for e in employees if e[1] == 'Manager']
        staff = [e for e in employees if e[1] == 'Staff']

        # BƯỚC 2: TẠO PERFORMANCE TRACKERS (KPIs)
        print("-> Đang tạo Performance Trackers...")
        
        # Xóa dữ liệu cũ
        cursor.execute("DELETE FROM ohrm_performance_tracker_log")
        cursor.execute("DELETE FROM ohrm_performance_track")
        cursor.execute("DELETE FROM ohrm_reviewer")
        cursor.execute("DELETE FROM ohrm_performance_review")
        
        tracker_templates = [
            {
                'name': 'Sales Performance Q4 2024',
                'kpis': ['Monthly Revenue Target', 'Customer Acquisition', 'Client Retention Rate']
            },
            {
                'name': 'Project Delivery Metrics',
                'kpis': ['On-time Delivery', 'Code Quality Score', 'Bug Fix Rate']
            },
            {
                'name': 'Customer Service Excellence',
                'kpis': ['Customer Satisfaction Score', 'Response Time', 'Issue Resolution Rate']
            }
        ]

        tracker_ids = []
        
        for template in tracker_templates:
            for emp_number, job_title, user_id in staff[:15]:  # 15 staff đầu tiên
                # Chọn reviewer (Manager hoặc Director)
                if managers:
                    reviewer = random.choice(managers)
                    reviewer_emp = reviewer[0]
                else:
                    reviewer_emp = directors[0][0] if directors else emp_number

                # Insert tracker
                cursor.execute("""
                    INSERT INTO ohrm_performance_track 
                    (tracker_name, emp_number, added_date, modified_date, status)
                    VALUES (%s, %s, %s, %s, 1)
                """, (
                    template['name'],
                    emp_number,
                    datetime.now() - timedelta(days=random.randint(30, 90)),
                    datetime.now()
                ))
                tracker_id = cursor.lastrowid
                tracker_ids.append(tracker_id)

                # Thêm reviewer cho tracker
                cursor.execute("""
                    INSERT INTO ohrm_reviewer (review_id, employee_number, status, reviewer_group_id)
                    VALUES (%s, %s, 1, 1)
                """, (tracker_id, reviewer_emp))

                # Thêm logs cho tracker
                for kpi in template['kpis']:
                    log_date = datetime.now() - timedelta(days=random.randint(1, 30))
                    achievement = random.randint(60, 100)
                    
                    comments = [
                        f"Achieved {achievement}% of target for {kpi}",
                        f"Good progress on {kpi}, need improvement in next quarter",
                        f"Exceeded expectations on {kpi}",
                        f"Met all requirements for {kpi}"
                    ]
                    
                    cursor.execute("""
                        INSERT INTO ohrm_performance_tracker_log 
                        (performance_track_id, log, comment, added_date, modified_date, 
                         achievement, user_id, reviewer_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        tracker_id,
                        kpi,
                        random.choice(comments),
                        log_date,
                        log_date,
                        str(achievement),
                        user_id,
                        reviewer_emp
                    ))

        print(f"   Đã tạo {len(tracker_ids)} Performance Trackers")

        # BƯỚC 3: TẠO KPIs
        print("-> Đang tạo KPIs...")
        
        cursor.execute("SELECT id FROM ohrm_job_title")
        job_title_ids = [j[0] for j in cursor.fetchall()]
        
        kpis = [
            ('Sales Target Achievement', 1, 100, 'Percentage of sales target achieved'),
            ('Customer Satisfaction Score', 1, 5, 'Average customer rating'),
            ('Project Delivery On-Time', 1, 100, 'Percentage of projects delivered on schedule'),
            ('Code Quality Index', 1, 100, 'Code review and testing score'),
            ('Bug Resolution Rate', 1, 100, 'Percentage of bugs fixed within SLA'),
            ('Team Collaboration Score', 1, 5, 'Peer review rating'),
            ('Learning & Development', 1, 100, 'Training completion rate'),
            ('Client Retention Rate', 1, 100, 'Percentage of clients retained'),
            ('Innovation Contribution', 1, 5, 'New ideas and improvements'),
            ('Attendance Rate', 1, 100, 'Work attendance percentage'),
        ]
        
        kpi_ids = []
        for kpi_title, min_rating, max_rating, desc in kpis:
            job_title_id = random.choice(job_title_ids) if job_title_ids else None
            try:
                cursor.execute("""
                    INSERT INTO ohrm_kpi (job_title_code, kpi_indicators, min_rating, max_rating, deleted_at, default_kpi)
                    VALUES (%s, %s, %s, %s, NULL, 0)
                """, (job_title_id, kpi_title, min_rating, max_rating))
                kpi_ids.append(cursor.lastrowid)
            except Exception as e:
                print(f"   Lỗi tạo KPI {kpi_title}: {e}")
        
        print(f"   Đã tạo {len(kpi_ids)} KPIs")

        # BƯỚC 4: TẠO PERFORMANCE REVIEWS
        print("-> Đang tạo Performance Reviews...")
        
        # Lấy job_title_code cho Staff
        cursor.execute("SELECT id FROM ohrm_job_title WHERE job_title = 'Staff' LIMIT 1")
        staff_job_result = cursor.fetchone()
        staff_job_code = staff_job_result[0] if staff_job_result else job_title_ids[0] if job_title_ids else None
        
        review_statuses = [1, 2, 3, 4]  # 1=Activated, 2=In Progress, 3=Completed, 4=Approved
        review_count = 0
        review_ids = []

        for emp_number, job_title, user_id in staff[:20]:  # 20 staff
            # Xác định reviewer
            if managers:
                reviewer = random.choice(managers)
            else:
                reviewer = directors[0] if directors else None

            if not reviewer:
                continue

            review_date = datetime.now() - timedelta(days=random.randint(1, 60))
            due_date = review_date + timedelta(days=30)
            status = random.choice(review_statuses)

            # Tạo review
            cursor.execute("""
                INSERT INTO ohrm_performance_review 
                (status_id, employee_number, work_period_start, 
                 work_period_end, job_title_code, department_id, due_date, 
                 completed_date, activated_date, final_comment, final_rate)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                status,
                emp_number,
                review_date - timedelta(days=90),  # work_period_start
                review_date,  # work_period_end
                staff_job_code,  # job_title_code (lấy từ database)
                None,
                due_date,
                review_date if status >= 3 else None,  # completed_date
                review_date - timedelta(days=5),  # activated_date
                f"Performance review for period ending {review_date.strftime('%Y-%m-%d')}" if status >= 3 else None,
                random.choice([3.0, 3.5, 4.0, 4.5, 5.0]) if status >= 3 else None
            ))
            review_id = cursor.lastrowid
            review_ids.append((review_id, status, reviewer[0]))
            review_count += 1
            
            # Thêm reviewer cho review (BẮT BUỘC để hiển thị trên UI)
            cursor.execute("""
                INSERT INTO ohrm_reviewer 
                (review_id, employee_number, status, reviewer_group_id)
                VALUES (%s, %s, %s, %s)
            """, (review_id, reviewer[0], 1 if status < 3 else 2, 1))

        print(f"   Đã tạo {review_count} Performance Reviews")

        # BƯỚC 5: TẠO REVIEWER RATINGS
        print("-> Đang tạo Reviewer Ratings...")
        
        rating_count = 0
        for review_id, status, reviewer_emp in review_ids:
            if status >= 3 and kpi_ids:  # Chỉ tạo rating cho reviews đã completed
                # Chọn 3-5 KPIs ngẫu nhiên để đánh giá
                selected_kpis = random.sample(kpi_ids, min(random.randint(3, 5), len(kpi_ids)))
                for kpi_id in selected_kpis:
                    rating = round(random.uniform(3.0, 5.0), 1)
                    comment = random.choice([
                        "Excellent performance, exceeded expectations",
                        "Good work, met all targets",
                        "Satisfactory performance, room for improvement",
                        "Strong contribution to team goals",
                        "Demonstrated leadership qualities"
                    ])
                    try:
                        cursor.execute("""
                            INSERT INTO ohrm_reviewer_rating 
                            (review_id, kpi_id, rating, comment, reviewer_id)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (review_id, kpi_id, rating, comment, reviewer_emp))
                        rating_count += 1
                    except:
                        pass
        
        print(f"   Đã tạo {rating_count} Reviewer Ratings")

        # BƯỚC 6: COMMIT
        conn.commit()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print("\n[THÀNH CÔNG] Đã tạo dữ liệu Performance Management!")
        print(f"  - KPIs: {len(kpi_ids)}")
        print(f"  - Performance Trackers: {len(tracker_ids)}")
        print(f"  - Performance Reviews: {review_count}")
        print(f"  - Reviewer Ratings: {rating_count}")

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
    print("GENERATE PERFORMANCE MANAGEMENT DATA")
    print("="*50)
    generate_performance_data()
