from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Resume(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    file=models.FileField(upload_to='resumes/')
    extracted_text=models.TextField(blank=True)
    extracted_skills=models.TextField(blank=True)
    uploaded_at=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
class Skill(models.Model):
    CATEGORY_CHOICE=[
        ('language','Programing Language'),
        ('framework','Framework'),
        ('database','Database'),
        ('tool','Tool')
    ]
    name=models.CharField(max_length=100,unique=True)
    category=models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICE
    )
    
    def __str__(self):
        return self.name
    
class Job(models.Model):
    EXPERIENCE_CHOICE=[
        ('fresher','Fresher'),
        ('junior','Junior (1-3 years)'),
        ('mid','Mid (3-5 years)'),
        ('senior','Senior (5+ years)'),
    ]
    
    ROLE_TYPE_CHOICE=[
        ('internship','Internship'),
        ('full_time','Full Time'),
        ('part_time','Part Time'),
        ('contract','Contract'),
    ]
    
    title=models.CharField(max_length=150)
    description=models.TextField()
    required_skills=models.ManyToManyField(Skill)
    
    experience_level=models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICE
    )
    
    role_type=models.CharField(
        max_length=20,
        choices=ROLE_TYPE_CHOICE
    )
    
    created_at=models.DateField(auto_now_add=True)
       
    def __str__(self):
        return self.title