import re
import PyPDF2
import pdfplumber
from docx import Document
import spacy
from typing import Dict, List, Any

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

class ResumeParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.text = ""
        self.extracted_data = {
            'full_name': '',
            'email': '',
            'phone': '',
            'skills': [],
            'education': [],
            'experience': [],
            'certifications': [],
            'projects': []
        }
    
    def extract_text_from_pdf(self) -> str:
        """Extract text from PDF file"""
        text = ""
        
        # Try with pdfplumber first (better for complex PDFs)
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except:
            # Fallback to PyPDF2
            try:
                with open(self.file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""
            except Exception as e:
                print(f"Error extracting PDF: {e}")
        
        return text
    
    def extract_text_from_docx(self) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = Document(self.file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
        return text
    
    def extract_text(self) -> str:
        """Extract text based on file type"""
        if self.file_path.endswith('.pdf'):
            return self.extract_text_from_pdf()
        elif self.file_path.endswith('.docx'):
            return self.extract_text_from_docx()
        return ""
    
    def extract_email(self) -> str:
        """Extract email from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, self.text)
        return emails[0] if emails else ""
    
    def extract_phone(self) -> str:
        """Extract phone number from text"""
        phone_pattern = r'\b(?:\+?91)?[-\s]?(?:[6-9]\d{9}|\d{10})\b'
        phones = re.findall(phone_pattern, self.text)
        return phones[0] if phones else ""
    
    def extract_name(self) -> str:
        """Extract name from text using NLP"""
        doc = nlp(self.text[:500])  # First 500 characters usually contain name
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return ""
    
    def extract_skills(self) -> List[str]:
        """Extract skills from text"""
        common_skills = {
            'python', 'java', 'javascript', 'html', 'css', 'react', 'angular', 'vue',
            'django', 'flask', 'spring', 'node.js', 'express', 'mongodb', 'mysql',
            'postgresql', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git',
            'machine learning', 'deep learning', 'nlp', 'data analysis', 'pandas',
            'numpy', 'tensorflow', 'pytorch', 'scikit-learn', 'tableau', 'power bi',
            'agile', 'scrum', 'jira', 'confluence', 'rest api', 'graphql'
        }
        
        found_skills = []
        text_lower = self.text.lower()
        
        for skill in common_skills:
            if skill in text_lower:
                found_skills.append(skill)
        
        # Also extract using NLP for technical terms
        doc = nlp(self.text)
        for token in doc:
            if token.pos_ == "NOUN" and token.text.lower() in common_skills:
                if token.text not in found_skills:
                    found_skills.append(token.text)
        
        return found_skills
    
    def extract_education(self) -> List[Dict[str, str]]:
        """Extract education details"""
        education_keywords = ['bachelor', 'master', 'phd', 'b.tech', 'm.tech', 'b.e', 'm.e',
                              'b.sc', 'm.sc', 'b.com', 'm.com', 'b.a', 'm.a', 'diploma']
        
        education = []
        lines = self.text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            for keyword in education_keywords:
                if keyword in line_lower:
                    edu_entry = {'degree': line.strip()}
                    
                    # Try to get year
                    year_match = re.search(r'\b(19|20)\d{2}\b', line)
                    if year_match:
                        edu_entry['year'] = year_match.group()
                    
                    # Try to get institution (next few lines)
                    if i + 1 < len(lines):
                        edu_entry['institution'] = lines[i + 1].strip()
                    
                    education.append(edu_entry)
                    break
        
        return education
    
    def extract_experience(self) -> List[Dict[str, str]]:
        """Extract work experience"""
        experience = []
        exp_keywords = ['experience', 'work', 'employment', 'job', 'position', 'role']
        
        lines = self.text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in exp_keywords):
                if len(line.strip()) > 5:  # Avoid empty or very short lines
                    exp_entry = {'title': line.strip()}
                    
                    # Extract company (next line)
                    if i + 1 < len(lines) and len(lines[i + 1].strip()) > 2:
                        exp_entry['company'] = lines[i + 1].strip()
                    
                    # Extract duration
                    duration_match = re.search(r'\d+\s*(?:years?|yrs?)\s*(?:of)?\s*experience', line_lower)
                    if duration_match:
                        exp_entry['duration'] = duration_match.group()
                    
                    experience.append(exp_entry)
        
        return experience
    
    def extract_certifications(self) -> List[str]:
        """Extract certifications"""
        cert_keywords = ['certified', 'certification', 'certificate', 'coursera', 'udemy', 'edx']
        certifications = []
        
        lines = self.text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in cert_keywords):
                if len(line.strip()) > 3:
                    certifications.append(line.strip())
        
        return certifications
    
    def extract_projects(self) -> List[str]:
        """Extract projects"""
        project_keywords = ['project', 'developed', 'built', 'created', 'implemented']
        projects = []
        
        lines = self.text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in project_keywords):
                if len(line.strip()) > 5:
                    projects.append(line.strip())
        
        return projects
    
    def parse(self) -> Dict[str, Any]:
        """Complete parsing pipeline"""
        self.text = self.extract_text()
        
        if not self.text:
            return self.extracted_data
        
        self.extracted_data['email'] = self.extract_email()
        self.extracted_data['phone'] = self.extract_phone()
        self.extracted_data['full_name'] = self.extract_name() or "Not Found"
        self.extracted_data['skills'] = self.extract_skills()
        self.extracted_data['education'] = self.extract_education()
        self.extracted_data['experience'] = self.extract_experience()
        self.extracted_data['certifications'] = self.extract_certifications()
        self.extracted_data['projects'] = self.extract_projects()
        
        return self.extracted_data