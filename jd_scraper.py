import os
os.environ['USER_AGENT'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36"


from langchain_community.document_loaders import WebBaseLoader
import requests
from bs4 import BeautifulSoup

def scrape_job_description(url):
   
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        if docs:
            page_content = docs[0].page_content.strip()
            if page_content:
                return page_content
    except Exception as e:
        print(f"LangChain loader failed: {e}")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                          " AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/90.0.4430.85 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        
        selectors = [
            "div.job-description",
            "div.description",
            "section.job-description",
            "div#jobDescriptionText",
            "div.job-posting-description",
            "div[data-testid='jobDescriptionText']",
            "article",
            "main"
        ]

        for selector in selectors:
            desc = soup.select_one(selector)
            if desc and desc.get_text(strip=True):
                return desc.get_text(separator="\n", strip=True)

        return soup.get_text(separator="\n", strip=True)

    except Exception as e:
        print(f"Fallback scraping failed: {e}")
        return "Failed to scrape job description."
    
    

