# EdTech Platform

A simple online learning platform built with **Flask**, **MySQL**, and **HTML/CSS**.

---

## Features

- User registration and login
- Admin panel to add courses and lessons
- My Courses dashboard with progress tracking
- Certificate generation
- Responsive templates

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/suneeta01/edtech-platform.git
cd edtech-platform

2. Create a virtual environment and activate it:

```bash
# Windows
python -m venv myvenv
myvenv\Scripts\activate

# Mac/Linux
python -m venv myvenv
source myvenv/bin/activate

3. Install dependencies:

    pip install -r requirements.txt


### Database Setup

1. Make sure MySQL server is running.
2. Create a database named `edtech`:

```sql
CREATE DATABASE edtech;
USE edtech;

3.1 Create tables and insert sample data:

-- Users table
CREATE TABLE users(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    email VARCHAR(120) UNIQUE,
    password VARCHAR(200),
    role VARCHAR(20) DEFAULT 'student'
);

-- Courses table
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100)
);

-- Lessons table
CREATE TABLE lessons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT,
    lesson_title VARCHAR(200),
    video_url VARCHAR(300)
);

-- Enrollments table
CREATE TABLE enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100),
    course_name VARCHAR(100)
);

-- Progress table
CREATE TABLE progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100),
    lesson_id INT,
    completed BOOLEAN DEFAULT FALSE
);

### .env Setup
4. Create a .env file in the project root with  the following format (example):

    MYSQL_HOST=your_host
    MYSQL_USER=your_user_name
    MYSQL_PASSWORD=your_mysql_password
    MYSQL_DB=your_db_name
    SECRET_KEY=any_random_string

### Running the App Locally
5. Activate your virtual environment:

    # Windows
     myvenv\Scripts\activate

    # Mac/Linux
     source myvenv/bin/activate

### Run the Flask app:
6. Run the Flask app:
     python app.py
    
    Open your browser and go to: [http://127.0.0.1:5000]
    Log in or register to test the platform.
    
### GitHub Notes
7. To add your README.md to the repository:

    git add README.md
    git commit -m "Add README file"
    git push

8. Keep your .env file local and never push it to GitHub. Add this line to .gitignore:

        .env
        __pycache__/
        *.pyc


### License
9. This project is for learning purposes. You can modify and use it freely.

    It includes:  

    - All instructions for installation  
    - Database setup (optional SQL snippet)  
    - `.env` setup example  
    - Running locally  
    - GitHub instructions  
    - License   