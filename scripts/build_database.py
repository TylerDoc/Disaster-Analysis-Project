import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

csv_path = BASE_DIR / "data" / "raw" / "DisasterDeclarationsSummaries.csv"
db_path = BASE_DIR / "database" / "disasters.db"

# Read CSV
df = pd.read_csv(csv_path)

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# ----------------------------
# Create normalized tables
# ----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS states (
    state_id INTEGER PRIMARY KEY AUTOINCREMENT,
    state_code TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS incident_types (
    incident_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_type TEXT UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS disasters (
    disaster_id INTEGER PRIMARY KEY,
    declaration_type TEXT,
    declaration_date TEXT,
    fy_declared INTEGER,
    declaration_title TEXT,
    state_id INTEGER,
    incident_type_id INTEGER,

    FOREIGN KEY(state_id) REFERENCES states(state_id),
    FOREIGN KEY(incident_type_id) REFERENCES incident_types(incident_type_id)
)
""")

# ----------------------------
# Populate states table
# ----------------------------

states = df["state"].dropna().unique()

for state in states:
    cursor.execute("""
    INSERT OR IGNORE INTO states (state_code)
    VALUES (?)
    """, (state,))

# ----------------------------
# Populate incident types table
# ----------------------------

incident_types = df["incidentType"].dropna().unique()

for incident in incident_types:
    cursor.execute("""
    INSERT OR IGNORE INTO incident_types (incident_type)
    VALUES (?)
    """, (incident,))

conn.commit()

# ----------------------------
# Populate disasters table
# ----------------------------

for _, row in df.iterrows():

    # Get state_id
    cursor.execute("""
    SELECT state_id FROM states
    WHERE state_code = ?
    """, (row["state"],))

    state_id = cursor.fetchone()[0]

    # Get incident_type_id
    cursor.execute("""
    SELECT incident_type_id FROM incident_types
    WHERE incident_type = ?
    """, (row["incidentType"],))

    incident_type_id = cursor.fetchone()[0]

    # Insert disaster
    cursor.execute("""
    INSERT OR IGNORE INTO disasters (
        disaster_id,
        declaration_type,
        declaration_date,
        fy_declared,
        declaration_title,
        state_id,
        incident_type_id
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        int(row["disasterNumber"]),
        row["declarationType"],
        row["declarationDate"],
        int(row["fyDeclared"]),
        row["declarationTitle"],
        state_id,
        incident_type_id
    ))

conn.commit()
conn.close()

print("SQLite database created successfully.")
