"""
Test Cases Definition for HR Administration & Performance Management
45 Test Cases using Black-Box Testing Techniques:
- Domain Testing: 18 cases (40%)
- Decision Table: 14 cases (31%)
- Use Case Testing: 13 cases (29%)
"""

# ============================================
# HR ADMINISTRATION MODULE - 29 TEST CASES
# ============================================

HR_ADMIN_TEST_CASES = [
    # ========== LOCATIONS - Domain Testing (7 cases) ==========
    {
        "id": "TC_LOC_D01",
        "module": "HR Administration",
        "feature": "Locations",
        "technique": "Domain Testing",
        "test_case": "Add location with valid data (Happy Path)",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Admin > Organization > Locations\n2. Click Add\n3. Fill Name: 'HCM Office', Country: Viet Nam, City: Ho Chi Minh\n4. Click Save",
        "test_data": "Name: HCM Office, Country: Viet Nam, City: Ho Chi Minh",
        "expected_result": "Location added successfully",
        "priority": "High",
        "ec_covered": "EC2, EC6, EC8, EC10"
    },
    {
        "id": "TC_LOC_D02",
        "module": "HR Administration",
        "feature": "Locations",
        "technique": "Domain Testing",
        "test_case": "Add location with minimum name length (1 char) - Boundary",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Admin > Organization > Locations\n2. Click Add\n3. Fill Name: 'A', Country: Viet Nam\n4. Click Save",
        "test_data": "Name: A (1 character)",
        "expected_result": "Location added successfully",
        "priority": "Medium",
        "ec_covered": "EC2 - Boundary Min"
    },
    {
        "id": "TC_LOC_D03",
        "module": "HR Administration",
        "feature": "Locations",
        "technique": "Domain Testing",
        "test_case": "Add location with maximum name length (100 chars) - Boundary",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Admin > Organization > Locations\n2. Click Add\n3. Fill Name with 100 characters\n4. Click Save",
        "test_data": "Name: 'A' * 100 (100 characters)",
        "expected_result": "Location added successfully",
        "priority": "Medium",
        "ec_covered": "EC2 - Boundary Max"
    },
    {
        "id": "TC_LOC_D04",
        "module": "HR Administration",
        "feature": "Locations",
        "technique": "Domain Testing",
        "test_case": "Add location with empty name - Invalid",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Admin > Organization > Locations\n2. Click Add\n3. Leave Name empty, Select Country\n4. Click Save",
        "test_data": "Name: (empty)",
        "expected_result": "Error message: Required",
        "priority": "High",
        "ec_covered": "EC1 - Invalid Empty"
    },
    {
        "id": "TC_LOC_D05",
        "module": "HR Administration",
        "feature": "Locations",
        "technique": "Domain Testing",
        "test_case": "Add location with name exceeding max length - Invalid",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Admin > Organization > Locations\n2. Click Add\n3. Fill Name with 101 characters\n4. Click Save",
        "test_data": "Name: 'A' * 101 (101 characters)",
        "expected_result": "Error or name truncated to 100 chars",
        "priority": "Medium",
        "ec_covered": "EC3 - Invalid Length"
    },
    {
        "id": "TC_LOC_D06",
        "module": "HR Administration",
        "feature": "Locations",
        "technique": "Domain Testing",
        "test_case": "Add location without selecting country - Invalid",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Admin > Organization > Locations\n2. Click Add\n3. Fill Name, do not select Country\n4. Click Save",
        "test_data": "Name: Office, Country: (not selected)",
        "expected_result": "Error message: Required",
        "priority": "High",
        "ec_covered": "EC5 - Invalid Country"
    },
    {
        "id": "TC_LOC_D07",
        "module": "HR Administration",
        "feature": "Locations",
        "technique": "Domain Testing",
        "test_case": "Add location with duplicate name - Invalid",
        "precondition": "Location 'HCM Office' already exists",
        "steps": "1. Go to Admin > Organization > Locations\n2. Click Add\n3. Fill Name: 'HCM Office' (duplicate)\n4. Click Save",
        "test_data": "Name: HCM Office (duplicate)",
        "expected_result": "Error message: Already exists",
        "priority": "High",
        "ec_covered": "EC4 - Duplicate"
    },
    
    # ========== LOCATIONS - Decision Table (3 cases) ==========
    {
        "id": "TC_LOC_DT01",
        "module": "HR Administration",
        "feature": "Locations",
        "technique": "Decision Table",
        "test_case": "Rule 1: All conditions valid - Success",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Locations\n2. Add with Name: 'Office A', Country: VN, Unique name\n3. Save",
        "test_data": "Name: Office A, Country: Viet Nam, Unique: Yes",
        "expected_result": "Location created successfully",
        "priority": "High",
        "rule": "R1: Name=T, Country=T, Unique=T -> Success"
    },
    {
        "id": "TC_LOC_DT02",
        "module": "HR Administration",
        "feature": "Locations",
        "technique": "Decision Table",
        "test_case": "Rule 2: Name empty - Error",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Locations\n2. Add with Name: empty, Country: VN\n3. Save",
        "test_data": "Name: (empty), Country: Viet Nam",
        "expected_result": "Error: Name required",
        "priority": "High",
        "rule": "R2: Name=F, Country=T -> Error Name"
    },
    {
        "id": "TC_LOC_DT03",
        "module": "HR Administration",
        "feature": "Locations",
        "technique": "Decision Table",
        "test_case": "Rule 3: Country not selected - Error",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Locations\n2. Add with Name: 'Office B', Country: not selected\n3. Save",
        "test_data": "Name: Office B, Country: (not selected)",
        "expected_result": "Error: Country required",
        "priority": "High",
        "rule": "R3: Name=T, Country=F -> Error Country"
    },
    
    # ========== LOCATIONS - Use Case (2 cases) ==========
    {
        "id": "TC_LOC_UC01",
        "module": "HR Administration",
        "feature": "Locations",
        "technique": "Use Case Testing",
        "test_case": "Scenario 1: Add location with full information",
        "precondition": "User logged in as Admin",
        "steps": "1. Login as Admin\n2. Go to Admin > Organization > Locations\n3. Click Add\n4. Fill Name, Country, City, Address, Phone\n5. Click Save",
        "test_data": "Full location info",
        "expected_result": "Location added successfully, displayed in list",
        "priority": "High",
        "scenario": "S1 - Happy Path"
    },
    {
        "id": "TC_LOC_UC02",
        "module": "HR Administration",
        "feature": "Locations",
        "technique": "Use Case Testing",
        "test_case": "Scenario 3: Search location by name",
        "precondition": "Locations exist in system",
        "steps": "1. Go to Locations\n2. Enter search term 'HCM'\n3. Click Search",
        "test_data": "Search: HCM",
        "expected_result": "Matching locations displayed",
        "priority": "Medium",
        "scenario": "S3 - Search"
    },
    
    # ========== JOB TITLES - Domain Testing (4 cases) ==========
    {
        "id": "TC_JOB_D01",
        "module": "HR Administration",
        "feature": "Job Titles",
        "technique": "Domain Testing",
        "test_case": "Add job title with valid data",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Admin > Job > Job Titles\n2. Click Add\n3. Enter Title: 'Senior Developer'\n4. Click Save",
        "test_data": "Title: Senior Developer",
        "expected_result": "Job title added successfully",
        "priority": "High",
        "ec_covered": "EC2, EC5"
    },
    {
        "id": "TC_JOB_D02",
        "module": "HR Administration",
        "feature": "Job Titles",
        "technique": "Domain Testing",
        "test_case": "Add job title with empty name - Invalid",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Admin > Job > Job Titles\n2. Click Add\n3. Leave Title empty\n4. Click Save",
        "test_data": "Title: (empty)",
        "expected_result": "Error message: Required",
        "priority": "High",
        "ec_covered": "EC1"
    },
    {
        "id": "TC_JOB_D03",
        "module": "HR Administration",
        "feature": "Job Titles",
        "technique": "Domain Testing",
        "test_case": "Add duplicate job title - Invalid",
        "precondition": "Job title 'Staff' already exists",
        "steps": "1. Go to Admin > Job > Job Titles\n2. Click Add\n3. Enter Title: 'Staff' (duplicate)\n4. Click Save",
        "test_data": "Title: Staff (duplicate)",
        "expected_result": "Error message: Already exists",
        "priority": "Medium",
        "ec_covered": "EC4"
    },
    {
        "id": "TC_JOB_D04",
        "module": "HR Administration",
        "feature": "Job Titles",
        "technique": "Domain Testing",
        "test_case": "Add job title with max length (100 chars) - Boundary",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Admin > Job > Job Titles\n2. Click Add\n3. Enter Title with 100 characters\n4. Click Save",
        "test_data": "Title: 'A' * 100",
        "expected_result": "Job title added successfully",
        "priority": "Medium",
        "ec_covered": "EC2 - Boundary Max"
    },
    
    # ========== JOB TITLES - Decision Table (2 cases) ==========
    {
        "id": "TC_JOB_DT01",
        "module": "HR Administration",
        "feature": "Job Titles",
        "technique": "Decision Table",
        "test_case": "Rule 1: All conditions valid",
        "precondition": "User logged in as Admin",
        "steps": "1. Add job title with valid, unique name\n2. Save",
        "test_data": "Title: QA Engineer (unique)",
        "expected_result": "Job title created successfully",
        "priority": "High",
        "rule": "R1: Title=T, Unique=T -> Success"
    },
    {
        "id": "TC_JOB_DT02",
        "module": "HR Administration",
        "feature": "Job Titles",
        "technique": "Decision Table",
        "test_case": "Rule 2: Title empty",
        "precondition": "User logged in as Admin",
        "steps": "1. Leave title empty\n2. Save",
        "test_data": "Title: (empty)",
        "expected_result": "Error: Required",
        "priority": "High",
        "rule": "R2: Title=F -> Error"
    },
    
    # ========== JOB TITLES - Use Case (3 cases) ==========
    {
        "id": "TC_JOB_UC01",
        "module": "HR Administration",
        "feature": "Job Titles",
        "technique": "Use Case Testing",
        "test_case": "Scenario 1: Add new job title",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Admin > Job > Job Titles\n2. Click Add\n3. Enter Title\n4. Save",
        "test_data": "Title: Project Manager",
        "expected_result": "Job title added",
        "priority": "High",
        "scenario": "S1 - Add"
    },
    {
        "id": "TC_JOB_UC02",
        "module": "HR Administration",
        "feature": "Job Titles",
        "technique": "Use Case Testing",
        "test_case": "Scenario 4: View job titles list",
        "precondition": "Job titles exist",
        "steps": "1. Go to Admin > Job > Job Titles",
        "test_data": "N/A",
        "expected_result": "Job titles list displayed",
        "priority": "High",
        "scenario": "S4 - View List"
    },
    {
        "id": "TC_JOB_UC03",
        "module": "HR Administration",
        "feature": "Job Titles",
        "technique": "Use Case Testing",
        "test_case": "Scenario 5: Delete job title",
        "precondition": "Job title exists, not assigned",
        "steps": "1. Go to Job Titles\n2. Select a job title\n3. Click Delete\n4. Confirm",
        "test_data": "Title: Test Title",
        "expected_result": "Job title deleted",
        "priority": "Medium",
        "scenario": "S5 - Delete"
    },
    
    # ========== SKILLS - Use Case (2 cases) + Domain (1 case) ==========
    {
        "id": "TC_SKL_UC01",
        "module": "HR Administration",
        "feature": "Skills",
        "technique": "Use Case Testing",
        "test_case": "Add new skill",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Admin > Qualifications > Skills\n2. Click Add\n3. Enter Name: 'Python Programming'\n4. Click Save",
        "test_data": "Name: Python Programming",
        "expected_result": "Skill added successfully",
        "priority": "High",
        "scenario": "S1 - Add"
    },
    {
        "id": "TC_SKL_UC02",
        "module": "HR Administration",
        "feature": "Skills",
        "technique": "Use Case Testing",
        "test_case": "View skills list",
        "precondition": "Skills exist",
        "steps": "1. Go to Admin > Qualifications > Skills",
        "test_data": "N/A",
        "expected_result": "Skills list displayed",
        "priority": "Medium",
        "scenario": "S2 - View"
    },
    {
        "id": "TC_SKL_D01",
        "module": "HR Administration",
        "feature": "Skills",
        "technique": "Domain Testing",
        "test_case": "Add skill with empty name - Invalid",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Skills\n2. Click Add\n3. Leave Name empty\n4. Click Save",
        "test_data": "Name: (empty)",
        "expected_result": "Error message: Required",
        "priority": "High",
        "ec_covered": "EC1"
    },
    
    # ========== EDUCATION - Use Case (1 case) + Domain (1 case) ==========
    {
        "id": "TC_EDU_UC01",
        "module": "HR Administration",
        "feature": "Education",
        "technique": "Use Case Testing",
        "test_case": "Add new education level",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Admin > Qualifications > Education\n2. Click Add\n3. Enter Level: 'Bachelor Degree'\n4. Click Save",
        "test_data": "Level: Bachelor Degree",
        "expected_result": "Education level added",
        "priority": "High",
        "scenario": "S1 - Add"
    },
    {
        "id": "TC_EDU_D01",
        "module": "HR Administration",
        "feature": "Education",
        "technique": "Domain Testing",
        "test_case": "Add education with empty name - Invalid",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Education\n2. Click Add\n3. Leave Level empty\n4. Click Save",
        "test_data": "Level: (empty)",
        "expected_result": "Error: Required",
        "priority": "High",
        "ec_covered": "EC1"
    },
    
    # ========== LANGUAGES - Use Case (1 case) + Domain (1 case) ==========
    {
        "id": "TC_LNG_UC01",
        "module": "HR Administration",
        "feature": "Languages",
        "technique": "Use Case Testing",
        "test_case": "Add new language",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Admin > Qualifications > Languages\n2. Click Add\n3. Enter Name: 'Vietnamese'\n4. Click Save",
        "test_data": "Name: Vietnamese",
        "expected_result": "Language added",
        "priority": "High",
        "scenario": "S1 - Add"
    },
    {
        "id": "TC_LNG_D01",
        "module": "HR Administration",
        "feature": "Languages",
        "technique": "Domain Testing",
        "test_case": "Add language with empty name - Invalid",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Languages\n2. Click Add\n3. Leave Name empty\n4. Click Save",
        "test_data": "Name: (empty)",
        "expected_result": "Error: Required",
        "priority": "High",
        "ec_covered": "EC1"
    },
    
    # ========== LICENSES - Use Case (1 case) ==========
    {
        "id": "TC_LIC_UC01",
        "module": "HR Administration",
        "feature": "Licenses",
        "technique": "Use Case Testing",
        "test_case": "Add new license type",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Admin > Qualifications > Licenses\n2. Click Add\n3. Enter Name: 'AWS Certified'\n4. Click Save",
        "test_data": "Name: AWS Certified",
        "expected_result": "License added",
        "priority": "High",
        "scenario": "S1 - Add"
    },
]

# ============================================
# PERFORMANCE MANAGEMENT MODULE - 16 TEST CASES
# ============================================

PERFORMANCE_TEST_CASES = [
    # ========== KPIs - Domain Testing (6 cases) ==========
    {
        "id": "TC_KPI_D01",
        "module": "Performance Management",
        "feature": "KPIs",
        "technique": "Domain Testing",
        "test_case": "Add KPI with valid data (Happy Path)",
        "precondition": "User logged in as Admin, Job Titles exist",
        "steps": "1. Go to Performance > Configure > KPIs\n2. Click Add\n3. Fill: Indicator='Sales Target', Job='Sales Rep', Min=0, Max=100\n4. Save",
        "test_data": "Indicator: Sales Target, Job: Sales Rep, Min: 0, Max: 100",
        "expected_result": "KPI added successfully",
        "priority": "High",
        "ec_covered": "EC2, EC4, EC6, EC8"
    },
    {
        "id": "TC_KPI_D02",
        "module": "Performance Management",
        "feature": "KPIs",
        "technique": "Domain Testing",
        "test_case": "Add KPI with empty indicator - Invalid",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to KPIs\n2. Click Add\n3. Leave Indicator empty\n4. Save",
        "test_data": "Indicator: (empty)",
        "expected_result": "Error message: Required",
        "priority": "High",
        "ec_covered": "EC1"
    },
    {
        "id": "TC_KPI_D03",
        "module": "Performance Management",
        "feature": "KPIs",
        "technique": "Domain Testing",
        "test_case": "Add KPI without selecting Job Title - Invalid",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to KPIs\n2. Click Add\n3. Fill Indicator, don't select Job Title\n4. Save",
        "test_data": "Indicator: Test KPI, Job: (not selected)",
        "expected_result": "Error message: Required",
        "priority": "High",
        "ec_covered": "EC3"
    },
    {
        "id": "TC_KPI_D04",
        "module": "Performance Management",
        "feature": "KPIs",
        "technique": "Domain Testing",
        "test_case": "Add KPI with Min > Max - Invalid range",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to KPIs\n2. Click Add\n3. Fill Min: 80, Max: 50\n4. Save",
        "test_data": "Min: 80, Max: 50",
        "expected_result": "Error: Invalid range (Min cannot exceed Max)",
        "priority": "High",
        "ec_covered": "EC7"
    },
    {
        "id": "TC_KPI_D05",
        "module": "Performance Management",
        "feature": "KPIs",
        "technique": "Domain Testing",
        "test_case": "Add KPI with Min = Max - Boundary valid",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to KPIs\n2. Click Add\n3. Fill Min: 50, Max: 50\n4. Save",
        "test_data": "Min: 50, Max: 50",
        "expected_result": "KPI added successfully",
        "priority": "Medium",
        "ec_covered": "EC6, EC8 - Boundary"
    },
    {
        "id": "TC_KPI_D06",
        "module": "Performance Management",
        "feature": "KPIs",
        "technique": "Domain Testing",
        "test_case": "Add KPI with negative Min - Invalid",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to KPIs\n2. Click Add\n3. Fill Min: -10\n4. Save",
        "test_data": "Min: -10",
        "expected_result": "Error: Invalid value",
        "priority": "Medium",
        "ec_covered": "EC5"
    },
    
    # ========== KPIs - Decision Table (3 cases) ==========
    {
        "id": "TC_KPI_DT01",
        "module": "Performance Management",
        "feature": "KPIs",
        "technique": "Decision Table",
        "test_case": "Rule 1: All conditions valid",
        "precondition": "User logged in as Admin",
        "steps": "1. Add KPI with valid indicator, job title, and valid range\n2. Save",
        "test_data": "Indicator: KPI1, Job: Developer, Min: 0, Max: 100",
        "expected_result": "KPI created successfully",
        "priority": "High",
        "rule": "R1: Indicator=T, Job=T, Range=T -> Success"
    },
    {
        "id": "TC_KPI_DT02",
        "module": "Performance Management",
        "feature": "KPIs",
        "technique": "Decision Table",
        "test_case": "Rule 2: Indicator empty",
        "precondition": "User logged in as Admin",
        "steps": "1. Leave indicator empty\n2. Save",
        "test_data": "Indicator: (empty)",
        "expected_result": "Error: Indicator required",
        "priority": "High",
        "rule": "R2: Indicator=F -> Error"
    },
    {
        "id": "TC_KPI_DT03",
        "module": "Performance Management",
        "feature": "KPIs",
        "technique": "Decision Table",
        "test_case": "Rule 3: Job Title not selected",
        "precondition": "User logged in as Admin",
        "steps": "1. Fill indicator, don't select job\n2. Save",
        "test_data": "Indicator: Test, Job: (none)",
        "expected_result": "Error: Job Title required",
        "priority": "High",
        "rule": "R3: Indicator=T, Job=F -> Error"
    },
    
    # ========== KPIs - Use Case (2 cases) ==========
    {
        "id": "TC_KPI_UC01",
        "module": "Performance Management",
        "feature": "KPIs",
        "technique": "Use Case Testing",
        "test_case": "Scenario 1: Add KPI with full information",
        "precondition": "User logged in as Admin",
        "steps": "1. Go to Performance > Configure > KPIs\n2. Click Add\n3. Fill all fields\n4. Save",
        "test_data": "Full KPI data",
        "expected_result": "KPI added, displayed in list",
        "priority": "High",
        "scenario": "S1 - Add"
    },
    {
        "id": "TC_KPI_UC02",
        "module": "Performance Management",
        "feature": "KPIs",
        "technique": "Use Case Testing",
        "test_case": "Scenario 2: View KPIs list",
        "precondition": "KPIs exist",
        "steps": "1. Go to Performance > Configure > KPIs",
        "test_data": "N/A",
        "expected_result": "KPIs list displayed",
        "priority": "High",
        "scenario": "S2 - View"
    },
    
    # ========== REVIEWS - Decision Table (3 cases) ==========
    {
        "id": "TC_REV_DT01",
        "module": "Performance Management",
        "feature": "Reviews",
        "technique": "Decision Table",
        "test_case": "Rule 1: Create review with all valid data",
        "precondition": "Employees exist",
        "steps": "1. Go to Performance > Manage Reviews > Manage Reviews\n2. Add review with Employee, Supervisor, valid dates\n3. Save",
        "test_data": "Employee: John, Supervisor: Admin, Start: 2025-01-01, End: 2025-12-31",
        "expected_result": "Review created successfully",
        "priority": "High",
        "rule": "R1: Employee=T, Supervisor=T, Dates=T -> Success"
    },
    {
        "id": "TC_REV_DT02",
        "module": "Performance Management",
        "feature": "Reviews",
        "technique": "Decision Table",
        "test_case": "Rule 2: No employee selected",
        "precondition": "User logged in as Admin",
        "steps": "1. Try to add review without selecting employee\n2. Save",
        "test_data": "Employee: (not selected)",
        "expected_result": "Error: Employee required",
        "priority": "High",
        "rule": "R2: Employee=F -> Error"
    },
    {
        "id": "TC_REV_DT03",
        "module": "Performance Management",
        "feature": "Reviews",
        "technique": "Decision Table",
        "test_case": "Rule 5: End date before start date",
        "precondition": "User logged in as Admin",
        "steps": "1. Add review with End date before Start date\n2. Save",
        "test_data": "Start: 2025-12-31, End: 2025-01-01",
        "expected_result": "Error: Invalid date range",
        "priority": "High",
        "rule": "R5: End < Start -> Error"
    },
    
    # ========== REVIEWS - Use Case (2 cases) ==========
    {
        "id": "TC_REV_UC01",
        "module": "Performance Management",
        "feature": "Reviews",
        "technique": "Use Case Testing",
        "test_case": "Scenario 1: Create new review",
        "precondition": "Employees and supervisors exist",
        "steps": "1. Go to Performance > Manage Reviews > Manage Reviews\n2. Click Add\n3. Fill Employee, Supervisor, Dates\n4. Save",
        "test_data": "Full review data",
        "expected_result": "Review created, displayed in list",
        "priority": "High",
        "scenario": "S1 - Create"
    },
    {
        "id": "TC_REV_UC02",
        "module": "Performance Management",
        "feature": "Reviews",
        "technique": "Use Case Testing",
        "test_case": "Scenario 3: Search reviews by employee",
        "precondition": "Reviews exist",
        "steps": "1. Go to Manage Reviews\n2. Enter employee name\n3. Click Search",
        "test_data": "Search: John",
        "expected_result": "Reviews for employee displayed",
        "priority": "Medium",
        "scenario": "S3 - Search"
    },
    
    # ========== TRACKERS - Use Case (1 case) ==========
    {
        "id": "TC_TRK_UC01",
        "module": "Performance Management",
        "feature": "Trackers",
        "technique": "Use Case Testing",
        "test_case": "View My Trackers page",
        "precondition": "User logged in",
        "steps": "1. Go to Performance > My Trackers",
        "test_data": "N/A",
        "expected_result": "My Trackers page displayed",
        "priority": "High",
        "scenario": "S1 - View"
    },
]

# ============================================
# COMBINED TEST CASES
# ============================================

ALL_TEST_CASES = HR_ADMIN_TEST_CASES + PERFORMANCE_TEST_CASES

# ============================================
# STATISTICS
# ============================================

def get_test_statistics():
    """Get statistics about test cases"""
    stats = {
        "total": len(ALL_TEST_CASES),
        "by_technique": {},
        "by_module": {},
        "by_feature": {}
    }
    
    for tc in ALL_TEST_CASES:
        # By technique
        technique = tc.get("technique", "Unknown")
        stats["by_technique"][technique] = stats["by_technique"].get(technique, 0) + 1
        
        # By module
        module = tc.get("module", "Unknown")
        stats["by_module"][module] = stats["by_module"].get(module, 0) + 1
        
        # By feature
        feature = tc.get("feature", "Unknown")
        stats["by_feature"][feature] = stats["by_feature"].get(feature, 0) + 1
    
    return stats


if __name__ == "__main__":
    stats = get_test_statistics()
    print(f"\n{'='*60}")
    print(f"TEST CASES STATISTICS")
    print(f"{'='*60}")
    print(f"Total Test Cases: {stats['total']}")
    print(f"\nBy Technique:")
    for tech, count in stats["by_technique"].items():
        percentage = (count / stats['total']) * 100
        print(f"  - {tech}: {count} ({percentage:.1f}%)")
    print(f"\nBy Module:")
    for mod, count in stats["by_module"].items():
        print(f"  - {mod}: {count}")
    print(f"\nBy Feature:")
    for feat, count in stats["by_feature"].items():
        print(f"  - {feat}: {count}")
    print(f"{'='*60}")
