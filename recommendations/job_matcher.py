from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import Dict, List, Tuple

class JobMatcher:
    def __init__(self, resume_text: str, job_description: str):
        self.resume_text = resume_text
        self.job_description = job_description
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def extract_keywords(self, text: str) -> set:
        """Extract important keywords from text"""
        # Common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'up', 'down', 'is', 'are', 'was', 'were',
                     'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
                     'did', 'doing', 'would', 'could', 'should', 'might', 'must'}
        
        words = text.split()
        keywords = {word for word in words if len(word) > 3 and word not in stop_words}
        return keywords
    
    def calculate_similarity(self) -> float:
        """Calculate cosine similarity between resume and job description"""
        try:
            # Preprocess texts
            resume_processed = self.preprocess_text(self.resume_text)
            job_processed = self.preprocess_text(self.job_description)
            
            # Create TF-IDF vectors
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([resume_processed, job_processed])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            
            return similarity[0][0] * 100  # Convert to percentage
        
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0
    
    def find_missing_keywords(self) -> Tuple[List[str], List[str]]:
        """Find missing and matched keywords"""
        # Extract keywords from both texts
        resume_processed = self.preprocess_text(self.resume_text)
        job_processed = self.preprocess_text(self.job_description)
        
        resume_keywords = self.extract_keywords(resume_processed)
        job_keywords = self.extract_keywords(job_processed)
        
        # Find matches and missing
        matched = list(resume_keywords.intersection(job_keywords))
        missing = list(job_keywords - resume_keywords)
        
        # Sort by relevance (frequency in job description)
        missing.sort(key=lambda x: self.job_description.lower().count(x), reverse=True)
        
        return matched[:20], missing[:20]
    
    def get_match_analysis(self) -> Dict[str, any]:
        """Complete job match analysis"""
        similarity = self.calculate_similarity()
        matched_keywords, missing_keywords = self.find_missing_keywords()
        
        # Determine match level
        if similarity >= 80:
            level = "Excellent Match"
            color = "success"
        elif similarity >= 60:
            level = "Good Match"
            color = "primary"
        elif similarity >= 40:
            level = "Moderate Match"
            color = "warning"
        else:
            level = "Needs Improvement"
            color = "danger"
        
        return {
            'match_percentage': round(similarity, 2),
            'match_level': level,
            'color': color,
            'matched_keywords': matched_keywords,
            'missing_keywords': missing_keywords,
            'recommendation': self.get_recommendation(similarity, missing_keywords)
        }
    
    def get_recommendation(self, similarity: float, missing_keywords: List[str]) -> str:
        """Generate recommendation based on match analysis"""
        if similarity >= 80:
            return "Excellent match! Your resume aligns very well with this position. Consider highlighting the matched keywords in your application."
        elif similarity >= 60:
            return f"Good match. Add keywords like {', '.join(missing_keywords[:5])} to improve your chances."
        elif similarity >= 40:
            return f"Moderate match. Your resume needs significant optimization. Add keywords: {', '.join(missing_keywords[:8])}"
        else:
            return f"Your resume doesn't match well with this job. Consider updating your skills or tailoring your resume. Key missing terms: {', '.join(missing_keywords[:10])}"