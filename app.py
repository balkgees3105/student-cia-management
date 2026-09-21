from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "student.db"


# ==================================================
# DATABASE CONNECTION
# ==================================================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==================================================
# CREATE TABLES
# ==================================================

def create_tables():

    conn = get_db_connection()
    cursor = conn.cursor()

    # ------------------------------------------------
    # STUDENT PERSONAL INFORMATION TABLE
    # ------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            register_no TEXT UNIQUE NOT NULL,
            student_name TEXT,
            father_name TEXT,
            father_contact TEXT,
            mother_name TEXT,
            mother_contact TEXT,
            gender TEXT,
            dob TEXT,
            student_contact TEXT,
            student_address TEXT,
            school_address TEXT,
            taluk TEXT,
            district TEXT,
            caste TEXT,
            community TEXT,
            twelth_mark TEXT,
            medium TEXT,
            pudhumai_penn TEXT
        )
    """)

    # ------------------------------------------------
    # ACADEMIC MARKS TABLE
    # ------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS academic_marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            register_no TEXT NOT NULL,
            semester INTEGER NOT NULL,
            subject_code TEXT NOT NULL,
            subject_name TEXT NOT NULL,
            cia1 TEXT,
            cia2 TEXT,
            model_mark TEXT,
            attendance TEXT,
            semester_exam TEXT,
            UNIQUE(register_no, semester, subject_code)
        )
    """)

    conn.commit()
    conn.close()


# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def home():

    return render_template("index.html")


# ==================================================
# ADD STUDENT PAGE
# ==================================================

@app.route("/add_student")
def add_student():

    return render_template("student_form.html")


# ==================================================
# SAVE STUDENT
# ==================================================

@app.route("/save_student", methods=["POST"])
def save_student():

    register_no = request.form.get("register_no", "").strip()
    student_name = request.form.get("student_name", "").strip()
    father_name = request.form.get("father_name", "").strip()
    father_contact = request.form.get("father_contact", "").strip()
    mother_name = request.form.get("mother_name", "").strip()
    mother_contact = request.form.get("mother_contact", "").strip()
    gender = request.form.get("gender", "").strip()
    dob = request.form.get("dob", "").strip()
    student_contact = request.form.get("student_contact", "").strip()
    student_address = request.form.get("student_address", "").strip()
    school_address = request.form.get("school_address", "").strip()
    taluk = request.form.get("taluk", "").strip()
    district = request.form.get("district", "").strip()
    caste = request.form.get("caste", "").strip()
    community = request.form.get("community", "").strip()
    twelth_mark = request.form.get("twelth_mark", "").strip()
    medium = request.form.get("medium", "").strip()
    pudhumai_penn = request.form.get("pudhumai_penn", "").strip()

    conn = get_db_connection()

    try:

        conn.execute("""
            INSERT INTO students (
                register_no,
                student_name,
                father_name,
                father_contact,
                mother_name,
                mother_contact,
                gender,
                dob,
                student_contact,
                student_address,
                school_address,
                taluk,
                district,
                caste,
                community,
                twelth_mark,
                medium,
                pudhumai_penn
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            register_no,
            student_name,
            father_name,
            father_contact,
            mother_name,
            mother_contact,
            gender,
            dob,
            student_contact,
            student_address,
            school_address,
            taluk,
            district,
            caste,
            community,
            twelth_mark,
            medium,
            pudhumai_penn
        ))

        conn.commit()
        conn.close()

        return render_template(
            "success.html",
            message="Student information saved successfully!"
        )

    except sqlite3.IntegrityError:

        conn.close()

        return render_template(
            "success.html",
            message="Register number already exists!"
        )


# ==================================================
# SAVED STUDENTS PAGE
# ==================================================

@app.route("/students")
def students():

    conn = get_db_connection()

    students = conn.execute("""
        SELECT *
        FROM students
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=students
    )


# ==================================================
# SEARCH STUDENT
# ==================================================

@app.route("/search", methods=["POST"])
def search():

    register_no = request.form.get("register_no", "").strip()

    if not register_no:

        return render_template(
            "success.html",
            message="Please enter a Register Number!"
        )

    conn = get_db_connection()

    # Get student

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE UPPER(TRIM(register_no)) = UPPER(TRIM(?))
    """, (register_no,)).fetchone()

    if student:

        # Get academic marks

        academic_marks = conn.execute("""
            SELECT *
            FROM academic_marks
            WHERE UPPER(TRIM(register_no)) = UPPER(TRIM(?))
            ORDER BY semester ASC, id ASC
        """, (student["register_no"],)).fetchall()

        conn.close()

        student_data = {

            "Register No":
                student["register_no"],

            "Student Name":
                student["student_name"],

            "Father Name":
                student["father_name"],

            "Father Contact":
                student["father_contact"],

            "Mother Name":
                student["mother_name"],

            "Mother Contact":
                student["mother_contact"],

            "Gender":
                student["gender"],

            "Date of Birth":
                student["dob"],

            "Student Contact":
                student["student_contact"],

            "Student Address":
                student["student_address"],

            "School Address":
                student["school_address"],

            "Taluk":
                student["taluk"],

            "District":
                student["district"],

            "Caste":
                student["caste"],

            "Community":
                student["community"],

            "Twelth Mark":
                student["twelth_mark"],

            "Medium 6 to 12":
                student["medium"],

            "Pudhumai Penn Scheme":
                student["pudhumai_penn"]
        }

        return render_template(
            "student_details.html",
            student=student_data,
            academic_marks=academic_marks
        )

    conn.close()

    return render_template(
        "success.html",
        message="Student not found!"
    )


# ==================================================
# EDIT STUDENT PAGE
# ==================================================

@app.route("/edit_student/<int:student_id>")
def edit_student(student_id):

    conn = get_db_connection()

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE id = ?
    """, (student_id,)).fetchone()

    conn.close()

    if student:

        return render_template(
            "edit_student.html",
            student=student
        )

    return render_template(
        "success.html",
        message="Student not found!"
    )


# ==================================================
# UPDATE STUDENT
# ==================================================

@app.route("/update_student/<int:student_id>", methods=["POST"])
def update_student(student_id):

    register_no = request.form.get("register_no", "").strip()
    student_name = request.form.get("student_name", "").strip()
    father_name = request.form.get("father_name", "").strip()
    father_contact = request.form.get("father_contact", "").strip()
    mother_name = request.form.get("mother_name", "").strip()
    mother_contact = request.form.get("mother_contact", "").strip()
    gender = request.form.get("gender", "").strip()
    dob = request.form.get("dob", "").strip()
    student_contact = request.form.get("student_contact", "").strip()
    student_address = request.form.get("student_address", "").strip()
    school_address = request.form.get("school_address", "").strip()
    taluk = request.form.get("taluk", "").strip()
    district = request.form.get("district", "").strip()
    caste = request.form.get("caste", "").strip()
    community = request.form.get("community", "").strip()
    twelth_mark = request.form.get("twelth_mark", "").strip()
    medium = request.form.get("medium", "").strip()
    pudhumai_penn = request.form.get("pudhumai_penn", "").strip()

    conn = get_db_connection()

    try:

        old_student = conn.execute("""
            SELECT register_no
            FROM students
            WHERE id = ?
        """, (student_id,)).fetchone()

        if not old_student:

            conn.close()

            return render_template(
                "success.html",
                message="Student not found!"
            )

        old_register_no = old_student["register_no"]

        conn.execute("""
            UPDATE students
            SET
                register_no = ?,
                student_name = ?,
                father_name = ?,
                father_contact = ?,
                mother_name = ?,
                mother_contact = ?,
                gender = ?,
                dob = ?,
                student_contact = ?,
                student_address = ?,
                school_address = ?,
                taluk = ?,
                district = ?,
                caste = ?,
                community = ?,
                twelth_mark = ?,
                medium = ?,
                pudhumai_penn = ?
            WHERE id = ?
        """, (
            register_no,
            student_name,
            father_name,
            father_contact,
            mother_name,
            mother_contact,
            gender,
            dob,
            student_contact,
            student_address,
            school_address,
            taluk,
            district,
            caste,
            community,
            twelth_mark,
            medium,
            pudhumai_penn,
            student_id
        ))

        # If register number changes,
        # update academic marks also.

        if old_register_no != register_no:

            conn.execute("""
                UPDATE academic_marks
                SET register_no = ?
                WHERE UPPER(TRIM(register_no))
                      = UPPER(TRIM(?))
            """, (
                register_no,
                old_register_no
            ))

        conn.commit()
        conn.close()

        return render_template(
            "success.html",
            message="Student information updated successfully!"
        )

    except sqlite3.IntegrityError:

        conn.close()

        return render_template(
            "success.html",
            message="Register number already exists!"
        )


# ==================================================
# ACADEMIC MARKS ENTRY PAGE
# ==================================================

@app.route("/academic_marks/<register_no>")
def academic_marks(register_no):

    conn = get_db_connection()

    # Get student

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE UPPER(TRIM(register_no))
              = UPPER(TRIM(?))
    """, (register_no,)).fetchone()

    # Get saved academic marks
    #
    # IMPORTANT:
    # SELECT * includes the "id" field.
    # This id is required for the Edit button.

    marks = conn.execute("""
        SELECT *
        FROM academic_marks
        WHERE UPPER(TRIM(register_no))
              = UPPER(TRIM(?))
        ORDER BY semester ASC, id ASC
    """, (register_no,)).fetchall()

    conn.close()

    if not student:

        return render_template(
            "success.html",
            message="Student not found!"
        )

    return render_template(
        "academic_marks.html",
        student=student,
        marks=marks
    )


# ==================================================
# SAVE ACADEMIC MARKS
# ==================================================

@app.route("/save_academic_marks", methods=["POST"])
def save_academic_marks():

    register_no = request.form.get("register_no", "").strip()
    semester = request.form.get("semester", "").strip()
    subject_code = request.form.get("subject_code", "").strip()
    subject_name = request.form.get("subject_name", "").strip()
    cia1 = request.form.get("cia1", "").strip()
    cia2 = request.form.get("cia2", "").strip()
    model_mark = request.form.get("model_mark", "").strip()
    attendance = request.form.get("attendance", "").strip()
    semester_exam = request.form.get("semester_exam", "").strip()

    conn = get_db_connection()

    # Check student

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE UPPER(TRIM(register_no))
              = UPPER(TRIM(?))
    """, (register_no,)).fetchone()

    if not student:

        conn.close()

        return render_template(
            "success.html",
            message="Student not found!"
        )

    try:

        # Check whether same mark already exists

        existing = conn.execute("""
            SELECT id
            FROM academic_marks
            WHERE UPPER(TRIM(register_no))
                  = UPPER(TRIM(?))
              AND semester = ?
              AND UPPER(TRIM(subject_code))
                  = UPPER(TRIM(?))
        """, (
            register_no,
            semester,
            subject_code
        )).fetchone()

        # ------------------------------------------------
        # UPDATE EXISTING RECORD
        # ------------------------------------------------

        if existing:

            conn.execute("""
                UPDATE academic_marks
                SET
                    subject_name = ?,
                    cia1 = ?,
                    cia2 = ?,
                    model_mark = ?,
                    attendance = ?,
                    semester_exam = ?
                WHERE id = ?
            """, (
                subject_name,
                cia1,
                cia2,
                model_mark,
                attendance,
                semester_exam,
                existing["id"]
            ))

            message = "Academic marks updated successfully!"

        # ------------------------------------------------
        # INSERT NEW RECORD
        # ------------------------------------------------

        else:

            conn.execute("""
                INSERT INTO academic_marks (
                    register_no,
                    semester,
                    subject_code,
                    subject_name,
                    cia1,
                    cia2,
                    model_mark,
                    attendance,
                    semester_exam
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                register_no,
                semester,
                subject_code,
                subject_name,
                cia1,
                cia2,
                model_mark,
                attendance,
                semester_exam
            ))

            message = "Academic marks saved successfully!"

        conn.commit()
        conn.close()

        return render_template(
            "success.html",
            message=message
        )

    except Exception as e:

        conn.close()

        return render_template(
            "success.html",
            message="Error saving marks: " + str(e)
        )


# ==================================================
# EDIT ACADEMIC MARKS PAGE
# ==================================================

@app.route("/edit_academic_marks/<int:mark_id>")
def edit_academic_marks(mark_id):

    conn = get_db_connection()

    mark = conn.execute("""
        SELECT *
        FROM academic_marks
        WHERE id = ?
    """, (mark_id,)).fetchone()

    conn.close()

    if not mark:

        return render_template(
            "success.html",
            message="Academic mark record not found!"
        )

    return render_template(
        "mark_edit.html",
        mark=mark
    )


# ==================================================
# UPDATE ACADEMIC MARKS
# ==================================================

@app.route("/update_academic_marks/<int:mark_id>", methods=["POST"])
def update_academic_marks(mark_id):

    register_no = request.form.get("register_no", "").strip()
    semester = request.form.get("semester", "").strip()
    subject_code = request.form.get("subject_code", "").strip()
    subject_name = request.form.get("subject_name", "").strip()
    cia1 = request.form.get("cia1", "").strip()
    cia2 = request.form.get("cia2", "").strip()
    model_mark = request.form.get("model_mark", "").strip()
    attendance = request.form.get("attendance", "").strip()
    semester_exam = request.form.get("semester_exam", "").strip()

    conn = get_db_connection()

    try:

        # ------------------------------------------------
        # CHECK RECORD EXISTS
        # ------------------------------------------------

        existing = conn.execute("""
            SELECT *
            FROM academic_marks
            WHERE id = ?
        """, (mark_id,)).fetchone()

        if not existing:

            conn.close()

            return render_template(
                "success.html",
                message="Academic mark record not found!"
            )

        # ------------------------------------------------
        # CHECK DUPLICATE
        # ------------------------------------------------

        duplicate = conn.execute("""
            SELECT id
            FROM academic_marks
            WHERE UPPER(TRIM(register_no))
                  = UPPER(TRIM(?))
              AND semester = ?
              AND UPPER(TRIM(subject_code))
                  = UPPER(TRIM(?))
              AND id != ?
        """, (
            register_no,
            semester,
            subject_code,
            mark_id
        )).fetchone()

        if duplicate:

            conn.close()

            return render_template(
                "success.html",
                message="Another mark record already exists for this semester and subject code!"
            )

        # ------------------------------------------------
        # UPDATE MARKS
        # ------------------------------------------------

        conn.execute("""
            UPDATE academic_marks
            SET
                register_no = ?,
                semester = ?,
                subject_code = ?,
                subject_name = ?,
                cia1 = ?,
                cia2 = ?,
                model_mark = ?,
                attendance = ?,
                semester_exam = ?
            WHERE id = ?
        """, (
            register_no,
            semester,
            subject_code,
            subject_name,
            cia1,
            cia2,
            model_mark,
            attendance,
            semester_exam,
            mark_id
        ))

        conn.commit()
        conn.close()

        # After update, go back to academic marks page

        return redirect(
            url_for(
                "academic_marks",
                register_no=register_no
            )
        )

    except Exception as e:

        conn.close()

        return render_template(
            "success.html",
            message="Error updating marks: " + str(e)
        )


# ==================================================
# VIEW ACADEMIC MARKS / RESULT
# ==================================================

@app.route("/view_marks/<register_no>")
def view_marks(register_no):

    conn = get_db_connection()

    # Get student

    student = conn.execute("""
        SELECT *
        FROM students
        WHERE UPPER(TRIM(register_no))
              = UPPER(TRIM(?))
    """, (register_no,)).fetchone()

    # Get academic marks

    academic_marks = conn.execute("""
        SELECT *
        FROM academic_marks
        WHERE UPPER(TRIM(register_no))
              = UPPER(TRIM(?))
        ORDER BY semester ASC, id ASC
    """, (register_no,)).fetchall()

    conn.close()

    if not student:

        return render_template(
            "success.html",
            message="Student not found!"
        )

    return render_template(
        "academic_result.html",
        student=student,
        academic_marks=academic_marks
    )


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":

    create_tables()

    app.run(debug=True)