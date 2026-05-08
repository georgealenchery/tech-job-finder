import sqlite3

DB_NAME = "jobs.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        company TEXT,
        location TEXT,
        url TEXT UNIQUE,
        date_posted TEXT,
        source TEXT,
        date_scraped TEXT DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'New',
        notes TEXT DEFAULT ''
    )
""")
    conn.commit()
    conn.close()

def insert_job(job: dict):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO jobs (title, company, location, url, date_posted, source)
            VALUES (:title, :company, :location, :url, :date_posted, :source)
        """, job)
        conn.commit()
    except sqlite3.Error as e:
        print(f"DB error: {e}")
    finally:
        conn.close()

def get_all_jobs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs ORDER BY date_scraped DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_job_status(job_id: int, status: str, notes: str = ""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE jobs SET status = ?, notes = ? WHERE id = ?
    """, (status, notes, job_id))
    conn.commit()
    conn.close()

def get_jobs_by_status(status: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE status = ?", (status,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_job_status(job_id: int, status: str, notes: str = ""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE jobs SET status = ?, notes = ? WHERE id = ?
    """, (status, notes, job_id))
    conn.commit()
    conn.close()

def get_jobs_by_status(status: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE status = ?", (status,))
    rows = cursor.fetchall()
    conn.close()
    return rows