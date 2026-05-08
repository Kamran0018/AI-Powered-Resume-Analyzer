from django import forms

class JobDescriptionForm(forms.Form):
    job_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'Paste the job description here...'
        }),
        label='Job Description'
    )