import os
import google.generativeai as genai
from typing import Dict, Any

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class AIRecommender:
    def __init__(self, resume_data: Dict[str, Any], ats_score: int):
        self.resume_data = resume_data
        self.ats_score = ats_score
    
    def generate_english_recommendation(self) -> str:
        """Generate English recommendations using Gemini API"""
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            As an expert resume coach, analyze this resume and provide specific recommendations for improvement.
            
            RESUME DATA:
            Skills: {', '.join(self.resume_data.get('skills', []))}
            Education: {self.resume_data.get('education', [])}
            Experience: {self.resume_data.get('experience', [])}
            Certifications: {self.resume_data.get('certifications', [])}
            Projects: {self.resume_data.get('projects', [])}
            ATS Score: {self.ats_score}/100
            
            Provide recommendations in the following structure:
            
            1. SKILLS IMPROVEMENT:
            - Missing in-demand skills
            - Skills to develop
            
            2. CERTIFICATIONS SUGGESTED:
            - Recommended certifications
            
            3. PROJECT SUGGESTIONS:
            - Projects to build
            
            4. CAREER ADVICE:
            - Career path recommendations
            
            5. RESUME FORMATTING:
            - Specific formatting improvements
            
            Keep recommendations practical and actionable. Be concise but detailed.
            """
            
            response = model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return self.get_fallback_recommendation()
    
    def generate_hindi_recommendation(self) -> str:
        """Generate Hindi recommendations"""
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            As an expert resume coach, provide recommendations in Hindi language.
            
            RESUME DATA:
            Skills: {', '.join(self.resume_data.get('skills', []))}
            ATS Score: {self.ats_score}/100
            
            Provide recommendations in Hindi with these sections:
            1. कौशल सुधार (Skills Improvement)
            2. प्रमाणपत्र सुझाव (Certifications Suggested)
            3. परियोजना सुझाव (Project Suggestions)
            4. करियर सलाह (Career Advice)
            5. रिज्यूमे फॉर्मेटिंग (Resume Formatting)
            
            Write in simple, professional Hindi.
            """
            
            response = model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            print(f"Gemini API Error for Hindi: {e}")
            return self.get_fallback_hindi_recommendation()
    
    def get_fallback_recommendation(self) -> str:
        """Fallback recommendations if API fails"""
        recommendations = []
        
        # Skills recommendation
        if len(self.resume_data.get('skills', [])) < 5:
            recommendations.append("SKILLS IMPROVEMENT:\n- Add more technical skills relevant to your target role\n- Include both hard and soft skills\n- List skill proficiency levels")
        else:
            recommendations.append("SKILLS IMPROVEMENT:\n- Your skills are good, consider adding emerging technologies\n- Quantify your skill levels")
        
        # Certification recommendations
        recommendations.append("\nCERTIFICATIONS SUGGESTED:\n- AWS Certified Solutions Architect\n- Google Professional Data Engineer\n- Certified Scrum Master (CSM)\n- Project Management Professional (PMP)")
        
        # Project recommendations
        recommendations.append("\nPROJECT SUGGESTIONS:\n- Build a portfolio project using modern tech stack\n- Contribute to open source\n- Create a technical blog or documentation")
        
        # Career advice
        if self.ats_score < 50:
            recommendations.append("\nCAREER ADVICE:\n- Focus on improving your resume's ATS compatibility\n- Tailor your resume for each application\n- Quantify your achievements")
        else:
            recommendations.append("\nCAREER ADVICE:\n- Your resume is performing well, focus on networking\n- Apply to senior positions\n- Consider mentorship roles")
        
        # Formatting
        recommendations.append("\nRESUME FORMATTING:\n- Use standard section headings (Experience, Education, Skills)\n- Use bullet points for achievements\n- Keep consistent formatting throughout\n- Save as PDF for better ATS parsing")
        
        return '\n'.join(recommendations)
    
    def get_fallback_hindi_recommendation(self) -> str:
        """Fallback Hindi recommendations"""
        return """
        कौशल सुधार:
        - अपने लक्ष्य भूमिका के लिए प्रासंगिक अधिक तकनीकी कौशल जोड़ें
        - हार्ड और सॉफ्ट दोनों कौशल शामिल करें
        - कौशल दक्षता स्तरों को सूचीबद्ध करें
        
        प्रमाणपत्र सुझाव:
        - AWS Certified Solutions Architect
        - Google Professional Data Engineer
        - Certified Scrum Master (CSM)
        
        परियोजना सुझाव:
        - आधुनिक तकनीक स्टैक का उपयोग करके एक पोर्टफोलियो परियोजना बनाएं
        - ओपन सोर्स में योगदान दें
        
        करियर सलाह:
        - अपने रिज्यूमे की एटीएस संगतता में सुधार पर ध्यान दें
        - अपनी उपलब्धियों को मात्रात्मक रूप में प्रस्तुत करें
        
        रिज्यूमे फॉर्मेटिंग:
        - मानक अनुभाग शीर्षकों का उपयोग करें
        - उपलब्धियों के लिए बुलेट पॉइंट्स का उपयोग करें
        - पूरे रिज्यूमे में Consistent formatting रखें
        """
    
    def get_missing_skills(self) -> list:
        """Identify missing in-demand skills"""
        current_skills = set([s.lower() for s in self.resume_data.get('skills', [])])
        
        in_demand_skills = {
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'django', 'flask', 'spring boot', 'aws', 'azure', 'docker', 'kubernetes',
            'machine learning', 'data science', 'sql', 'mongodb', 'graphql',
            'typescript', 'next.js', 'tailwind css', 'figma', 'jenkins', 'terraform'
        }
        
        missing = in_demand_skills - current_skills
        return list(missing)[:10]
    
    def get_full_recommendations(self) -> Dict[str, Any]:
        """Get complete recommendations"""
        return {
            'english_recommendation': self.generate_english_recommendation(),
            'hindi_recommendation': self.generate_hindi_recommendation(),
            'missing_skills': self.get_missing_skills(),
            'suggested_certifications': [
                "AWS Certified Solutions Architect",
                "Google Professional Cloud Architect",
                "Certified Kubernetes Administrator",
                "PMP Certification",
                "Scrum Master Certification",
                "Data Science Professional Certificate"
            ],
            'suggested_projects': [
                "E-commerce platform with microservices",
                "AI-powered chatbot using LLMs",
                "Real-time analytics dashboard",
                "Mobile app with React Native",
                "DevOps CI/CD pipeline project"
            ],
            'career_improvements': [
                "Contribute to open source projects",
                "Build a strong LinkedIn presence",
                "Attend tech conferences and meetups",
                "Start a technical blog",
                "Mentor junior developers"
            ]
        }