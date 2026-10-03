import sqlite3
import os

os.makedirs("data", exist_ok=True)

def connect_db():
    return sqlite3.connect("data/schemes.db")

def create_database():

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schemes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            description TEXT,
            occupation TEXT,
            min_age INTEGER,
            max_age INTEGER,
            max_income REAL,
            documents TEXT,
            instructions TEXT,
            official_url TEXT
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM schemes")

    if cursor.fetchone()[0] == 0:

        demo_data = [
            (
                "Demo Student Support",
                "Education",
                "Illustrative student education support record.",
                "Student", 16, 30, 500000,
                "ID proof, income certificate, education documents",
                "Check the official eligibility rules before applying.",
                "https://www.india.gov.in/"
            ),
            (
                "Demo Farmer Support",
                "Agriculture",
                "Illustrative farmer support record.",
                "Farmer", 18, 80, 800000,
                "ID proof, land records, bank details",
                "Verify scheme conditions with the relevant department.",
                "https://www.india.gov.in/"
            ),
            (
                "Demo Women Support",
                "Women Welfare",
                "Illustrative women welfare record.",
                "Women", 18, 60, 400000,
                "ID proof, address proof, income certificate",
                "Check the applicable government scheme guidelines.",
                "https://www.india.gov.in/"
            ),
            (
                "Demo Employment Support",
                "Employment",
                "Illustrative employment support record.",
                "Unemployed", 18, 40, 300000,
                "ID proof, address proof, education certificate",
                "Verify the official application process.",
                "https://www.india.gov.in/"
            )
        ]

        cursor.executemany("""
            INSERT INTO schemes
            (name, category, description, occupation,
             min_age, max_age, max_income, documents,
             instructions, official_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, demo_data)

    conn.commit()
    conn.close()


def get_schemes():

    conn = connect_db()

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM schemes")

    rows = cursor.fetchall()

    conn.close()

    return rows