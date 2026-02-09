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
    list_display=(
        'title',
        'experience_level',
        'role_type',
        'created_at'
    )
    list_filter=(
        'experience_level',
        'role_type',
        'created_at',
    )
    search_fields=(
        'title',
        'description',    
    )
    ordering=['-created_at']
    filter_horizontal=('required_skills',)
    list_per_page=10
    def skills_required(self,obj):
        return obj.required_skills.count()
    skills_required.short_description='Skills Required'
    
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display=('user','uploaded_at')
    def resume_match_count(self,obj):
        return Resume.objects.filter(
            extracted_skills__icontains=obj.title.lower()
        ).count()
    resume_match_count.short_description="Matched Resumes"