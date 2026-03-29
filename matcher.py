def match_resume_to_job(resume_skills, job_description):
    job_lower = job_description.lower()
    
    SKILLS_DB = [
        "python", "java", "javascript", "react", "node.js", "sql", "mysql",
        "postgresql", "mongodb", "html", "css", "machine learning", "deep learning",
        "data analysis", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
        "docker", "kubernetes", "aws", "azure", "git", "linux", "fastapi", "flask",
        "django", "c++", "c#", "kotlin", "swift", "flutter", "excel", "power bi",
        "tableau", "communication", "leadership", "teamwork", "problem solving"
    ]
    
    job_skills = []
    for skill in SKILLS_DB:
        if skill in job_lower:
            job_skills.append(skill)
    
    if not job_skills:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "job_skills": []
        }
    
    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))
    score = int((len(matched) / len(job_skills)) * 100)
    
    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "job_skills": job_skills
    }
    