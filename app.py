# app.py
import streamlit as st
import os
import tempfile
from utils.ai_service import AIService
from utils.ppt_generator import PPTGenerator
from utils.templates import ResumeTemplates
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Resume PowerPoint Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'generate_clicked' not in st.session_state:
    st.session_state.generate_clicked = False
if 'download_ready' not in st.session_state:
    st.session_state.download_ready = False
if 'temp_file' not in st.session_state:
    st.session_state.temp_file = None


def main():
    st.title("AI Resume PowerPoint Generator")
    st.markdown("Transform your resume into a professional presentation with AI")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        
        ai_service = st.selectbox(
            "AI Service",
            ["OpenAI", "Perplexity AI"],
            index=0,
            help="Select the AI service to use for content generation"
        )
        
        template = st.selectbox(
            "Presentation Template",
            ResumeTemplates.get_template_options(),
            index=0,
            help="Select a template style for your presentation"
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("This tool uses AI to transform your resume information into a professional PowerPoint presentation.")
        st.markdown("Your data is processed securely and not stored permanently.")
    
    # Main form for resume information
    with st.form("resume_form"):
        st.header("Your Resume Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name", placeholder="John Doe")
            title = st.text_input("Professional Title", placeholder="Senior Software Engineer")
            email = st.text_input("Email", placeholder="john.doe@example.com")
            phone = st.text_input("Phone", placeholder="+1 (123) 456-7890")
        
        with col2:
            linkedin = st.text_input("LinkedIn", placeholder="linkedin.com/in/johndoe")
            portfolio = st.text_input("Portfolio/Website", placeholder="johndoe.com")
        
        st.subheader("Professional Summary")
        summary = st.text_area(
            "Summary",
            placeholder="A brief summary of your professional background and career goals.",
            height=100
        )
        
        st.subheader("Work Experience")
        experience = st.text_area(
            "Experience",
            placeholder="Describe your work experience in detail. Format: Job Title, Company, Dates, Responsibilities (separate multiple positions with a new line)",
            height=200
        )
        
        st.subheader("Education")
        education = st.text_area(
            "Education",
            placeholder="List your education details. Format: Degree, Institution, Year, GPA/Achievements (separate multiple entries with a new line)",
            height=100
        )
        
        st.subheader("Skills")
        skills = st.text_area(
            "Skills",
            placeholder="List your skills, preferably categorized (e.g., Technical: Python, Java; Soft: Communication, Leadership)",
            height=100
        )
        
        st.subheader("Achievements & Certifications")
        achievements = st.text_area(
            "Achievements",
            placeholder="List your key achievements, awards, and certifications",
            height=100
        )
        
        # Submit button
        submitted = st.form_submit_button("Generate Presentation")
        
        if submitted:
            if not name or not title:
                st.error("Name and Professional Title are required!")
            else:
                st.session_state.generate_clicked = True
                
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Update progress
                status_text.text("Processing your information...")
                progress_bar.progress(20)
                
                # Prepare user data
                user_data = {
                    "name": name,
                    "title": title,
                    "contact": {
                        "email": email,
                        "phone": phone,
                        "linkedin": linkedin,
                        "portfolio": portfolio
                    },
                    "summary": summary,
                    "experience": experience,
                    "education": education,
                    "skills": skills,
                    "achievements": achievements
                }
                
                # Initialize AI service
                service_type = "perplexity" if ai_service == "Perplexity AI" else "openai"

                ai = AIService(service_type=service_type)
                
                # Generate content with AI
                status_text.text("Generating content with AI...")
                progress_bar.progress(40)
                ai_content = ai.generate_resume_content(user_data)
                
                # Initialize PowerPoint generator
                status_text.text("Creating your presentation...")
                progress_bar.progress(60)
                ppt_gen = PPTGenerator()
                
                # Get template details
                template_details = ResumeTemplates.get_template_structure(template)
                
                # Generate PowerPoint
                if not isinstance(ai_content, dict) or "error" in ai_content:
                    st.error(f"AI Content Generation Failed: {ai_content.get('error', 'Unknown error')}")
                    return

                try:
                    ppt_gen.generate_from_ai_content(ai_content, template_details["color_scheme"])
                except Exception as e:
                    st.error(f"Presentation Generation Error: {str(e)}")
                    return
                
                # Save to temporary file
                status_text.text("Finalizing your presentation...")
                progress_bar.progress(80)
                temp_dir = tempfile.gettempdir()
                temp_file = os.path.join(temp_dir, "resume_presentation.pptx")
                ppt_gen.save(temp_file)
                
                st.session_state.temp_file = temp_file
                st.session_state.download_ready = True
                
                # Complete progress
                progress_bar.progress(100)
                status_text.text("Presentation generated successfully!")
    
    
    # Show download option if generation is complete
    if st.session_state.download_ready and st.session_state.temp_file:
        st.success("Your presentation is ready for download!")
        
        with open(st.session_state.temp_file, "rb") as file:
            st.download_button(
                label="Download Presentation",
                data=file,
                file_name="resume_presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        
        # Preview section
        st.subheader("Preview (Sample Slides)")
        st.image("https://via.placeholder.com/800x450.png?text=Preview+Not+Available", 
                 caption="Preview functionality requires additional components", 
                 use_column_width=True)
        
        # Reset button
        if st.button("Create Another Presentation"):
            st.session_state.generate_clicked = False
            st.session_state.download_ready = False
            st.session_state.temp_file = None
            st.experimental_rerun()

if __name__ == "__main__":
    main()
