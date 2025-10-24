## 📁 Folder Structure
# AI Cover Letter Generator

A Streamlit web app that generates personalized cover letters using Google Gemini (gemini-2.5-flash). The app extracts text from uploaded resumes (PDF/DOCX), analyzes job descriptions, generates tailored cover letters with a selectable tone, and optionally translates the output into multiple languages.

---

## Tech Stack

* **Streamlit** — Web UI
* **google-generativeai** — Google Gemini 2.5 Flash model for text generation
* **docx2txt** — Extract text from DOCX files
* **PyPDF2** — PDF parsing (fallback)
* **PyMuPDF (fitz)** — High-quality PDF text extraction
* **python-docx** — Create/download DOCX cover letters
* **python-dotenv** — Load environment variables (GEMINI_API_KEY)
* **deep-translator** — Translate generated letters into other languages

---

## Features

* Upload resume (PDF or DOCX) and paste job description
* Analyze job descriptions to extract key skills and tone
* Generate AI-powered, customized cover letters using Gemini 2.5 Flash
* Choose writing tone (Formal, Friendly, Confident, Persuasive, Creative, Enthusiastic)
* Translate output to multiple languages (Hindi, Telugu, French, Spanish, German)
* Regenerate or improve generated letters
* Download generated letter as a DOCX file

---

## Quick Start

1. Clone the repository:

```bash
git clone <your-repo-url>
cd <repo-folder>
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # macOS / Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Add your Gemini API key in a `.env` file (project root):

```
GEMINI_API_KEY=your_gemini_api_key_here
```

4. Run the Streamlit app:

```bash
streamlit run app.py
```

Open the URL shown by Streamlit in your browser.

---

## Environment & Security

* Store all sensitive keys (API tokens) in `.env` and **do not commit** `.env` to version control.
* Add `.env` to `.gitignore`:

```
.env
```

---

## File Structure (Suggested)

```
/your-project
├─ app.py                 # Main Streamlit application
├─ requirements.txt       # Project dependencies
├─ .env                   # Environment variables (ignored)
├─ utils/
│  └─ file_parser.py      # Helpers: extract_text_from_pdf, extract_text_from_docx
├─ assets/                # Images, icons (optional)
├─ README.md              # This file
└─ docs/                  # Optional: demo video, design docs
```

---

## How It Works (High Level)

1. User opens the app and chooses either **Generate Cover Letter** or **Analyze Job Description** tab.
2. For generation: user provides the job description, uploads a resume, selects tone and language, then clicks **Generate**.
3. The app extracts text from the resume (PyMuPDF preferred; fallback to PyPDF2 or docx2txt). The text + job description + tone are formed into a prompt.
4. The prompt is sent to Gemini 2.5 Flash (`google-generativeai`) which returns an English cover letter.
5. If requested, the letter is translated using `deep-translator` to the target language.
6. The final text is displayed and can be improved or downloaded as a DOCX via `python-docx`.

---

## Example Prompts

**Generation prompt** (sent to Gemini):

```
You are an expert career coach and professional writer.
Write a personalized {tone} cover letter based on the information below.

Job Description:
{job_description}

Candidate Resume:
{resume_text}

Instructions:
- Make the letter engaging and relevant to the job.
- Highlight the most suitable skills and experiences.
- Keep it professional and concise.
- Include a polite closing statement.
```

**Analysis prompt** (JD Analyzer):

```
Analyze the following job description and extract:
- Key technical and soft skills
- Job role focus areas
- Important keywords and themes
- Ideal tone or communication style

Job Description:
{jd_text}
```

---

## Tips & Best Practices

* Prefer **PyMuPDF (fitz)** for robust PDF extraction, especially for complex layouts.
* Keep prompts concise and include explicit instructions about tone and formatting.
* Translate only after finalizing the English version for best accuracy.
* Respect user privacy: do not persist resumes or generated letters unless users explicitly opt in.

---

## Future Enhancements (Optional)

* Add user accounts and a history of generated letters (with user consent).
* Add DOCX templates and multi-template export (PDF + DOCX).
* Add more advanced prompt templates or few-shot examples to improve output quality.
* Add caching to reduce repeated API calls for the same inputs.

---

## License

Add your preferred license here (e.g., MIT).

---

If you want, I can also generate a `requirements.txt`, `.gitignore`, or a ready-to-copy DOCX export helper function for this repo.


