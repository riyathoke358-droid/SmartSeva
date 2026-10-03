import sqlite3
import os

if os.path.isfile("data"):
    raise RuntimeError(
        "A file named data exists. Rename it and create a folder named data."
    )

os.makedirs("data", exist_ok=True)
import sqlite3
import os

import os
import sqlite3

DATA_DIR = "data"

os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "schemes.db")

def connect_db():
    return sqlite3.connect(DB_PATH)


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

def add_real_schemes():

    conn = connect_db()
    cursor = conn.cursor()

    schemes = [
        (
            "PM-KISAN",
            "Agriculture",
            "Income support scheme for eligible farmer families.",
            "Farmer",
            0,
            100,
            999999999,
            "Aadhaar and land records as applicable",
            "Check the latest eligibility rules on the official portal.",
            "https://pmkisan.gov.in/"
        ),
        (
            "Ayushman Bharat PM-JAY",
            "Healthcare",
            "Health assurance scheme for eligible beneficiaries.",
            "All",
            0,
            100,
            999999999,
            "Documents required for beneficiary verification",
            "Check eligibility and beneficiary details on the official portal.",
            "https://pmjay.gov.in/"
        ),
        (
            "Post Matric Scholarship",
            "Education",
            "Scholarship assistance for eligible students after matriculation.",
            "Student",
            15,
            100,
            999999999,
            "Income certificate, marksheet and other scheme-specific documents",
            "Check the applicable scholarship rules and documents on the official portal.",
            "https://www.myscheme.gov.in/"
        )
    ]

    for scheme in schemes:

        cursor.execute(
            "SELECT id FROM schemes WHERE name = ?",
            (scheme[0],)
        )

        if cursor.fetchone() is None:

            cursor.execute("""
                INSERT INTO schemes (
                    name, category, description, occupation,
                    min_age, max_age, max_income, documents,
                    instructions, official_url
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, scheme)

    conn.commit()
    conn.close()
