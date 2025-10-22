import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from utils.file_parser import extract_text_from_pdf, extract_text_from_docx

# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Streamlit App Title
st.set_page_config(page_title="AI Cover Letter Generator", layout="centered")
st.title("📝 AI Cover Letter Generator (Gemini)")

st.write("Generate a professional, personalized cover letter from your resume and job description.")

# Inputs
job_description = st.text_area("📄 Job Description", height=200)

uploaded_file = st.file_uploader("📎 Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

tone = st.selectbox("🎯 Choose Tone", ["Formal", "Friendly", "Creative", "Concise"])

# Generate Button
if st.button("✨ Generate Cover Letter"):
    if not job_description:
        st.warning("Please paste the job description.")
    elif not uploaded_file:
        st.warning("Please upload your resume.")
    else:
        # Extract resume text
        if uploaded_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)
        else:
            resume_text = extract_text_from_docx(uploaded_file)

        # Prompt for Gemini model
        prompt = f"""
        You are an expert HR assistant.
        Generate a {tone.lower()} cover letter tailored for the following job description and resume.
        Make it sound professional, unique, and concise.

        Job Description:
        {job_description}

        Resume:
        {resume_text}
        """

        # Generate response
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)

            st.subheader("🧾 Generated Cover Letter:")
            st.write(response.text)

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
