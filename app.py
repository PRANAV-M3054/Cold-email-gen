import streamlit as st
from resume_parser import extract_resume_text
from jd_scraper import scrape_job_description
from llm_engine import generate_cold_email_and_cover
from email_sender import send_email
import os

st.set_page_config(page_title="Cold Email & Cover Letter Generator", layout="centered")
st.title("Cold Email + Cover Letter Generator")

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "job_description" not in st.session_state:
    st.session_state.job_description = ""
if "cold_email" not in st.session_state:
    st.session_state.cold_email = ""
if "cover_letter" not in st.session_state:
    st.session_state.cover_letter = ""

resume_file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"])
if resume_file:
    try:
        st.session_state.resume_text = extract_resume_text(resume_file)
        st.success("Resume text extracted successfully.")
    except Exception as e:
        st.error(f"Failed to read resume: {e}")
        st.session_state.resume_text = ""

if st.session_state.resume_text:
    with st.expander("Preview Extracted Resume Text"):
        st.text_area("Resume Preview", st.session_state.resume_text[:3000], height=300)

job_url = st.text_input("Paste Job Description URL")
manual_jd = st.text_area("Or paste the job description manually (recommended):", height=300)

if manual_jd.strip():
    st.session_state.job_description = manual_jd
elif job_url:
    try:
        scraped_text = scrape_job_description(job_url)
        if "Security Check" in scraped_text or "Failed to scrape" in scraped_text:
            st.warning("Couldn't fetch a proper job description from the URL.")
        else:
            st.session_state.job_description = scraped_text
            st.success("Job description scraped successfully.")
    except Exception as e:
        st.error(f"Error fetching job description: {e}")

if st.session_state.job_description:
    with st.expander("Preview Job Description"):
        st.text_area("Job Description Preview", st.session_state.job_description[:3000], height=300)

github_link = st.text_input("Your GitHub URL (optional)")
portfolio_link = st.text_input("Your Portfolio/Website URL (optional)")

send_option = st.checkbox("Send Email Automatically?")
if send_option:
    recruiter_email = st.text_input("Recruiter's Email")

if st.button("Generate Email & Cover Letter"):
    if not st.session_state.resume_text or not st.session_state.job_description:
        st.error("Resume or job description is incomplete. Cannot generate content.")
    else:
        with st.spinner("Generating with LLM..."):
            try:
                cold_email, cover_letter = generate_cold_email_and_cover(
                    st.session_state.resume_text,
                    st.session_state.job_description,
                    github_link,
                    portfolio_link
                )
                st.session_state.cold_email = cold_email
                st.session_state.cover_letter = cover_letter
            except Exception as e:
                st.error(f"Error generating content: {e}")
                st.session_state.cold_email = ""
                st.session_state.cover_letter = ""

if st.session_state.cold_email:
    st.subheader("Cold Email")
    st.text_area("Generated Cold Email", st.session_state.cold_email, height=250)
else:
    st.warning("Cold email not generated yet.")

if st.session_state.cover_letter:
    st.subheader("Cover Letter")
    st.text_area("Generated Cover Letter", st.session_state.cover_letter, height=350)
else:
    st.warning("Cover letter not generated yet.")

if send_option and recruiter_email and st.session_state.cold_email:
    try:
        send_email(st.session_state.cold_email, recruiter_email)
        st.success("Email Sent Successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")
