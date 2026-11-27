
import os
import re
import json
import fitz


# ==========================================
# STEP 1: CONFIGURATION
# ==========================================

RESUME_FOLDER = "resumes"

PROMPT_VERSION = "1.0"


# ==========================================
# STEP 2: JSON SCHEMA
# ==========================================

JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "candidate_name": {
            "type": ["string", "null"]
        },
        "skills": {
            "type": "array",
            "items": {"type": "string"}
        },
        "years_of_experience": {
            "type": ["number", "null"]
        },
        "education": {
            "type": "array",
            "items": {"type": "string"}
        },
        "strengths": {
            "type": "array",
            "items": {"type": "string"}
        },
        "gaps": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": [
        "candidate_name",
        "skills",
        "years_of_experience",
        "education",
        "strengths",
        "gaps"
    ],
    "additionalProperties": False
}


# ==========================================
# STEP 3: READ RESUME
# ==========================================

def read_resume(path):

    extension = os.path.splitext(path)[1].lower()

    try:

        if extension == ".pdf":

            document = fitz.open(path)

            text = ""

            for page in document:
                text += page.get_text() + "\n"

            document.close()

        elif extension == ".txt":

            with open(
                path,
                "r",
                encoding="utf-8"
            ) as file:

                text = file.read()

        else:

            return None

        if not text.strip():
            return None

        return clean_text(text)

    except Exception as error:

        print("Reading error:", error)
        return None


# ==========================================
# STEP 4: CLEAN TEXT
# ==========================================

def clean_text(text):

    text = re.sub(
        r"(?im)^\s*RESUME\s*$",
        "",
        text
    )

    text = re.sub(
        r"(?im)^\s*Page\s+\d+\s*$",
        "",
        text
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n\s*\n+",
        "\n",
        text
    )

    return text.strip()


# ==========================================
# STEP 5: EXTRACT SECTION
# ==========================================

def get_section(text, section_name):

    lines = text.splitlines()

    capture = False
    result = []

    headings = [
        "skills:",
        "education:",
        "experience:",
        "projects:",
        "certifications:",
        "strengths:",
        "gaps:"
    ]

    for line in lines:

        line = line.strip()

        if line.lower() == section_name.lower() + ":":
            capture = True
            continue

        if capture:

            if any(
                line.lower().startswith(h)
                for h in headings
            ):
                break

            if line:
                result.append(line)

    return result


# ==========================================
# STEP 6: EXTRACT CANDIDATE NAME
# ==========================================

def extract_name(text):

    for line in text.splitlines():

        line = line.strip()

        if line and line.upper() != "RESUME":

            if not line.lower().startswith(
                ("email:", "phone:", "skills:")
            ):
                return line

    return None


# ==========================================
# STEP 7: EXTRACT SKILLS
# ==========================================

def extract_skills(text):

    section = get_section(text, "Skills")

    skills = []

    for line in section:

        items = line.split(",")

        for item in items:

            item = item.strip()

            if item and item not in skills:
                skills.append(item)

    return skills


# ==========================================
# STEP 8: EXTRACT EXPERIENCE
# ==========================================

def extract_experience(text):

    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s+years?\s+experience",
        text,
        re.IGNORECASE
    )

    if not matches:
        return None

    return max(float(value) for value in matches)


# ==========================================
# STEP 9: EXTRACT EDUCATION
# ==========================================

def extract_education(text):

    return get_section(text, "Education")


# ==========================================
# STEP 10: EXTRACT STRENGTHS
# ==========================================

def extract_strengths(text):

    experience = get_section(text, "Experience")

    return [
        line for line in experience
        if line
    ]


# ==========================================
# STEP 11: EXTRACT GAPS
# ==========================================

def extract_gaps(text):

    return get_section(text, "Gaps")


# ==========================================
# STEP 12: JSON EXTRACTION
# ==========================================

def extract_resume_data(text):

    result = {

        "candidate_name": extract_name(text),

        "skills": extract_skills(text),

        "years_of_experience": extract_experience(text),

        "education": extract_education(text),

        "strengths": extract_strengths(text),

        "gaps": extract_gaps(text)

    }

    return result


# ==========================================
# STEP 13: VALIDATE JSON SCHEMA
# ==========================================

def validate_schema(data):

    required_fields = JSON_SCHEMA["required"]

    if set(data.keys()) != set(required_fields):
        return False

    if data["candidate_name"] is not None:
        if not isinstance(data["candidate_name"], str):
            return False

    if data["years_of_experience"] is not None:
        if not isinstance(
            data["years_of_experience"],
            (int, float)
        ):
            return False

    for field in [
        "skills",
        "education",
        "strengths",
        "gaps"
    ]:

        if not isinstance(data[field], list):
            return False

        if not all(
            isinstance(item, str)
            for item in data[field]
        ):
            return False

    return True


# ==========================================
# STEP 14: MANUAL VERIFICATION
# ==========================================

expected_results = {

    "resume_01.pdf": {
        "candidate_name": "John Smith",
        "skills": [
            "Python", "Django", "Flask",
            "SQL", "HTML", "CSS"
        ],
        "years_of_experience": 2,
        "education": [
            "B.Tech Computer Science, 2023"
        ]
    },

    "resume_02.pdf": {
        "candidate_name": "Priya Sharma",
        "skills": [
            "Python", "SQL", "Excel",
            "Power BI", "Tableau"
        ],
        "years_of_experience": 3,
        "education": [
            "B.Tech Information Technology, 2022"
        ]
    },

    "resume_03.pdf": {
        "candidate_name": "Rahul Kumar",
        "skills": [
            "Java", "Spring Boot",
            "MySQL", "REST API"
        ],
        "years_of_experience": 4,
        "education": [
            "B.Tech Computer Science, 2021"
        ]
    }
}


# ==========================================
# STEP 15: PROCESS ALL 8 RESUMES
# ==========================================

print("\n========== RESUME EXTRACTION ==========\n")

manual_errors = 0

for filename in sorted(os.listdir(RESUME_FOLDER)):

    path = os.path.join(
        RESUME_FOLDER,
        filename
    )

    if not filename.lower().endswith(
        (".pdf", ".txt")
    ):
        continue

    text = read_resume(path)

    if text is None:

        print(filename, ": Error - no text found")
        continue

    extracted_data = extract_resume_data(text)

    if not validate_schema(extracted_data):

        print(filename, ": Schema validation failed")
        continue

    print("\nFile:", filename)

    print(
        json.dumps(
            extracted_data,
            indent=4
        )
    )

    # Save extracted JSON
    output_name = os.path.splitext(filename)[0] + ".json"

    with open(
        os.path.join(RESUME_FOLDER, output_name),
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            extracted_data,
            file,
            indent=4
        )

    # Manual verification of first 3 resumes
    if filename in expected_results:

        expected = expected_results[filename]

        for field, expected_value in expected.items():

            if extracted_data[field] != expected_value:

                manual_errors += 1

                print(
                    "Mismatch:",
                    field,
                    "Expected:",
                    expected_value,
                    "Got:",
                    extracted_data[field]
                )


# ==========================================
# STEP 16: FINAL ERROR COUNT
# ==========================================

print("\n========== MANUAL VERIFICATION ==========\n")

print("Resumes manually checked: 3")

print("Total field comparison errors:", manual_errors)

print(
    "Verification result:",
    "PASSED" if manual_errors == 0 else "FAILED"
)

print("\nPrompt version:", PROMPT_VERSION)

print("\n========== EXTRACTION COMPLETED ==========")
