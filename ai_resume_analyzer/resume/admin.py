from django.contrib import admin
from .models import Resume,Job,Skill

# Register your models here.
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display=('name','category',)
    list_filter=('category',)
    search_fields=('name',)
    
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display=('title','experience_level','role_type','created_at')
    list_filter=('experience_level','role_type')
    search_fields=('title',)
    filter_horizontal=('required_skills',)
    
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display=('user','uploaded_at')