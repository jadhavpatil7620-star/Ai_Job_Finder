from django import forms
from .models import Resume

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model=Resume
        fields=['file']
        
        def clean_file(self):
            file=self.cleaned_data.get('file')
            if not file.name.endswith(('.pdf','.docx')):
                raise forms.ValidationError('Only PDF or DOCX files allowed.')
            return file