# 📊 AI Resume PowerPoint Generator

Transform your resume into a **professional PowerPoint presentation** with the help of **AI-powered content generation**. This Streamlit web application takes your resume data and turns it into a ready-to-download `.pptx` file using customizable templates and smart content suggestions.

---

## 🚀 Features

- 🔮 **AI-Powered Content Generation**  
  Leverages services like OpenAI and Perplexity AI to generate personalized presentation content.

- 🎨 **Custom Templates**  
  Choose from multiple professionally designed presentation styles.

- 📑 **Interactive Form**  
  Enter resume details directly in the app with real-time validation.

- 📥 **Instant Download**  
  Download the generated PowerPoint presentation with one click.

- 🔐 **Secure Data Handling**  
  Your data is processed temporarily and never stored.

---

## 📂 Directory Structure

---

## 🧠 How It Works

1. **User Input**  
   Fill out the interactive form with resume information such as name, experience, skills, etc.

2. **AI Content Generation**  
   Selected AI service generates slide content based on your input.

3. **PowerPoint Creation**  
   A presentation is built using a chosen template and AI-generated content.

4. **Download Output**  
   The generated presentation is saved and made available for download.

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Backend**: Python
- **AI Services**: OpenAI, Perplexity AI (selectable)
- **Presentation Generator**: `python-pptx`
- **Environment Variables**: Managed using `python-dotenv`

---

## 🧪 Installation & Run Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-resume-ppt-generator.git
cd ai-resume-ppt-generator

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
touch .env
# Add your API keys in the .env file:
# OPENAI_API_KEY=your_key_here
# PERPLEXITY_API_KEY=your_key_here (if used)

# Run the app
streamlit run app.py

