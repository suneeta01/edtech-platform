from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, session, redirect
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config["MYSQL_PORT"] = 19200
app.secret_key = "your_secret_key_here"  # required for sessions

mysql = MySQL(app)


# ✅ ADD THIS RIGHT HERE
@app.route("/testdb")
def testdb():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        return f"Database connected ✅ Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

#@app.route("/")     (this code is written to check the connection to the database, you can uncomment it to test)
#def home():
   # cur = mysql.connection.cursor()
    #cur.execute("SELECT DATABASE();")
   # db = cur.fetchone()
    #return f"Connected to database: {db}"


@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password),
        )
        mysql.connection.commit()
        cur.close()

        return "User Registered Successfully!"

    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password_input = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT name, password, role FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            name, stored_password, role = user   # ✅ properly indented

            if check_password_hash(stored_password, password_input):
                session["user"] = name
                session["role"] = role.strip()  # remove any extra whitespace
                return redirect("/dashboard")
            else:
                return "Wrong Password ❌"
        else:
            return "User not found ❌"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    user_name = session.get("user")
    if user_name:
        return render_template("dashboard.html", name=user_name)
    else:
        return redirect("/login")
    


@app.route("/admin")
def admin():

    if "user" not in session:
        return redirect("/login")
    
    if session.get("role") != "admin":
        return "Access Denied"

    # 🔥 Fetch all courses
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    # ✅ Fetch lessons with course name (NEW PART)
    cursor.execute("""
    SELECT lessons.id, lessons.lesson_title, lessons.video_url, courses.course_name
    FROM lessons
    JOIN courses ON lessons.course_id = courses.id
""")
    lessons = cursor.fetchall()

    cursor.close()   # ✅ ADD THIS

    return render_template("admin.html", courses=courses, lessons=lessons) 



@app.route("/addcourse", methods=["GET","POST"])
def addcourse():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        course_name = request.form["course_name"]

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO courses (course_name) VALUES (%s)",
            (course_name,)
        )

        mysql.connection.commit()
        cur.close()

        return redirect("/courses")

    return render_template("addcourse.html")



@app.route("/addlesson", methods=["GET","POST"])
def addlesson():

    if "user" not in session:
        return redirect("/login")

    cur = mysql.connection.cursor()

    # get courses for dropdown
    cur.execute("SELECT id, course_name FROM courses")
    courses = cur.fetchall()

    if request.method == "POST":

        course_id = request.form["course_id"]
        lesson_title = request.form["lesson_title"]
        video_url = request.form["video_url"]

        cur.execute(
            "INSERT INTO lessons (course_id, lesson_title, video_url) VALUES (%s,%s,%s)",
            (course_id, lesson_title, video_url)
        )

        mysql.connection.commit()
        cur.close()

        return redirect("/admin")

    return render_template("addlesson.html", courses=courses)


@app.route("/logout")
def logout():
    session.clear()  # removes everything
    return redirect("/login")


#@app.route("/courses")
#def courses():
  #  if "user" in session:
   #     return render_template("courses.html")
 #   else:
 #       return redirect("/login")

@app.route("/courses")
def courses():
    if "user" in session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM courses")
        courses = cur.fetchall()
        cur.close()

        return render_template("courses.html", courses=courses)
    else:
        return redirect("/login")
    

@app.route("/mycourses")
def mycourses():
    if "user" not in session:
        return redirect("/login")

    user_name = session["user"]

    cur = mysql.connection.cursor()

    # Correct JOIN using course_name
    cur.execute("""
        SELECT c.id, c.course_name,
               COUNT(l.id) AS total_lessons,
               SUM(CASE WHEN p.completed = 1 THEN 1 ELSE 0 END) AS completed_lessons
        FROM courses c
        JOIN enrollments e ON c.course_name = e.course_name
        LEFT JOIN lessons l ON c.id = l.course_id
        LEFT JOIN progress p ON l.id = p.lesson_id AND p.user_name = %s
        WHERE e.user_name = %s
        GROUP BY c.id
    """, (user_name, user_name))

    courses = cur.fetchall()
    cur.close()

    return render_template("mycourses.html", courses=courses)
    

@app.route("/course/<int:course_id>")
def course_detail(course_id):

    if "user" not in session:
        return redirect("/login")

    user_name = session["user"]

    cur = mysql.connection.cursor()

    # get course name
    cur.execute("SELECT course_name FROM courses WHERE id=%s",(course_id,))
    course = cur.fetchone()


    if not course:
        cur.close()
        return "Course not found ❌"

    course_name = course[0]

    # check enrollment
    cur.execute(
        "SELECT * FROM enrollments WHERE user_name=%s AND course_name=%s",
        (user_name, course_name)
    )

    enrolled = cur.fetchone()

    if not enrolled:
        cur.close()
        return "You must enroll in this course first."

    # get lessons
    cur.execute(
        "SELECT id, lesson_title FROM lessons WHERE course_id=%s",
        (course_id,)
    )

    lessons = cur.fetchall()

    cur.execute("""
    SELECT DISTINCT progress.lesson_id
    FROM progress
    JOIN lessons ON progress.lesson_id = lessons.id
    WHERE progress.user_name = %s AND lessons.course_id = %s
    """, (user_name, course_id))

    completed_lessons = cur.fetchall()
    completed_lessons = [lesson[0] for lesson in completed_lessons]

    # progress calculation
    total_lessons = len(lessons)
    completed_count = len(completed_lessons)

    if total_lessons > 0:
        progress_percent = int((completed_count / total_lessons) * 100)
    else:
        progress_percent = 0

    cur.close()

    return render_template(
        "course_detail.html",
        course=course,
        course_id=course_id,
        lessons=lessons,
        completed_lessons=completed_lessons,
        progress_percent=progress_percent
    ) 
    

@app.route("/lesson/<int:lesson_id>")
def lesson_page(lesson_id):

    if "user" not in session:
        return redirect("/login")
    
    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT lesson_title, video_url FROM lessons WHERE id=%s",
        (lesson_id,)
    )

    lesson = cur.fetchone()
    cur.close()

    return render_template("lesson.html", lesson=lesson)


@app.route("/complete/<int:lesson_id>")
def complete_lesson(lesson_id):

    if "user" not in session:
        return redirect("/login")

    user_name = session["user"]

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM progress WHERE user_name=%s AND lesson_id=%s",
        (user_name, lesson_id)
    )

    existing = cur.fetchone()

    if not existing:
        cur.execute(
        "INSERT INTO progress (user_name, lesson_id, completed) VALUES (%s,%s,%s)",
        (user_name, lesson_id, 1)
    )

    mysql.connection.commit()

    cur.close()

    return redirect(request.referrer)



@app.route("/enroll/<int:course_id>")
def enroll(course_id):
    if "user" in session:
        user_name = session["user"]
        cur = mysql.connection.cursor()

        # Get course name from course_id
        cur.execute("SELECT course_name FROM courses WHERE id=%s", (course_id,))
        course = cur.fetchone()
        if not course:
            cur.close()
            return "Course not found ❌"

        course_name = course[0]

        # Check if already enrolled
        cur.execute(
            "SELECT * FROM enrollments WHERE user_name=%s AND course_name=%s",
            (user_name, course_name)
        )
        existing = cur.fetchone()
        if existing:
            cur.close()
            return f"You are already enrolled in {course_name}"

        # Enroll the user
        cur.execute(
            "INSERT INTO enrollments (user_name, course_name) VALUES (%s,%s)",
            (user_name, course_name)
        )
        mysql.connection.commit()
        cur.close()

        return redirect("/mycourses")
    else:
        return redirect("/login")
    


@app.route("/certificate/<int:course_id>")
def certificate(course_id):

    if "user" not in session:
        return redirect("/login")

    user_name = session["user"]

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT course_name FROM courses WHERE id=%s",
        (course_id,)
    )

    course = cur.fetchone()

    cur.close()

    return render_template(
        "certificate.html",
        user_name=user_name,
        course_name=course[0] if course else "Unknown Course"
    )


# ================= EDIT COURSE =================
@app.route("/edit_course/<int:id>", methods=["GET", "POST"])
def edit_course(id):

    if "user" not in session or session.get("role") != "admin":
        return "Access Denied"

    cur = mysql.connection.cursor()

    if request.method == "POST":
        course_name = request.form["course_name"]

        cur.execute("UPDATE courses SET course_name=%s WHERE id=%s", (course_name, id))
        mysql.connection.commit()

        return redirect("/admin")

    cur.execute("SELECT * FROM courses WHERE id=%s", (id,))
    course = cur.fetchone()

    return render_template("edit_course.html", course=course)


# ================= DELETE COURSE =================
@app.route("/delete_course/<int:id>")
def delete_course(id):

    if "user" not in session or session.get("role") != "admin":
        return "Access Denied"

    cur = mysql.connection.cursor()

    # delete lessons first
    cur.execute("DELETE FROM lessons WHERE course_id=%s", (id,))

    # delete course
    cur.execute("DELETE FROM courses WHERE id=%s", (id,))

    mysql.connection.commit()
    cur.close()

    return redirect("/admin")


@app.route('/delete_lesson/<int:id>')
def delete_lesson(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM lessons WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect('/admin')


@app.route('/edit_lesson/<int:id>', methods=['GET', 'POST'])
def edit_lesson(id):
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        lesson_title = request.form['lesson_title']
        video_url = request.form['video_url']

        cursor.execute("""
            UPDATE lessons
            SET lesson_title=%s, video_url=%s
            WHERE id=%s
        """, (lesson_title, video_url, id))

        mysql.connection.commit()
        return redirect('/admin')

    # GET request
    cursor.execute("SELECT * FROM lessons WHERE id=%s", (id,))
    lesson = cursor.fetchone()

    return render_template('edit_lesson.html', lesson=lesson)



@app.route('/create_tables')
def create_tables():
    cursor = mysql.connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(255),
        role VARCHAR(20)
    )
    """)

     # ADD ROLE COLUMN IF MISSING
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20)")
    except:
        pass  # already exists

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        course_name VARCHAR(255)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lessons (
        id INT AUTO_INCREMENT PRIMARY KEY,
        course_id INT,
        title VARCHAR(255),
        content TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        course_id INT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS progress (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        lesson_id INT,
        completed BOOLEAN DEFAULT FALSE
    )
    """)

    mysql.connection.commit()
    cursor.close()

    return "Tables updated successfully!"


@app.route('/fix_admin')
def fix_admin():
    cursor = mysql.connection.cursor()

    cursor.execute(
        "UPDATE users SET role='admin' WHERE email=%s",
        ("suneeta01@gmail.com",)
    )

    mysql.connection.commit()
    cursor.close()

    return "Done"


@app.route('/create_user')
def create_user():
    cursor = mysql.connection.cursor()

    hashed_password = generate_password_hash("2026")

    cursor.execute("""
    INSERT INTO users (name, email, password, role)
    VALUES (%s, %s, %s, %s)
    """, ("Suneeta", "suneeta01@gmail.com", hashed_password, "admin"))

    mysql.connection.commit()
    cursor.close()

    return "User created"


@app.route('/delete_user')
def delete_user():
    cursor = mysql.connection.cursor()

    cursor.execute("DELETE FROM users WHERE email=%s", ("suneeta01@gmail.com",))

    mysql.connection.commit()
    cursor.close()

    return "User deleted"


@app.route("/check_courses")
def check_courses():
    cursor = mysql.connection.cursor()
    cursor.execute("DESCRIBE courses")
    data = cursor.fetchall()
    return str(data)

if __name__ == "__main__":
    app.run(debug=True)


    

    