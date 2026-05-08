from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ResumeUploadForm
from .models import Resume, ATSScore
from .resume_parser import ResumeParser
from .ats_scorer import ATSScorer
from recommendations.models import Recommendation, VoiceFeedback, JobMatch
from recommendations.ai_recommender import AIRecommender
from recommendations.voice_generator import VoiceGenerator
from recommendations.job_matcher import JobMatcher
import os
from django.conf import settings

@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            
            # Parse resume
            file_path = os.path.join(settings.MEDIA_ROOT, resume.file.name)
            parser = ResumeParser(file_path)
            parsed_data = parser.parse()
            
            # Update resume with parsed data
            resume.full_name = parsed_data['full_name']
            resume.email = parsed_data['email']
            resume.phone = parsed_data['phone']
            resume.skills = parsed_data['skills']
            resume.education = parsed_data['education']
            resume.experience = parsed_data['experience']
            resume.certifications = parsed_data['certifications']
            resume.projects = parsed_data['projects']
            resume.extracted_text = parser.text
            resume.save()
            
            # Calculate ATS score
            scorer = ATSScorer(parsed_data)
            ats_data = scorer.get_full_score()
            
            ats_score = ATSScore.objects.create(
                resume=resume,
                overall_score=ats_data['overall_score'],
                skills_match=ats_data['skills_match'],
                formatting_score=ats_data['formatting_score'],
                keyword_score=ats_data['keyword_score'],
                experience_score=ats_data['experience_score'],
                education_score=ats_data['education_score'],
                strengths=ats_data['strengths'],
                weaknesses=ats_data['weaknesses']
            )
            
            # Generate AI recommendations
            recommender = AIRecommender(parsed_data, ats_data['overall_score'])
            recommendations_data = recommender.get_full_recommendations()
            
            recommendation = Recommendation.objects.create(
                resume=resume,
                english_recommendation=recommendations_data['english_recommendation'],
                hindi_recommendation=recommendations_data['hindi_recommendation'],
                missing_skills=recommendations_data['missing_skills'],
                suggested_certifications=recommendations_data['suggested_certifications'],
                suggested_projects=recommendations_data['suggested_projects'],
                career_improvements=recommendations_data['career_improvements']
            )
            
            # Generate voice feedback
            voice_gen = VoiceGenerator()
            
            # English voice
            english_audio = voice_gen.text_to_speech_english(recommendations_data['english_recommendation'][:500])
            if english_audio:
                voice_feedback = VoiceFeedback.objects.create(
                    recommendation=recommendation
                )
                voice_feedback.english_audio.save(f'english_{resume.id}.mp3', english_audio)
                voice_feedback.save()
            
            messages.success(request, 'Resume uploaded and analyzed successfully!')
            return redirect('result', resume_id=resume.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ResumeUploadForm()
    
    return render(request, 'analyzer/upload.html', {'form': form})

@login_required
def result_view(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    context = {
        'resume': resume,
        'ats_score': resume.ats_score if hasattr(resume, 'ats_score') else None,
        'recommendation': resume.recommendation if hasattr(resume, 'recommendation') else None,
        'voice': resume.recommendation.voice if hasattr(resume, 'recommendation') and hasattr(resume.recommendation, 'voice') else None,
    }
    
    return render(request, 'analyzer/result.html', context)

@login_required
def match_job(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id, user=request.user)
    
    if request.method == 'POST':
        job_description = request.POST.get('job_description')
        
        if job_description:
            matcher = JobMatcher(resume.extracted_text, job_description)
            match_data = matcher.get_match_analysis()
            
            # Save to database
            JobMatch.objects.create(
                resume=resume,
                job_description=job_description,
                match_percentage=match_data['match_percentage'],
                missing_keywords=match_data['missing_keywords'],
                matched_keywords=match_data['matched_keywords']
            )
            
            context = {
                'resume': resume,
                'match_data': match_data
            }
            return render(request, 'analyzer/match_result.html', context)
    
    return render(request, 'analyzer/match_job.html', {'resume': resume})

@login_required
def resume_history(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'analyzer/history.html', {'resumes': resumes})