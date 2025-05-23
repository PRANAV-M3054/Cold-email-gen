import pdfplumber
import docx
import tempfile

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text.strip()

def extract_resume_text(uploaded_file):
    file_type = uploaded_file.type
    
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name
        
    if "pdf" in file_type:
        return extract_text_from_pdf(tmp_file_path)
    elif "word" in file_type or "docx" in file_type:
        return extract_text_from_docx(tmp_file_path)
    else:
        return "Unsupported file type. Please upload a PDF or DOCX file."
    
  # Show first 500 characters
