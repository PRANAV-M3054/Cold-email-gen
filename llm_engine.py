import os
from dotenv import load_dotenv
from groq import Groq  

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

def generate_cold_email_and_cover(resume_text, job_description, github_link, portfolio_link):
    prompt = f"""
You are a professional AI assistant that writes tailored job application content.

Below is a resume and a job description. Use them to generate:
1. A personalized, concise cold email written directly to a recruiter.
2. A formal, tailored cover letter for the role.

Ensure:
- No placeholders like [Job Title] or [Company Name]; use actual values from the job description.
- Refer to specific company values, role responsibilities, and candidate strengths from the resume.
- Include the candidate’s GitHub and Portfolio links naturally.

Resume:
{resume_text}

Job Description:
{job_description}

GitHub: {github_link}
Portfolio: {portfolio_link}

Respond in the following format:

[COLD EMAIL]
<email content>

[COVER LETTER]
<cover letter content>
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192", 
        messages=[
            {"role": "system", "content": "You are a professional job application assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    full_response = response.choices[0].message.content

    
    if "[COLD EMAIL]" in full_response and "[COVER LETTER]" in full_response:
        email_part = full_response.split("[COLD EMAIL]")[1].split("[COVER LETTER]")[0].strip()
        cover_part = full_response.split("[COVER LETTER]")[1].strip()
    else:
        email_part = "Failed to generate cold email."
        cover_part = "Failed to generate cover letter."

    return email_part, cover_part