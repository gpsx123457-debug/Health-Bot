import sqlite3
import json
from datetime import datetime

DB_NAME = "health_ai.db"

# -------------------------------
# INIT DATABASE
# -------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
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
    conn.close()

# -------------------------------
# INSERT RECORD
# -------------------------------
def insert_record(data):
    conn = sqlite3.connect(DB_NAME)
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
        data["name"],
        data["age"],
        str(data["dob"]),
        json.dumps(data["symptoms"]),
        data["disease"],
        data["confidence"],
        data["medicine"],
        data["units"],
        data["cost"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()