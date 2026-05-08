from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Extracted data
    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    extracted_text = models.TextField(blank=True)
    
    # Skills and experience
    skills = models.JSONField(default=list)
    education = models.JSONField(default=list)
    experience = models.JSONField(default=list)
    certifications = models.JSONField(default=list)
    projects = models.JSONField(default=list)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

class ATSScore(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='ats_score')
    overall_score = models.IntegerField(default=0)
    skills_match = models.IntegerField(default=0)
    formatting_score = models.IntegerField(default=0)
    keyword_score = models.IntegerField(default=0)
    experience_score = models.IntegerField(default=0)
    education_score = models.IntegerField(default=0)
    strengths = models.JSONField(default=list)
    weaknesses = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"ATS Score: {self.overall_score} for {self.resume.title}"