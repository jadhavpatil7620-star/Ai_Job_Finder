from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Resume,Skill

@staff_member_required
def analytics_view(request):
    total_resumes=Resume.objects.count()
    total_skills=Skill.objects.count()
    
    skill_usages={}
    for skill in Skill.objects.all():
        count=Resume.objects.filter(extracted_skills__icontains=skill.name).count()
        skill_usages[skill.name]=count
        
    return render(request,'resume/admin_analytics.html',{
        'total_resumes':total_resumes,
        'total_skills':total_skills,
        'skill_usages':skill_usages
    })