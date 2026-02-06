from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import ResumeUploadForm
from django.http import FileResponse,Http404
from .models import Resume
import os
from .utils import extract_text_from_docx,extract_text_from_pdf

# Create your views here.
@login_required
def upload_resume(request):
    if request.method=='POST':
        form=ResumeUploadForm(request.POST,request.FILES)
        if form.is_valid():
            resume=form.save(commit=False)
            resume.user=request.user
            resume.save()
            file_path=resume.file.path
            ext=os.path.splitext(file_path)[1].lower()
            
            if ext==".pdf":
                resume.extracted_text=extract_text_from_pdf(file_path)
            elif ext==".docx":
                resume.extracted_text=extract_text_from_docx(file_path)
                
            resume.save()
            return redirect('dashboard')
    else:
        form=ResumeUploadForm()
    return render(request,'resume/upload.html',{'form':form})

@login_required
def view_resume(request,resume_id):
    try:
        resume=Resume.objects.get(id=resume_id,user=request.user)
    except:
        raise Http404('Resume not found.')
    
    file_path=resume.file.path
    
    if not os.path.exists(file_path):
        raise Http404('File not found.')
    return FileResponse(open(file_path,'rb'),as_attachment=False)