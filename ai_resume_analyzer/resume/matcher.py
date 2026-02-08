def calculate_job_match(resume_skills,job):
    job_skills=[skill.name.lower() for skill in job.required_skills.all()]
    
    if not job_skills:
        return 0
    
    matched=set(resume_skills).intersection(resume_skills)
    match_percentage=int((len(matched)/len(job_skills))*100)
    
    return match_percentage,matched