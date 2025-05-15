# utils/ai_service.py
import os
import json
from dotenv import load_dotenv
import openai
import requests

load_dotenv()

class AIService:
    def __init__(self, service_type="openai"):
        self.service_type = service_type
        
        if service_type == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY")
            openai.api_key = self.api_key
        elif service_type == "perplexity":
            self.api_key = os.getenv("PERPLEXITY_API_KEY")
            self.perplexity_api_url = "https://api.perplexity.ai/chat/completions"
        else:
            raise ValueError(f"Unsupported service type: {service_type}")

    def _create_resume_prompt(self, user_input):
        """Create a detailed prompt for the AI based on user input"""
        return f"""
        Generate a professional resume presentation with the following information:
        
        {json.dumps(user_input, indent=2)}
        
        Create structured JSON with these REQUIRED fields:
        {{
            "title_slide": {{
                "name": "FULL_NAME (REQUIRED)",
                "title": "PROFESSIONAL_TITLE (REQUIRED)",
                "tagline": "Optional tagline"
            }},
            "about_me": {{
                "points": ["Bullet point 1", "Bullet point 2"]
            }},
            "work_experience": [
                {{
                    "title": "Job Title",
                    "company": "Company Name",
                    "dates": "Employment Dates",
                    "responsibilities": ["Responsibility 1", "Responsibility 2"]
                }}
            ],
            "education": [
                {{
                    "degree": "Degree Name",
                    "institution": "Institution Name",
                    "year": "Graduation Year",
                    "gpa": "Optional GPA",
                    "achievements": ["Achievement 1"]
                }}
            ],
            "skills": {{
                "technical": ["Skill 1"],
                "soft": ["Skill 2"],
                "domain": ["Skill 3"]
            }},
            "achievements": ["Achievement 1"],
            "contact": {{
                "email": "user@example.com",
                "phone": "+1234567890",
                "linkedin": "linkedin.com/in/username",
                "portfolio": "portfolio.com"
            }}
        }}
        """

    def generate_resume_content(self, user_input):
        """
        Generate structured resume content from user input using AI
        """
        prompt = self._create_resume_prompt(user_input)
        
        if self.service_type == "openai":
            return self._generate_with_openai(prompt)
        elif self.service_type == "perplexity":
            return self._generate_with_perplexity(prompt)

    def _generate_with_openai(self, prompt):
        """Generate content using OpenAI API"""
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert resume writer creating PowerPoint content."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": str(e)}

    def _generate_with_perplexity(self, prompt):
        """Generate content using Perplexity AI API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "sonar-pro",
                "messages": [
                  {
                        "role": "system", 
                        "content": "You are an expert resume writer. Return ONLY valid JSON."
                    },
                    {
                    "role": "user", 
                            "content": f"{prompt}\n\nReturn response as valid JSON only."
                    }
                ]
            }
        
            response = requests.post(
                self.perplexity_api_url,
                headers=headers,
                json=data,
                timeout=30
            )
        
            if response.status_code == 200:
                raw_response = response.json()["choices"][0]["message"]["content"]
                # Clean response before parsing
                cleaned_response = raw_response.replace("``````", "").strip()
                return json.loads(cleaned_response)
            return {"error": f"API Error {response.status_code}: {response.text}"}
        except json.JSONDecodeError as e:
            return {"error": f"JSON Parsing Error: {str(e)}"}
        except Exception as e:
            return {"error": str(e)}
