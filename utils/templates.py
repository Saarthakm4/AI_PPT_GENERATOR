# utils/templates.py
class ResumeTemplates:
    """Predefined templates for resume presentations"""
    
    @staticmethod
    def get_template_options():
        """Return a list of available templates"""
        return [
            "professional",
            "modern",
            "creative",
            "executive",
            "academic"
        ]
    
    @staticmethod
    def get_template_structure(template_name):
        """Return the structure for a specific template"""
        templates = {
            "professional": {
                "name": "Professional",
                "description": "Clean and traditional template suitable for most industries",
                "slides": [
                    "title_slide",
                    "about_me",
                    "work_experience",
                    "education",
                    "skills",
                    "achievements",
                    "contact"
                ],
                "color_scheme": "professional"
            },
            "modern": {
                "name": "Modern",
                "description": "Contemporary design with a clean aesthetic",
                "slides": [
                    "title_slide",
                    "about_me",
                    "skills",
                    "work_experience",
                    "education",
                    "achievements",
                    "contact"
                ],
                "color_scheme": "modern"
            },
            "creative": {
                "name": "Creative",
                "description": "Bold and innovative design for creative fields",
                "slides": [
                    "title_slide",
                    "about_me",
                    "skills",
                    "portfolio_highlights",
                    "work_experience",
                    "education",
                    "contact"
                ],
                "color_scheme": "creative"
            },
            "executive": {
                "name": "Executive",
                "description": "Sophisticated design for senior professionals",
                "slides": [
                    "title_slide",
                    "executive_summary",
                    "leadership_experience",
                    "key_achievements",
                    "education",
                    "board_positions",
                    "contact"
                ],
                "color_scheme": "professional"
            },
            "academic": {
                "name": "Academic",
                "description": "Focused on education and research experience",
                "slides": [
                    "title_slide",
                    "research_interests",
                    "education",
                    "publications",
                    "teaching_experience",
                    "grants_awards",
                    "contact"
                ],
                "color_scheme": "professional"
            }
        }
        
        return templates.get(template_name, templates["professional"])
