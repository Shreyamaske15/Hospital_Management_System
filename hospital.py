import sqlite3

# -----------------------------
# Database setup
# -----------------------------
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

# Patients table
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    disease TEXT NOT NULL
)
""")

# Appointments table
cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    doctor_name TEXT NOT NULL,
    appointment_date TEXT NOT NULL,
    appointment_time TEXT NOT NULL,
    FOREIGN KEY(patient_id) REFERENCES patients(id)
)
""")

conn.commit()


# -----------------------------
# Patient functions
# -----------------------------
def add_patient():
    print("\n========== ADD PATIENT ==========\n")
    name = input("Enter patient name: ")
    age = int(input("Enter age: "))
    disease = input("Enter disease: ")

    cursor.execute(
        "INSERT INTO patients (name, age, disease) VALUES (?, ?, ?)",
        (name, age, disease)
    )
    conn.commit()
    print("\nPatient added successfully!\n")


def view_patients():
    print("\n========== PATIENT RECORDS ==========\n")
    cursor.execute("SELECT * FROM patients")
    data = cursor.fetchall()

    if not data:
        print("No patient records found.\n")
        return

    print("ID\tName\t\tAge\tDisease")
    print("-----------------------------------------")
    for patient in data:
        print(f"{patient[0]}\t{patient[1]}\t\t{patient[2]}\t{patient[3]}")
    print()


def search_patient():
    print("\n========== SEARCH PATIENT ==========\n")
    search_id = input("Enter patient ID: ")

    cursor.execute("SELECT * FROM patients WHERE id = ?", (search_id,))
    patient = cursor.fetchone()

    if patient:
        print("\nPatient Found:\n")
        print(f"ID      : {patient[0]}")
        print(f"Name    : {patient[1]}")
        print(f"Age     : {patient[2]}")
        print(f"Disease : {patient[3]}\n")
    else:
        print("\nPatient not found!\n")


def update_patient():
    print("\n========== UPDATE PATIENT ==========\n")
    patient_id = input("Enter patient ID: ")

    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()

    if not patient:
        print("\nPatient not found!\n")
        return

    print("\nLeave blank to keep old value.\n")

    new_name = input(f"Enter new name [{patient[1]}]: ")
    new_age = input(f"Enter new age [{patient[2]}]: ")
    new_disease = input(f"Enter new disease [{patient[3]}]: ")

    name = new_name if new_name else patient[1]
    age = int(new_age) if new_age else patient[2]
    disease = new_disease if new_disease else patient[3]

    cursor.execute("""
        UPDATE patients
        SET name = ?, age = ?, disease = ?
        WHERE id = ?
    """, (name, age, disease, patient_id))
    conn.commit()

    print("\nPatient updated successfully!\n")


def delete_patient():
    print("\n========== DELETE PATIENT ==========\n")
    patient_id = input("Enter patient ID: ")

    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()

    if not patient:
        print("\nPatient not found!\n")
        return

    confirm = input("Are you sure you want to delete this patient? (y/n): ")
    if confirm.lower() == "y":
        cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
        conn.commit()
        print("\nPatient deleted successfully!\n")
    else:
        print("\nDelete cancelled.\n")


# -----------------------------
# Appointment functions
# -----------------------------
def add_appointment():
    print("\n========== BOOK APPOINTMENT ==========\n")

    patient_id = input("Enter patient ID: ")
    doctor_name = input("Enter doctor name: ")
    appointment_date = input("Enter appointment date (YYYY-MM-DD): ")
    appointment_time = input("Enter appointment time (HH:MM): ")

    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    patient = cursor.fetchone()

    if not patient:
        print("\nPatient not found! Please add the patient first.\n")
        return

    cursor.execute("""
        INSERT INTO appointments(patient_id, doctor_name, appointment_date, appointment_time)
        VALUES (?, ?, ?, ?)
    """, (patient_id, doctor_name, appointment_date, appointment_time))
    conn.commit()

    print("\nAppointment booked successfully!\n")


def view_appointments():
    print("\n========== APPOINTMENT LIST ==========\n")

    cursor.execute("""
        SELECT appointments.id, patients.name, appointments.doctor_name,
               appointments.appointment_date, appointments.appointment_time
        FROM appointments
        JOIN patients ON appointments.patient_id = patients.id
    """)

    data = cursor.fetchall()

    if not data:
        print("No appointments found.\n")
        return

    print("ID\tPatient Name\tDoctor\t\tDate\t\tTime")
    print("-------------------------------------------------------------")
    for appt in data:
        print(f"{appt[0]}\t{appt[1]}\t\t{appt[2]}\t\t{appt[3]}\t{appt[4]}")
    print()


def cancel_appointment():
    print("\n========== CANCEL APPOINTMENT ==========\n")

    appointment_id = input("Enter appointment ID: ")

    cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
    appointment = cursor.fetchone()

    if not appointment:
        print("\nAppointment not found!\n")
        return

    confirm = input("Are you sure you want to cancel this appointment? (y/n): ")
    if confirm.lower() == "y":
        cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        conn.commit()
        print("\nAppointment cancelled successfully!\n")
    else:
        print("\nCancelled.\n")


# -----------------------------
# Role menus
# -----------------------------
def admin_menu():
    while True:
        print("\n========== ADMIN MENU ==========\n")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Delete Patient")
        print("6. Book Appointment")
        print("7. View Appointments")
        print("8. Cancel Appointment")
        print("9. Back to Main Menu\n")

        choice = input("Enter choice: ")

        if choice == "1":
            add_patient()
        elif choice == "2":
            view_patients()
        elif choice == "3":
            search_patient()
        elif choice == "4":
            update_patient()
        elif choice == "5":
            delete_patient()
        elif choice == "6":
            add_appointment()
        elif choice == "7":
            view_appointments()
        elif choice == "8":
            cancel_appointment()
        elif choice == "9":
            break
        else:
            print("\nInvalid choice!\n")


def doctor_menu():
    while True:
        print("\n========== DOCTOR MENU ==========\n")
        print("1. View Patients")
        print("2. View Appointments")
        print("3. Search Patient")
        print("4. Back to Main Menu\n")

        choice = input("Enter choice: ")

        if choice == "1":
            view_patients()
        elif choice == "2":
            view_appointments()
        elif choice == "3":
            search_patient()
        elif choice == "4":
            break
        else:
            print("\nInvalid choice!\n")


def patient_menu():
    while True:
        print("\n========== PATIENT MENU ==========\n")
        print("1. Book Appointment")
        print("2. View Appointments")
        print("3. Cancel Appointment")
        print("4. Back to Main Menu\n")

        choice = input("Enter choice: ")

        if choice == "1":
            add_appointment()
        elif choice == "2":
            view_appointments()
        elif choice == "3":
            cancel_appointment()
        elif choice == "4":
            break
        else:
            print("\nInvalid choice!\n")


# -----------------------------
# Main menu
# -----------------------------
while True:
    print("=====================================")
    print("    HOSPITAL MANAGEMENT SYSTEM")
    print("=====================================\n")
    print("1. Admin")
    print("2. Doctor")
    print("3. Patient")
    print("4. Exit\n")

    role = input("Choose Role : ")

    if role == "1":
        admin_menu()
    elif role == "2":
        doctor_menu()
    elif role == "3":
        patient_menu()
    elif role == "4":
        print("\nThank you!")
        break
    else:
        print("\nInvalid choice!\n")

conn.close()