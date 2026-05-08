from django.db import models
from analyzer.models import Resume

class Recommendation(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='recommendation')
    english_recommendation = models.TextField()
    hindi_recommendation = models.TextField()
    missing_skills = models.JSONField(default=list)
    suggested_certifications = models.JSONField(default=list)
    suggested_projects = models.JSONField(default=list)
    career_improvements = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Recommendations for {self.resume.title}"

class VoiceFeedback(models.Model):
    recommendation = models.OneToOneField(Recommendation, on_delete=models.CASCADE, related_name='voice')
    english_audio = models.FileField(upload_to='audio/english/', blank=True)
    hindi_audio = models.FileField(upload_to='audio/hindi/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Voice feedback for {self.recommendation.resume.title}"

class JobMatch(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='job_matches')
    job_description = models.TextField()
    match_percentage = models.FloatField(default=0)
    missing_keywords = models.JSONField(default=list)
    matched_keywords = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Job match {self.match_percentage}% for {self.resume.title}"