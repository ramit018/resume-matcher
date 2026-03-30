def match_resume_to_job(resume_skills, job_description):
    job_lower = job_description.lower()
    
    SKILLS_DB = [
        "python", "java", "javascript", "react", "node.js", "sql", "mysql",
        "postgresql", "mongodb", "html", "css", "machine learning", "deep learning",
        "data analysis", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
        "docker", "kubernetes", "aws", "azure", "git", "linux", "fastapi", "flask",
        "django", "c++", "c#", "kotlin", "swift", "flutter", "excel", "power bi",
        "tableau", "communication", "leadership", "teamwork", "problem solving",
        "data science", "artificial intelligence", "nlp", "computer vision",
        "rest api", "microservices", "agile", "scrum", "jira", "figma",
        "typescript", "vue", "angular", "spring", "hibernate", "redis",
        "elasticsearch", "graphql", "firebase", "gcp", "devops", "ci/cd",
        "selenium", "pytest", "junit", "maven", "gradle", "bash", "shell",
        "r", "matlab", "scala", "hadoop", "spark", "kafka", "airflow",
        "powerpoint", "word", "project management", "time management",
        "analytical", "critical thinking", "research", "presentation"
    ]
    
    job_skills = []
    for skill in SKILLS_DB:
        if skill in job_lower:
            job_skills.append(skill)
    
    resume_skills_lower = [s.lower() for s in resume_skills]
    
    if not job_skills:
        all_words = job_lower.split()
        for word in all_words:
            if len(word) > 3:
                job_skills.append(word)
    
    if not job_skills:
        return {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "job_skills": []
        }
    
    matched = []
    missing = []
    
   for skill in job_skills:
    found = False
    for r_skill in resume_skills_lower:
        if skill == r_skill or (len(skill) > 3 and skill in r_skill) or (len(r_skill) > 3 and r_skill in skill):
                found = True
                matched.append(skill)
                break
        if not found:
            missing.append(skill)
    
    matched = list(set(matched))
    missing = list(set(missing))
    
    score = int((len(matched) / len(job_skills)) * 100)
    score = max(0, min(100, score))
    
    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "job_skills": job_skills
    }
