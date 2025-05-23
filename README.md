# 📬 Cold Email & Cover Letter Generator with AI

This tool helps job seekers save time by generating personalized cold emails and cover letters from their resume and a job description — powered by LLMs (ChatGROQ)!

## ✨ Features

- Upload resume (.pdf or .docx)
- Scrape or paste job descriptions
- Generate email and cover letter instantly
- Preview and edit content
- Auto-send email to recruiter (optional)
- Mobile + Desktop responsive

## 🔧 Tech Stack

- 🧠 LLM via ChatGROQ API
- ⚡ Streamlit for UI
- 📄 PDF / DOCX parsing (pdfplumber, python-docx)
- 🌐 Web scraping with BeautifulSoup
- 📧 Email via Gmail SMTP
- 🔐 Secrets via .env or Streamlit Cloud secrets

## 🚀 How to Run Locally

```bash
git clone https://github.com/yourusername/cold-email-gen.git
cd cold-email-gen
pip install -r requirements.txt
