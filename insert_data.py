import sqlite3
def insert_sample_data():
    conn = sqlite3.connect("labs.db")
    cursor = conn.cursor()

    # Add lab
    cursor.execute("INSERT OR IGNORE INTO labs (room_number, lab_name) VALUES (?, ?)", ("417", "SJT 417 Lab"))
    conn.commit()

    # Get lab_id
    cursor.execute("SELECT id FROM labs WHERE room_number = ?", ("417",))
    lab_id = cursor.fetchone()[0]

    # Add sample images
    cursor.execute("INSERT INTO lab_images (lab_id, image_path) VALUES (?, ?)", (lab_id, "/static/images/418.jpg"))
    cursor.execute("INSERT INTO lab_images (lab_id, image_path) VALUES (?, ?)", (lab_id, "/static/images/417.jpg"))
    cursor.execute("INSERT INTO lab_images (lab_id, image_path) VALUES (?, ?)", (lab_id, "/static/images/515.jpg"))

    # Add software
    cursor.execute("INSERT INTO software (lab_id, name) VALUES (?, ?)", (lab_id, "MATLAB"))
    cursor.execute("INSERT INTO software (lab_id, name) VALUES (?, ?)", (lab_id, "Python"))

    # Add hardware
    cursor.execute("INSERT INTO hardware (lab_id, name) VALUES (?, ?)", (lab_id, "Raspberry Pi"))
    cursor.execute("INSERT INTO hardware (lab_id, name) VALUES (?, ?)", (lab_id, "Oscilloscope"))

    # Add faculty incharge
    cursor.execute('''INSERT INTO incharge 
        (lab_id, name, mobile, email, cabin, designation, type, image_path) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (lab_id, "Dr. A Kumar", "9876543210", "a.kumar@univ.edu", "B-204", "Professor", "faculty", "/static/img/faculty1.jpg"))

    # Add staff incharge
    cursor.execute('''INSERT INTO incharge 
        (lab_id, name, mobile, email, cabin, designation, type, image_path) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (lab_id, "Mr. S Raj", "9123456789", "s.raj@univ.edu", "C-101", "Lab Staff", "staff", "/static/img/staff1.jpg"))

    conn.commit()
    conn.close()
    print("✅ Sample data inserted.")

# Call it once
insert_sample_data()
