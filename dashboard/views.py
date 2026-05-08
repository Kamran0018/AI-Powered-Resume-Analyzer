from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg
from analyzer.models import Resume, ATSScore
from recommendations.models import JobMatch

@login_required
def dashboard_view(request):
    user = request.user
    resumes = Resume.objects.filter(user=user)
    
    # Statistics
    total_resumes = resumes.count()
    
    # Calculate average ATS score safely
    avg_ats_score = 0
    ats_scores_list = []
    if total_resumes > 0:
        ats_scores = []
        for resume in resumes:
            if hasattr(resume, 'ats_score') and resume.ats_score:
                ats_scores.append(resume.ats_score.overall_score)
                ats_scores_list.append(resume.ats_score.overall_score)
        if ats_scores:
            avg_ats_score = sum(ats_scores) / len(ats_scores)
    
    total_job_matches = JobMatch.objects.filter(resume__in=resumes).count() if resumes.exists() else 0
    
    # Get recent resumes
    recent_resumes = resumes.order_by('-uploaded_at')[:5]
    
    # Get ATS scores for chart
    ats_scores = []
    resume_titles = []
    for resume in recent_resumes:
        if hasattr(resume, 'ats_score') and resume.ats_score:
            ats_scores.append(resume.ats_score.overall_score)
            resume_titles.append(resume.title[:20])
        else:
            ats_scores.append(0)
            resume_titles.append(resume.title[:20])
    
    # Get top skills
    all_skills = []
    for resume in resumes:
        if resume.skills:
            all_skills.extend(resume.skills)
    
    from collections import Counter
    top_skills = Counter(all_skills).most_common(10) if all_skills else []
    
    context = {
        'total_resumes': total_resumes,
        'avg_ats_score': round(avg_ats_score, 1),
        'total_job_matches': total_job_matches,
        'recent_resumes': recent_resumes,
        'ats_scores': ats_scores,
        'resume_titles': resume_titles,
        'top_skills': top_skills,
    }
    
    return render(request, 'dashboard/dashboard.html', context)