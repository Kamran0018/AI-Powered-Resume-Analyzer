from django import forms
from .models import Resume

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter resume title'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.docx'}),
        }
    
    def clean_file(self):
        file = self.cleaned_data['file']
        allowed_extensions = ['.pdf', '.docx']
        ext = '.' + file.name.split('.')[-1].lower()
        
        if ext not in allowed_extensions:
            raise forms.ValidationError('Only PDF and DOCX files are allowed.')
        
        if file.size > 5 * 1024 * 1024:  # 5MB limit
            raise forms.ValidationError('File size must be less than 5MB.')
        
        return file