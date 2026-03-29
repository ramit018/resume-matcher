import pdfplumber
import docx
import re

def extract_text(file_path):
    text = ""
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    return text

SKILLS_DB = [
    "python", "java", "javascript", "react", "node.js", "sql", "mysql",
    "postgresql", "mongodb", "html", "css", "machine learning", "deep learning",
    "data analysis", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "docker", "kubernetes", "aws", "azure", "git", "linux", "fastapi", "flask",
    "django", "c++", "c#", "kotlin", "swift", "flutter", "excel", "power bi",
    "tableau", "communication", "leadership", "teamwork", "problem solving"
]

def extract_skills(text):
    text_lower = text.lower()
    found_skills = []
    for skill in SKILLS_DB:
        if skill in text_lower:
            found_skills.append(skill)
    return found_skills

def extract_email(text):
    match = re.search(r'[\w.-]+@[\w.-]+\.\w+', text)
    return match.group(0) if match else "Not found"

def extract_name(text):
    lines = text.strip().split('\n')
    for line in lines[:5]:
        line = line.strip()
        if len(line) > 2 and len(line) < 40:
            return line
    return "Not found"

def parse_resume(file_path):
    text = extract_text(file_path)
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "skills": extract_skills(text),
        "raw_text": text
    }