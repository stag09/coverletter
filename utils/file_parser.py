import docx2txt
import PyPDF2

def extract_text_from_pdf(file):
    """Extract text from an uploaded PDF file"""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    """Extract text from an uploaded DOCX file"""
    return docx2txt.process(file)
