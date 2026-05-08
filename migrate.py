import sqlite3

conn = sqlite3.connect("jobs.db")

try:
    conn.execute("ALTER TABLE jobs ADD COLUMN status TEXT DEFAULT 'New'")
    print("Added status column")
except Exception as e:
    print(f"status column may already exist: {e}")

try:
    conn.execute("ALTER TABLE jobs ADD COLUMN notes TEXT DEFAULT ''")
    print("Added notes column")
except Exception as e:
    print(f"notes column may already exist: {e}")

conn.commit()
conn.close()
print("Done")