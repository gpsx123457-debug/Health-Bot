import sqlite3
import json
from datetime import datetime

DB_NAME = "health_ai.db"

# -------------------------------
# INIT DATABASE
# -------------------------------
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()

        c.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            dob TEXT,
            symptoms TEXT,
            disease TEXT,
            confidence REAL,
            medicine TEXT,
            units INTEGER,
            cost REAL,
            timestamp TEXT
        )
        """)

        conn.commit()


# -------------------------------
# INSERT RECORD
# -------------------------------
def insert_record(data):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()

        c.execute("""
        INSERT INTO records (
            name, age, dob, symptoms,
            disease, confidence,
            medicine, units, cost,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("name", ""),
            data.get("age", 0),
            str(data.get("dob", "")),
            json.dumps(data.get("symptoms", {})),
            data.get("disease", ""),
            data.get("confidence", 0),
            data.get("medicine", ""),
            data.get("units", 0),
            data.get("cost", 0),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()


# -------------------------------
# FETCH RECORDS (NEW)
# -------------------------------
def fetch_records():
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM records ORDER BY id DESC")
        rows = c.fetchall()

        columns = [desc[0] for desc in c.description]

    return rows, columns