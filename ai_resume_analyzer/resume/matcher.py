def calculate_job_match(resume_skills,job):
    job_skills=[skill.name.lower() for skill in job.required_skills.all()]
    
    if not job_skills:
        return 0,[],[]
    
    resume_skills=[s.lower() for s in resume_skills]
    
    matched=sorted(set(resume_skills).intersection(job_skills))
    missing=sorted(set(job_skills)-set(matched))
    match_percentage=int((len(matched)/len(job_skills))*100)
    
    return match_percentage,matched,missing