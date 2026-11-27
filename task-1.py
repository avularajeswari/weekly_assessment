
import os
import re
import fitz  # PyMuPDF


# ==========================================
# STEP 1: CREATE RESUMES FOLDER
# ==========================================

RESUME_FOLDER = "resumes"

os.makedirs(RESUME_FOLDER, exist_ok=True)


# ==========================================
# STEP 2: CREATE 8 DUMMY RESUMES
# ==========================================

resume_data = {
    "resume_01": """John Smith
Python Developer

Email: john@example.com
Phone: 9876543210

Skills:
Python, Django, Flask, SQL, HTML, CSS

Education:
B.Tech Computer Science, 2023

Experience:
2 years experience in Python development.
Developed web applications using Django.
Worked with SQL databases and REST APIs.

Projects:
Employee Management System
Online Shopping Application

Certifications:
Python Programming Certification.
""",

    "resume_02": """Priya Sharma
Data Analyst

Email: priya@example.com

Skills:
Python, SQL, Excel, Power BI, Tableau

Education:
B.Tech Information Technology, 2022

Experience:
3 years experience in data analysis.
Created dashboards and reports.
Performed data cleaning and visualization.

Projects:
Sales Analysis Dashboard
Customer Data Analysis

Certifications:
Data Analytics Certification.
""",

    "resume_03": """Rahul Kumar
Java Developer

Email: rahul@example.com

Skills:
Java, Spring Boot, MySQL, REST API

Education:
B.Tech Computer Science, 2021

Experience:
4 years experience in Java development.
Built backend applications.
Developed REST APIs using Spring Boot.

Projects:
Bank Management System
Online Booking System
""",

    "resume_04": """Anita Reddy
Machine Learning Engineer

Email: anita@example.com

Skills:
Python, Machine Learning, Pandas, NumPy,
Scikit-learn, TensorFlow

Education:
M.Tech Artificial Intelligence, 2024

Experience:
2 years experience in machine learning.
Built classification and prediction models.

Projects:
House Price Prediction
Customer Churn Prediction
""",

    "resume_05": """Suresh Kumar
Frontend Developer

Skills:
HTML, CSS, JavaScript, React

Education:
B.Tech, 2022

Experience:
2 years frontend development experience.
Created responsive websites.

Projects:
Portfolio Website
E-commerce Website
""",

    "resume_06": """Meena Patel
Database Administrator

Skills:
SQL, MySQL, Oracle, PostgreSQL

Education:
B.Sc Computer Science, 2021

Experience:
3 years database administration.
Database optimization and backup.

Projects:
Database Management System
""",

    "resume_07": """Arjun Rao
Cloud Engineer

Skills:
AWS, Azure, Docker, Linux, Python

Education:
B.Tech, 2023

Experience:
2 years cloud computing experience.
Worked with cloud deployment.

Projects:
Cloud Hosting Application
""",

    "resume_08": """Sneha Verma
Software Tester

Skills:
Manual Testing, Selenium, Python, SQL

Education:
B.Tech, 2022

Experience:
2 years software testing experience.
Performed functional and automation testing.

Projects:
Web Application Testing
Mobile Application Testing
"""
}


# ==========================================
# STEP 3: GENERATE PDF AND TXT FILES
# ==========================================

for index, (name, content) in enumerate(
    resume_data.items(), start=1
):

    if index <= 4:

        # Create PDF resumes
        pdf = fitz.open()

        page = pdf.new_page()

        page.insert_text(
            (50, 50),
            "RESUME\n\n" + content,
            fontsize=11
        )

        page.insert_text(
            (250, 780),
            f"Page 1",
            fontsize=9
        )

        pdf.save(
            os.path.join(
                RESUME_FOLDER,
                name + ".pdf"
            )
        )

        pdf.close()

    else:

        # Create TXT resumes
        with open(
            os.path.join(
                RESUME_FOLDER,
                name + ".txt"
            ),
            "w",
            encoding="utf-8"
        ) as file:

            file.write("RESUME\n\n" + content)
            file.write("\nPage 1\n")


# ==========================================
# STEP 4: CREATE SCANNED PDF
# ==========================================

# This PDF contains an image instead of
# selectable text.

scanned_pdf = fitz.open()

page = scanned_pdf.new_page()

pixmap = fitz.Pixmap(
    fitz.csRGB,
    (0, 0, 400, 200),
    0
)

pixmap.clear_with(255)

page.insert_image(
    page.rect,
    pixmap=pixmap
)

scanned_pdf.save(
    os.path.join(
        RESUME_FOLDER,
        "scanned.pdf"
    )
)

scanned_pdf.close()


# ==========================================
# STEP 5: CLEAN RESUME TEXT
# ==========================================

def clean_text(text):

    # Remove common resume headers
    text = re.sub(
        r"(?im)^\s*RESUME\s*$",
        "",
        text
    )

    # Remove page numbers
    text = re.sub(
        r"(?im)^\s*page\s+\d+\s*$",
        "",
        text
    )

    # Remove extra spaces and tabs
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Remove excessive blank lines
    text = re.sub(
        r"\n\s*\n+",
        "\n",
        text
    )

    return text.strip()


# ==========================================
# STEP 6: READ RESUME
# ==========================================

def read_resume(path):

    if not os.path.exists(path):

        return None, "Error - file not found"

    extension = os.path.splitext(path)[1].lower()

    try:

        if extension == ".pdf":

            document = fitz.open(path)

            text = ""

            for page in document:

                text += page.get_text() + "\n"

            document.close()

            if not text.strip():

                return (
                    None,
                    "Error - no text found (scanned file)"
                )

        elif extension == ".txt":

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read()

        else:

            return None, "Error - unsupported file format"

        # Clean extracted text
        text = clean_text(text)

        if not text:

            return None, "Error - resume is empty"

        return text, None

    except Exception as error:

        return None, f"Error - {str(error)}"


# ==========================================
# STEP 7: COUNT CHARACTERS AND TOKENS
# ==========================================

def count_characters(text):

    return len(text)


def count_tokens(text):

    # Simple whitespace-based token count
    return len(text.split())


# ==========================================
# STEP 8: PROCESS ALL RESUMES
# ==========================================

print("\n========== AI RESUME ANALYZER ==========\n")

files = sorted(os.listdir(RESUME_FOLDER))

for filename in files:

    path = os.path.join(
        RESUME_FOLDER,
        filename
    )

    text, error = read_resume(path)

    if error:

        print(f"{filename}: {error}")

    else:

        characters = count_characters(text)

        tokens = count_tokens(text)

        print(
            f"{filename}: "
            f"{characters} characters, "
            f"{tokens} tokens"
        )

print("\n========== PROCESSING COMPLETED ==========")
