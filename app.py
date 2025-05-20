import streamlit as st
from resume_parser import extract_resume_text
from jd_scraper import scrape_job_description
from llm_engine import generate_cold_email_and_cover
from email_sender import send_email
import os

st.set_page_config(page_title="Cold Email & Cover Letter Generator", layout="centered")
st.title("Cold Email + Cover Letter Generator")

resume_file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"])
job_url = st.text_input("Paste Job Description URL")
github_link = st.text_input("Your GitHub URL")
portfolio_link = st.text_input("Your Portfolio/Website URL")

send_option = st.checkbox("Send Email Automatically?")
if send_option:
    recruiter_email = st.text_input("Recruiter's Email")

if st.button("Generate Email & Cover Letter"):
    if not resume_file or not job_url:
        st.error("Please upload your resume and provide a job description URL.")
    else:
        with st.spinner("Processing..."):
            resume_text = extract_resume_text(resume_file)
            job_description = scrape_job_description(job_url)

            cold_email, cover_letter = generate_cold_email_and_cover(
                resume_text, job_description, github_link, portfolio_link
            )

            st.subheader("Cold Email")
            st.text_area("Generated Email", cold_email, height=250)

            st.subheader("Cover Letter")
            st.text_area("Generated Cover Letter", cover_letter, height=350)

            if send_option and recruiter_email:
                send_email(cold_email, recruiter_email)
                st.success("Email Sent Successfully!")
