import os
import sqlite3
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

DB_NAME = "labs.db"
EXCEL_FILE = "sample_lab_data.xlsx"

def create_excel_file():
    """Creates a sample Excel file if it doesn't exist."""
    if os.path.exists(EXCEL_FILE):
        return  # Skip if already exists

    labs_df = pd.DataFrame([
        {"room_number": "417", "lab_name": "SJT 417 Lab"},
        {"room_number": "418", "lab_name": "SJT 418 Lab"}
    ])

    images_df = pd.DataFrame([
        {"room_number": "417", "image_path": "/static/images/417.jpg"},
        {"room_number": "418", "image_path": "/static/images/418.jpg"},
    ])

    software_df = pd.DataFrame([
        {"room_number": "417", "name": "MATLAB"},
        {"room_number": "418", "name": "Python"},
    ])

    hardware_df = pd.DataFrame([
        {"room_number": "417", "name": "Oscilloscope"},
        {"room_number": "418", "name": "Arduino"},
    ])

    incharge_df = pd.DataFrame([
        {"room_number": "417", "name": "Dr. A Kumar", "mobile": "9876543210",
         "email": "a.kumar@univ.edu", "cabin": "B-204", "designation": "Professor",
         "type": "faculty", "image_path": "/static/img/faculty1.jpg"},
        {"room_number": "418", "name": "Dr. B Singh", "mobile": "9123456789",
         "email": "b.singh@univ.edu", "cabin": "C-101", "designation": "Assistant Professor",
         "type": "faculty", "image_path": "/static/img/faculty2.jpg"}
    ])

    with pd.ExcelWriter(EXCEL_FILE) as writer:
        labs_df.to_excel(writer, sheet_name="labs", index=False)
        images_df.to_excel(writer, sheet_name="lab_images", index=False)
        software_df.to_excel(writer, sheet_name="software", index=False)
        hardware_df.to_excel(writer, sheet_name="hardware", index=False)
        incharge_df.to_excel(writer, sheet_name="incharge", index=False)

    print("✅ Sample Excel file created.")

def create_database():
    """Creates SQLite database and tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS labs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT UNIQUE NOT NULL,
            lab_name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lab_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lab_id INTEGER,
            image_path TEXT UNIQUE,
            FOREIGN KEY (lab_id) REFERENCES labs(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS software (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lab_id INTEGER,
            name TEXT UNIQUE,
            FOREIGN KEY (lab_id) REFERENCES labs(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hardware (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lab_id INTEGER,
            name TEXT UNIQUE,
            FOREIGN KEY (lab_id) REFERENCES labs(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incharge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lab_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            mobile TEXT,
            email TEXT,
            cabin TEXT,
            designation TEXT,
            type TEXT,
            image_path TEXT,
            UNIQUE(lab_id, name),
            FOREIGN KEY (lab_id) REFERENCES labs(id) ON DELETE CASCADE
        )
    ''')


    conn.commit()
    conn.close()
    print("✅ Database and tables created successfully.")

def insert_data_from_excel():
    """Inserts or updates data from the Excel file into the SQLite database."""
    df_labs = pd.read_excel(EXCEL_FILE, sheet_name="labs")
    df_images = pd.read_excel(EXCEL_FILE, sheet_name="lab_images")
    df_software = pd.read_excel(EXCEL_FILE, sheet_name="software")
    df_hardware = pd.read_excel(EXCEL_FILE, sheet_name="hardware")
    df_incharge = pd.read_excel(EXCEL_FILE, sheet_name="incharge")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Insert or update labs
    for _, row in df_labs.iterrows():
        cursor.execute("INSERT INTO labs (room_number, lab_name) VALUES (?, ?) "
                       "ON CONFLICT(room_number) DO UPDATE SET lab_name = ?",
                       (row["room_number"], row["lab_name"], row["lab_name"]))

    # Insert or ignore lab images
    for _, row in df_images.iterrows():
        cursor.execute("SELECT id FROM labs WHERE room_number = ?", (row["room_number"],))
        lab_id = cursor.fetchone()
        if lab_id:
            cursor.execute("INSERT OR IGNORE INTO lab_images (lab_id, image_path) VALUES (?, ?)",
                           (lab_id[0], row["image_path"]))

    # Insert or ignore software
    for _, row in df_software.iterrows():
        cursor.execute("SELECT id FROM labs WHERE room_number = ?", (row["room_number"],))
        lab_id = cursor.fetchone()
        if lab_id:
            cursor.execute("INSERT OR IGNORE INTO software (lab_id, name) VALUES (?, ?)",
                           (lab_id[0], row["name"]))

    # Insert or ignore hardware
    for _, row in df_hardware.iterrows():
        cursor.execute("SELECT id FROM labs WHERE room_number = ?", (row["room_number"],))
        lab_id = cursor.fetchone()
        if lab_id:
            cursor.execute("INSERT OR IGNORE INTO hardware (lab_id, name) VALUES (?, ?)",
                           (lab_id[0], row["name"]))

    # Insert or update incharge details
    for _, row in df_incharge.iterrows():
        cursor.execute("SELECT id FROM labs WHERE room_number = ?", (row["room_number"],))
        lab_id = cursor.fetchone()
        if lab_id:
            cursor.execute('''INSERT INTO incharge (lab_id, name, mobile, email, cabin, designation, type, image_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(lab_id, name) DO UPDATE SET 
                mobile = excluded.mobile, email = excluded.email, cabin = excluded.cabin,
                designation = excluded.designation, type = excluded.type, image_path = excluded.image_path''',
                (lab_id[0], row["name"], row["mobile"], row["email"], row["cabin"],
                 row["designation"], row["type"], row["image_path"]))

    conn.commit()
    conn.close()
    print("✅ Data inserted/updated from Excel file.")

@app.route('/')
def home():
    return render_template('index.html', lab=None)


@app.route('/lab_json/<room_number>')
def get_lab_data(room_number):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, lab_name FROM labs WHERE room_number = ?", (room_number,))
    lab = cursor.fetchone()
    if not lab:
        return jsonify({"error": "Lab not found."})
    
    lab_id, lab_name = lab

    # Get images
    cursor.execute("SELECT image_path FROM lab_images WHERE lab_id = ?", (lab_id,))
    images = [row[0] for row in cursor.fetchall()]

    # Get software
    cursor.execute("SELECT name FROM software WHERE lab_id = ?", (lab_id,))
    software = [row[0] for row in cursor.fetchall()]

    # Get hardware
    cursor.execute("SELECT name FROM hardware WHERE lab_id = ?", (lab_id,))
    hardware = [row[0] for row in cursor.fetchall()]

    # Get incharges and separate by type
    cursor.execute("SELECT name, mobile, email, cabin, designation, type, image_path FROM incharge WHERE lab_id = ?", (lab_id,))
    faculty = []
    staff = []
    for row in cursor.fetchall():
        incharge = {
            "name": row[0],
            "mobile": row[1],
            "email": row[2],
            "cabin": row[3],
            "designation": row[4],
            "type": row[5],
            "image": row[6]
        }
        if incharge["type"] == "faculty":
            faculty.append(incharge)
        else:
            staff.append(incharge)

    conn.close()

    return jsonify({
        "room_number": room_number,
        "lab_name": lab_name,
        "images": images,
        "software": software,
        "hardware": hardware,
        "faculty": faculty,
        "staff": staff
    })

def get_lab_details(room_number):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, lab_name FROM labs WHERE room_number = ?", (room_number,))
    lab = cursor.fetchone()
    if not lab:
        return None

    lab_id, lab_name = lab

    cursor.execute("SELECT image_path FROM lab_images WHERE lab_id = ?", (lab_id,))
    images = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT name FROM software WHERE lab_id = ?", (lab_id,))
    software = [row[0] for row in cursor.fetchall()]

    conn.close()
    return {"room_number": room_number, "lab_name": lab_name, "images": images, "software": software}

if __name__ == "__main__":
    create_excel_file()
    create_database()
    insert_data_from_excel()
    app.run(debug=True)