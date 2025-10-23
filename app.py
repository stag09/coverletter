import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from utils.file_parser import extract_text_from_pdf, extract_text_from_docx
from deep_translator import GoogleTranslator
import fitz  # PyMuPDF for better PDF extraction

# Load environment variables
load_dotenv()

# Configure Gemini API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Streamlit page config
st.set_page_config(page_title="AI Cover Letter Generator", layout="centered")
st.title("📝 AI Cover Letter Generator")

st.write("Generate a personalized, professional cover letter using AI — from your resume and job description.")

# --- Tabs for better UI ---
tab1, tab2 = st.tabs(["🧾 Generate Cover Letter", "🔍 Analyze Job Description"])

# =====================
# 📄 Resume Extractor
# =====================
def extract_resume_text(uploaded_file):
    """Enhanced resume text extraction"""
    text = ""
    try:
        if uploaded_file.name.endswith(".pdf"):
            try:
                with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
                    for page in doc:
                        text += page.get_text("text")
            except Exception:
                uploaded_file.seek(0)
                text = extract_text_from_pdf(uploaded_file)
        else:
            text = extract_text_from_docx(uploaded_file)
    except Exception as e:
        st.error(f"Error extracting resume text: {e}")
    return text.strip()

# =====================
# 🧠 Job Description Analyzer
# =====================
with tab2:
    st.subheader("🔍 Job Description Analyzer")
    jd_text = st.text_area("Paste a Job Description here to analyze skills and keywords:", height=200)
    if st.button("Analyze Job Description"):
        if not jd_text.strip():
            st.warning("Please paste a job description to analyze.")
        else:
            model = genai.GenerativeModel("gemini-2.5-flash")
            analysis_prompt = f"""
            Analyze the following job description and extract:
            - Key technical and soft skills
            - Job role focus areas
            - Important keywords and themes
            - Ideal tone or communication style

            Job Description:
            {jd_text}
            """
            response = model.generate_content(analysis_prompt)
            st.markdown("### 🧠 Job Description Insights")
            st.write(response.text)

# =====================
# 🧾 Cover Letter Generator
# =====================
with tab1:
    st.subheader("📑 Generate Your Cover Letter")

    job_description = st.text_area("📄 Job Description", height=200)
    uploaded_file = st.file_uploader("📎 Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

    tone = st.selectbox("🎯 Choose Tone", [
        "Formal", "Friendly", "Confident", "Persuasive", "Creative", "Enthusiastic"
    ])

    # Language support expanded
    language = st.selectbox("🌍 Select Output Language", [
        "English", "Hindi", "Telugu", "French", "Spanish", "German", "Japanesh"
    ])

    if st.button("✨ Generate Cover Letter"):
        if not job_description:
            st.warning("Please paste the job description.")
        elif not uploaded_file:
            st.warning("Please upload your resume.")
        else:
            with st.spinner("Generating your AI-powered cover letter..."):
                resume_text = extract_resume_text(uploaded_file)

                # Construct AI prompt (always in English for best accuracy)
                prompt = f"""
                You are an expert career coach and professional writer.
                Write a personalized {tone.lower()} cover letter based on the information below.

                ### Job Description:
                {job_description}

                ### Candidate Resume:
                {resume_text}

                ### Instructions:
                - Make the letter engaging and relevant to the job.
                - Highlight the most suitable skills and experiences.
                - Keep it professional and concise.
                - Include a polite closing statement.
                """

                try:
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    response = model.generate_content(prompt)
                    english_letter = response.text.strip()

                    # Translate to selected language if not English
                    if language != "English":
                        with st.spinner(f"Translating cover letter to {language}..."):
                            translated_letter = GoogleTranslator(
                                source="en",
                                target=language.lower()
                            ).translate(english_letter)
                        st.subheader(f"🧾 Generated Cover Letter ({language})")
                        st.write(translated_letter)
                    else:
                        st.subheader("🧾 Generated Cover Letter:")
                        st.write(english_letter)

                    # Smart Rewrite Options
                    st.markdown("---")
                    st.markdown("### ✨ Improve or Regenerate")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Regenerate"):
                            st.experimental_rerun()
                    with col2:
                        if st.button("🚀 Improve This Version"):
                            improve_prompt = f"Improve the following cover letter for clarity, tone, and impact:\n\n{english_letter}"
                            improved = model.generate_content(improve_prompt)
                            improved_text = improved.text.strip()
                            if language != "English":
                                improved_text = GoogleTranslator(source="en", target=language.lower()).translate(improved_text)
                            st.subheader(f"🌟 Improved Version ({language})")
                            st.write(improved_text)

                except Exception as e:
                    st.error(f"⚠️ Error generating cover letter: {e}")
