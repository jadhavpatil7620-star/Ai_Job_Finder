import re
from .models import Skill

def extract_skills_from_text(text):
    if not text:
        return []
    
    text=text.lower()
    text=re.sub(r'[^a-z0-9\s]','',text)
    
    db_skills=Skill.objects.values_list('name',flat=True)
    
    found_skills=set()
    
    for skill in db_skills:
        pattern=r'\b'+re.escape(skill.lower())+r'\b'
        if re.search(pattern,text):
            found_skills.add(skill)
            
    return sorted(found_skills)