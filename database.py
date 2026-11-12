import sqlite3

DB_NAME = "stmarys_school.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # 1. Students Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        gender TEXT CHECK(gender IN ('Male', 'Female')),
        level TEXT CHECK(level IN ('O-Level', 'A-Level')) NOT NULL,
        class_name TEXT NOT NULL,
        stream TEXT,
        combination TEXT,
        boarding_status TEXT CHECK(boarding_status IN ('Boarding', 'Day')),
        guardian_name TEXT,
        guardian_phone TEXT,
        termly_fee_due REAL DEFAULT 0.0,
        photo_path TEXT
    );
    """)

    # 2. Subjects Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_code TEXT UNIQUE NOT NULL,
        subject_name TEXT NOT NULL,
        level TEXT CHECK(level IN ('O-Level', 'A-Level')) NOT NULL,
        is_subsidiary INTEGER DEFAULT 0,
        paper_count INTEGER DEFAULT 1
    );
    """)

    # 3. Marks Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS marks (
        mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        subject_id INTEGER NOT NULL,
        term TEXT NOT NULL,
        year INTEGER NOT NULL,
        exam_type TEXT CHECK(exam_type IN ('Mid-Term', 'End-of-Term')) NOT NULL,
        aoi_score REAL DEFAULT 0.0,
        paper_1 REAL DEFAULT 0.0,
        paper_2 REAL DEFAULT 0.0,
        paper_3 REAL DEFAULT 0.0,
        exam_score REAL DEFAULT 0.0,
        teacher_comment TEXT,
        teacher_initials TEXT,
        UNIQUE(student_id, subject_id, term, year, exam_type),
        FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
    );
    """)

    # 4. Staff Registry
    cur.execute("""
    CREATE TABLE IF NOT EXISTS staff (
        staff_id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL,
        subjects_taught TEXT,
        base_salary REAL NOT NULL,
        default_allowance REAL DEFAULT 0.0,
        payment_account TEXT
    );
    """)

    # 5. Staff Payroll
    cur.execute("""
    CREATE TABLE IF NOT EXISTS staff_payroll (
        payroll_id INTEGER PRIMARY KEY AUTOINCREMENT,
        staff_id TEXT NOT NULL,
        month TEXT NOT NULL,
        year INTEGER NOT NULL,
        base_salary REAL NOT NULL,
        allowances REAL DEFAULT 0.0,
        gross_pay REAL NOT NULL,
        salary_advance REAL DEFAULT 0.0,
        net_paid REAL NOT NULL,
        status TEXT CHECK(status IN ('Pending', 'Approved', 'Paid')) DEFAULT 'Pending',
        UNIQUE(staff_id, month, year),
        FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

def seed_demo_data():
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM students;")
    if cur.fetchone()[0] > 0:
        conn.close()
        return

    # Seed Sample Students
    students = [
        ("SMHS-2026-001", "Namukasa Sarah", "Female", "O-Level", "S.3", "East", None, "Boarding", "Mr. Mukasa John", "0772112233", 850000, "assets/sample_student.png"),
        ("SMHS-2026-002", "Ssekandi Brian", "Male", "O-Level", "S.4", "North", None, "Day", "Mrs. Ssekandi Grace", "0701445566", 550000, "assets/sample_student.png"),
        ("SMHS-2026-003", "Nabulya Esther", "Female", "A-Level", "S.6", "Science", "PEM/ICT", "Boarding", "Mr. Wasswa Peter", "0782998877", 950000, "assets/sample_student.png"),
    ]
    cur.executemany("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", students)

    # Seed Sample Staff
    staff = [
        ("STF-001", "Kigozi Robert", "Teacher", "Mathematics / Physics", 1200000, 150000, "Airtel Money"),
        ("STF-002", "Namusoke Lillian", "Bursar", "Finance & Administration", 1000000, 100000, "MTN MoMo"),
    ]
    cur.executemany("INSERT OR IGNORE INTO staff VALUES (?, ?, ?, ?, ?, ?, ?);", staff)

    conn.commit()
    conn.close()