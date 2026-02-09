from django.shortcuts import render,redirect
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from resume.models import Resume
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from resume.models import Resume,Job,Skill
from resume.matcher import calculate_job_match
from django.contrib import messages

# Create your views here.
def register_view(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        form=RegisterForm()
    return render(request,'users/register.html',{'form':form})

def login_view(request):
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request,"Invalid username or password")
    else:
        form=AuthenticationForm()
    return render(request,'users/login.html',{'form':form})
    
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    resume=Resume.objects.filter(user=request.user).last()
    job_matches=[]
    
    if resume and resume.extracted_skills:
        resume_skills=[s.strip().lower() for s in resume.extracted_skills.split(',')]
        
        for job in Job.objects.all():
            match_percentege,matched_skills,missing_skills=calculate_job_match(resume_skills,job)
            if match_percentege>0:
                job_matches.append({
                    'job':job,
                    'match':match_percentege,
                    'matched_skills':matched_skills,
                    'missing_skills':missing_skills,
                })
                
        job_matches.sort(key=lambda x:x['match'],reverse=True)
    categarized_skill={
        'Programing Language':[],
        'Framework':[],
        'Database':[],
        'Tool':[],
    }
    db_skills=Skill.objects.none()
    if resume and resume.extracted_skills:
        resume_skills_names=[s.strip().lower() for s in resume.extracted_skills.split(',')]
        db_skills=Skill.objects.filter(name__in=resume_skills_names)
        
    for skill in db_skills:
        if skill.category_choice=='language':
            categarized_skill['Programing Language'].append(skill.name)
        elif skill.category_choice=='framework':
            categarized_skill['Framework'].append(skill.name)
        elif skill.category_choice=='database':
            categarized_skill['Database'].append(skill.name)
        elif skill.category_choice=='tool':
            categarized_skill['Tool'].append(skill.name)
    return render(request,'dashboard.html',{
        'resume':resume,
        'job_matches':job_matches,
        'categarized_skill':categarized_skill
    })

@staff_member_required
def admin_dashboard(request):
    context={
        'total_users':User.objects.count(),
        'total_resumes':Resume.objects.count(),
        'total_jobs':Job.objects.count(),
        'total_skills':Skill.objects.count(),
        'recent_users':User.objects.order_by('-date_joined')[:5],
        'recent_jobs':Job.objects.order_by('-created_at')[:5]
    }
    return render(request,'admin_dashboard.html',context)