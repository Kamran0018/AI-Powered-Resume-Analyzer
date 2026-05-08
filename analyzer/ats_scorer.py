from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class ATSScorer:
    def __init__(self, resume_data: Dict[str, Any], job_description: str = ""):
        self.resume_data = resume_data
        self.job_description = job_description
        self.score_weights = {
            'skills': 30,
            'formatting': 20,
            'keywords': 20,
            'experience': 15,
            'education': 15
        }
    
    def calculate_skills_match(self) -> int:
        """Calculate skills match score"""
        if not self.resume_data.get('skills'):
            return 0
        
        # Common in-demand skills weighting
        high_value_skills = {'python', 'java', 'javascript', 'react', 'django', 'aws', 'docker'}
        medium_value_skills = {'html', 'css', 'sql', 'git', 'rest api'}
        
        total_weight = 0
        max_weight = 100
        
        for skill in self.resume_data['skills']:
            if skill.lower() in high_value_skills:
                total_weight += 20
            elif skill.lower() in medium_value_skills:
                total_weight += 10
            else:
                total_weight += 5
        
        return min(total_weight, 100)
    
    def calculate_formatting_score(self) -> int:
        """Evaluate resume formatting"""
        score = 0
        text = ' '.join([
            ' '.join(self.resume_data.get('skills', [])),
            ' '.join([str(e) for e in self.resume_data.get('education', [])]),
            ' '.join([str(e) for e in self.resume_data.get('experience', [])])
        ])
        
        # Check for proper sections
        sections = ['skills', 'education', 'experience', 'projects']
        found_sections = sum(1 for section in sections if self.resume_data.get(section))
        score += (found_sections / len(sections)) * 40
        
        # Check for bullet points (indicating good formatting)
        bullet_count = len(re.findall(r'[•●■▪-]', text))
        score += min(bullet_count * 5, 30)
        
        # Check for length (ideal: 1-2 pages)
        word_count = len(text.split())
        if 300 <= word_count <= 800:
            score += 30
        elif 200 <= word_count <= 1000:
            score += 15
        else:
            score += 5
        
        return min(score, 100)
    
    def calculate_keyword_score(self) -> int:
        """Calculate keyword relevance"""
        if not self.job_description:
            return 70  # Default score if no job description
        
        # Extract keywords from job description
        job_keywords = set(re.findall(r'\b\w+\b', self.job_description.lower()))
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                       'of', 'with', 'by', 'from', 'up', 'down', 'is', 'are', 'was', 'were'}
        
        job_keywords = job_keywords - common_words
        job_keywords = {word for word in job_keywords if len(word) > 3}
        
        # Extract resume keywords
        resume_text = ' '.join([
            ' '.join(self.resume_data.get('skills', [])),
            ' '.join([str(e) for e in self.resume_data.get('experience', [])]),
            ' '.join(self.resume_data.get('certifications', []))
        ]).lower()
        
        resume_keywords = set(resume_text.split())
        
        # Calculate overlap
        if not job_keywords:
            return 70
        
        matched_keywords = job_keywords.intersection(resume_keywords)
        score = (len(matched_keywords) / len(job_keywords)) * 100
        
        return int(score)
    
    def calculate_experience_score(self) -> int:
        """Calculate experience relevance score"""
        experience_years = 0
        
        for exp in self.resume_data.get('experience', []):
            if isinstance(exp, dict) and 'duration' in exp:
                # Extract years from duration text
                duration = exp['duration'].lower()
                years_match = re.search(r'(\d+)', duration)
                if years_match:
                    experience_years += int(years_match.group(1))
        
        # Score based on years of experience
        if experience_years >= 5:
            return 100
        elif experience_years >= 3:
            return 80
        elif experience_years >= 1:
            return 60
        elif experience_years > 0:
            return 40
        else:
            return 20
    
    def calculate_education_score(self) -> int:
        """Calculate education score"""
        education_levels = {
            'phd': 100,
            'master': 90,
            'bachelor': 70,
            'b.tech': 70,
            'b.e': 70,
            'diploma': 50,
            'high school': 30
        }
        
        highest_level = 0
        for edu in self.resume_data.get('education', []):
            if isinstance(edu, dict):
                edu_text = edu.get('degree', '').lower()
                for level, score in education_levels.items():
                    if level in edu_text:
                        highest_level = max(highest_level, score)
        
        if highest_level == 0:
            return 40  # Default score if no education found
        
        return highest_level
    
    def calculate_overall_score(self) -> int:
        """Calculate overall ATS score"""
        scores = {
            'skills': self.calculate_skills_match(),
            'formatting': self.calculate_formatting_score(),
            'keywords': self.calculate_keyword_score(),
            'experience': self.calculate_experience_score(),
            'education': self.calculate_education_score()
        }
        
        overall = sum(scores[key] * (self.score_weights[key] / 100) for key in scores)
        
        return int(overall)
    
    def get_strengths_weaknesses(self) -> tuple:
        """Identify strengths and weaknesses"""
        strengths = []
        weaknesses = []
        
        skills_score = self.calculate_skills_match()
        if skills_score > 70:
            strengths.append("Strong technical skills portfolio")
        elif skills_score < 40:
            weaknesses.append("Limited technical skills mentioned")
        
        exp_score = self.calculate_experience_score()
        if exp_score > 70:
            strengths.append("Relevant work experience")
        elif exp_score < 40:
            weaknesses.append("Limited work experience")
        
        edu_score = self.calculate_education_score()
        if edu_score > 70:
            strengths.append("Good educational background")
        elif edu_score < 50:
            weaknesses.append("Education section needs improvement")
        
        keyword_score = self.calculate_keyword_score()
        if keyword_score > 70:
            strengths.append("Good keyword optimization")
        elif keyword_score < 50:
            weaknesses.append("Needs better keyword optimization")
        
        if len(self.resume_data.get('projects', [])) > 2:
            strengths.append("Multiple projects demonstrated")
        elif len(self.resume_data.get('projects', [])) == 0:
            weaknesses.append("No projects mentioned")
        
        if len(self.resume_data.get('certifications', [])) > 1:
            strengths.append("Relevant certifications")
        
        return strengths[:5], weaknesses[:5]
    
    def get_full_score(self) -> Dict[str, Any]:
        """Get complete ATS score report"""
        strengths, weaknesses = self.get_strengths_weaknesses()
        
        return {
            'overall_score': self.calculate_overall_score(),
            'skills_match': self.calculate_skills_match(),
            'formatting_score': self.calculate_formatting_score(),
            'keyword_score': self.calculate_keyword_score(),
            'experience_score': self.calculate_experience_score(),
            'education_score': self.calculate_education_score(),
            'strengths': strengths,
            'weaknesses': weaknesses
        }